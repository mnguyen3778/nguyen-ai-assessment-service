from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from assessment.methodology_config import (
    AnswerTypeConfig,
    BUSINESS_DECISION_METHODOLOGY,
    BusinessDecisionMethodologyConfig,
    QuestionConfig,
    validate_methodology_config,
)


MIN_NORMALIZED_SCORE = 0.0
MAX_NORMALIZED_SCORE = 100.0


@dataclass(frozen=True)
class QuestionEvaluation:
    question_id: str
    readiness_dimension: str
    normalized_score: float
    weight: float = 1.0
    evidence_category: str = ""
    weight_category: str = ""


@dataclass(frozen=True)
class DimensionEvaluation:
    dimension_id: str
    normalized_score: float
    total_weight: float
    question_count: int
    contributing_questions: tuple[str, ...]


@dataclass(frozen=True)
class QuestionExplanation:
    question_id: str
    readiness_dimension: str
    evidence_category: str
    weight_category: str
    applied_weight: float
    normalized_score: float


@dataclass(frozen=True)
class DimensionExplanation:
    dimension_id: str
    contributing_questions: tuple[str, ...]
    applied_weights: Mapping[str, float]
    normalized_score: float
    total_weight: float


@dataclass(frozen=True)
class EvaluationExplanation:
    evaluated_dimensions: tuple[str, ...]
    contributing_questions: tuple[str, ...]
    applied_weights: Mapping[str, float]
    question_explanations: Mapping[str, QuestionExplanation]
    dimension_explanations: Mapping[str, DimensionExplanation]


@dataclass(frozen=True)
class DecisionEvaluationResult:
    overall_score: float
    total_weight: float
    question_count: int
    dimensions: Mapping[str, DimensionEvaluation]
    explanation: EvaluationExplanation | None = None


def evaluate_decision(
    question_evaluations: Iterable[QuestionEvaluation],
) -> DecisionEvaluationResult:
    evaluations = tuple(question_evaluations)
    _validate_question_evaluations(evaluations)

    dimensions = _aggregate_dimensions(evaluations)
    return DecisionEvaluationResult(
        overall_score=_weighted_average(evaluations),
        total_weight=sum(evaluation.weight for evaluation in evaluations),
        question_count=len(evaluations),
        dimensions=MappingProxyType(dimensions),
        explanation=_build_evaluation_explanation(evaluations, dimensions),
    )


def evaluate_assessment(
    answers: Mapping[str, object],
    methodology_config: BusinessDecisionMethodologyConfig = (
        BUSINESS_DECISION_METHODOLOGY
    ),
) -> DecisionEvaluationResult:
    question_evaluations = build_question_evaluations(
        answers,
        methodology_config,
    )
    return evaluate_decision(question_evaluations)


def build_question_evaluations(
    answers: Mapping[str, object],
    methodology_config: BusinessDecisionMethodologyConfig = (
        BUSINESS_DECISION_METHODOLOGY
    ),
) -> tuple[QuestionEvaluation, ...]:
    validate_methodology_config(methodology_config)
    _validate_answer_set(answers, methodology_config)

    return tuple(
        build_question_evaluation(
            question_id,
            answers[question_id],
            methodology_config,
        )
        for question_id in sorted(methodology_config.questions)
    )


def load_question_definition(
    question_id: str,
    methodology_config: BusinessDecisionMethodologyConfig = (
        BUSINESS_DECISION_METHODOLOGY
    ),
) -> QuestionConfig:
    try:
        return methodology_config.questions[question_id]
    except KeyError as exc:
        raise ValueError(f"Unknown question ID: {question_id}") from exc


def build_question_evaluation(
    question_id: str,
    answer: object,
    methodology_config: BusinessDecisionMethodologyConfig = (
        BUSINESS_DECISION_METHODOLOGY
    ),
) -> QuestionEvaluation:
    question = load_question_definition(question_id, methodology_config)
    answer_type = load_answer_type(question, methodology_config)
    validate_answer(question, answer, answer_type)

    return QuestionEvaluation(
        question_id=question.id,
        readiness_dimension=question.readiness_dimension,
        normalized_score=normalize_answer(question, answer, answer_type),
        weight=methodology_config.placeholder_question_weights[question.id],
        evidence_category=question.evidence_category,
        weight_category=question.weight_category,
    )


def load_answer_type(
    question: QuestionConfig,
    methodology_config: BusinessDecisionMethodologyConfig = (
        BUSINESS_DECISION_METHODOLOGY
    ),
) -> AnswerTypeConfig:
    try:
        return methodology_config.answer_types[question.expected_answer_type]
    except KeyError as exc:
        raise ValueError(
            f"Unknown answer type for question {question.id}: "
            f"{question.expected_answer_type}"
        ) from exc


def validate_answer(
    question: QuestionConfig,
    answer: object,
    answer_type: AnswerTypeConfig,
) -> None:
    if not answer_type.is_normalizable:
        raise ValueError(
            f"Question {question.id} answer type is not evaluable in this increment: "
            f"{question.expected_answer_type}"
        )
    if not _is_number(answer):
        raise ValueError(f"Answer for {question.id} must be numeric.")
    if not answer_type.minimum <= answer <= answer_type.maximum:
        raise ValueError(
            f"Answer for {question.id} must be between "
            f"{answer_type.minimum:g} and {answer_type.maximum:g}."
        )


