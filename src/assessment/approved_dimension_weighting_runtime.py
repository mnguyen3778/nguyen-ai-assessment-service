from dataclasses import dataclass

from assessment.approved_dimension_aggregation_runtime import (
    ApprovedDimensionAggregationResult,
    ApprovedDimensionEvaluation,
)
from assessment.approved_methodology_runtime_config import (
    APPROVED_DIMENSION_ORDER,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    OFFICIAL_DIMENSION_WEIGHT_SET_VERSION,
    ApprovedMethodologyRuntimeConfig,
    validate_approved_methodology_runtime_config,
)


@dataclass(frozen=True)
class ApprovedWeightedDimensionEvaluation:
    dimension_id: str
    dimension_name: str
    raw_aggregated_score: float
    official_weight: int
    weighted_score: float
    methodology_version: str
    runtime_config_version: str
    weight_set_version: str


@dataclass(frozen=True)
class ApprovedDimensionWeightingResult:
    methodology_version: str
    runtime_config_version: str
    weight_set_version: str
    dimension_count: int
    total_official_weight: int
    dimensions: tuple[ApprovedWeightedDimensionEvaluation, ...]


def weight_approved_dimensions(
    dimension_aggregation: object,
    runtime_config: ApprovedMethodologyRuntimeConfig = (
        APPROVED_METHODOLOGY_RUNTIME_CONFIG
    ),
) -> ApprovedDimensionWeightingResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_runtime_config_version(runtime_config)
    _validate_weight_set(runtime_config)

    if not isinstance(dimension_aggregation, ApprovedDimensionAggregationResult):
        raise ValueError(
            "Approved dimension weighting requires "
            "ApprovedDimensionAggregationResult."
        )
    _validate_dimension_aggregation_result(dimension_aggregation, runtime_config)

    weighted_dimensions = tuple(
        _build_weighted_dimension(
            dimension,
            runtime_config,
        )
        for dimension in dimension_aggregation.dimensions
    )

    return ApprovedDimensionWeightingResult(
        methodology_version=dimension_aggregation.methodology_version,
        runtime_config_version=dimension_aggregation.runtime_config_version,
        weight_set_version=(
            runtime_config.version_manifest.official_dimension_weight_set_version
        ),
        dimension_count=len(weighted_dimensions),
        total_official_weight=sum(
            dimension.official_weight for dimension in weighted_dimensions
        ),
        dimensions=weighted_dimensions,
    )


def _validate_runtime_config_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.runtime_config_version
        != APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION
    ):
        raise ValueError("Unsupported approved methodology runtime config version.")


def _validate_weight_set(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.official_dimension_weight_set_version
        != OFFICIAL_DIMENSION_WEIGHT_SET_VERSION
    ):
        raise ValueError("Unsupported official dimension weight set version.")

    if tuple(runtime_config.dimensions) != APPROVED_DIMENSION_ORDER:
        raise ValueError("Approved Business Capability Dimension weights are invalid.")

    if len(runtime_config.dimensions) != 5:
        raise ValueError("Approved dimension weighting requires exactly 5 dimensions.")

    total_weight = 0
    for dimension_id, dimension in runtime_config.dimensions.items():
        if dimension_id != dimension.id:
            raise ValueError(f"Dimension weight key mismatch: {dimension_id}")
        if not isinstance(dimension.weight, int) or isinstance(dimension.weight, bool):
            raise ValueError(f"Dimension weight must be an integer: {dimension_id}")
        if dimension.weight <= 0:
            raise ValueError(f"Dimension weight must be greater than 0: {dimension_id}")
        total_weight += dimension.weight

    if total_weight != 100:
        raise ValueError("Approved dimension weights must sum to 100.")


def _validate_dimension_aggregation_result(
    dimension_aggregation: ApprovedDimensionAggregationResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        dimension_aggregation.methodology_version
        != runtime_config.version_manifest.methodology_version
    ):
        raise ValueError("Dimension aggregation methodology version is unsupported.")
    if (
        dimension_aggregation.runtime_config_version
        != runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError("Dimension aggregation runtime config version is unsupported.")
    if (
        dimension_aggregation.dimension_count != 5
        or len(dimension_aggregation.dimensions) != 5
    ):
        raise ValueError("Approved dimension weighting requires 5 dimensions.")

    observed_dimension_ids: list[str] = []
    for dimension in dimension_aggregation.dimensions:
        _validate_dimension_evaluation(dimension, runtime_config)
        observed_dimension_ids.append(dimension.dimension_id)

    if len(set(observed_dimension_ids)) != len(observed_dimension_ids):
        raise ValueError("Duplicate approved dimension aggregation result.")
    if tuple(observed_dimension_ids) != APPROVED_DIMENSION_ORDER:
        raise ValueError("Approved dimension aggregation order is invalid.")


def _validate_dimension_evaluation(
    dimension: ApprovedDimensionEvaluation,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if not isinstance(dimension, ApprovedDimensionEvaluation):
        raise ValueError("Approved dimension weighting requires dimension artifacts.")

    try:
        dimension_config = runtime_config.dimensions[dimension.dimension_id]
    except KeyError as exc:
        raise ValueError(
            f"Unknown approved dimension aggregation result: {dimension.dimension_id}"
        ) from exc

    if dimension.dimension_name != dimension_config.label:
        raise ValueError(
            f"Approved dimension name mismatch: {dimension.dimension_id}"
        )
    if (
        dimension.methodology_version
        != runtime_config.version_manifest.methodology_version
    ):
        raise ValueError(
            f"Approved dimension methodology mismatch: {dimension.dimension_id}"
        )
    if (
        dimension.runtime_config_version
        != runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError(
            f"Approved dimension runtime config mismatch: {dimension.dimension_id}"
        )
    if not isinstance(dimension.score, (int, float)) or isinstance(
        dimension.score,
        bool,
    ):
        raise ValueError(
            f"Approved dimension score must be numeric: {dimension.dimension_id}"
        )
    if not 0 <= float(dimension.score) <= 100:
        raise ValueError(
            "Approved dimension score must be between 0 and 100: "
            f"{dimension.dimension_id}"
        )


def _build_weighted_dimension(
    dimension: ApprovedDimensionEvaluation,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> ApprovedWeightedDimensionEvaluation:
    dimension_config = runtime_config.dimensions[dimension.dimension_id]
    raw_aggregated_score = float(dimension.score)
    official_weight = dimension_config.weight

    return ApprovedWeightedDimensionEvaluation(
        dimension_id=dimension.dimension_id,
        dimension_name=dimension.dimension_name,
        raw_aggregated_score=raw_aggregated_score,
        official_weight=official_weight,
        weighted_score=raw_aggregated_score * official_weight / 100,
        methodology_version=dimension.methodology_version,
        runtime_config_version=dimension.runtime_config_version,
        weight_set_version=(
            runtime_config.version_manifest.official_dimension_weight_set_version
        ),
    )
