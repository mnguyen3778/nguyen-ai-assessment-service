"""Internal producer-snapshot-attestation-v1 output verification adapter.

Byte contract:
* The snapshot is the *unchanged* UTF-8 JSON bytes supplied to ``issue`` and
  subsequently handed to a consumer. Its digest is SHA-256 of
  b"NGUYEN-SNAPSHOT-v1\\0" followed by those bytes. Identity is the ASCII
  string "sha256:" followed by that digest's lowercase hexadecimal encoding.
* Conclusions are read at businessDecisionPackage.governedConclusions after
  frozen producer validation. A new ordered object is built using the field
  orders below; array order is never changed. Only JSON strings, exact integers,
  arrays, objects, and the explicitly allowed null findingId are supported.
  Compact JSON uses comma/colon separators and no ASCII-only escaping:
  quotation mark and backslash are escaped; U+0000..U+001F use JSON's short
  escapes where defined, otherwise lowercase ``\\u00xx``; slash and other
  Unicode scalars remain literal. Integers use base-10 digits with an optional
  leading minus and no leading zeros. No Unicode normalization is performed.
  SHA-256 hashes b"NGUYEN-CONCLUSIONS-v1\\0" followed by these UTF-8 bytes.
* The Ed25519 payload is b"NGUYEN-ATTESTATION-v1\\0" followed, in
  SIDECAR_FIELDS order except signature, by a four-byte unsigned big-endian
  length and the exact UTF-8 bytes of each field value. All fields are strings.
  Digests are lowercase hex; signature is canonical padded standard Base64.

This module signs no business decisions and creates no public response fields.
"""

import base64
import binascii
import hashlib
import json
import math
import re
from enum import Enum
from typing import Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from assessment.business_decision_package import (
    GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
)
from assessment.executive_assessment_snapshot import (
    validate_executive_assessment_snapshot_serialization,
)
from assessment.executive_runtime import EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION
from assessment.governed_assessment_input import EXECUTIVE_ASSESSMENT_VERSION_V2
from assessment.methodology_config import METHODOLOGY_VERSION


VERIFICATION_CONTRACT_VERSION = "producer-snapshot-attestation-v1"
CANONICALIZATION_ID = "governed-conclusions-json-v1"
DIGEST_ALGORITHM = "SHA-256"
_SNAPSHOT_DOMAIN = b"NGUYEN-SNAPSHOT-v1\x00"
_CONCLUSIONS_DOMAIN = b"NGUYEN-CONCLUSIONS-v1\x00"
_SIGNATURE_DOMAIN = b"NGUYEN-ATTESTATION-v1\x00"
SIDECAR_FIELDS = (
    "verificationContractVersion", "issuerId", "producerReleaseCommit",
    "producerSnapshotIdentity", "snapshotResponseContractVersion",
    "packageContractVersion", "assessmentVersion", "methodologyVersion",
    "canonicalizationId", "digestAlgorithm", "snapshotDigest",
    "governedConclusionsDigest", "keyId", "signature",
)
_GROUP_FIELDS = (
    "severityAssignedFindings", "assessmentRisk", "confidence",
    "recommendations", "executiveSummary",
)
_FINDING_FIELDS = (
    "findingId", "title", "primaryDimension", "relatedDimensions",
    "triggerSource", "findingType", "businessConsequenceBasis",
    "sourceReferences", "sequenceIdentifier", "severityClassification",
    "severityDecisionIdentifier", "severityDecisionTableVersion",
)
_RISK_FIELDS = (
    "riskClassification", "riskDecisionIdentifier", "riskDecisionTableVersion",
)
_CONFIDENCE_FIELDS = (
    "confidenceClassification", "confidenceDecisionIdentifier",
    "confidenceDecisionTableVersion",
)
_RECOMMENDATION_FIELDS = (
    "findingId", "recommendationClassification",
    "recommendationDecisionIdentifier", "recommendationDecisionTableVersion",
)
_SUMMARY_FIELDS = ("findingCount", "sectionText")
_SECTION_FIELDS = (
    "overall-assessment-overview", "business-capability-highlights",
    "significant-findings", "risk-overview", "confidence-statement",
    "recommended-actions", "closing-assessment-statement",
)
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}\Z")
_HEX_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_COMMIT = re.compile(r"[0-9a-f]{40}\Z")


