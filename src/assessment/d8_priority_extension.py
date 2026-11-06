"""Strict, unsigned local synthetic D8 extension; no production caller."""

import hashlib
import json
import re
from dataclasses import fields

from assessment.approved_confidence_runtime import ApprovedConfidenceAssessmentResult
from assessment.approved_methodology_runtime_config import (
    CONFIDENCE_DECISION_RULES, CONFIDENCE_DECISION_TABLE_SET_VERSION,
    RECOMMENDATION_DECISION_RULES, RECOMMENDATION_DECISION_TABLE_SET_VERSION,
)
from assessment.decision_engine import GovernedAssessmentResult
from assessment.governed_assessment_input import (
    EXECUTIVE_ASSESSMENT_VERSION_V2, FindingInput,
    ValidatedCanonicalExecutiveAssessmentInputV2,
)
from assessment.governed_decision_runtime import GovernedRecommendationResult
from assessment.local_d8_priority import (
    METHODOLOGY_VERSION as D8_METHODOLOGY_VERSION,
    RULE_TABLE_VERSION as D8_RULE_TABLE_VERSION,
    NO_FINDINGS_MONITOR, PRIORITY_ASSIGNED, PRIORITY_NOT_DETERMINED,
    LocalD8Result,
)
from assessment.local_d8_producer_adapter import (
    LocalD8ProducerRequest, LocalSyntheticProducerBinding,
)
from assessment.local_priority_assertions import (
    MAX_ASSERTIONS, MAX_EVIDENCE_REFERENCES, MAX_TEXT, VALID_EVALUATED,
    RecommendationInstance, SyntheticContext, validate_local_assertions,
)
from assessment.methodology_config import METHODOLOGY_VERSION as PRODUCER_METHODOLOGY_VERSION


SCHEMA_ID = "nguyen-ai-local-d8-priority-extension"
SCHEMA_VERSION = 1
DESIGNATION = "SYNTHETIC_NONPRODUCTION"
CANONICALIZATION_ID = "local-d8-extension-json-v1"
DIGEST_ALGORITHM = "SHA-256"
MAX_ARTIFACT_BYTES = 65536
_DOMAIN = b"NGUYEN-LOCAL-D8-EXTENSION-v1\x00"
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
_REVIEW = re.compile(r"local-synthetic-d8-review-v1:[0-9a-f]{64}\Z")
_DRIVERS = ("customer-impact", "executive-urgency", "dependency-role")
_VALUES = {
    "customer-impact": {"impact-present", "impact-affirmed-absent"},
    "executive-urgency": {"time-bound-executive-action", "executive-action-required",
                          "executive-action-affirmed-absent"},
    "dependency-role": {"blocks-related-work", "unlocks-related-work",
                        "no-dependency-affirmed"},
}
_RULE_IDS = {"B-C1", "G-H1", "G-H2", "B-H3", "N-H7", "B-M1", "G-L1"}
_PRIORITIES = {"critical", "high", "medium", "low"}
_BASE_FIELDS = (
    "schemaId", "schemaVersion", "designation", "assessmentIdentity",
    "assessmentVersion", "producerMethodologyVersion", "snapshotIdentity",
    "findingId", "recommendationInstanceIdentity", "recommendationDecisionIdentifier",
    "recommendationDecisionTableVersion", "confidenceClassification",
    "confidenceDecisionIdentifier", "confidenceDecisionTableVersion",
    "d8MethodologyVersion", "d8RuleTableVersion", "outcome", "confidenceGate",
    "validatedAssertionIds", "evidenceProvenance", "reviewRequired",
)
_CONDITIONAL_FIELDS = {
    PRIORITY_ASSIGNED: ("priority", "winningRuleIds"),
    PRIORITY_NOT_DETERMINED: (
        "governedFindingType", "governedConsequenceBasis", "excludedRuleIds",
        "evaluatedDriverValues", "reviewReference",
    ),
    NO_FINDINGS_MONITOR: (),
}
_INTEGRITY_FIELDS = ("canonicalizationId", "digestAlgorithm", "payloadDigest")


def _fail(reason: str) -> None:
    raise ValueError("Invalid local D8 extension: " + reason)


def _text(value: object) -> bool:
    return type(value) is str and 0 < len(value) <= MAX_TEXT and value.strip() == value


def _complete(value: object, kind: type) -> bool:
    return type(value) is kind and all(hasattr(value, field.name) for field in fields(kind))


