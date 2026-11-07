"""Synthetic local D8 extension interpretation; no production admission path.

Expected context is supplied independently by the caller. Integrity, binding,
issuer authenticity, and consumer authorization are separate concerns. This
module establishes only the first two for local synthetic inputs.
"""

from dataclasses import dataclass

from assessment.approved_methodology_runtime_config import (
    CONFIDENCE_DECISION_TABLE_SET_VERSION,
    RECOMMENDATION_DECISION_TABLE_SET_VERSION,
)
from assessment.d8_priority_extension import (
    CANONICALIZATION_ID, DESIGNATION, DIGEST_ALGORITHM, MAX_ARTIFACT_BYTES,
    SCHEMA_ID, SCHEMA_VERSION, _BASE_FIELDS, _CONDITIONAL_FIELDS, _DIGEST,
    _INTEGRITY_FIELDS, _validate_payload, validate_local_d8_extension,
)
from assessment.governed_assessment_input import EXECUTIVE_ASSESSMENT_VERSION_V2
from assessment.local_d8_priority import (
    METHODOLOGY_VERSION as D8_METHODOLOGY_VERSION,
    RULE_TABLE_VERSION as D8_RULE_TABLE_VERSION,
    NO_FINDINGS_MONITOR, PRIORITY_ASSIGNED, PRIORITY_NOT_DETERMINED,
)
from assessment.local_priority_assertions import MAX_TEXT
from assessment.methodology_config import METHODOLOGY_VERSION as PRODUCER_METHODOLOGY_VERSION


# Local consumer control values, not producer outcome or publication authority.
VERIFIED = "VERIFIED"
REJECTED = "REJECTED"

_OUTCOMES = frozenset((PRIORITY_ASSIGNED, PRIORITY_NOT_DETERMINED, NO_FINDINGS_MONITOR))
_DRIVERS = ("customer-impact", "executive-urgency", "dependency-role")
_PRIORITIES = frozenset(("critical", "high", "medium", "low"))


@dataclass(frozen=True, slots=True)
class LocalD8ExpectedContext:
    """Independently established synthetic decision binding, not an authority token."""

    schema_id: str
    schema_version: int
    designation: str
    assessment_identity: str
    assessment_version: str
    producer_methodology_version: str
    snapshot_identity: str
    finding_id: str | None
    recommendation_instance_identity: str
    recommendation_decision_identifier: str
    recommendation_decision_table_version: str
    confidence_classification: str
    confidence_decision_identifier: str
    confidence_decision_table_version: str
    d8_methodology_version: str
    d8_rule_table_version: str
    outcome: str
    priority: str | None = None
    winning_rule_ids: tuple[str, ...] = ()
    governed_finding_type: str | None = None
    governed_consequence_basis: str | None = None
    excluded_rule_ids: tuple[str, ...] = ()
    evaluated_driver_values: tuple[tuple[str, str | None], ...] = ()
    review_reference: str | None = None


@dataclass(frozen=True, slots=True)
class LocalD8ConsumerProjection:
    """Copied, verified local view; all field names here are consumer fields."""

    schema_id: str
    schema_version: int
    designation: str
    assessment_identity: str
    assessment_version: str
    producer_methodology_version: str
    snapshot_identity: str
    finding_id: str | None
    recommendation_instance_identity: str
    recommendation_decision_identifier: str
    recommendation_decision_table_version: str
    confidence_classification: str
    confidence_decision_identifier: str
    confidence_decision_table_version: str
    d8_methodology_version: str
    d8_rule_table_version: str
    outcome: str
    validated_assertion_ids: tuple[str, ...]
    evidence_provenance: tuple[tuple[str, tuple[str, ...]], ...]
    priority: str | None
    winning_rule_ids: tuple[str, ...]
    review_required: bool
    governed_finding_type: str | None
    governed_consequence_basis: str | None
    excluded_rule_ids: tuple[str, ...]
    evaluated_driver_values: tuple[tuple[str, str | None], ...]
    review_reference: str | None


@dataclass(frozen=True, slots=True)
class LocalD8ConsumerResult:
    """Local disposition and projection; no artifact bytes or raw exception."""

    disposition: str
    outcome: str | None = None
    projection: LocalD8ConsumerProjection | None = None
    reason_code: str | None = None


def _text(value: object) -> bool:
    return type(value) is str and 0 < len(value) <= MAX_TEXT and value.strip() == value


def _strings(values: object, *, nonempty: bool = False) -> bool:
    return (type(values) is tuple and (not nonempty or bool(values))
            and all(_text(value) for value in values)
            and values == tuple(sorted(set(values))))