class FailureCode(str, Enum):
    INVALID_SNAPSHOT_ENCODING = "invalid-snapshot-encoding"
    PRODUCER_VALIDATION_FAILURE = "producer-validation-failure"
    UNSUPPORTED_PRODUCER_CONTRACT = "unsupported-producer-contract"
    INVALID_CONCLUSION_STRUCTURE = "invalid-conclusion-structure"
    MISSING_ATTESTATION = "missing-attestation"
    MISSING_ATTESTATION_FIELD = "missing-attestation-field"
    UNEXPECTED_ATTESTATION_FIELD = "unexpected-attestation-field"
    MALFORMED_ATTESTATION = "malformed-attestation"
    UNSUPPORTED_ATTESTATION_VERSION = "unsupported-attestation-version"
    UNKNOWN_ISSUER = "unknown-issuer"
    UNKNOWN_KEY_ID = "unknown-key-id"
    INVALID_SIGNATURE = "invalid-signature"
    SNAPSHOT_DIGEST_MISMATCH = "snapshot-digest-mismatch"
    SNAPSHOT_IDENTITY_MISMATCH = "snapshot-identity-mismatch"
    CONCLUSIONS_DIGEST_MISMATCH = "conclusions-digest-mismatch"
    PRODUCER_VERSION_MISMATCH = "producer-version-mismatch"


class AttestationError(ValueError):
    """A payload-free internal failure with a stable machine-readable category."""

    def __init__(self, code: FailureCode):
        self.code = code
        super().__init__(code.value)


def _reject_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise AttestationError(FailureCode.INVALID_SNAPSHOT_ENCODING)
        result[key] = value
    return result


def _reject_nonfinite(_value: str) -> None:
    raise AttestationError(FailureCode.INVALID_SNAPSHOT_ENCODING)


def _finite_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise AttestationError(FailureCode.INVALID_SNAPSHOT_ENCODING)
    return number


