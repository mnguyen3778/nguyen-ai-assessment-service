from dataclasses import dataclass

from assessment.approved_methodology_runtime_config import (
    APPROVED_CONFIDENCE_LEVEL_ORDER,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    APPROVED_RISK_LEVEL_ORDER,
    APPROVED_SEVERITY_LEVEL_ORDER,
    CONFIDENCE_DECISION_TABLE_SET_VERSION,
    RISK_DECISION_TABLE_SET_VERSION,
    ApprovedMethodologyRuntimeConfig,
    DecisionRuleRuntimeConfig,
    validate_approved_methodology_runtime_config,
)
from assessment.approved_risk_runtime import (
    ApprovedRiskAssessmentResult,
)


CONFIDENCE_ASSIGNMENT_METHOD = "risk-context-confidence-decision-table-v1"

CONFIDENCE_DECISION_RULE_IDS = (
    "confidence-v1-insufficient-unassertable",
    "confidence-v1-low-basic-only",
    "confidence-v1-moderate-mixed-basic-adequate",
    "confidence-v1-high-strong-present",
    "confidence-v1-very-high-strong-only",
)

DEFAULT_CONFIDENCE_DECISION_RULE_ID = (
    "confidence-v1-moderate-mixed-basic-adequate"
)


@dataclass(frozen=True)
class ApprovedConfidenceAssessmentResult:
    confidence_classification: str
    risk_classification: str
    severity_classifications: tuple[str, ...]
    readiness_classification: str
    overall_assessment_score: float
    confidence_decision_identifier: str
    confidence_decision_table_version: str
    methodology_version: str
    runtime_config_version: str
    assignment_method: str


def determine_approved_confidence(
    risk: object,
    runtime_config: ApprovedMethodologyRuntimeConfig = (
        APPROVED_METHODOLOGY_RUNTIME_CONFIG
    ),
) -> ApprovedConfidenceAssessmentResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_runtime_config_version(runtime_config)
    _validate_confidence_decision_table_version(runtime_config)
    _validate_required_confidence_rules(runtime_config)
    _validate_risk(risk, runtime_config)

    confidence_rule = _resolve_confidence_rule(runtime_config)

    return ApprovedConfidenceAssessmentResult(
        confidence_classification=confidence_rule.output,
        risk_classification=risk.risk_classification,
        severity_classifications=risk.severity_classifications,
        readiness_classification=risk.readiness_classification,
        overall_assessment_score=risk.overall_assessment_score,
        confidence_decision_identifier=confidence_rule.id,
        confidence_decision_table_version=confidence_rule.table_version,
        methodology_version=risk.methodology_version,
        runtime_config_version=risk.runtime_config_version,
        assignment_method=CONFIDENCE_ASSIGNMENT_METHOD,
    )


def _validate_runtime_config_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.runtime_config_version
        != APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION
    ):
        raise ValueError("Unsupported approved methodology runtime config version.")


def _validate_confidence_decision_table_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.confidence_decision_table_set_version
        != CONFIDENCE_DECISION_TABLE_SET_VERSION
    ):
        raise ValueError("Unsupported confidence decision table set version.")


def _validate_required_confidence_rules(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    for rule_id in CONFIDENCE_DECISION_RULE_IDS:
        try:
            rule = runtime_config.confidence_decision_rules[rule_id]
        except KeyError as exc:
            raise ValueError(
                f"Missing approved confidence decision rule: {rule_id}"
            ) from exc
        _validate_confidence_rule(rule)


def _validate_confidence_rule(rule: DecisionRuleRuntimeConfig) -> None:
    if rule.table_version != CONFIDENCE_DECISION_TABLE_SET_VERSION:
        raise ValueError(
            f"Unsupported confidence decision table version: {rule.id}"
        )
    if rule.output not in APPROVED_CONFIDENCE_LEVEL_ORDER:
        raise ValueError(f"Unsupported confidence decision output: {rule.id}")


def _validate_risk(
    risk: object,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if not isinstance(risk, ApprovedRiskAssessmentResult):
        raise ValueError("Approved confidence requires ApprovedRiskAssessmentResult.")
    if risk.methodology_version != runtime_config.version_manifest.methodology_version:
        raise ValueError("Risk methodology version is unsupported.")
    if (
        risk.runtime_config_version
        != runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError("Risk runtime config version is unsupported.")
    if risk.risk_decision_table_version != RISK_DECISION_TABLE_SET_VERSION:
        raise ValueError("Risk decision table version is unsupported.")
    if risk.risk_classification not in APPROVED_RISK_LEVEL_ORDER:
        raise ValueError("Risk classification is unsupported.")
    if not risk.severity_classifications:
        raise ValueError("Risk severity classifications are required.")
    for severity_classification in risk.severity_classifications:
        if severity_classification not in APPROVED_SEVERITY_LEVEL_ORDER:
            raise ValueError("Risk severity classification is unsupported.")
    if not isinstance(risk.readiness_classification, str) or not (
        risk.readiness_classification.strip()
    ):
        raise ValueError("Risk readiness classification is required.")
    if not isinstance(risk.overall_assessment_score, (int, float)) or isinstance(
        risk.overall_assessment_score,
        bool,
    ):
        raise ValueError("Risk overall assessment score must be numeric.")
    if not 0 <= float(risk.overall_assessment_score) <= 100:
        raise ValueError("Risk overall assessment score must be between 0 and 100.")

    _validate_risk_decision_alignment(risk, runtime_config)


def _validate_risk_decision_alignment(
    risk: ApprovedRiskAssessmentResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    try:
        risk_rule = runtime_config.risk_decision_rules[
            risk.risk_decision_identifier
        ]
    except KeyError as exc:
        raise ValueError("Risk decision identifier is unsupported.") from exc

    if risk_rule.table_version != RISK_DECISION_TABLE_SET_VERSION:
        raise ValueError("Risk decision table version is unsupported.")
    if risk_rule.output != risk.risk_classification:
        raise ValueError("Risk classification does not match decision table.")


def _resolve_confidence_rule(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> DecisionRuleRuntimeConfig:
    return runtime_config.confidence_decision_rules[
        DEFAULT_CONFIDENCE_DECISION_RULE_ID
    ]