def _valid_context(context: object) -> bool:
    if type(context) is not LocalD8ExpectedContext:
        return False
    for value in (
        context.schema_id, context.designation, context.assessment_version,
        context.producer_methodology_version,
        context.recommendation_decision_table_version,
        context.confidence_decision_table_version, context.d8_methodology_version,
        context.d8_rule_table_version, context.outcome,
    ):
        if type(value) is not str:
            return False
    if (type(context.schema_version) is not int
            or context.schema_id != SCHEMA_ID
            or context.schema_version != SCHEMA_VERSION
            or context.designation != DESIGNATION
            or context.assessment_version != EXECUTIVE_ASSESSMENT_VERSION_V2
            or context.producer_methodology_version != PRODUCER_METHODOLOGY_VERSION
            or context.recommendation_decision_table_version !=
                RECOMMENDATION_DECISION_TABLE_SET_VERSION
            or context.confidence_decision_table_version !=
                CONFIDENCE_DECISION_TABLE_SET_VERSION
            or context.d8_methodology_version != D8_METHODOLOGY_VERSION
            or context.d8_rule_table_version != D8_RULE_TABLE_VERSION
            or context.outcome not in _OUTCOMES):
        return False
    for value in (
        context.assessment_identity, context.snapshot_identity,
        context.recommendation_instance_identity,
        context.recommendation_decision_identifier,
        context.confidence_classification, context.confidence_decision_identifier,
    ):
        if not _text(value):
            return False
    if context.confidence_classification == "insufficient-confidence":
        return False
    if context.outcome == PRIORITY_ASSIGNED:
        return (_text(context.finding_id) and type(context.priority) is str
                and context.priority in _PRIORITIES
                and _strings(context.winning_rule_ids, nonempty=True)
                and context.governed_finding_type is None
                and context.governed_consequence_basis is None
                and type(context.excluded_rule_ids) is tuple
                and context.excluded_rule_ids == ()
                and type(context.evaluated_driver_values) is tuple
                and context.evaluated_driver_values == ()
                and context.review_reference is None)
    if context.outcome == PRIORITY_NOT_DETERMINED:
        drivers = context.evaluated_driver_values
        return (_text(context.finding_id) and context.priority is None
                and type(context.winning_rule_ids) is tuple
                and context.winning_rule_ids == ()
                and _text(context.governed_finding_type)
                and _text(context.governed_consequence_basis)
                and _strings(context.excluded_rule_ids, nonempty=True)
                and type(drivers) is tuple and len(drivers) == len(_DRIVERS)
                and all(type(pair) is tuple and len(pair) == 2
                        and pair[0] == driver
                        and (pair[1] is None or _text(pair[1]))
                        for pair, driver in zip(drivers, _DRIVERS))
                and _text(context.review_reference))
    return (context.finding_id is None and context.priority is None
            and type(context.winning_rule_ids) is tuple
            and context.winning_rule_ids == ()
            and context.governed_finding_type is None
            and context.governed_consequence_basis is None
            and type(context.excluded_rule_ids) is tuple
            and context.excluded_rule_ids == ()
            and type(context.evaluated_driver_values) is tuple
            and context.evaluated_driver_values == ()
            and context.review_reference is None
            and context.recommendation_decision_identifier ==
                "recommendation-v1-no-findings-monitor")


def _verified_payload(value: object) -> dict | None:
    """Require the verifier's exact parsed-object success shape."""
    if type(value) is not dict or tuple(value) != ("payload", "integrity"):
        return None
    payload = value["payload"]
    integrity = value["integrity"]
    if type(payload) is not dict or type(integrity) is not dict:
        return None
    outcome = payload.get("outcome")
    if type(outcome) is not str or outcome not in _CONDITIONAL_FIELDS:
        return None
    if (tuple(payload) != _BASE_FIELDS + _CONDITIONAL_FIELDS[outcome]
            or tuple(integrity) != _INTEGRITY_FIELDS
            or integrity["canonicalizationId"] != CANONICALIZATION_ID
            or integrity["digestAlgorithm"] != DIGEST_ALGORITHM
            or type(integrity["payloadDigest"]) is not str
            or _DIGEST.fullmatch(integrity["payloadDigest"]) is None):
        return None
    try:
        _validate_payload(payload)
    except ValueError:
        return None
    return payload