def _check_unicode(value: object) -> None:
    if isinstance(value, str):
        value.encode("utf-8", "strict")
    elif isinstance(value, list):
        for item in value:
            _check_unicode(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            _check_unicode(key)
            _check_unicode(item)


def _parse_snapshot(snapshot_bytes: bytes) -> dict:
    if type(snapshot_bytes) is not bytes or snapshot_bytes.startswith(b"\xef\xbb\xbf"):
        raise AttestationError(FailureCode.INVALID_SNAPSHOT_ENCODING)
    try:
        value = json.loads(
            snapshot_bytes.decode("utf-8", "strict"),
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=_reject_nonfinite,
            parse_float=_finite_float,
        )
        _check_unicode(value)
    except AttestationError:
        raise
    except (UnicodeError, ValueError, OverflowError, RecursionError, TypeError) as exc:
        raise AttestationError(FailureCode.INVALID_SNAPSHOT_ENCODING) from None
    if type(value) is not dict:
        raise AttestationError(FailureCode.INVALID_SNAPSHOT_ENCODING)
    return value


def _snapshot_versions(snapshot: dict) -> dict[str, str]:
    try:
        metadata = snapshot["businessDecisionPackage"]["versionMetadata"]
        versions = {
            "snapshotResponseContractVersion": snapshot["responseContractVersion"],
            "packageContractVersion": metadata["contractVersion"],
            "assessmentVersion": metadata["assessmentVersion"],
            "methodologyVersion": metadata["methodologyVersion"],
        }
    except (KeyError, TypeError, AttributeError) as exc:
        raise AttestationError(FailureCode.UNSUPPORTED_PRODUCER_CONTRACT) from None
    expected = {
        "snapshotResponseContractVersion": EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
        "packageContractVersion": GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
        "assessmentVersion": EXECUTIVE_ASSESSMENT_VERSION_V2,
        "methodologyVersion": METHODOLOGY_VERSION,
    }
    if versions != expected:
        raise AttestationError(FailureCode.UNSUPPORTED_PRODUCER_CONTRACT)
    return versions


def _validated_snapshot(snapshot_bytes: bytes) -> tuple[dict, dict[str, str]]:
    snapshot = _parse_snapshot(snapshot_bytes)
    try:
        result = validate_executive_assessment_snapshot_serialization(snapshot)
    except Exception as exc:
        raise AttestationError(FailureCode.PRODUCER_VALIDATION_FAILURE) from None
    if getattr(result, "is_valid", None) is not True:
        try:
            _snapshot_versions(snapshot)
        except AttestationError as exc:
            raise exc from None
        raise AttestationError(FailureCode.PRODUCER_VALIDATION_FAILURE)
    versions = _snapshot_versions(snapshot)
    return snapshot, versions


def _ordered_object(value: object, fields: tuple[str, ...]) -> dict:
    if type(value) is not dict or tuple(value) != fields:
        raise AttestationError(FailureCode.INVALID_CONCLUSION_STRUCTURE)
    return {field: value[field] for field in fields}


def _string(value: object) -> str:
    if type(value) is not str:
        raise AttestationError(FailureCode.INVALID_CONCLUSION_STRUCTURE)
    return value


def _integer(value: object) -> int:
    if type(value) is not int:
        raise AttestationError(FailureCode.INVALID_CONCLUSION_STRUCTURE)
    return value


def _string_array(value: object) -> list[str]:
    if type(value) is not list:
        raise AttestationError(FailureCode.INVALID_CONCLUSION_STRUCTURE)
    return [_string(item) for item in value]


def _canonical_conclusions(snapshot: dict) -> bytes:
    try:
        governed = snapshot["businessDecisionPackage"]["governedConclusions"]
        groups = _ordered_object(governed, _GROUP_FIELDS)
        findings = groups["severityAssignedFindings"]
        recommendations = groups["recommendations"]
        if type(findings) is not list or type(recommendations) is not list:
            raise AttestationError(FailureCode.INVALID_CONCLUSION_STRUCTURE)
        ordered_findings = []
        for item in findings:
            row = _ordered_object(item, _FINDING_FIELDS)
            ordered_findings.append({
                field: (_integer(row[field]) if field == "sequenceIdentifier" else
                        _string_array(row[field]) if field in ("relatedDimensions", "sourceReferences") else
                        _string(row[field]))
                for field in _FINDING_FIELDS
            })
        ordered_recommendations = []
        for item in recommendations:
            row = _ordered_object(item, _RECOMMENDATION_FIELDS)
            ordered_recommendations.append({
                field: (None if field == "findingId" and row[field] is None else
                        _string(row[field]))
                for field in _RECOMMENDATION_FIELDS
            })
        risk = _ordered_object(groups["assessmentRisk"], _RISK_FIELDS)
        confidence = _ordered_object(groups["confidence"], _CONFIDENCE_FIELDS)
        summary = _ordered_object(groups["executiveSummary"], _SUMMARY_FIELDS)
        sections = _ordered_object(summary["sectionText"], _SECTION_FIELDS)
        canonical = {
            "severityAssignedFindings": ordered_findings,
            "assessmentRisk": {field: _string(risk[field]) for field in _RISK_FIELDS},
            "confidence": {field: _string(confidence[field]) for field in _CONFIDENCE_FIELDS},
            "recommendations": ordered_recommendations,
            "executiveSummary": {
                "findingCount": _integer(summary["findingCount"]),
                "sectionText": {field: _string(sections[field]) for field in _SECTION_FIELDS},
            },
        }
        return json.dumps(
            canonical, ensure_ascii=False, separators=(",", ":"), allow_nan=False,
        ).encode("utf-8", "strict")
    except AttestationError:
        raise
    except (KeyError, TypeError, ValueError, UnicodeError, OverflowError) as exc:
        raise AttestationError(FailureCode.INVALID_CONCLUSION_STRUCTURE) from None


def _digest(domain: bytes, content: bytes) -> str:
    return hashlib.sha256(domain + content).hexdigest()


def _signed_payload(sidecar: Mapping[str, str]) -> bytes:
    parts = [_SIGNATURE_DOMAIN]
    for field in SIDECAR_FIELDS[:-1]:
        encoded = sidecar[field].encode("utf-8", "strict")
        parts.append(len(encoded).to_bytes(4, "big"))
        parts.append(encoded)
    return b"".join(parts)


def _identifier(value: str) -> bool:
    return type(value) is str and _IDENTIFIER.fullmatch(value) is not None


def _sidecar(sidecar: object) -> dict[str, str]:
    if sidecar is None:
        raise AttestationError(FailureCode.MISSING_ATTESTATION)
    if type(sidecar) is not dict:
        raise AttestationError(FailureCode.MALFORMED_ATTESTATION)
    expected = set(SIDECAR_FIELDS)
    if expected - sidecar.keys():
        raise AttestationError(FailureCode.MISSING_ATTESTATION_FIELD)
    if sidecar.keys() - expected:
        raise AttestationError(FailureCode.UNEXPECTED_ATTESTATION_FIELD)
    if any(type(sidecar[field]) is not str or not sidecar[field] for field in SIDECAR_FIELDS):
        raise AttestationError(FailureCode.MALFORMED_ATTESTATION)
    try:
        for field in SIDECAR_FIELDS:
            sidecar[field].encode("utf-8", "strict")
    except UnicodeError:
        raise AttestationError(FailureCode.MALFORMED_ATTESTATION) from None
    if sidecar["verificationContractVersion"] != VERIFICATION_CONTRACT_VERSION:
        raise AttestationError(FailureCode.UNSUPPORTED_ATTESTATION_VERSION)
    if sidecar["canonicalizationId"] != CANONICALIZATION_ID or sidecar["digestAlgorithm"] != DIGEST_ALGORITHM:
        raise AttestationError(FailureCode.MALFORMED_ATTESTATION)
    if not _identifier(sidecar["issuerId"]) or not _identifier(sidecar["keyId"]):
        raise AttestationError(FailureCode.MALFORMED_ATTESTATION)
    if _COMMIT.fullmatch(sidecar["producerReleaseCommit"]) is None:
        raise AttestationError(FailureCode.MALFORMED_ATTESTATION)
    if any(_HEX_DIGEST.fullmatch(sidecar[field]) is None for field in
           ("snapshotDigest", "governedConclusionsDigest")):
        raise AttestationError(FailureCode.MALFORMED_ATTESTATION)
    if sidecar["producerSnapshotIdentity"] != "sha256:" + sidecar["snapshotDigest"]:
        raise AttestationError(FailureCode.SNAPSHOT_IDENTITY_MISMATCH)
    try:
        raw_signature = base64.b64decode(sidecar["signature"], validate=True)
    except (ValueError, binascii.Error) as exc:
        raise AttestationError(FailureCode.MALFORMED_ATTESTATION) from None
    if len(raw_signature) != 64 or base64.b64encode(raw_signature).decode("ascii") != sidecar["signature"]:
        raise AttestationError(FailureCode.MALFORMED_ATTESTATION)
    return sidecar


class ProducerSnapshotIssuer:
    """Owner-constructed issuer; snapshot callers cannot supply a signing key."""

    def __init__(self, signing_key: Ed25519PrivateKey, *, issuer_id: str,
                 key_id: str, producer_release_commit: str):
        if not isinstance(signing_key, Ed25519PrivateKey):
            raise TypeError("An Ed25519 signing capability is required.")
        if not _identifier(issuer_id) or not _identifier(key_id) or type(producer_release_commit) is not str or _COMMIT.fullmatch(producer_release_commit) is None:
            raise ValueError("Invalid issuer configuration.")
        self._signing_key = signing_key
        self._issuer_id = issuer_id
        self._key_id = key_id
        self._release = producer_release_commit

    def issue(self, snapshot_bytes: bytes) -> dict[str, str]:
        snapshot, versions = _validated_snapshot(snapshot_bytes)
        conclusions = _canonical_conclusions(snapshot)
        snapshot_digest = _digest(_SNAPSHOT_DOMAIN, snapshot_bytes)
        sidecar = {
            "verificationContractVersion": VERIFICATION_CONTRACT_VERSION,
            "issuerId": self._issuer_id,
            "producerReleaseCommit": self._release,
            "producerSnapshotIdentity": "sha256:" + snapshot_digest,
            **versions,
            "canonicalizationId": CANONICALIZATION_ID,
            "digestAlgorithm": DIGEST_ALGORITHM,
            "snapshotDigest": snapshot_digest,
            "governedConclusionsDigest": _digest(_CONCLUSIONS_DOMAIN, conclusions),
            "keyId": self._key_id,
        }
        sidecar["signature"] = base64.b64encode(
            self._signing_key.sign(_signed_payload(sidecar))
        ).decode("ascii")
        return sidecar


class ProducerSnapshotVerifier:
    """Owner-constructed verifier with a separately supplied trusted key registry."""

    def __init__(self, *, trusted_issuer_id: str,
                 trusted_keys: Mapping[str, Ed25519PublicKey],
                 expected_release_commit: str):
        if not _identifier(trusted_issuer_id) or type(expected_release_commit) is not str or _COMMIT.fullmatch(expected_release_commit) is None:
            raise ValueError("Invalid verifier configuration.")
        if type(trusted_keys) is not dict or not trusted_keys or any(
            not _identifier(key_id) or not isinstance(key, Ed25519PublicKey)
            for key_id, key in trusted_keys.items()
        ):
            raise ValueError("Invalid trusted key registry.")
        self._trusted_issuer_id = trusted_issuer_id
        self._trusted_keys = dict(trusted_keys)
        self._release = expected_release_commit

    def verify(self, snapshot_bytes: bytes, sidecar: object) -> None:
        attestation = _sidecar(sidecar)
        if attestation["issuerId"] != self._trusted_issuer_id:
            raise AttestationError(FailureCode.UNKNOWN_ISSUER)
        key = self._trusted_keys.get(attestation["keyId"])
        if key is None:
            raise AttestationError(FailureCode.UNKNOWN_KEY_ID)
        try:
            key.verify(base64.b64decode(attestation["signature"], validate=True),
                       _signed_payload(attestation))
        except (InvalidSignature, ValueError, TypeError) as exc:
            raise AttestationError(FailureCode.INVALID_SIGNATURE) from None
        if attestation["producerReleaseCommit"] != self._release:
            raise AttestationError(FailureCode.PRODUCER_VERSION_MISMATCH)
        _parse_snapshot(snapshot_bytes)
        digest = _digest(_SNAPSHOT_DOMAIN, snapshot_bytes)
        if attestation["snapshotDigest"] != digest:
            raise AttestationError(FailureCode.SNAPSHOT_DIGEST_MISMATCH)
        if attestation["producerSnapshotIdentity"] != "sha256:" + digest:
            raise AttestationError(FailureCode.SNAPSHOT_IDENTITY_MISMATCH)
        validated, versions = _validated_snapshot(snapshot_bytes)
        if any(attestation[field] != versions[field] for field in versions):
            raise AttestationError(FailureCode.PRODUCER_VERSION_MISMATCH)
        conclusions = _canonical_conclusions(validated)
        if attestation["governedConclusionsDigest"] != _digest(_CONCLUSIONS_DOMAIN, conclusions):
            raise AttestationError(FailureCode.CONCLUSIONS_DIGEST_MISMATCH)
