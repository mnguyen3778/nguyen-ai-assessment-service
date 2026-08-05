from dataclasses import dataclass

from assessment.approved_dimension_weighting_runtime import (
    ApprovedDimensionWeightingResult,
    ApprovedWeightedDimensionEvaluation,
)
from assessment.approved_methodology_runtime_config import (
    APPROVED_DIMENSION_ORDER,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    OFFICIAL_DIMENSION_WEIGHT_SET_VERSION,
    ApprovedMethodologyRuntimeConfig,
    validate_approved_methodology_runtime_config,
)


OVERALL_ASSESSMENT_CALCULATION_METHOD = (
    "weighted-dimension-contribution-sum-v1"
)


@dataclass(frozen=True)
class ApprovedOverallDimensionContribution:
    dimension_id: str
    dimension_name: str
    raw_aggregated_score: float
    official_weight: int
    weighted_score: float


@dataclass(frozen=True)
class ApprovedOverallAssessmentResult:
    overall_assessment_score: float
    weighted_dimension_contributions: tuple[
        ApprovedOverallDimensionContribution,
        ...,
    ]
    methodology_version: str
    runtime_config_version: str
    weight_set_version: str
    calculation_method: str
    dimension_count: int
    total_official_weight: int


def calculate_approved_overall_assessment(
    dimension_weighting: object,
    runtime_config: ApprovedMethodologyRuntimeConfig = (
        APPROVED_METHODOLOGY_RUNTIME_CONFIG
    ),
) -> ApprovedOverallAssessmentResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_runtime_config_version(runtime_config)
    _validate_weight_set_version(runtime_config)

    if not isinstance(dimension_weighting, ApprovedDimensionWeightingResult):
        raise ValueError(
            "Approved overall assessment requires "
            "ApprovedDimensionWeightingResult."
        )
    _validate_dimension_weighting_result(dimension_weighting, runtime_config)

    contributions = tuple(
        _build_dimension_contribution(weighted_dimension)
        for weighted_dimension in dimension_weighting.dimensions
    )

    overall_assessment_score = sum(
        contribution.weighted_score
        for contribution in contributions
    )
    _validate_overall_assessment_score(overall_assessment_score)

    return ApprovedOverallAssessmentResult(
        overall_assessment_score=overall_assessment_score,
        weighted_dimension_contributions=contributions,
        methodology_version=dimension_weighting.methodology_version,
        runtime_config_version=dimension_weighting.runtime_config_version,
        weight_set_version=dimension_weighting.weight_set_version,
        calculation_method=OVERALL_ASSESSMENT_CALCULATION_METHOD,
        dimension_count=len(contributions),
        total_official_weight=dimension_weighting.total_official_weight,
    )


def _validate_runtime_config_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.runtime_config_version
        != APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION
    ):
        raise ValueError("Unsupported approved methodology runtime config version.")


def _validate_weight_set_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.official_dimension_weight_set_version
        != OFFICIAL_DIMENSION_WEIGHT_SET_VERSION
    ):
        raise ValueError("Unsupported official dimension weight set version.")