def _matches_context(payload: dict, context: LocalD8ExpectedContext) -> bool:
    expected = (
        ("schemaId", context.schema_id),
        ("schemaVersion", context.schema_version),
        ("designation", context.designation),
        ("assessmentIdentity", context.assessment_identity),
        ("assessmentVersion", context.assessment_version),
        ("producerMethodologyVersion", context.producer_methodology_version),
        ("snapshotIdentity", context.snapshot_identity),
        ("findingId", context.finding_id),
        ("recommendationInstanceIdentity", context.recommendation_instance_identity),
        ("recommendationDecisionIdentifier", context.recommendation_decision_identifier),
        ("recommendationDecisionTableVersion", context.recommendation_decision_table_version),
        ("confidenceClassification", context.confidence_classification),
        ("confidenceDecisionIdentifier", context.confidence_decision_identifier),
        ("confidenceDecisionTableVersion", context.confidence_decision_table_version),
        ("d8MethodologyVersion", context.d8_methodology_version),
        ("d8RuleTableVersion", context.d8_rule_table_version),
        ("outcome", context.outcome),
    )
    if any(type(payload[key]) is not type(value) or payload[key] != value
           for key, value in expected):
        return False
    if context.outcome == PRIORITY_ASSIGNED:
        return (payload["priority"] == context.priority
                and payload["winningRuleIds"] == list(context.winning_rule_ids)
                and payload["confidenceGate"] == "PASSED"
                and payload["reviewRequired"] is False)
    if context.outcome == PRIORITY_NOT_DETERMINED:
        return (payload["governedFindingType"] == context.governed_finding_type
                and payload["governedConsequenceBasis"] == context.governed_consequence_basis
                and payload["excludedRuleIds"] == list(context.excluded_rule_ids)
                and payload["evaluatedDriverValues"] == [
                    {"driverId": driver, "assertedValue": value}
                    for driver, value in context.evaluated_driver_values]
                and payload["reviewReference"] == context.review_reference
                and payload["confidenceGate"] == "PASSED"
                and payload["reviewRequired"] is True)
    return (payload["findingId"] is None
            and payload["confidenceGate"] == "NOT_APPLICABLE_NO_FINDINGS"
            and payload["reviewRequired"] is False
            and payload["validatedAssertionIds"] == []
            and payload["evidenceProvenance"] == [])


def consume_local_d8_extension(
    artifact: bytes, expected_context: LocalD8ExpectedContext,
) -> LocalD8ConsumerResult:
    """Verify and interpret one local synthetic artifact; never assign priority."""
    if type(artifact) is not bytes or not artifact or len(artifact) > MAX_ARTIFACT_BYTES:
        return LocalD8ConsumerResult(REJECTED, reason_code="INVALID_ARTIFACT_INPUT")
    if not _valid_context(expected_context):
        return LocalD8ConsumerResult(REJECTED, reason_code="INVALID_EXPECTED_CONTEXT")
    try:
        verified = validate_local_d8_extension(artifact)
    except Exception:
        # Only the untrusted verifier boundary is contained; no exception text escapes.
        return LocalD8ConsumerResult(REJECTED, reason_code="ARTIFACT_VERIFICATION_FAILED")
    payload = _verified_payload(verified)
    if payload is None:
        return LocalD8ConsumerResult(REJECTED, reason_code="INVALID_VERIFIER_RESULT")
    if not _matches_context(payload, expected_context):
        return LocalD8ConsumerResult(REJECTED, reason_code="CONTEXT_MISMATCH")
    outcome = payload["outcome"]
    projection = LocalD8ConsumerProjection(
        schema_id=payload["schemaId"],
        schema_version=payload["schemaVersion"],
        designation=payload["designation"],
        assessment_identity=payload["assessmentIdentity"],
        assessment_version=payload["assessmentVersion"],
        producer_methodology_version=payload["producerMethodologyVersion"],
        snapshot_identity=payload["snapshotIdentity"],
        finding_id=payload["findingId"],
        recommendation_instance_identity=payload["recommendationInstanceIdentity"],
        recommendation_decision_identifier=payload["recommendationDecisionIdentifier"],
        recommendation_decision_table_version=payload["recommendationDecisionTableVersion"],
        confidence_classification=payload["confidenceClassification"],
        confidence_decision_identifier=payload["confidenceDecisionIdentifier"],
        confidence_decision_table_version=payload["confidenceDecisionTableVersion"],
        d8_methodology_version=payload["d8MethodologyVersion"],
        d8_rule_table_version=payload["d8RuleTableVersion"],
        outcome=outcome,
        validated_assertion_ids=tuple(payload["validatedAssertionIds"]),
        evidence_provenance=tuple(
            (entry["assertionId"], tuple(entry["evidenceReferences"]))
            for entry in payload["evidenceProvenance"]),
        priority=payload.get("priority"),
        winning_rule_ids=tuple(payload.get("winningRuleIds", ())),
        review_required=payload["reviewRequired"],
        governed_finding_type=payload.get("governedFindingType"),
        governed_consequence_basis=payload.get("governedConsequenceBasis"),
        excluded_rule_ids=tuple(payload.get("excludedRuleIds", ())),
        evaluated_driver_values=tuple(
            (entry["driverId"], entry["assertedValue"])
            for entry in payload.get("evaluatedDriverValues", ())),
        review_reference=payload.get("reviewReference"),
    )
    return LocalD8ConsumerResult(VERIFIED, outcome, projection)
