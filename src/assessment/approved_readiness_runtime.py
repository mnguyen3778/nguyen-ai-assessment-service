from dataclasses import dataclass

from assessment.approved_methodology_runtime_config import (
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    READINESS_BOUNDARY_CONVENTION_VERSION,
    READINESS_THRESHOLD_SET_VERSION,
    READINESS_THRESHOLD_VALUES_VERSION,
    ApprovedMethodologyRuntimeConfig,
    ReadinessThresholdRuntimeConfig,
    validate_approved_methodology_runtime_config,
)
from assessment.approved_overall_assessment_runtime import (
    ApprovedOverallAssessmentResult,
)


READINESS_ASSIGNMENT_METHOD = "overall-score-threshold-assignment-v1"


@dataclass(frozen=True)
class ApprovedReadinessAssessmentResult:
    readiness_classification: str
    readiness_score: float
    readiness_threshold_id: str
    threshold_lower_bound: int
    threshold_upper_bound: int
    threshold_lower_inclusive: bool
    threshold_upper_inclusive: bool
    methodology_version: str
    runtime_config_version: str
    readiness_threshold_version: str
    readiness_threshold_set_version: str
    readiness_boundary_convention_version: str
    assignment_method: str


def determine_approved_readiness(
    overall_assessment: object,
    runtime_config: ApprovedMethodologyRuntimeConfig = (
        APPROVED_METHODOLOGY_RUNTIME_CONFIG
    ),
) -> ApprovedReadinessAssessmentResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_runtime_config_version(runtime_config)
    _validate_readiness_versions(runtime_config)
    _validate_thresholds(runtime_config)

    if not isinstance(overall_assessment, ApprovedOverallAssessmentResult):
        raise ValueError(
            "Approved readiness requires ApprovedOverallAssessmentResult."
        )
    _validate_overall_assessment(overall_assessment, runtime_config)

    threshold = _resolve_threshold(
        overall_assessment.overall_assessment_score,
        runtime_config,
    )

    return ApprovedReadinessAssessmentResult(
        readiness_classification=threshold.label,
        readiness_score=float(overall_assessment.overall_assessment_score),
        readiness_threshold_id=threshold.id,
        threshold_lower_bound=threshold.lower_bound,
        threshold_upper_bound=threshold.upper_bound,
        threshold_lower_inclusive=threshold.lower_inclusive,
        threshold_upper_inclusive=threshold.upper_inclusive,
        methodology_version=overall_assessment.methodology_version,
        runtime_config_version=overall_assessment.runtime_config_version,
        readiness_threshold_version=(
            runtime_config.version_manifest.readiness_threshold_values_version
        ),
        readiness_threshold_set_version=(
            runtime_config.version_manifest.readiness_threshold_set_version
        ),
        readiness_boundary_convention_version=(
            runtime_config.version_manifest.readiness_boundary_convention_version
        ),
        assignment_method=READINESS_ASSIGNMENT_METHOD,
    )


def _validate_runtime_config_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.runtime_config_version
        != APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION
    ):
        raise ValueError("Unsupported approved methodology runtime config version.")


def _validate_readiness_versions(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.readiness_threshold_values_version
        != READINESS_THRESHOLD_VALUES_VERSION
    ):
        raise ValueError("Unsupported readiness threshold values version.")
    if (
        runtime_config.version_manifest.readiness_threshold_set_version
        != READINESS_THRESHOLD_SET_VERSION
    ):
        raise ValueError("Unsupported readiness threshold set version.")
    if (
        runtime_config.version_manifest.readiness_boundary_convention_version
        != READINESS_BOUNDARY_CONVENTION_VERSION
    ):
        raise ValueError("Unsupported readiness boundary convention version.")


def _validate_thresholds(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    thresholds = tuple(runtime_config.readiness_thresholds.values())
    if len(thresholds) != 4:
        raise ValueError("Approved readiness requires 4 threshold ranges.")

    expected_lower = 0
    seen_threshold_ids: set[str] = set()
    for threshold in thresholds:
        if threshold.id in seen_threshold_ids:
            raise ValueError(f"Duplicate readiness threshold: {threshold.id}")
        seen_threshold_ids.add(threshold.id)
        if threshold.lower_bound != expected_lower:
            raise ValueError("Approved readiness thresholds contain a gap.")
        if not threshold.lower_inclusive:
            raise ValueError("Approved readiness lower bounds must be inclusive.")
        if threshold.upper_bound <= threshold.lower_bound:
            raise ValueError(
                f"Approved readiness threshold range is invalid: {threshold.id}"
            )
        if threshold.id == "advanced":
            if threshold.upper_bound != 100 or not threshold.upper_inclusive:
                raise ValueError("Approved Advanced threshold must include 100.")
        elif threshold.upper_inclusive:
            raise ValueError(
                "Approved readiness upper bounds must be exclusive before Advanced."
            )
        expected_lower = threshold.upper_bound

    if expected_lower != 100:
        raise ValueError("Approved readiness thresholds must cover 0 through 100.")


def _validate_overall_assessment(
    overall_assessment: ApprovedOverallAssessmentResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        overall_assessment.methodology_version
        != runtime_config.version_manifest.methodology_version
    ):
        raise ValueError("Overall assessment methodology version is unsupported.")
    if (
        overall_assessment.runtime_config_version
        != runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError("Overall assessment runtime config version is unsupported.")
    if (
        overall_assessment.dimension_count != 5
        or len(overall_assessment.weighted_dimension_contributions) != 5
    ):
        raise ValueError("Approved readiness requires 5 dimension contributions.")
    if not isinstance(overall_assessment.overall_assessment_score, (int, float)) or (
        isinstance(overall_assessment.overall_assessment_score, bool)
    ):
        raise ValueError("Overall assessment score must be numeric.")
    if not 0 <= float(overall_assessment.overall_assessment_score) <= 100:
        raise ValueError("Overall assessment score must be between 0 and 100.")

    contribution_total = sum(
        contribution.weighted_score
        for contribution in overall_assessment.weighted_dimension_contributions
    )
    if contribution_total != overall_assessment.overall_assessment_score:
        raise ValueError("Overall assessment score does not match contributions.")


def _resolve_threshold(
    readiness_score: float,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> ReadinessThresholdRuntimeConfig:
    matching_thresholds = tuple(
        threshold
        for threshold in runtime_config.readiness_thresholds.values()
        if _threshold_contains_score(threshold, readiness_score)
    )

    if len(matching_thresholds) != 1:
        raise ValueError("Approved readiness score must resolve to one threshold.")

    return matching_thresholds[0]


def _threshold_contains_score(
    threshold: ReadinessThresholdRuntimeConfig,
    score: float,
) -> bool:
    lower_matches = (
        score >= threshold.lower_bound
        if threshold.lower_inclusive
        else score > threshold.lower_bound
    )
    upper_matches = (
        score <= threshold.upper_bound
        if threshold.upper_inclusive
        else score < threshold.upper_bound
    )
    return lower_matches and upper_matches
