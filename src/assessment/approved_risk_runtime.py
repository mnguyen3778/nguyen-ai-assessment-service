from dataclasses import dataclass
from typing import Iterable

from assessment.approved_methodology_runtime_config import (
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    APPROVED_RISK_LEVEL_ORDER,
    APPROVED_SEVERITY_LEVEL_ORDER,
    RISK_DECISION_TABLE_SET_VERSION,
    SEVERITY_DECISION_TABLE_SET_VERSION,
    ApprovedMethodologyRuntimeConfig,
    DecisionRuleRuntimeConfig,
    validate_approved_methodology_runtime_config,
)
from assessment.approved_severity_runtime import (
    ApprovedSeverityAssessmentResult,
)


RISK_ASSIGNMENT_METHOD = "severity-distribution-risk-decision-table-v1"

RISK_DECISION_RULE_IDS = (
    "risk-v1-critical-any-critical",
    "risk-v1-elevated-high-concentration",
    "risk-v1-moderate-single-high",
    "risk-v1-moderate-any-medium",
    "risk-v1-low-low-only-defects",
    "risk-v1-minimal-informational-only",
)


@dataclass(frozen=True)
class ApprovedRiskAssessmentResult:
    risk_classification: str
    severity_classifications: tuple[str, ...]
    readiness_classification: str
    overall_assessment_score: float
    risk_decision_identifier: str
    risk_decision_table_version: str
    methodology_version: str
    runtime_config_version: str
    assignment_method: str


def determine_approved_risk(
    severity_results: object,
    runtime_config: ApprovedMethodologyRuntimeConfig = (
        APPROVED_METHODOLOGY_RUNTIME_CONFIG
    ),
) -> ApprovedRiskAssessmentResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_runtime_config_version(runtime_config)
    _validate_risk_decision_table_version(runtime_config)
    _validate_required_risk_rules(runtime_config)

    severity_artifacts = _coerce_severity_artifacts(severity_results)
    _validate_severity_artifacts(severity_artifacts, runtime_config)

    risk_rule = _resolve_risk_rule(severity_artifacts, runtime_config)

    return ApprovedRiskAssessmentResult(
        risk_classification=risk_rule.output,
        severity_classifications=tuple(
            severity.severity_classification
            for severity in severity_artifacts
        ),
        readiness_classification=severity_artifacts[0].readiness_classification,
        overall_assessment_score=severity_artifacts[0].readiness_score,
        risk_decision_identifier=risk_rule.id,
        risk_decision_table_version=risk_rule.table_version,
        methodology_version=severity_artifacts[0].methodology_version,
        runtime_config_version=severity_artifacts[0].runtime_config_version,
        assignment_method=RISK_ASSIGNMENT_METHOD,
    )


def _validate_runtime_config_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.runtime_config_version
        != APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION
    ):
        raise ValueError("Unsupported approved methodology runtime config version.")


def _validate_risk_decision_table_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.risk_decision_table_set_version
        != RISK_DECISION_TABLE_SET_VERSION
    ):
        raise ValueError("Unsupported risk decision table set version.")


def _validate_required_risk_rules(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    for rule_id in RISK_DECISION_RULE_IDS:
        try:
            rule = runtime_config.risk_decision_rules[rule_id]
        except KeyError as exc:
            raise ValueError(
                f"Missing approved risk decision rule: {rule_id}"
            ) from exc
        _validate_risk_rule(rule)


def _validate_risk_rule(rule: DecisionRuleRuntimeConfig) -> None:
    if rule.table_version != RISK_DECISION_TABLE_SET_VERSION:
        raise ValueError(f"Unsupported risk decision table version: {rule.id}")
    if rule.output not in APPROVED_RISK_LEVEL_ORDER:
        raise ValueError(f"Unsupported risk decision output: {rule.id}")


def _coerce_severity_artifacts(
    severity_results: object,
) -> tuple[ApprovedSeverityAssessmentResult, ...]:
    if isinstance(severity_results, ApprovedSeverityAssessmentResult):
        return (severity_results,)

    if isinstance(severity_results, (str, bytes)):
        raise ValueError(
            "Approved risk requires ApprovedSeverityAssessmentResult artifacts."
        )

    if isinstance(severity_results, Iterable):
        severity_artifacts = tuple(severity_results)
        if not severity_artifacts:
            raise ValueError("Approved risk requires at least one severity artifact.")
        return severity_artifacts

    raise ValueError(
        "Approved risk requires ApprovedSeverityAssessmentResult artifacts."
    )


def _validate_severity_artifacts(
    severity_artifacts: tuple[ApprovedSeverityAssessmentResult, ...],
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    first = severity_artifacts[0]
    for severity in severity_artifacts:
        _validate_severity_artifact(severity, runtime_config)
        if severity.methodology_version != first.methodology_version:
            raise ValueError("Severity methodology versions do not match.")
        if severity.runtime_config_version != first.runtime_config_version:
            raise ValueError("Severity runtime config versions do not match.")
        if severity.readiness_classification != first.readiness_classification:
            raise ValueError("Severity readiness classifications do not match.")
        if severity.readiness_score != first.readiness_score:
            raise ValueError("Severity readiness scores do not match.")


def _validate_severity_artifact(
    severity: object,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if not isinstance(severity, ApprovedSeverityAssessmentResult):
        raise ValueError(
            "Approved risk requires ApprovedSeverityAssessmentResult artifacts."
        )
    if (
        severity.methodology_version
        != runtime_config.version_manifest.methodology_version
    ):
        raise ValueError("Severity methodology version is unsupported.")
    if (
        severity.runtime_config_version
        != runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError("Severity runtime config version is unsupported.")
    if severity.decision_table_version != SEVERITY_DECISION_TABLE_SET_VERSION:
        raise ValueError("Severity decision table version is unsupported.")
    if severity.severity_classification not in APPROVED_SEVERITY_LEVEL_ORDER:
        raise ValueError("Severity classification is unsupported.")
    if not isinstance(severity.readiness_score, (int, float)) or isinstance(
        severity.readiness_score,
        bool,
    ):
        raise ValueError("Severity readiness score must be numeric.")
    if not 0 <= float(severity.readiness_score) <= 100:
        raise ValueError("Severity readiness score must be between 0 and 100.")


def _resolve_risk_rule(
    severity_artifacts: tuple[ApprovedSeverityAssessmentResult, ...],
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> DecisionRuleRuntimeConfig:
    severity_counts = {
        severity_level: 0
        for severity_level in APPROVED_SEVERITY_LEVEL_ORDER
    }
    for severity in severity_artifacts:
        severity_counts[severity.severity_classification] += 1

    if severity_counts["critical"] >= 1:
        rule_id = "risk-v1-critical-any-critical"
    elif severity_counts["high"] >= 2:
        rule_id = "risk-v1-elevated-high-concentration"
    elif severity_counts["high"] == 1:
        rule_id = "risk-v1-moderate-single-high"
    elif severity_counts["medium"] >= 1:
        rule_id = "risk-v1-moderate-any-medium"
    elif severity_counts["low"] >= 1:
        rule_id = "risk-v1-low-low-only-defects"
    else:
        rule_id = "risk-v1-minimal-informational-only"

    return runtime_config.risk_decision_rules[rule_id]
