from dataclasses import dataclass

from assessment.approved_methodology_runtime_config import (
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    APPROVED_SEVERITY_LEVEL_ORDER,
    READINESS_BOUNDARY_CONVENTION_VERSION,
    READINESS_THRESHOLD_SET_VERSION,
    READINESS_THRESHOLD_VALUES_VERSION,
    SEVERITY_DECISION_TABLE_SET_VERSION,
    ApprovedMethodologyRuntimeConfig,
    DecisionRuleRuntimeConfig,
    ReadinessThresholdRuntimeConfig,
    validate_approved_methodology_runtime_config,
)
from assessment.approved_readiness_runtime import (
    ApprovedReadinessAssessmentResult,
)


SEVERITY_ASSIGNMENT_METHOD = "readiness-context-severity-decision-table-v1"

READINESS_SEVERITY_DECISION_RULE_IDS = {
    "not-ready": "severity-v1-deficiency-critical",
    "developing": "severity-v1-deficiency-high",
    "ready": "severity-v1-deficiency-medium",
    "advanced": "severity-v1-observation-informational",
}


@dataclass(frozen=True)
class ApprovedSeverityAssessmentResult:
    severity_classification: str
    readiness_classification: str
    readiness_score: float
    severity_decision_identifier: str
    decision_table_version: str
    methodology_version: str
    runtime_config_version: str
    assignment_method: str


def determine_approved_severity(
    readiness: object,
    runtime_config: ApprovedMethodologyRuntimeConfig = (
        APPROVED_METHODOLOGY_RUNTIME_CONFIG
    ),
) -> ApprovedSeverityAssessmentResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_runtime_config_version(runtime_config)
    _validate_severity_decision_table_version(runtime_config)
    _validate_required_severity_rules(runtime_config)

    if not isinstance(readiness, ApprovedReadinessAssessmentResult):
        raise ValueError(
            "Approved severity requires ApprovedReadinessAssessmentResult."
        )
    _validate_readiness(readiness, runtime_config)

    severity_rule = _resolve_severity_rule(readiness, runtime_config)

    return ApprovedSeverityAssessmentResult(
        severity_classification=severity_rule.output,
        readiness_classification=readiness.readiness_classification,
        readiness_score=readiness.readiness_score,
        severity_decision_identifier=severity_rule.id,
        decision_table_version=severity_rule.table_version,
        methodology_version=readiness.methodology_version,
        runtime_config_version=readiness.runtime_config_version,
        assignment_method=SEVERITY_ASSIGNMENT_METHOD,
    )


def _validate_runtime_config_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.runtime_config_version
        != APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION
    ):
        raise ValueError("Unsupported approved methodology runtime config version.")


def _validate_severity_decision_table_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.severity_decision_table_set_version
        != SEVERITY_DECISION_TABLE_SET_VERSION
    ):
        raise ValueError("Unsupported severity decision table set version.")


def _validate_required_severity_rules(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    for rule_id in READINESS_SEVERITY_DECISION_RULE_IDS.values():
        try:
            rule = runtime_config.severity_decision_rules[rule_id]
        except KeyError as exc:
            raise ValueError(
                f"Missing approved severity decision rule: {rule_id}"
            ) from exc
        _validate_severity_rule(rule)


def _validate_severity_rule(rule: DecisionRuleRuntimeConfig) -> None:
    if rule.table_version != SEVERITY_DECISION_TABLE_SET_VERSION:
        raise ValueError(f"Unsupported severity decision table version: {rule.id}")
    if rule.output not in APPROVED_SEVERITY_LEVEL_ORDER:
        raise ValueError(f"Unsupported severity decision output: {rule.id}")


def _validate_readiness(
    readiness: ApprovedReadinessAssessmentResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        readiness.methodology_version
        != runtime_config.version_manifest.methodology_version
    ):
        raise ValueError("Readiness methodology version is unsupported.")
    if (
        readiness.runtime_config_version
        != runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError("Readiness runtime config version is unsupported.")
    if (
        readiness.readiness_threshold_version
        != runtime_config.version_manifest.readiness_threshold_values_version
    ):
        raise ValueError("Readiness threshold values version is unsupported.")
    if (
        readiness.readiness_threshold_set_version
        != runtime_config.version_manifest.readiness_threshold_set_version
    ):
        raise ValueError("Readiness threshold set version is unsupported.")
    if (
        readiness.readiness_boundary_convention_version
        != runtime_config.version_manifest.readiness_boundary_convention_version
    ):
        raise ValueError("Readiness boundary convention version is unsupported.")
    if readiness.readiness_threshold_version != READINESS_THRESHOLD_VALUES_VERSION:
        raise ValueError("Unsupported readiness threshold values version.")
    if readiness.readiness_threshold_set_version != READINESS_THRESHOLD_SET_VERSION:
        raise ValueError("Unsupported readiness threshold set version.")
    if (
        readiness.readiness_boundary_convention_version
        != READINESS_BOUNDARY_CONVENTION_VERSION
    ):
        raise ValueError("Unsupported readiness boundary convention version.")
    if not isinstance(readiness.readiness_score, (int, float)) or isinstance(
        readiness.readiness_score,
        bool,
    ):
        raise ValueError("Readiness score must be numeric.")
    if not 0 <= float(readiness.readiness_score) <= 100:
        raise ValueError("Readiness score must be between 0 and 100.")

    threshold = _load_readiness_threshold(readiness, runtime_config)
    if readiness.readiness_classification != threshold.label:
        raise ValueError("Readiness classification does not match threshold.")
    if (
        readiness.threshold_lower_bound != threshold.lower_bound
        or readiness.threshold_upper_bound != threshold.upper_bound
        or readiness.threshold_lower_inclusive != threshold.lower_inclusive
        or readiness.threshold_upper_inclusive != threshold.upper_inclusive
    ):
        raise ValueError("Readiness threshold metadata is unsupported.")
    if not _threshold_contains_score(
        readiness,
        threshold.lower_bound,
        threshold.upper_bound,
    ):
        raise ValueError("Readiness score does not match threshold range.")


def _load_readiness_threshold(
    readiness: ApprovedReadinessAssessmentResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> ReadinessThresholdRuntimeConfig:
    try:
        return runtime_config.readiness_thresholds[readiness.readiness_threshold_id]
    except KeyError as exc:
        raise ValueError(
            f"Unknown readiness threshold: {readiness.readiness_threshold_id}"
        ) from exc


def _threshold_contains_score(
    readiness: ApprovedReadinessAssessmentResult,
    lower_bound: int,
    upper_bound: int,
) -> bool:
    lower_matches = (
        readiness.readiness_score >= lower_bound
        if readiness.threshold_lower_inclusive
        else readiness.readiness_score > lower_bound
    )
    upper_matches = (
        readiness.readiness_score <= upper_bound
        if readiness.threshold_upper_inclusive
        else readiness.readiness_score < upper_bound
    )
    return lower_matches and upper_matches


def _resolve_severity_rule(
    readiness: ApprovedReadinessAssessmentResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> DecisionRuleRuntimeConfig:
    try:
        rule_id = READINESS_SEVERITY_DECISION_RULE_IDS[
            readiness.readiness_threshold_id
        ]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported readiness threshold for severity: "
            f"{readiness.readiness_threshold_id}"
        ) from exc

    return runtime_config.severity_decision_rules[rule_id]
