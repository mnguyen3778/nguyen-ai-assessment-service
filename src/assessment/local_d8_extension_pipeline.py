"""Local synthetic D8 adapter-to-extension orchestration; no production caller."""

from dataclasses import dataclass

from assessment.d8_priority_extension import (
    CANONICALIZATION_ID, DESIGNATION, DIGEST_ALGORITHM, SCHEMA_ID,
    SCHEMA_VERSION, _BASE_FIELDS, _CONDITIONAL_FIELDS, _DIGEST,
    _INTEGRITY_FIELDS,
    build_local_d8_extension, validate_local_d8_extension,
)
from assessment.local_d8_priority import (
    BLOCKED_REQUIRED_EVIDENCE, INSUFFICIENT_CONFIDENCE, NO_FINDINGS_MONITOR,
    PRIORITY_ASSIGNED, PRIORITY_NOT_DETERMINED, REJECTED_INVALID_ASSERTION,
    LocalD8Result,
)
from assessment.local_d8_producer_adapter import (
    LocalD8ProducerRequest, evaluate_local_d8_producer,
)


VERIFIED_EXTENSION = "VERIFIED_EXTENSION"
ADAPTER_OUTCOME_INELIGIBLE = "ADAPTER_OUTCOME_INELIGIBLE"
INVALID_ADAPTER_RESULT = "INVALID_ADAPTER_RESULT"
EXTENSION_VALIDATION_FAILURE = "EXTENSION_VALIDATION_FAILURE"
INTEGRITY_VERIFICATION_FAILURE = "INTEGRITY_VERIFICATION_FAILURE"

_ELIGIBLE = frozenset((PRIORITY_ASSIGNED, PRIORITY_NOT_DETERMINED,
                       NO_FINDINGS_MONITOR))
_INELIGIBLE = frozenset((BLOCKED_REQUIRED_EVIDENCE, REJECTED_INVALID_ASSERTION,
                         INSUFFICIENT_CONFIDENCE))


@dataclass(frozen=True, slots=True)
class LocalD8ExtensionPipelineResult:
    """One local evaluation and, only after verification, its artifact bytes."""

    evaluation: LocalD8Result | None
    artifact: bytes | None
    status: str

    @property
    def is_verified(self) -> bool:
        return self.status == VERIFIED_EXTENSION and type(self.artifact) is bytes