def _sorted_unique(values: object, *, allow_empty: bool = True) -> bool:
    return (type(values) is list and (allow_empty or bool(values))
            and len(values) <= MAX_ASSERTIONS
            and all(_text(value) for value in values)
            and values == sorted(set(values)))


def _json_bytes(value: dict) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"),
                          allow_nan=False).encode("utf-8", "strict")
    except (TypeError, ValueError, UnicodeError, OverflowError, RecursionError):
        _fail("noncanonical JSON value")


def _validate_payload(payload: object) -> None:
    if type(payload) is not dict:
        _fail("payload type")
    outcome = payload.get("outcome")
    if type(outcome) is not str or outcome not in _CONDITIONAL_FIELDS:
        _fail("ineligible outcome")
    if tuple(payload) != _BASE_FIELDS + _CONDITIONAL_FIELDS[outcome]:
        _fail("payload fields or order")
    if (payload["schemaId"] != SCHEMA_ID or type(payload["schemaId"]) is not str
            or type(payload["schemaVersion"]) is not int
            or payload["schemaVersion"] != SCHEMA_VERSION
            or payload["designation"] != DESIGNATION
            or type(payload["designation"]) is not str
            or payload["assessmentVersion"] != EXECUTIVE_ASSESSMENT_VERSION_V2
            or payload["producerMethodologyVersion"] != PRODUCER_METHODOLOGY_VERSION
            or payload["d8MethodologyVersion"] != D8_METHODOLOGY_VERSION
            or payload["d8RuleTableVersion"] != D8_RULE_TABLE_VERSION):
        _fail("unsupported schema or methodology version")
    for key in (
        "assessmentIdentity", "snapshotIdentity", "recommendationInstanceIdentity",
        "recommendationDecisionIdentifier", "recommendationDecisionTableVersion",
        "confidenceClassification", "confidenceDecisionIdentifier",
        "confidenceDecisionTableVersion",
    ):
        if not _text(payload[key]):
            _fail("invalid identity or decision field")
    if not _sorted_unique(payload["validatedAssertionIds"]):
        _fail("assertion IDs")
    provenance = payload["evidenceProvenance"]
    if type(provenance) is not list or len(provenance) > MAX_ASSERTIONS:
        _fail("provenance type or count")
    ids = []
    for entry in provenance:
        if type(entry) is not dict or tuple(entry) != ("assertionId", "evidenceReferences"):
            _fail("provenance fields")
        refs = entry["evidenceReferences"]
        if (not _text(entry["assertionId"]) or not _sorted_unique(refs, allow_empty=False)
                or len(refs) > MAX_EVIDENCE_REFERENCES):
            _fail("provenance reference")
        ids.append(entry["assertionId"])
    if ids != payload["validatedAssertionIds"]:
        _fail("provenance assertion mismatch")
    if type(payload["reviewRequired"]) is not bool:
        _fail("review flag")
    if outcome == PRIORITY_ASSIGNED:
        if (not _text(payload["findingId"])
                or payload["confidenceGate"] != "PASSED"
                or payload["reviewRequired"] is not False
                or type(payload["priority"]) is not str
                or payload["priority"] not in _PRIORITIES
                or not _sorted_unique(payload["winningRuleIds"], allow_empty=False)
                or not set(payload["winningRuleIds"]) <= _RULE_IDS):
            _fail("assigned outcome shape")
    elif outcome == PRIORITY_NOT_DETERMINED:
        if (not _text(payload["findingId"])
                or payload["confidenceGate"] != "PASSED"
                or payload["reviewRequired"] is not True
                or not _text(payload["governedFindingType"])
                or not _text(payload["governedConsequenceBasis"])
                or not _sorted_unique(payload["excludedRuleIds"], allow_empty=False)
                or not set(payload["excludedRuleIds"]) <= _RULE_IDS
                or type(payload["reviewReference"]) is not str
                or _REVIEW.fullmatch(payload["reviewReference"]) is None):
            _fail("PND outcome shape")
        drivers = payload["evaluatedDriverValues"]
        if type(drivers) is not list or len(drivers) != len(_DRIVERS):
            _fail("PND driver count")
        for entry, driver in zip(drivers, _DRIVERS):
            if (type(entry) is not dict or tuple(entry) != ("driverId", "assertedValue")
                    or entry["driverId"] != driver
                    or (entry["assertedValue"] is not None
                        and (type(entry["assertedValue"]) is not str
                             or entry["assertedValue"] not in _VALUES[driver]))):
                _fail("PND driver value")
    else:
        if (payload["findingId"] is not None
                or payload["confidenceGate"] != "NOT_APPLICABLE_NO_FINDINGS"
                or payload["reviewRequired"] is not False
                or payload["validatedAssertionIds"] != []
                or provenance != []
                or payload["recommendationDecisionIdentifier"] !=
                   "recommendation-v1-no-findings-monitor"
                or payload["confidenceClassification"] == "insufficient-confidence"):
            _fail("D7 outcome shape")
    if outcome != NO_FINDINGS_MONITOR and payload["confidenceClassification"] == "insufficient-confidence":
        _fail("insufficient confidence")


