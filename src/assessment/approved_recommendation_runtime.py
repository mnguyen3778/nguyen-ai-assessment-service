from dataclasses import dataclass

from assessment.approved_confidence_runtime import (
    ApprovedConfidenceAssessmentResult,
)
from assessment.approved_methodology_runtime_config import (
    APPROVED_CONFIDENCE_LEVEL_ORDER,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    APPROVED_RECOMMENDATION_LABEL_ORDER,
    APPROVED_RISK_LEVEL_ORDER,
    APPROVED_SEVERITY_LEVEL_ORDER,
    CONFIDENCE_DECISION_TABLE_SET_VERSION,
    RECOMMENDATION_DECISION_TABLE_SET_VERSION,
    ApprovedMethodologyRuntimeConfig,
    DecisionRuleRuntimeConfig,
    validate_approved_methodology_runtime_config,
)


RECOMMENDATION_ASSIGNMENT_METHOD = (
    "confidence-context-recommendation-decision-table-v1"
)

RECOMMENDATION_DECISION_RULE_IDS = (
    "recommendation-v1-deficiency-critical-immediate",
    "recommendation-v1-deficiency-high-priority",
    "recommendation-v1-deficiency-medium-planned",
    "recommendation-v1-deficiency-low-planned",
    "recommendation-v1-observation-monitor",
    "recommendation-v1-strength-best-practice",
    "recommendation-v1-opportunity-best-practice",
    "recommendation-v1-no-findings-monitor",
)

SEVERITY_RECOMMENDATION_DECISION_RULE_IDS = {
    "critical": "recommendation-v1-deficiency-critical-immediate",
    "high": "recommendation-v1-deficiency-high-priority",
    "medium": "recommendation-v1-deficiency-medium-planned",
    "low": "recommendation-v1-deficiency-low-planned",
    "informational": "recommendation-v1-observation-monitor",
}


@dataclass(frozen=True)
class ApprovedRecommendationAssessmentResult:
    recommendation_classification: str
    confidence_classification: str
    risk_classification: str
    severity_classification: str
    readiness_classification: str
    overall_assessment_score: float
    recommendation_decision_identifier: str
    recommendation_decision_table_version: str
    methodology_version: str
    runtime_config_version: str
    assignment_method: str


def determine_approved_recommendation(
    confidence: object,
    runtime_config: ApprovedMethodologyRuntimeConfig = (
        APPROVED_METHODOLOGY_RUNTIME_CONFIG
    ),
) -> ApprovedRecommendationAssessmentResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_runtime_config_version(runtime_config)
    _validate_recommendation_decision_table_version(runtime_config)
    _validate_required_recommendation_rules(runtime_config)
    _validate_confidence(confidence, runtime_config)

    recommendation_rule = _resolve_recommendation_rule(confidence, runtime_config)

    return ApprovedRecommendationAssessmentResult(
        recommendation_classification=recommendation_rule.output,
        confidence_classification=confidence.confidence_classification,
        risk_classification=confidence.risk_classification,
        severity_classification=confidence.severity_classifications[0],
        readiness_classification=confidence.readiness_classification,
        overall_assessment_score=confidence.overall_assessment_score,
        recommendation_decision_identifier=recommendation_rule.id,
        recommendation_decision_table_version=recommendation_rule.table_version,
        methodology_version=confidence.methodology_version,
        runtime_config_version=confidence.runtime_config_version,
        assignment_method=RECOMMENDATION_ASSIGNMENT_METHOD,
    )


def _validate_runtime_config_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.runtime_config_version
        != APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION
    ):
        raise ValueError("Unsupported approved methodology runtime config version.")


def _validate_recommendation_decision_table_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.recommendation_decision_table_set_version
        != RECOMMENDATION_DECISION_TABLE_SET_VERSION
    ):
        raise ValueError("Unsupported recommendation decision table set version.")


def _validate_required_recommendation_rules(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    for rule_id in RECOMMENDATION_DECISION_RULE_IDS:
        try:
            rule = runtime_config.recommendation_decision_rules[rule_id]
        except KeyError as exc:
            raise ValueError(
                f"Missing approved recommendation decision rule: {rule_id}"
            ) from exc
        _validate_recommendation_rule(rule)


def _validate_recommendation_rule(rule: DecisionRuleRuntimeConfig) -> None:
    if rule.table_version != RECOMMENDATION_DECISION_TABLE_SET_VERSION:
        raise ValueError(
            f"Unsupported recommendation decision table version: {rule.id}"
        )
    if rule.output not in APPROVED_RECOMMENDATION_LABEL_ORDER:
        raise ValueError(f"Unsupported recommendation decision output: {rule.id}")


def _validate_confidence(
    confidence: object,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if not isinstance(confidence, ApprovedConfidenceAssessmentResult):
        raise ValueError(
            "Approved recommendation requires ApprovedConfidenceAssessmentResult."
        )
    if (
        confidence.methodology_version
        != runtime_config.version_manifest.methodology_version
    ):
        raise ValueError("Confidence methodology version is unsupported.")
    if (
        confidence.runtime_config_version
        != runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError("Confidence runtime config version is unsupported.")
    if (
        confidence.confidence_decision_table_version
        != CONFIDENCE_DECISION_TABLE_SET_VERSION
    ):
        raise ValueError("Confidence decision table version is unsupported.")
    if confidence.confidence_classification not in APPROVED_CONFIDENCE_LEVEL_ORDER:
        raise ValueError("Confidence classification is unsupported.")
    if confidence.risk_classification not in APPROVED_RISK_LEVEL_ORDER:
        raise ValueError("Confidence risk classification is unsupported.")
    if len(confidence.severity_classifications) != 1:
        raise ValueError(
            "Confidence severity classification must resolve to exactly one value."
        )
    if confidence.severity_classifications[0] not in APPROVED_SEVERITY_LEVEL_ORDER:
        raise ValueError("Confidence severity classification is unsupported.")
    if not isinstance(confidence.readiness_classification, str) or not (
        confidence.readiness_classification.strip()
    ):
        raise ValueError("Confidence readiness classification is required.")
    if not isinstance(
        confidence.overall_assessment_score,
        (int, float),
    ) or isinstance(confidence.overall_assessment_score, bool):
        raise ValueError("Confidence overall assessment score must be numeric.")
    if not 0 <= float(confidence.overall_assessment_score) <= 100:
        raise ValueError(
            "Confidence overall assessment score must be between 0 and 100."
        )

    _validate_confidence_decision_alignment(confidence, runtime_config)


def _validate_confidence_decision_alignment(
    confidence: ApprovedConfidenceAssessmentResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    try:
        confidence_rule = runtime_config.confidence_decision_rules[
            confidence.confidence_decision_identifier
        ]
    except KeyError as exc:
        raise ValueError("Confidence decision identifier is unsupported.") from exc

    if confidence_rule.table_version != CONFIDENCE_DECISION_TABLE_SET_VERSION:
        raise ValueError("Confidence decision table version is unsupported.")
    if confidence_rule.output != confidence.confidence_classification:
        raise ValueError(
            "Confidence classification does not match decision table."
        )


def _resolve_recommendation_rule(
    confidence: ApprovedConfidenceAssessmentResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> DecisionRuleRuntimeConfig:
    severity_classification = confidence.severity_classifications[0]
    try:
        rule_id = SEVERITY_RECOMMENDATION_DECISION_RULE_IDS[
            severity_classification
        ]
    except KeyError as exc:
        raise ValueError(
            "Unsupported severity classification for recommendation: "
            f"{severity_classification}"
        ) from exc

    return runtime_config.recommendation_decision_rules[rule_id]
