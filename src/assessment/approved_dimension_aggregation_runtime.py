from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from assessment.approved_methodology_runtime_config import (
    APPROVED_DIMENSION_ORDER,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    SCORING_SCALE_VERSION,
    ApprovedMethodologyRuntimeConfig,
    validate_approved_methodology_runtime_config,
)
from assessment.approved_question_scoring_runtime import (
    ApprovedQuestionScore,
    ApprovedQuestionScoringResult,
)


DIMENSION_AGGREGATION_METHOD = "equal-contribution-arithmetic-mean-v1"


@dataclass(frozen=True)
class ApprovedDimensionEvaluation:
    dimension_id: str
    dimension_name: str
    score: float
    contributing_question_ids: tuple[str, ...]
    contributing_scores: Mapping[str, float]
    aggregation_method: str
    expected_question_count: int
    question_count: int
    methodology_version: str
    runtime_config_version: str
    scoring_scale_version: str

    def __post_init__(self) -> None:
        if isinstance(self.contributing_scores, Mapping):
            object.__setattr__(
                self,
                "contributing_scores",
                MappingProxyType(dict(self.contributing_scores)),
            )


@dataclass(frozen=True)
class ApprovedDimensionAggregationResult:
    methodology_version: str
    runtime_config_version: str
    aggregation_method: str
    dimension_count: int
    dimensions: tuple[ApprovedDimensionEvaluation, ...]


def aggregate_approved_dimensions(
    question_scoring: object,
    runtime_config: ApprovedMethodologyRuntimeConfig = (
        APPROVED_METHODOLOGY_RUNTIME_CONFIG
    ),
) -> ApprovedDimensionAggregationResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_runtime_config_version(runtime_config)
    if not isinstance(question_scoring, ApprovedQuestionScoringResult):
        raise ValueError(
            "Approved dimension aggregation requires ApprovedQuestionScoringResult."
        )
    _validate_question_scoring_result(question_scoring, runtime_config)

    scores_by_dimension = _group_scores_by_dimension(question_scoring, runtime_config)
    dimensions = tuple(
        _build_dimension_evaluation(
            dimension_id,
            scores_by_dimension[dimension_id],
            runtime_config,
        )
        for dimension_id in APPROVED_DIMENSION_ORDER
    )

    return ApprovedDimensionAggregationResult(
        methodology_version=question_scoring.methodology_version,
        runtime_config_version=question_scoring.runtime_config_version,
        aggregation_method=DIMENSION_AGGREGATION_METHOD,
        dimension_count=len(dimensions),
        dimensions=dimensions,
    )


def _validate_runtime_config_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.runtime_config_version
        != APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION
    ):
        raise ValueError("Unsupported approved methodology runtime config version.")


def _validate_question_scoring_result(
    question_scoring: ApprovedQuestionScoringResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        question_scoring.methodology_version
        != runtime_config.version_manifest.methodology_version
    ):
        raise ValueError("Question scoring methodology version is unsupported.")
    if (
        question_scoring.runtime_config_version
        != runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError("Question scoring runtime config version is unsupported.")
    if (
        question_scoring.question_count != 48
        or len(question_scoring.question_scores) != 48
    ):
        raise ValueError("Approved dimension aggregation requires 48 question scores.")

    seen_question_ids: set[str] = set()
    for question_score in question_scoring.question_scores:
        _validate_question_score(question_score, runtime_config)
        if question_score.question_id in seen_question_ids:
            raise ValueError(f"Duplicate question score: {question_score.question_id}")
        seen_question_ids.add(question_score.question_id)

    approved_question_ids = set(runtime_config.questions)
    observed_question_ids = seen_question_ids

    unknown_question_ids = observed_question_ids - approved_question_ids
    if unknown_question_ids:
        raise ValueError(
            f"Unknown question score: {sorted(unknown_question_ids)[0]}"
        )

    missing_question_ids = approved_question_ids - observed_question_ids
    if missing_question_ids:
        raise ValueError(
            f"Missing question score: {sorted(missing_question_ids)[0]}"
        )


def _validate_question_score(
    question_score: ApprovedQuestionScore,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    try:
        question = runtime_config.questions[question_score.question_id]
    except KeyError:
        return

    if question_score.primary_dimension != question.primary_dimension:
        raise ValueError(
            f"Question score Primary Dimension mismatch: {question_score.question_id}"
        )
    if question_score.secondary_dimensions != question.secondary_dimensions:
        raise ValueError(
            f"Question score Secondary Dimensions mismatch: {question_score.question_id}"
        )
    if question_score.response_model_id != question.response_model_id:
        raise ValueError(
            f"Question score response model mismatch: {question_score.question_id}"
        )
    if question_score.scoring_table_version != question.scoring_table_version:
        raise ValueError(
            f"Question score scoring table mismatch: {question_score.question_id}"
        )
    if question_score.taxonomy_version != question.taxonomy_version:
        raise ValueError(
            f"Question score taxonomy version mismatch: {question_score.question_id}"
        )
    if question_score.runtime_config_version != (
        runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError(
            f"Question score runtime config mismatch: {question_score.question_id}"
        )
    if not isinstance(question_score.score, (int, float)) or isinstance(
        question_score.score,
        bool,
    ):
        raise ValueError(
            f"Question score must be numeric: {question_score.question_id}"
        )
    if not 0 <= float(question_score.score) <= 100:
        raise ValueError(
            f"Question score must be between 0 and 100: {question_score.question_id}"
        )


def _group_scores_by_dimension(
    question_scoring: ApprovedQuestionScoringResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> dict[str, tuple[ApprovedQuestionScore, ...]]:
    grouped_scores: dict[str, list[ApprovedQuestionScore]] = {
        dimension_id: []
        for dimension_id in runtime_config.dimensions
    }

    for question_score in question_scoring.question_scores:
        grouped_scores[question_score.primary_dimension].append(question_score)

    grouped_tuple_scores = {
        dimension_id: tuple(
            sorted(
                dimension_scores,
                key=lambda question_score: question_score.question_id,
            )
        )
        for dimension_id, dimension_scores in grouped_scores.items()
    }

    for dimension_id, dimension_config in runtime_config.dimensions.items():
        if not grouped_tuple_scores[dimension_id]:
            raise ValueError(f"Missing approved dimension scores: {dimension_id}")
        if (
            len(grouped_tuple_scores[dimension_id])
            != dimension_config.expected_primary_question_count
        ):
            raise ValueError(
                f"Approved dimension question count mismatch: {dimension_id}"
            )

    return grouped_tuple_scores


def _build_dimension_evaluation(
    dimension_id: str,
    question_scores: tuple[ApprovedQuestionScore, ...],
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> ApprovedDimensionEvaluation:
    dimension_config = runtime_config.dimensions[dimension_id]
    contributing_scores = MappingProxyType(
        {
            question_score.question_id: float(question_score.score)
            for question_score in question_scores
        }
    )

    return ApprovedDimensionEvaluation(
        dimension_id=dimension_id,
        dimension_name=dimension_config.label,
        score=sum(contributing_scores.values()) / len(contributing_scores),
        contributing_question_ids=tuple(contributing_scores),
        contributing_scores=contributing_scores,
        aggregation_method=DIMENSION_AGGREGATION_METHOD,
        expected_question_count=dimension_config.expected_primary_question_count,
        question_count=len(contributing_scores),
        methodology_version=runtime_config.version_manifest.methodology_version,
        runtime_config_version=runtime_config.version_manifest.runtime_config_version,
        scoring_scale_version=SCORING_SCALE_VERSION,
    )