def _pairs(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            _fail("duplicate JSON field")
        result[key] = value
    return result


def _nonfinite(_value: str) -> None:
    _fail("nonfinite JSON number")


def validate_local_d8_extension(blob: bytes) -> dict:
    """Verify strict local schema and digest; return the validated JSON object."""
    if type(blob) is not bytes or len(blob) > MAX_ARTIFACT_BYTES or blob.startswith(b"\xef\xbb\xbf"):
        _fail("artifact type, size, or encoding")
    try:
        artifact = json.loads(blob.decode("utf-8", "strict"),
                              object_pairs_hook=_pairs, parse_constant=_nonfinite)
    except (UnicodeError, json.JSONDecodeError, RecursionError, OverflowError):
        _fail("malformed JSON")
    if type(artifact) is not dict or tuple(artifact) != ("payload", "integrity"):
        _fail("artifact fields")
    payload = artifact["payload"]
    _validate_payload(payload)
    integrity = artifact["integrity"]
    if (type(integrity) is not dict or tuple(integrity) != _INTEGRITY_FIELDS
            or integrity["canonicalizationId"] != CANONICALIZATION_ID
            or integrity["digestAlgorithm"] != DIGEST_ALGORITHM
            or type(integrity["payloadDigest"]) is not str
            or _DIGEST.fullmatch(integrity["payloadDigest"]) is None):
        _fail("integrity metadata")
    expected = "sha256:" + hashlib.sha256(_DOMAIN + _json_bytes(payload)).hexdigest()
    if integrity["payloadDigest"] != expected:
        _fail("digest mismatch")
    if _json_bytes(artifact) != blob:
        _fail("noncanonical artifact bytes")
    return artifact


def build_local_d8_extension(request: LocalD8ProducerRequest,
                             result: LocalD8Result) -> bytes:
    """Copy one eligible adapter decision into a local synthetic artifact."""
    if not _complete(request, LocalD8ProducerRequest) or not _complete(result, LocalD8Result):
        _fail("request or result type")
    binding = request.binding
    context = request.synthetic_context
    canonical = request.canonical_input
    producer = request.governed_result
    if (not _complete(binding, LocalSyntheticProducerBinding)
            or not _complete(context, SyntheticContext)
            or not _complete(canonical, ValidatedCanonicalExecutiveAssessmentInputV2)
            or not _complete(producer, GovernedAssessmentResult)
            or not _complete(producer.confidence, ApprovedConfidenceAssessmentResult)):
        _fail("request structure")
    if (canonical.assessment_version != EXECUTIVE_ASSESSMENT_VERSION_V2
            or canonical.methodology_version != PRODUCER_METHODOLOGY_VERSION
            or type(canonical.findings) is not tuple
            or type(producer.findings) is not tuple
            or producer.findings != canonical.findings
            or type(producer.recommendations) is not tuple
            or type(context.recommendations) is not tuple
            or len(producer.recommendations) != max(1, len(canonical.findings))
            or len(context.recommendations) != len(producer.recommendations)
            or any(not _complete(item, FindingInput) for item in canonical.findings)
            or any(not _complete(item, GovernedRecommendationResult)
                   for item in producer.recommendations)
            or any(not _complete(item, RecommendationInstance)
                   for item in context.recommendations)):
        _fail("producer collection or version")
    if (not all(_text(value) for value in (
            binding.assessment_identity, binding.snapshot_identity,
            binding.recommendation_instance_identity,
            binding.recommendation_decision_identifier,
            binding.recommendation_decision_table_version,
            context.assessment_identity, context.snapshot_identity,
            result.assessment_identity, result.snapshot_identity,
            result.recommendation_instance_identity))
            or len({binding.assessment_identity, context.assessment_identity,
                    result.assessment_identity}) != 1
            or len({binding.snapshot_identity, context.snapshot_identity,
                    result.snapshot_identity}) != 1
            or binding.recommendation_instance_identity != result.recommendation_instance_identity
            or (binding.finding_id is not None and not _text(binding.finding_id))
            or (result.finding_id is not None and not _text(result.finding_id))
            or binding.finding_id != result.finding_id
            or result.methodology_version != D8_METHODOLOGY_VERSION
            or result.rule_table_version != D8_RULE_TABLE_VERSION):
        _fail("identity or D8 version binding")
    if (any(not _text(item.finding_id) for item in canonical.findings)
            or any(item.finding_id is not None and not _text(item.finding_id)
                   for item in producer.recommendations)
            or any(not all(_text(value) for value in (
                item.recommendation_classification,
                item.recommendation_decision_identifier,
                item.recommendation_decision_table_version))
                   for item in producer.recommendations)
            or any(item.finding_id is not None and not _text(item.finding_id)
                   or not _text(item.instance_identity)
                   or not _text(item.decision_identifier)
                   or not _text(item.decision_table_version)
                   for item in context.recommendations)
            or type(result.outcome) is not str
            or type(result.pending_rule_ids) is not tuple
            or type(result.validated_assertion_ids) is not tuple
            or type(result.matched_rule_ids) is not tuple
            or type(result.excluded_rule_ids) is not tuple
            or type(result.evaluated_driver_values) is not tuple
            or type(result.review_required) is not bool):
        _fail("malformed identity or result fields")
    findings = [item.finding_id for item in canonical.findings]
    rec_ids = [item.finding_id for item in producer.recommendations]
    inst_ids = [item.finding_id for item in context.recommendations]
    instance_names = [item.instance_identity for item in context.recommendations]
    expected = set(findings) if findings else {None}
    if (len(findings) != len(set(findings)) or len(rec_ids) != len(set(rec_ids))
            or len(inst_ids) != len(set(inst_ids))
            or len(instance_names) != len(set(instance_names))
            or set(rec_ids) != expected or set(inst_ids) != expected
            or binding.finding_id not in expected):
        _fail("ambiguous finding or recommendation binding")
    selected = next((item for item in context.recommendations
                     if item.finding_id == binding.finding_id), None)
    recommendation = next((item for item in producer.recommendations
                           if item.finding_id == binding.finding_id), None)
    if (type(selected) is not RecommendationInstance or recommendation is None
            or selected.instance_identity != binding.recommendation_instance_identity
            or selected.decision_identifier != binding.recommendation_decision_identifier
            or selected.decision_table_version != binding.recommendation_decision_table_version
            or recommendation.recommendation_decision_identifier != binding.recommendation_decision_identifier
            or recommendation.recommendation_decision_table_version != binding.recommendation_decision_table_version):
        _fail("selected recommendation binding")
    confidence = producer.confidence
    if (not all(_text(getattr(confidence, key, None)) for key in (
            "confidence_classification", "confidence_decision_identifier",
            "confidence_decision_table_version"))
            or confidence.methodology_version != PRODUCER_METHODOLOGY_VERSION
            or confidence.confidence_decision_table_version != CONFIDENCE_DECISION_TABLE_SET_VERSION
            or confidence.confidence_decision_identifier not in CONFIDENCE_DECISION_RULES
            or CONFIDENCE_DECISION_RULES[
                confidence.confidence_decision_identifier].output != confidence.confidence_classification
            or recommendation.recommendation_decision_table_version != RECOMMENDATION_DECISION_TABLE_SET_VERSION
            or recommendation.recommendation_decision_identifier not in RECOMMENDATION_DECISION_RULES
            or RECOMMENDATION_DECISION_RULES[
                recommendation.recommendation_decision_identifier].output !=
               recommendation.recommendation_classification):
        _fail("confidence binding")
    if result.outcome not in _CONDITIONAL_FIELDS:
        _fail("ineligible outcome")
    if (result.pending_rule_ids or type(request.synthetic_assertions) is not list
            or len(request.synthetic_assertions) > MAX_ASSERTIONS):
        _fail("pending rule or assertion collection")
    checked = validate_local_assertions(request.synthetic_assertions, context,
                                        required_driver_ids=frozenset())
    if any(item.status != VALID_EVALUATED for item in checked.outcomes):
        _fail("invalid synthetic assertions")
    records = []
    for record in request.synthetic_assertions:
        if type(record) is not dict:
            _fail("assertion record type")
        if record["recommendationInstanceIdentity"] == selected.instance_identity:
            records.append(record)
    records.sort(key=lambda item: item["assertionId"])
    assertion_ids = [item["assertionId"] for item in records]
    if tuple(assertion_ids) != result.validated_assertion_ids:
        _fail("assertion trace binding")
    provenance = [{"assertionId": item["assertionId"],
                   "evidenceReferences": list(item["evidenceReferences"])} for item in records]
    if result.outcome == NO_FINDINGS_MONITOR:
        if (findings or binding.finding_id is not None or request.synthetic_assertions
                or recommendation.recommendation_classification != "monitor"
                or result.priority is not None or result.matched_rule_ids
                or result.excluded_rule_ids or result.review_required
                or result.evaluated_driver_values or result.review_reference is not None):
            _fail("invalid D7 result")
    else:
        if (not findings or not _text(binding.finding_id)
                or confidence.confidence_classification == "insufficient-confidence"):
            _fail("invalid finding-scoped result")
    payload = {
        "schemaId": SCHEMA_ID,
        "schemaVersion": SCHEMA_VERSION,
        "designation": DESIGNATION,
        "assessmentIdentity": binding.assessment_identity,
        "assessmentVersion": canonical.assessment_version,
        "producerMethodologyVersion": canonical.methodology_version,
        "snapshotIdentity": binding.snapshot_identity,
        "findingId": binding.finding_id,
        "recommendationInstanceIdentity": selected.instance_identity,
        "recommendationDecisionIdentifier": recommendation.recommendation_decision_identifier,
        "recommendationDecisionTableVersion": recommendation.recommendation_decision_table_version,
        "confidenceClassification": confidence.confidence_classification,
        "confidenceDecisionIdentifier": confidence.confidence_decision_identifier,
        "confidenceDecisionTableVersion": confidence.confidence_decision_table_version,
        "d8MethodologyVersion": result.methodology_version,
        "d8RuleTableVersion": result.rule_table_version,
        "outcome": result.outcome,
        "confidenceGate": ("NOT_APPLICABLE_NO_FINDINGS" if result.outcome == NO_FINDINGS_MONITOR
                           else "PASSED"),
        "validatedAssertionIds": assertion_ids,
        "evidenceProvenance": provenance,
        "reviewRequired": result.review_required,
    }
    if result.outcome == PRIORITY_ASSIGNED:
        if (type(result.priority) is not str or result.priority not in _PRIORITIES
                or not result.matched_rule_ids
                or result.review_required or result.review_reference is not None
                or result.evaluated_driver_values):
            _fail("invalid assigned result")
        payload["priority"] = result.priority
        payload["winningRuleIds"] = list(result.matched_rule_ids)
    elif result.outcome == PRIORITY_NOT_DETERMINED:
        finding = next(item for item in canonical.findings
                       if item.finding_id == binding.finding_id)
        if (result.priority is not None or result.matched_rule_ids
                or not result.review_required
                or result.governed_finding_type != finding.finding_type
                or result.governed_consequence_basis != finding.business_consequence_basis
                or any(type(item) is not tuple or len(item) != 2
                       for item in result.evaluated_driver_values)
                or result.evaluated_driver_values != tuple(
                    (driver, next((record["assertedValue"] for record in records
                                   if record["driverId"] == driver), None))
                    for driver in _DRIVERS)):
            _fail("invalid PND result")
        payload["governedFindingType"] = result.governed_finding_type
        payload["governedConsequenceBasis"] = result.governed_consequence_basis
        payload["excludedRuleIds"] = list(result.excluded_rule_ids)
        payload["evaluatedDriverValues"] = [
            {"driverId": driver, "assertedValue": value}
            for driver, value in result.evaluated_driver_values
        ]
        payload["reviewReference"] = result.review_reference
    _validate_payload(payload)
    payload_bytes = _json_bytes(payload)
    artifact = {"payload": payload, "integrity": {
        "canonicalizationId": CANONICALIZATION_ID,
        "digestAlgorithm": DIGEST_ALGORITHM,
        "payloadDigest": "sha256:" + hashlib.sha256(_DOMAIN + payload_bytes).hexdigest(),
    }}
    blob = _json_bytes(artifact)
    if len(blob) > MAX_ARTIFACT_BYTES:
        _fail("artifact size")
    validate_local_d8_extension(blob)
    return blob