def _validate_dimension_weighting_result(
    dimension_weighting: ApprovedDimensionWeightingResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        dimension_weighting.methodology_version
        != runtime_config.version_manifest.methodology_version
    ):
        raise ValueError("Dimension weighting methodology version is unsupported.")
    if (
        dimension_weighting.runtime_config_version
        != runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError("Dimension weighting runtime config version is unsupported.")
    if (
        dimension_weighting.weight_set_version
        != runtime_config.version_manifest.official_dimension_weight_set_version
    ):
        raise ValueError("Dimension weighting weight set version is unsupported.")
    if (
        dimension_weighting.dimension_count != 5
        or len(dimension_weighting.dimensions) != 5
    ):
        raise ValueError("Approved overall assessment requires 5 dimensions.")
    if dimension_weighting.total_official_weight != 100:
        raise ValueError("Approved overall assessment requires total weight of 100.")

    observed_dimension_ids: list[str] = []
    observed_weight_total = 0
    for weighted_dimension in dimension_weighting.dimensions:
        _validate_weighted_dimension(weighted_dimension, runtime_config)
        observed_dimension_ids.append(weighted_dimension.dimension_id)
        observed_weight_total += weighted_dimension.official_weight

    if len(set(observed_dimension_ids)) != len(observed_dimension_ids):
        raise ValueError("Duplicate approved weighted dimension result.")
    if tuple(observed_dimension_ids) != APPROVED_DIMENSION_ORDER:
        raise ValueError("Approved weighted dimension order is invalid.")
    if observed_weight_total != 100:
        raise ValueError("Approved weighted dimension weights must sum to 100.")


def _validate_weighted_dimension(
    weighted_dimension: ApprovedWeightedDimensionEvaluation,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if not isinstance(weighted_dimension, ApprovedWeightedDimensionEvaluation):
        raise ValueError(
            "Approved overall assessment requires weighted dimension artifacts."
        )

    try:
        dimension_config = runtime_config.dimensions[weighted_dimension.dimension_id]
    except KeyError as exc:
        raise ValueError(
            "Unknown approved weighted dimension result: "
            f"{weighted_dimension.dimension_id}"
        ) from exc

    if weighted_dimension.dimension_name != dimension_config.label:
        raise ValueError(
            f"Approved weighted dimension name mismatch: "
            f"{weighted_dimension.dimension_id}"
        )
    if weighted_dimension.official_weight != dimension_config.weight:
        raise ValueError(
            f"Approved weighted dimension weight mismatch: "
            f"{weighted_dimension.dimension_id}"
        )
    if (
        weighted_dimension.methodology_version
        != runtime_config.version_manifest.methodology_version
    ):
        raise ValueError(
            "Approved weighted dimension methodology mismatch: "
            f"{weighted_dimension.dimension_id}"
        )
    if (
        weighted_dimension.runtime_config_version
        != runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError(
            "Approved weighted dimension runtime config mismatch: "
            f"{weighted_dimension.dimension_id}"
        )
    if (
        weighted_dimension.weight_set_version
        != runtime_config.version_manifest.official_dimension_weight_set_version
    ):
        raise ValueError(
            "Approved weighted dimension weight set mismatch: "
            f"{weighted_dimension.dimension_id}"
        )
    _validate_score(
        "raw aggregated score",
        weighted_dimension.dimension_id,
        weighted_dimension.raw_aggregated_score,
    )
    _validate_score(
        "weighted score",
        weighted_dimension.dimension_id,
        weighted_dimension.weighted_score,
    )

    expected_weighted_score = (
        float(weighted_dimension.raw_aggregated_score)
        * weighted_dimension.official_weight
        / 100
    )
    if weighted_dimension.weighted_score != expected_weighted_score:
        raise ValueError(
            "Approved weighted dimension contribution mismatch: "
            f"{weighted_dimension.dimension_id}"
        )


def _validate_score(field_name: str, dimension_id: str, value: object) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(
            f"Approved weighted dimension {field_name} must be numeric: "
            f"{dimension_id}"
        )
    if not 0 <= float(value) <= 100:
        raise ValueError(
            f"Approved weighted dimension {field_name} must be between 0 and 100: "
            f"{dimension_id}"
        )


def _validate_overall_assessment_score(score: float) -> None:
    if not 0 <= score <= 100:
        raise ValueError("Approved overall assessment score must be between 0 and 100.")


def _build_dimension_contribution(
    weighted_dimension: ApprovedWeightedDimensionEvaluation,
) -> ApprovedOverallDimensionContribution:
    return ApprovedOverallDimensionContribution(
        dimension_id=weighted_dimension.dimension_id,
        dimension_name=weighted_dimension.dimension_name,
        raw_aggregated_score=float(weighted_dimension.raw_aggregated_score),
        official_weight=weighted_dimension.official_weight,
        weighted_score=float(weighted_dimension.weighted_score),
    )