def _matches_verified_artifact(
    verified: object, request: LocalD8ProducerRequest, evaluation: LocalD8Result,
) -> bool:
    """Check the verifier's parsed result against this exact local evaluation."""
    if type(verified) is not dict or tuple(verified) != ("payload", "integrity"):
        return False
    payload = verified["payload"]
    integrity = verified["integrity"]
    if (type(payload) is not dict
            or tuple(payload) != _BASE_FIELDS + _CONDITIONAL_FIELDS[evaluation.outcome]
            or type(integrity) is not dict
            or tuple(integrity) != _INTEGRITY_FIELDS
            or integrity["canonicalizationId"] != CANONICALIZATION_ID
            or integrity["digestAlgorithm"] != DIGEST_ALGORITHM
            or type(integrity["payloadDigest"]) is not str
            or _DIGEST.fullmatch(integrity["payloadDigest"]) is None
            or type(payload["schemaVersion"]) is not int
            or type(payload["reviewRequired"]) is not bool):
        return False
    try:
        binding = request.binding
        canonical = request.canonical_input
        confidence = request.governed_result.confidence
        expected = (
            ("schemaId", SCHEMA_ID), ("schemaVersion", SCHEMA_VERSION),
            ("designation", DESIGNATION),
            ("assessmentIdentity", binding.assessment_identity),
            ("assessmentIdentity", evaluation.assessment_identity),
            ("assessmentVersion", canonical.assessment_version),
            ("producerMethodologyVersion", canonical.methodology_version),
            ("snapshotIdentity", binding.snapshot_identity),
            ("snapshotIdentity", evaluation.snapshot_identity),
            ("findingId", binding.finding_id),
            ("findingId", evaluation.finding_id),
            ("recommendationInstanceIdentity", binding.recommendation_instance_identity),
            ("recommendationInstanceIdentity", evaluation.recommendation_instance_identity),
            ("recommendationDecisionIdentifier", binding.recommendation_decision_identifier),
            ("recommendationDecisionTableVersion", binding.recommendation_decision_table_version),
            ("confidenceClassification", confidence.confidence_classification),
            ("confidenceDecisionIdentifier", confidence.confidence_decision_identifier),
            ("confidenceDecisionTableVersion", confidence.confidence_decision_table_version),
            ("d8MethodologyVersion", evaluation.methodology_version),
            ("d8RuleTableVersion", evaluation.rule_table_version),
            ("outcome", evaluation.outcome),
            ("validatedAssertionIds", list(evaluation.validated_assertion_ids)),
        )
        if any(payload[key] != value for key, value in expected):
            return False
        records = sorted(
            (record for record in request.synthetic_assertions
             if record["recommendationInstanceIdentity"] ==
                evaluation.recommendation_instance_identity),
            key=lambda record: record["assertionId"],
        )
        provenance = [
            {"assertionId": record["assertionId"],
             "evidenceReferences": list(record["evidenceReferences"])}
            for record in records
        ]
        if payload["evidenceProvenance"] != provenance:
            return False
        if evaluation.outcome == PRIORITY_ASSIGNED:
            return (payload["confidenceGate"] == "PASSED"
                    and payload["reviewRequired"] is False
                    and payload["priority"] == evaluation.priority
                    and payload["winningRuleIds"] == list(evaluation.matched_rule_ids))
        if evaluation.outcome == PRIORITY_NOT_DETERMINED:
            return (payload["confidenceGate"] == "PASSED"
                    and payload["reviewRequired"] is True
                    and payload["governedFindingType"] == evaluation.governed_finding_type
                    and payload["governedConsequenceBasis"] ==
                        evaluation.governed_consequence_basis
                    and payload["excludedRuleIds"] == list(evaluation.excluded_rule_ids)
                    and payload["evaluatedDriverValues"] == [
                        {"driverId": driver, "assertedValue": value}
                        for driver, value in evaluation.evaluated_driver_values]
                    and payload["reviewReference"] == evaluation.review_reference)
        return (payload["confidenceGate"] == "NOT_APPLICABLE_NO_FINDINGS"
                and payload["reviewRequired"] is False
                and payload["findingId"] is None
                and binding.finding_id is None
                and not request.canonical_input.findings
                and not request.synthetic_assertions
                and evaluation.priority is None)
    except (AttributeError, KeyError, TypeError, ValueError):
        return False


def run_local_d8_extension_pipeline(
    request: LocalD8ProducerRequest,
) -> LocalD8ExtensionPipelineResult:
    """Call the adapter once, build once if eligible, then verify once locally."""
    evaluation = evaluate_local_d8_producer(request)
    if type(evaluation) is not LocalD8Result:
        return LocalD8ExtensionPipelineResult(None, None, INVALID_ADAPTER_RESULT)
    if type(evaluation.outcome) is not str:
        return LocalD8ExtensionPipelineResult(evaluation, None, INVALID_ADAPTER_RESULT)
    if evaluation.outcome not in _ELIGIBLE:
        status = (ADAPTER_OUTCOME_INELIGIBLE if evaluation.outcome in _INELIGIBLE
                  else INVALID_ADAPTER_RESULT)
        return LocalD8ExtensionPipelineResult(evaluation, None, status)
    try:
        artifact = build_local_d8_extension(request, evaluation)
    except ValueError:
        return LocalD8ExtensionPipelineResult(
            evaluation, None, EXTENSION_VALIDATION_FAILURE)
    if type(artifact) is not bytes:
        return LocalD8ExtensionPipelineResult(
            evaluation, None, EXTENSION_VALIDATION_FAILURE)
    try:
        verified = validate_local_d8_extension(artifact)
    except ValueError:
        return LocalD8ExtensionPipelineResult(
            evaluation, None, INTEGRITY_VERIFICATION_FAILURE)
    if not _matches_verified_artifact(verified, request, evaluation):
        return LocalD8ExtensionPipelineResult(
            evaluation, None, INTEGRITY_VERIFICATION_FAILURE)
    return LocalD8ExtensionPipelineResult(evaluation, artifact, VERIFIED_EXTENSION)
