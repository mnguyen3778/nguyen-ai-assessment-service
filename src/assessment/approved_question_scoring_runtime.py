from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from assessment.approved_methodology_runtime_config import (
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    ApprovedMethodologyRuntimeConfig,
    QuestionRuntimeConfig,
    ResponseModelRuntimeConfig,
    validate_approved_methodology_runtime_config,
)


@dataclass(frozen=True)
class CanonicalQuestionResponse:
    question_id: str
    value: object


@dataclass(frozen=True)
class ApprovedQuestionScore:
    question_id: str
    primary_dimension: str
    secondary_dimensions: tuple[str, ...]
    response_model_id: str
    scoring_table_version: str
    taxonomy_version: str
    runtime_config_version: str
    score: float


@dataclass(frozen=True)
class ApprovedQuestionScoringResult:
    methodology_version: str
    runtime_config_version: str
    question_count: int
    question_scores: tuple[ApprovedQuestionScore, ...]


def score_approved_questions(
    responses: object,
    methodology_version: str,
    runtime_config: ApprovedMethodologyRuntimeConfig = (
        APPROVED_METHODOLOGY_RUNTIME_CONFIG
    ),
) -> ApprovedQuestionScoringResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_runtime_config_version(runtime_config)
    _validate_methodology_version(methodology_version, runtime_config)

    response_values = _coerce_response_values(responses)
    _validate_question_coverage(response_values, runtime_config)

    question_scores = tuple(
        _score_question(question, response_values[question_id], runtime_config)
        for question_id, question in runtime_config.questions.items()
    )

    return ApprovedQuestionScoringResult(
        methodology_version=methodology_version,
        runtime_config_version=runtime_config.version_manifest.runtime_config_version,
        question_count=len(question_scores),
        question_scores=question_scores,
    )


def _validate_runtime_config_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.runtime_config_version
        != APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION
    ):
        raise ValueError("Unsupported approved methodology runtime config version.")


def _validate_methodology_version(
    methodology_version: str,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if methodology_version != runtime_config.version_manifest.methodology_version:
        raise ValueError(
            "Unsupported methodology version for approved question scoring."
        )


def _coerce_response_values(responses: object) -> Mapping[str, object]:
    if isinstance(responses, Mapping):
        return MappingProxyType(
            {
                question_id: value
                for question_id, value in _validated_response_pairs(responses.items())
            }
        )

    if isinstance(responses, (str, bytes)):
        raise ValueError("Canonical question responses must be a mapping or entries.")

    if isinstance(responses, Iterable):
        return MappingProxyType(
            {
                question_id: value
                for question_id, value in _validated_response_pairs(responses)
            }
        )

    raise ValueError("Canonical question responses must be a mapping or entries.")


def _validated_response_pairs(
    responses: Iterable[object],
) -> tuple[tuple[str, object], ...]:
    pairs: list[tuple[str, object]] = []
    seen_question_ids: set[str] = set()

    for response in responses:
        question_id, value = _coerce_response_pair(response)
        if question_id in seen_question_ids:
            raise ValueError(f"Duplicate question response: {question_id}")
        seen_question_ids.add(question_id)
        pairs.append((question_id, value))

    return tuple(sorted(pairs, key=lambda item: item[0]))


def _coerce_response_pair(response: object) -> tuple[str, object]:
    if isinstance(response, CanonicalQuestionResponse):
        question_id = response.question_id
        value = response.value
    elif (
        isinstance(response, tuple)
        and len(response) == 2
    ):
        question_id, value = response
    else:
        raise ValueError("Malformed canonical question response.")

    if not isinstance(question_id, str) or not question_id.strip():
        raise ValueError("Question ID must be a non-empty string.")

    return question_id, value


def _validate_question_coverage(
    responses: Mapping[str, object],
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    response_question_ids = set(responses)
    approved_question_ids = set(runtime_config.questions)

    unknown_question_ids = response_question_ids - approved_question_ids
    if unknown_question_ids:
        raise ValueError(
            f"Unknown question response: {sorted(unknown_question_ids)[0]}"
        )

    missing_question_ids = approved_question_ids - response_question_ids
    if missing_question_ids:
        raise ValueError(
            f"Missing question response: {sorted(missing_question_ids)[0]}"
        )

    if len(responses) != 48:
        raise ValueError("Approved question scoring requires 48 canonical responses.")


def _score_question(
    question: QuestionRuntimeConfig,
    response: object,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> ApprovedQuestionScore:
    response_model = _load_response_model(question, runtime_config)
    score = _score_response(question, response, response_model)

    return ApprovedQuestionScore(
        question_id=question.id,
        primary_dimension=question.primary_dimension,
        secondary_dimensions=question.secondary_dimensions,
        response_model_id=question.response_model_id,
        scoring_table_version=question.scoring_table_version,
        taxonomy_version=question.taxonomy_version,
        runtime_config_version=runtime_config.version_manifest.runtime_config_version,
        score=score,
    )


def _load_response_model(
    question: QuestionRuntimeConfig,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> ResponseModelRuntimeConfig:
    try:
        return runtime_config.response_models[question.response_model_id]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported response model for question: {question.id}"
        ) from exc


def _score_response(
    question: QuestionRuntimeConfig,
    response: object,
    response_model: ResponseModelRuntimeConfig,
) -> float:
    if response_model.id == "scale-0-4":
        return _score_scale_response(question, response, response_model)
    if response_model.id == "numeric-0-100":
        return _score_numeric_identity_response(question, response, response_model)

    raise ValueError(f"Unsupported response model: {response_model.id}")


def _score_scale_response(
    question: QuestionRuntimeConfig,
    response: object,
    response_model: ResponseModelRuntimeConfig,
) -> float:
    if not isinstance(response, int) or isinstance(response, bool):
        raise ValueError(f"Malformed response for question: {question.id}")

    try:
        return float(response_model.allowed_response_scores[response])
    except KeyError as exc:
        raise ValueError(f"Out-of-range response for question: {question.id}") from exc


def _score_numeric_identity_response(
    question: QuestionRuntimeConfig,
    response: object,
    response_model: ResponseModelRuntimeConfig,
) -> float:
    if not isinstance(response, (int, float)) or isinstance(response, bool):
        raise ValueError(f"Malformed response for question: {question.id}")

    if (
        response_model.numeric_minimum is None
        or response_model.numeric_maximum is None
        or not response_model.identity_numeric_mapping
    ):
        raise ValueError(f"Unsupported numeric response model: {response_model.id}")

    numeric_response = float(response)
    if not (
        response_model.numeric_minimum
        <= numeric_response
        <= response_model.numeric_maximum
    ):
        raise ValueError(f"Out-of-range response for question: {question.id}")

    return numeric_response
