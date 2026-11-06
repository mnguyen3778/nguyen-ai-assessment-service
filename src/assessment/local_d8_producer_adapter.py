"""Local synthetic governed-result binding for D8; no production caller."""

from dataclasses import dataclass, fields, replace

from assessment.approved_confidence_runtime import ApprovedConfidenceAssessmentResult
from assessment.approved_methodology_runtime_config import SEVERITY_DECISION_TABLE_SET_VERSION
from assessment.approved_risk_runtime import ApprovedRiskAssessmentResult
from assessment.approved_severity_runtime import ApprovedSeverityAssessmentResult
from assessment.decision_engine import GovernedAssessmentResult
from assessment.governed_assessment_input import (
    FindingInput, ValidatedCanonicalExecutiveAssessmentInputV2,
)
from assessment.governed_decision_runtime import (
    GovernedRecommendationResult, GovernedSeverityAssignedFinding,
)
from assessment.local_d8_priority import (
    METHODOLOGY_VERSION, RULE_TABLE_VERSION, REJECTED_INVALID_ASSERTION,
    LocalD8Input, LocalD8Result, evaluate_local_d8_priority,
)
from assessment.local_priority_assertions import RecommendationInstance, SyntheticContext


@dataclass(frozen=True, slots=True)
class LocalSyntheticProducerBinding:
    assessment_identity: str
    snapshot_identity: str
    finding_id: str | None
    recommendation_instance_identity: str
    recommendation_decision_identifier: str
    recommendation_decision_table_version: str


@dataclass(frozen=True, slots=True)
class LocalD8ProducerRequest:
    canonical_input: ValidatedCanonicalExecutiveAssessmentInputV2
    governed_result: GovernedAssessmentResult
    synthetic_context: SyntheticContext
    synthetic_assertions: object
    binding: LocalSyntheticProducerBinding


def _complete(value: object, kind: type) -> bool:
    return isinstance(value, kind) and all(hasattr(value, field.name)
                                            for field in fields(kind))


def _rejected(request: object, reason: str) -> LocalD8Result:
    binding = request.binding if isinstance(request, LocalD8ProducerRequest) else None
    context = request.synthetic_context if isinstance(request, LocalD8ProducerRequest) else None
    if not _complete(binding, LocalSyntheticProducerBinding):
        binding = None
    if not _complete(context, SyntheticContext):
        context = None
    return LocalD8Result(
        outcome=REJECTED_INVALID_ASSERTION, priority=None, matched_rule_ids=(),
        excluded_rule_ids=(), pending_rule_ids=(),
        recommendation_instance_identity=(binding.recommendation_instance_identity
                                          if binding else ""),
        snapshot_identity=(context.snapshot_identity if context else ""),
        assessment_identity=(context.assessment_identity if context else ""),
        finding_id=(binding.finding_id if binding else None), reason=reason,
        validated_assertion_ids=(),
        methodology_version=METHODOLOGY_VERSION, rule_table_version=RULE_TABLE_VERSION,
    )


