"""Approved v1 decision tables applied to governed v2 evidence and findings."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from assessment.approved_confidence_runtime import ApprovedConfidenceAssessmentResult
from assessment.approved_executive_summary_runtime import (
    SECTION_TEMPLATE_TEXT,
    SIGNIFICANT_FINDINGS_EMPTY_TEMPLATE_TEXT,
    _format_score,
)
from assessment.approved_methodology_runtime_config import (
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    ApprovedMethodologyRuntimeConfig,
    validate_approved_methodology_runtime_config,
)
from assessment.approved_readiness_runtime import ApprovedReadinessAssessmentResult
from assessment.approved_risk_runtime import (
    ApprovedRiskAssessmentResult,
    RISK_ASSIGNMENT_METHOD,
    _resolve_risk_rule,
)
from assessment.approved_severity_runtime import (
    ApprovedSeverityAssessmentResult,
    _validate_readiness,
)
from assessment.governed_assessment_input import (
    EvidenceProfileInput,
    FindingInput,
    FINDING_CONSEQUENCE_RULES,
)


@dataclass(frozen=True)
class GovernedRecommendationResult:
    finding_id: str | None
    recommendation_classification: str
    recommendation_decision_identifier: str
    recommendation_decision_table_version: str


@dataclass(frozen=True)
class GovernedSeverityAssignedFinding:
    finding: FindingInput
    sequence_identifier: int
    linked_readiness: str
    evidence_qualities: tuple[str, ...]
    methodology_version: str
    severity_assignment: ApprovedSeverityAssessmentResult


@dataclass(frozen=True)
class GovernedExecutiveSummaryInputs:
    finding_count: int
    severity_classifications: tuple[str, ...]
    risk_classification: str
    confidence_classification: str
    recommendation_classifications: tuple[str, ...]
    section_text: Mapping[str, str]


RECOMMENDATION_RULE_BY_FINDING = MappingProxyType({
    ("Deficiency", "critical"): "recommendation-v1-deficiency-critical-immediate",
    ("Deficiency", "high"): "recommendation-v1-deficiency-high-priority",
    ("Deficiency", "medium"): "recommendation-v1-deficiency-medium-planned",
    ("Deficiency", "low"): "recommendation-v1-deficiency-low-planned",
    ("Observation", "informational"): "recommendation-v1-observation-monitor",
    ("Strength", "informational"): "recommendation-v1-strength-best-practice",
    ("Opportunity", "informational"): "recommendation-v1-opportunity-best-practice",
})


def assign_governed_severity(
    finding: FindingInput,
    readiness: ApprovedReadinessAssessmentResult,
    evidence: EvidenceProfileInput,
    runtime_config: ApprovedMethodologyRuntimeConfig = APPROVED_METHODOLOGY_RUNTIME_CONFIG,
) -> ApprovedSeverityAssessmentResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_readiness(readiness, runtime_config)
    _validate_evidence(evidence)
    if not isinstance(finding, FindingInput):
        raise ValueError("Governed Finding is required for severity.")
    finding = FindingInput(
        finding.finding_id,
        finding.title,
        finding.primary_dimension,
        finding.related_dimensions,
        finding.trigger_source,
        finding.finding_type,
        finding.business_consequence_basis,
        finding.source_references,
    )
    if not set(finding.source_references) <= {
        item.source_reference for item in evidence.items
    }:
        raise ValueError("Finding must reference evaluated evidence.")
    rule_id = FINDING_CONSEQUENCE_RULES[
        (finding.finding_type, finding.business_consequence_basis)
    ]
    rule = runtime_config.severity_decision_rules[rule_id]
    if rule.table_version != runtime_config.version_manifest.severity_decision_table_set_version:
        raise ValueError("Severity rule version mismatch.")
    return ApprovedSeverityAssessmentResult(
        severity_classification=rule.output,
        readiness_classification=readiness.readiness_classification,
        readiness_score=readiness.readiness_score,
        severity_decision_identifier=rule.id,
        decision_table_version=rule.table_version,
        methodology_version=readiness.methodology_version,
        runtime_config_version=readiness.runtime_config_version,
        assignment_method="finding-consequence-severity-decision-table-v1",
    )


def assess_governed_risk(
    severity_assigned_findings: tuple[GovernedSeverityAssignedFinding, ...],
    readiness: ApprovedReadinessAssessmentResult,
    evidence: EvidenceProfileInput,
    runtime_config: ApprovedMethodologyRuntimeConfig = APPROVED_METHODOLOGY_RUNTIME_CONFIG,
) -> ApprovedRiskAssessmentResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_readiness(readiness, runtime_config)
    _validate_evidence(evidence)
    if not isinstance(severity_assigned_findings, tuple):
        raise ValueError("Complete severity-assigned finding tuple is required.")
    observed_ids: set[str] = set()
    evidence_by_reference = {
        item.source_reference: item.quality for item in evidence.items
    }
    for sequence, assigned in enumerate(severity_assigned_findings, start=1):
        if not isinstance(assigned, GovernedSeverityAssignedFinding):
            raise ValueError("Unsupported severity-assigned finding.")
        if assigned.finding.finding_id in observed_ids:
            raise ValueError("Duplicate severity-assigned finding ID.")
        observed_ids.add(assigned.finding.finding_id)
        if assigned.sequence_identifier != sequence or (
            assigned.linked_readiness != readiness.readiness_classification or
            assigned.methodology_version != readiness.methodology_version
        ):
            raise ValueError("Severity-assigned finding context mismatch.")
        try:
            expected_qualities = tuple(
                evidence_by_reference[reference]
                for reference in assigned.finding.source_references
            )
        except KeyError as exc:
            raise ValueError("Finding evidence reference is unsupported.") from exc
        if assigned.evidence_qualities != expected_qualities:
            raise ValueError("Finding evidence qualities do not match evaluated evidence.")
    severity_assignments = tuple(
        assigned.severity_assignment for assigned in severity_assigned_findings
    )
    for severity in severity_assignments:
        if not isinstance(severity, ApprovedSeverityAssessmentResult):
            raise ValueError("Unsupported severity assignment.")
        if (severity.readiness_classification != readiness.readiness_classification or
                severity.readiness_score != readiness.readiness_score or
                severity.methodology_version != readiness.methodology_version or
                severity.runtime_config_version != readiness.runtime_config_version):
            raise ValueError("Severity assignment context mismatch.")
        rule = runtime_config.severity_decision_rules.get(
            severity.severity_decision_identifier
        )
        if rule is None or rule.output != severity.severity_classification or rule.table_version != severity.decision_table_version:
            raise ValueError("Unsupported severity decision assignment.")
    rule = _resolve_risk_rule(severity_assignments, runtime_config)
    if rule.table_version != runtime_config.version_manifest.risk_decision_table_set_version:
        raise ValueError("Risk rule version mismatch.")
    return ApprovedRiskAssessmentResult(
        risk_classification=rule.output,
        severity_classifications=tuple(
            severity.severity_classification for severity in severity_assignments
        ),
        readiness_classification=readiness.readiness_classification,
        overall_assessment_score=readiness.readiness_score,
        risk_decision_identifier=rule.id,
        risk_decision_table_version=rule.table_version,
        methodology_version=readiness.methodology_version,
        runtime_config_version=readiness.runtime_config_version,
        assignment_method=RISK_ASSIGNMENT_METHOD,
    )


def assess_governed_confidence(
    risk: ApprovedRiskAssessmentResult,
    evidence: EvidenceProfileInput,
    runtime_config: ApprovedMethodologyRuntimeConfig = APPROVED_METHODOLOGY_RUNTIME_CONFIG,
) -> ApprovedConfidenceAssessmentResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_evidence(evidence)
    if not isinstance(risk, ApprovedRiskAssessmentResult):
        raise ValueError("Approved risk context is required for confidence.")
    risk_rule = runtime_config.risk_decision_rules.get(risk.risk_decision_identifier)
    if (risk_rule is None or risk_rule.output != risk.risk_classification or
            risk_rule.table_version != risk.risk_decision_table_version or
            risk.methodology_version != runtime_config.version_manifest.methodology_version or
            risk.runtime_config_version != runtime_config.version_manifest.runtime_config_version):
        raise ValueError("Invalid risk context for confidence.")
    if any(item.assertability_limitation is not None for item in evidence.items):
        rule_id = "confidence-v1-insufficient-unassertable"
    else:
        qualities = {item.quality for item in evidence.items}
        if qualities == {"Basic"}:
            rule_id = "confidence-v1-low-basic-only"
        elif "Strong" not in qualities and "Adequate" in qualities:
            rule_id = "confidence-v1-moderate-mixed-basic-adequate"
        elif qualities == {"Strong"}:
            rule_id = "confidence-v1-very-high-strong-only"
        elif "Strong" in qualities and len(qualities) > 1:
            rule_id = "confidence-v1-high-strong-present"
        else:
            raise ValueError("Evidence qualities match no approved confidence rule.")
    rule = runtime_config.confidence_decision_rules[rule_id]
    if rule.table_version != runtime_config.version_manifest.confidence_decision_table_set_version:
        raise ValueError("Confidence rule version mismatch.")
    return ApprovedConfidenceAssessmentResult(
        confidence_classification=rule.output,
        risk_classification=risk.risk_classification,
        severity_classifications=risk.severity_classifications,
        readiness_classification=risk.readiness_classification,
        overall_assessment_score=risk.overall_assessment_score,
        confidence_decision_identifier=rule.id,
        confidence_decision_table_version=rule.table_version,
        methodology_version=risk.methodology_version,
        runtime_config_version=risk.runtime_config_version,
        assignment_method="evidence-quality-confidence-decision-table-v1",
    )


def recommend_governed_actions(
    findings: tuple[FindingInput, ...],
    severity_assignments: tuple[ApprovedSeverityAssessmentResult, ...],
    risk: ApprovedRiskAssessmentResult,
    confidence: ApprovedConfidenceAssessmentResult,
    runtime_config: ApprovedMethodologyRuntimeConfig = APPROVED_METHODOLOGY_RUNTIME_CONFIG,
) -> tuple[GovernedRecommendationResult, ...]:
    validate_approved_methodology_runtime_config(runtime_config)
    if len(findings) != len(severity_assignments):
        raise ValueError("Complete finding severity collection is required.")
    if (confidence.risk_classification != risk.risk_classification or
            confidence.severity_classifications != risk.severity_classifications or
            confidence.methodology_version != risk.methodology_version):
        raise ValueError("Confidence and risk context mismatch.")
    pairs = tuple(zip(findings, severity_assignments))
    if not pairs:
        rule_ids = ((None, "recommendation-v1-no-findings-monitor"),)
    else:
        try:
            rule_ids = tuple((finding.finding_id, RECOMMENDATION_RULE_BY_FINDING[
                (finding.finding_type, severity.severity_classification)
            ]) for finding, severity in pairs)
        except KeyError as exc:
            raise ValueError("Finding and severity match no recommendation rule.") from exc
    results = []
    for finding_id, rule_id in rule_ids:
        rule = runtime_config.recommendation_decision_rules[rule_id]
        if rule.table_version != runtime_config.version_manifest.recommendation_decision_table_set_version:
            raise ValueError("Recommendation rule version mismatch.")
        results.append(GovernedRecommendationResult(
            finding_id=finding_id,
            recommendation_classification=rule.output,
            recommendation_decision_identifier=rule.id,
            recommendation_decision_table_version=rule.table_version,
        ))
    return tuple(results)


def summarize_governed_decisions(
    findings: tuple[FindingInput, ...],
    severity_assignments: tuple[ApprovedSeverityAssessmentResult, ...],
    risk: ApprovedRiskAssessmentResult,
    confidence: ApprovedConfidenceAssessmentResult,
    recommendations: tuple[GovernedRecommendationResult, ...],
    runtime_config: ApprovedMethodologyRuntimeConfig = APPROVED_METHODOLOGY_RUNTIME_CONFIG,
) -> GovernedExecutiveSummaryInputs:
    validate_approved_methodology_runtime_config(runtime_config)
    if len(findings) != len(severity_assignments) or len(recommendations) != max(1, len(findings)):
        raise ValueError("Incomplete governed summary inputs.")
    severities = tuple(item.severity_classification for item in severity_assignments)
    labels = tuple(item.recommendation_classification for item in recommendations)
    score = _format_score(risk.overall_assessment_score)
    versions = (
        f"methodology_version={risk.methodology_version}; "
        f"runtime_config_version={risk.runtime_config_version}; "
        "recommendation_decision_table_version="
        f"{runtime_config.version_manifest.recommendation_decision_table_set_version}; "
        "executive_summary_template_version="
        f"{runtime_config.version_manifest.executive_summary_template_set_version}"
    )
    placeholders = {
        "overall_assessment_result": score,
        "readiness": risk.readiness_classification,
        "methodology_version": risk.methodology_version,
        "dimension_results": (
            f"readiness={risk.readiness_classification}; overall_assessment_score={score}"
        ),
        "finding_count": str(len(findings)),
        "significant_findings": ", ".join(severities),
        "risk_assessment": risk.risk_classification,
        "confidence_assessment": confidence.confidence_classification,
        "recommendation_count": str(len(recommendations)),
        "recommendations": ", ".join(labels),
        "artifact_versions": versions,
    }
    sections = {}
    for section_id in runtime_config.executive_summary_sections:
        template = (SIGNIFICANT_FINDINGS_EMPTY_TEMPLATE_TEXT
                    if section_id == "significant-findings" and not findings
                    else SECTION_TEMPLATE_TEXT[section_id])
        sections[section_id] = template.format(**placeholders)
    return GovernedExecutiveSummaryInputs(
        finding_count=len(findings),
        severity_classifications=severities,
        risk_classification=risk.risk_classification,
        confidence_classification=confidence.confidence_classification,
        recommendation_classifications=labels,
        section_text=MappingProxyType(sections),
    )


def _validate_evidence(evidence: EvidenceProfileInput) -> None:
    if not isinstance(evidence, EvidenceProfileInput):
        raise ValueError("Governed evidence profile is required.")
    # Recheck after construction: frozen dataclasses can still be fabricated with
    # object.__new__, and stage boundaries must fail closed on malformed inputs.
    EvidenceProfileInput(evidence.required_evidence_present, evidence.items)