def normalize_answer(
    question: QuestionConfig,
    answer: object,
    answer_type: AnswerTypeConfig,
) -> float:
    validate_answer(question, answer, answer_type)
    if answer_type.minimum is None or answer_type.maximum is None:
        raise ValueError(
            f"Question {question.id} answer type is not normalizable: "
            f"{question.expected_answer_type}"
        )

    return (
        (float(answer) - answer_type.minimum)
        / (answer_type.maximum - answer_type.minimum)
        * MAX_NORMALIZED_SCORE
    )


def _validate_answer_set(
    answers: Mapping[str, object],
    methodology_config: BusinessDecisionMethodologyConfig,
) -> None:
    unknown_question_ids = answers.keys() - methodology_config.questions.keys()
    if unknown_question_ids:
        raise ValueError(f"Unknown question ID: {sorted(unknown_question_ids)[0]}")

    missing_question_ids = methodology_config.questions.keys() - answers.keys()
    if missing_question_ids:
        raise ValueError(f"Missing required question: {sorted(missing_question_ids)[0]}")


def _aggregate_dimensions(
    evaluations: tuple[QuestionEvaluation, ...],
) -> dict[str, DimensionEvaluation]:
    by_dimension: dict[str, list[QuestionEvaluation]] = {}
    for evaluation in evaluations:
        by_dimension.setdefault(evaluation.readiness_dimension, []).append(evaluation)

    return {
        dimension_id: DimensionEvaluation(
            dimension_id=dimension_id,
            normalized_score=_weighted_average(dimension_evaluations),
            total_weight=sum(evaluation.weight for evaluation in dimension_evaluations),
            question_count=len(dimension_evaluations),
            contributing_questions=tuple(
                evaluation.question_id
                for evaluation in sorted(
                    dimension_evaluations,
                    key=lambda item: item.question_id,
                )
            ),
        )
        for dimension_id, dimension_evaluations in sorted(by_dimension.items())
    }


def _build_evaluation_explanation(
    evaluations: tuple[QuestionEvaluation, ...],
    dimensions: Mapping[str, DimensionEvaluation],
) -> EvaluationExplanation:
    sorted_evaluations = tuple(
        sorted(evaluations, key=lambda evaluation: evaluation.question_id)
    )
    applied_weights = {
        evaluation.question_id: evaluation.weight
        for evaluation in sorted_evaluations
    }
    question_explanations = {
        evaluation.question_id: QuestionExplanation(
            question_id=evaluation.question_id,
            readiness_dimension=evaluation.readiness_dimension,
            evidence_category=evaluation.evidence_category,
            weight_category=evaluation.weight_category,
            applied_weight=evaluation.weight,
            normalized_score=evaluation.normalized_score,
        )
        for evaluation in sorted_evaluations
    }
    dimension_explanations = {
        dimension_id: DimensionExplanation(
            dimension_id=dimension_id,
            contributing_questions=dimension.contributing_questions,
            applied_weights=MappingProxyType(
                {
                    question_id: applied_weights[question_id]
                    for question_id in dimension.contributing_questions
                }
            ),
            normalized_score=dimension.normalized_score,
            total_weight=dimension.total_weight,
        )
        for dimension_id, dimension in sorted(dimensions.items())
    }

    return EvaluationExplanation(
        evaluated_dimensions=tuple(sorted(dimensions)),
        contributing_questions=tuple(
            evaluation.question_id for evaluation in sorted_evaluations
        ),
        applied_weights=MappingProxyType(applied_weights),
        question_explanations=MappingProxyType(question_explanations),
        dimension_explanations=MappingProxyType(dimension_explanations),
    )


def _weighted_average(
    evaluations: tuple[QuestionEvaluation, ...] | list[QuestionEvaluation],
) -> float:
    weighted_score = sum(
        evaluation.normalized_score * evaluation.weight
        for evaluation in evaluations
    )
    total_weight = sum(evaluation.weight for evaluation in evaluations)
    return weighted_score / total_weight


def _validate_question_evaluations(
    evaluations: tuple[QuestionEvaluation, ...],
) -> None:
    if not evaluations:
        raise ValueError("At least one question evaluation is required.")

    seen_question_ids: set[str] = set()
    for evaluation in evaluations:
        _validate_non_empty_text("question_id", evaluation.question_id)
        _validate_non_empty_text(
            "readiness_dimension",
            evaluation.readiness_dimension,
        )
        if evaluation.question_id in seen_question_ids:
            raise ValueError(f"Duplicate question evaluation: {evaluation.question_id}")
        seen_question_ids.add(evaluation.question_id)

        if not _is_number(evaluation.normalized_score):
            raise ValueError("Question normalized_score must be numeric.")
        if not (
            MIN_NORMALIZED_SCORE
            <= evaluation.normalized_score
            <= MAX_NORMALIZED_SCORE
        ):
            raise ValueError("Question normalized_score must be between 0 and 100.")
        if not _is_number(evaluation.weight):
            raise ValueError("Question weight must be numeric.")
        if evaluation.weight <= 0:
            raise ValueError("Question weight must be greater than 0.")


def _validate_non_empty_text(field_name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Question {field_name} must be a non-empty string.")


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)