def evaluate_local_d8_producer(request: LocalD8ProducerRequest) -> LocalD8Result:
    """Bind one synthetic producer recommendation and delegate all D8 decisions."""
    if not isinstance(request, LocalD8ProducerRequest):
        return _rejected(request, "invalid-local-producer-request")
    canonical = request.canonical_input
    producer = request.governed_result
    context = request.synthetic_context
    binding = request.binding
    if (not isinstance(canonical, ValidatedCanonicalExecutiveAssessmentInputV2)
            or not isinstance(producer, GovernedAssessmentResult)
            or not isinstance(context, SyntheticContext)
            or not isinstance(binding, LocalSyntheticProducerBinding)):
        return _rejected(request, "invalid-local-producer-types")
    if (not _complete(canonical, ValidatedCanonicalExecutiveAssessmentInputV2)
            or not _complete(producer, GovernedAssessmentResult)
            or not _complete(context, SyntheticContext)
            or not _complete(binding, LocalSyntheticProducerBinding)
            or not isinstance(canonical.findings, tuple)
            or any(not _complete(item, FindingInput) for item in canonical.findings)
            or not isinstance(producer.findings, tuple)
            or any(not _complete(item, FindingInput) for item in producer.findings)):
        return _rejected(request, "incomplete-local-producer-structure")
    if (not isinstance(binding.assessment_identity, str)
            or not binding.assessment_identity
            or binding.assessment_identity != context.assessment_identity
            or not isinstance(binding.snapshot_identity, str)
            or not binding.snapshot_identity
            or binding.snapshot_identity != context.snapshot_identity):
        return _rejected(request, "invalid-synthetic-assessment-snapshot-binding")
    if (not isinstance(binding.recommendation_instance_identity, str)
            or not binding.recommendation_instance_identity
            or not isinstance(binding.recommendation_decision_identifier, str)
            or not binding.recommendation_decision_identifier
            or not isinstance(binding.recommendation_decision_table_version, str)
            or not binding.recommendation_decision_table_version):
        return _rejected(request, "invalid-synthetic-decision-binding")
    if (not isinstance(producer.findings, tuple)
            or producer.findings != canonical.findings
            or not isinstance(producer.recommendations, tuple)
            or not isinstance(producer.severity_assignments, tuple)
            or not isinstance(producer.severity_assigned_findings, tuple)
            or not _complete(producer.risk, ApprovedRiskAssessmentResult)
            or not _complete(producer.confidence, ApprovedConfidenceAssessmentResult)
            or len(producer.severity_assignments) != len(canonical.findings)
            or len(producer.severity_assigned_findings) != len(canonical.findings)
            or len(producer.recommendations) != max(1, len(canonical.findings))
            or any(not _complete(item, GovernedSeverityAssignedFinding)
                   for item in producer.severity_assigned_findings)
            or any(not _complete(item, ApprovedSeverityAssessmentResult)
                   for item in producer.severity_assignments)
            or any(not _complete(item, GovernedRecommendationResult)
                   for item in producer.recommendations)
            or tuple(item.finding for item in producer.severity_assigned_findings)
               != canonical.findings
            or tuple(item.severity_assignment for item in producer.severity_assigned_findings)
               != producer.severity_assignments
            or producer.risk.methodology_version != canonical.methodology_version
            or producer.confidence.methodology_version != canonical.methodology_version
            or producer.risk.severity_classifications != tuple(
                item.severity_classification for item in producer.severity_assignments)
            or producer.confidence.risk_classification != producer.risk.risk_classification
            or producer.confidence.severity_classifications
               != producer.risk.severity_classifications
            or any(item.methodology_version != canonical.methodology_version
                   or item.decision_table_version != SEVERITY_DECISION_TABLE_SET_VERSION
                   for item in producer.severity_assignments)):
        return _rejected(request, "invalid-governed-producer-alignment")
    if (not isinstance(context.recommendations, tuple)
            or len(context.recommendations) != len(producer.recommendations)
            or any(not isinstance(item, RecommendationInstance)
                   for item in context.recommendations)):
        return _rejected(request, "invalid-synthetic-instance-collection")

    # Finding ID is an occurrence link here, never a business priority signal.
    findings_by_id = {finding.finding_id: finding for finding in canonical.findings}
    recommendations_by_id = {item.finding_id: item for item in producer.recommendations}
    instances_by_id = {item.finding_id: item for item in context.recommendations}
    expected_ids = set(findings_by_id) if findings_by_id else {None}
    if (len(findings_by_id) != len(canonical.findings)
            or len(recommendations_by_id) != len(producer.recommendations)
            or len(instances_by_id) != len(context.recommendations)
            or set(recommendations_by_id) != expected_ids
            or set(instances_by_id) != expected_ids
            or any(not isinstance(item.instance_identity, str)
                   or not item.instance_identity for item in context.recommendations)
            or len({item.instance_identity for item in context.recommendations})
               != len(context.recommendations)):
        return _rejected(request, "ambiguous-synthetic-recommendation-binding")
    for finding_id, recommendation in recommendations_by_id.items():
        instance = instances_by_id[finding_id]
        if (instance.decision_identifier != recommendation.recommendation_decision_identifier
                or instance.decision_table_version
                   != recommendation.recommendation_decision_table_version):
            return _rejected(request, "invalid-synthetic-decision-link")
    if ((binding.finding_id is not None
         and (not isinstance(binding.finding_id, str) or not binding.finding_id))
            or binding.finding_id not in expected_ids):
        return _rejected(request, "invalid-synthetic-finding-binding")
    selected = instances_by_id[binding.finding_id]
    recommendation = recommendations_by_id[binding.finding_id]
    if (binding.recommendation_instance_identity != selected.instance_identity
            or binding.recommendation_decision_identifier
               != recommendation.recommendation_decision_identifier
            or binding.recommendation_decision_table_version
               != recommendation.recommendation_decision_table_version):
        return _rejected(request, "invalid-selected-recommendation-binding")

    # The evaluator expects aligned tuples; align only after explicit ID checks.
    ordered_instances = tuple(instances_by_id[item.finding_id]
                              for item in producer.recommendations)
    local_input = LocalD8Input(
        findings=canonical.findings,
        recommendations=producer.recommendations,
        recommendation_instance_identity=selected.instance_identity,
        context=replace(context, recommendations=ordered_instances),
        records=request.synthetic_assertions,
        severity_classifications=tuple(item.severity_classification
                                       for item in producer.severity_assignments),
        risk_classification=producer.risk.risk_classification,
        confidence_classification=producer.confidence.confidence_classification,
        severity_decision_identifiers=tuple(item.severity_decision_identifier
                                            for item in producer.severity_assignments),
        severity_decision_table_version=SEVERITY_DECISION_TABLE_SET_VERSION,
        risk_decision_identifier=producer.risk.risk_decision_identifier,
        risk_decision_table_version=producer.risk.risk_decision_table_version,
        confidence_decision_identifier=producer.confidence.confidence_decision_identifier,
        confidence_decision_table_version=producer.confidence.confidence_decision_table_version,
    )
    return evaluate_local_d8_priority(local_input)
