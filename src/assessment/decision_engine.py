from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from assessment.approved_dimension_aggregation_runtime import (
    ApprovedDimensionAggregationResult,
    aggregate_approved_dimensions,
)
from assessment.approved_dimension_weighting_runtime import (
    ApprovedDimensionWeightingResult,
    weight_approved_dimensions,
)
from assessment.approved_executive_summary_runtime import (
    ApprovedExecutiveSummaryResult,
    generate_approved_executive_summary,
)
from assessment.approved_confidence_runtime import (
    ApprovedConfidenceAssessmentResult,
    determine_approved_confidence,
)
from assessment.approved_methodology_runtime_config import (
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
)
from assessment.approved_overall_assessment_runtime import (
    ApprovedOverallAssessmentResult,
    calculate_approved_overall_assessment,
)
from assessment.approved_question_scoring_runtime import (
    ApprovedQuestionScore,
    ApprovedQuestionScoringResult,
    score_approved_questions,
)
from assessment.approved_readiness_runtime import (
    ApprovedReadinessAssessmentResult,
    determine_approved_readiness,
)
from assessment.approved_risk_runtime import (
    ApprovedRiskAssessmentResult,
    determine_approved_risk,
)
from assessment.approved_recommendation_runtime import (
    ApprovedRecommendationAssessmentResult,
    determine_approved_recommendation,
)
from assessment.approved_severity_runtime import (
    ApprovedSeverityAssessmentResult,
    READINESS_SEVERITY_DECISION_RULE_IDS,
    determine_approved_severity,
)
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
    validate_methodology_config(methodology_config)
    approved_scoring = score_approved_questions(
        answers,
        methodology_config.version,
    )
    approved_dimension_aggregation = aggregate_approved_dimensions(
        approved_scoring,
    )
    approved_dimension_weighting = weight_approved_dimensions(
        approved_dimension_aggregation,
    )
    approved_overall_assessment = calculate_approved_overall_assessment(
        approved_dimension_weighting,
    )
    approved_readiness = determine_approved_readiness(
        approved_overall_assessment,
    )
    approved_severity = determine_approved_severity(
        approved_readiness,
    )
    approved_risk = determine_approved_risk(
        approved_severity,
    )
    approved_confidence = determine_approved_confidence(
        approved_risk,
    )
    approved_recommendation = determine_approved_recommendation(
        approved_confidence,
    )
    approved_executive_summary = generate_approved_executive_summary(
        approved_recommendation,
    )
    question_evaluations = _build_question_evaluations_from_approved_scoring(
        approved_scoring,
        methodology_config,
    )
    _validate_approved_dimension_aggregation_alignment(
        approved_dimension_aggregation,
        question_evaluations,
    )
    _validate_approved_dimension_weighting_alignment(
        approved_dimension_weighting,
        approved_dimension_aggregation,
    )
    _validate_approved_overall_assessment_alignment(
        approved_overall_assessment,
        approved_dimension_weighting,
    )
    _validate_approved_readiness_alignment(
        approved_readiness,
        approved_overall_assessment,
    )
    _validate_approved_severity_alignment(
        approved_severity,
        approved_readiness,
    )
    _validate_approved_risk_alignment(
        approved_risk,
        approved_severity,
    )
    _validate_approved_confidence_alignment(
        approved_confidence,
        approved_risk,
    )
    _validate_approved_recommendation_alignment(
        approved_recommendation,
        approved_confidence,
    )
    _validate_approved_executive_summary_alignment(
        approved_executive_summary,
        approved_recommendation,
    )
    return _build_decision_result_with_approved_overall_score(
        question_evaluations,
        approved_overall_assessment,
    )


def build_question_evaluations(
    answers: Mapping[str, object],
    methodology_config: BusinessDecisionMethodologyConfig = (
        BUSINESS_DECISION_METHODOLOGY
    ),
) -> tuple[QuestionEvaluation, ...]:
    validate_methodology_config(methodology_config)
    approved_scoring = score_approved_questions(
        answers,
        methodology_config.version,
    )
    return _build_question_evaluations_from_approved_scoring(
        approved_scoring,
        methodology_config,
    )


def _build_question_evaluations_from_approved_scoring(
    approved_scoring: ApprovedQuestionScoringResult,
    methodology_config: BusinessDecisionMethodologyConfig,
) -> tuple[QuestionEvaluation, ...]:
    approved_scores = {
        question_score.question_id: question_score
        for question_score in approved_scoring.question_scores
    }

    return tuple(
        _build_question_evaluation_from_approved_score(
            question_id,
            approved_scores[question_id],
            methodology_config,
        )
        for question_id in sorted(methodology_config.questions)
    )


def _validate_approved_dimension_aggregation_alignment(
    approved_dimension_aggregation: ApprovedDimensionAggregationResult,
    question_evaluations: tuple[QuestionEvaluation, ...],
) -> None:
    question_scores = {
        evaluation.question_id: evaluation.normalized_score
        for evaluation in question_evaluations
    }
    aggregated_question_scores = {
        question_id: score
        for dimension in approved_dimension_aggregation.dimensions
        for question_id, score in dimension.contributing_scores.items()
    }

    if aggregated_question_scores != question_scores:
        raise ValueError("Approved dimension aggregation does not match question scores.")


def _validate_approved_dimension_weighting_alignment(
    approved_dimension_weighting: ApprovedDimensionWeightingResult,
    approved_dimension_aggregation: ApprovedDimensionAggregationResult,
) -> None:
    aggregated_scores = {
        dimension.dimension_id: dimension.score
        for dimension in approved_dimension_aggregation.dimensions
    }
    weighted_raw_scores = {
        dimension.dimension_id: dimension.raw_aggregated_score
        for dimension in approved_dimension_weighting.dimensions
    }

    if weighted_raw_scores != aggregated_scores:
        raise ValueError(
            "Approved dimension weighting does not match dimension aggregation."
        )


def _validate_approved_overall_assessment_alignment(
    approved_overall_assessment: ApprovedOverallAssessmentResult,
    approved_dimension_weighting: ApprovedDimensionWeightingResult,
) -> None:
    weighted_scores = {
        dimension.dimension_id: dimension.weighted_score
        for dimension in approved_dimension_weighting.dimensions
    }
    overall_contributions = {
        contribution.dimension_id: contribution.weighted_score
        for contribution in approved_overall_assessment.weighted_dimension_contributions
    }

    if overall_contributions != weighted_scores:
        raise ValueError(
            "Approved overall assessment does not match dimension weighting."
        )


def _build_decision_result_with_approved_overall_score(
    question_evaluations: tuple[QuestionEvaluation, ...],
    approved_overall_assessment: ApprovedOverallAssessmentResult,
) -> DecisionEvaluationResult:
    result = evaluate_decision(question_evaluations)
    return DecisionEvaluationResult(
        overall_score=approved_overall_assessment.overall_assessment_score,
        total_weight=result.total_weight,
        question_count=result.question_count,
        dimensions=result.dimensions,
        explanation=result.explanation,
    )


def _validate_approved_readiness_alignment(
    approved_readiness: ApprovedReadinessAssessmentResult,
    approved_overall_assessment: ApprovedOverallAssessmentResult,
) -> None:
    if (
        approved_readiness.readiness_score
        != approved_overall_assessment.overall_assessment_score
    ):
        raise ValueError(
            "Approved readiness does not match overall assessment score."
        )

    lower_matches = (
        approved_readiness.readiness_score
        >= approved_readiness.threshold_lower_bound
        if approved_readiness.threshold_lower_inclusive
        else approved_readiness.readiness_score
        > approved_readiness.threshold_lower_bound
    )
    upper_matches = (
        approved_readiness.readiness_score
        <= approved_readiness.threshold_upper_bound
        if approved_readiness.threshold_upper_inclusive
        else approved_readiness.readiness_score
        < approved_readiness.threshold_upper_bound
    )

    if not (lower_matches and upper_matches):
        raise ValueError(
            "Approved readiness classification does not match threshold range."
        )


def _validate_approved_severity_alignment(
    approved_severity: ApprovedSeverityAssessmentResult,
    approved_readiness: ApprovedReadinessAssessmentResult,
) -> None:
    if (
        approved_severity.readiness_classification
        != approved_readiness.readiness_classification
        or approved_severity.readiness_score != approved_readiness.readiness_score
    ):
        raise ValueError("Approved severity does not match readiness result.")

    expected_rule_id = READINESS_SEVERITY_DECISION_RULE_IDS[
        approved_readiness.readiness_threshold_id
    ]
    if approved_severity.severity_decision_identifier != expected_rule_id:
        raise ValueError(
            "Approved severity decision does not match readiness threshold."
        )


def _validate_approved_risk_alignment(
    approved_risk: ApprovedRiskAssessmentResult,
    approved_severity: ApprovedSeverityAssessmentResult,
) -> None:
    try:
        expected_risk_rule = (
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.risk_decision_rules[
                approved_risk.risk_decision_identifier
            ]
        )
    except KeyError as exc:
        raise ValueError(
            "Approved risk decision does not match approved risk decision tables."
        ) from exc

    if (
        approved_risk.risk_decision_table_version
        != expected_risk_rule.table_version
        or approved_risk.risk_classification != expected_risk_rule.output
    ):
        raise ValueError(
            "Approved risk classification does not match approved risk decision table."
        )
    if approved_risk.severity_classifications != (
        approved_severity.severity_classification,
    ):
        raise ValueError("Approved risk does not match severity result.")
    if (
        approved_risk.readiness_classification
        != approved_severity.readiness_classification
        or approved_risk.overall_assessment_score
        != approved_severity.readiness_score
    ):
        raise ValueError("Approved risk does not match severity context.")


def _validate_approved_confidence_alignment(
    approved_confidence: ApprovedConfidenceAssessmentResult,
    approved_risk: ApprovedRiskAssessmentResult,
) -> None:
    try:
        expected_confidence_rule = (
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.confidence_decision_rules[
                approved_confidence.confidence_decision_identifier
            ]
        )
    except KeyError as exc:
        raise ValueError(
            "Approved confidence decision does not match approved confidence "
            "decision tables."
        ) from exc

    if (
        approved_confidence.confidence_decision_table_version
        != expected_confidence_rule.table_version
        or approved_confidence.confidence_classification
        != expected_confidence_rule.output
    ):
        raise ValueError(
            "Approved confidence classification does not match approved "
            "confidence decision table."
        )
    if (
        approved_confidence.risk_classification
        != approved_risk.risk_classification
        or approved_confidence.severity_classifications
        != approved_risk.severity_classifications
        or approved_confidence.readiness_classification
        != approved_risk.readiness_classification
        or approved_confidence.overall_assessment_score
        != approved_risk.overall_assessment_score
    ):
        raise ValueError("Approved confidence does not match risk result.")


def _validate_approved_recommendation_alignment(
    approved_recommendation: ApprovedRecommendationAssessmentResult,
    approved_confidence: ApprovedConfidenceAssessmentResult,
) -> None:
    try:
        expected_recommendation_rule = (
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.recommendation_decision_rules[
                approved_recommendation.recommendation_decision_identifier
            ]
        )
    except KeyError as exc:
        raise ValueError(
            "Approved recommendation decision does not match approved "
            "recommendation decision tables."
        ) from exc

    if (
        approved_recommendation.recommendation_decision_table_version
        != expected_recommendation_rule.table_version
        or approved_recommendation.recommendation_classification
        != expected_recommendation_rule.output
    ):
        raise ValueError(
            "Approved recommendation classification does not match approved "
            "recommendation decision table."
        )
    if (
        approved_recommendation.confidence_classification
        != approved_confidence.confidence_classification
        or approved_recommendation.risk_classification
        != approved_confidence.risk_classification
        or approved_recommendation.severity_classification
        != approved_confidence.severity_classifications[0]
        or approved_recommendation.readiness_classification
        != approved_confidence.readiness_classification
        or approved_recommendation.overall_assessment_score
        != approved_confidence.overall_assessment_score
    ):
        raise ValueError("Approved recommendation does not match confidence result.")


def _validate_approved_executive_summary_alignment(
    approved_executive_summary: ApprovedExecutiveSummaryResult,
    approved_recommendation: ApprovedRecommendationAssessmentResult,
) -> None:
    if not isinstance(approved_executive_summary, ApprovedExecutiveSummaryResult):
        raise ValueError(
            "Approved Executive Summary Runtime did not produce an approved "
            "Executive Summary artifact."
        )
    if (
        approved_executive_summary.recommendation_classification
        != approved_recommendation.recommendation_classification
        or approved_executive_summary.confidence_classification
        != approved_recommendation.confidence_classification
        or approved_executive_summary.risk_classification
        != approved_recommendation.risk_classification
        or approved_executive_summary.severity_classification
        != approved_recommendation.severity_classification
        or approved_executive_summary.readiness_classification
        != approved_recommendation.readiness_classification
        or approved_executive_summary.overall_assessment_score
        != approved_recommendation.overall_assessment_score
        or approved_executive_summary.methodology_version
        != approved_recommendation.methodology_version
        or approved_executive_summary.runtime_config_version
        != approved_recommendation.runtime_config_version
    ):
        raise ValueError(
            "Approved Executive Summary does not match recommendation result."
        )

    expected_section_ids = tuple(
        APPROVED_METHODOLOGY_RUNTIME_CONFIG.executive_summary_sections
    )
    observed_section_ids = tuple(
        section.section_id
        for section in approved_executive_summary.sections
    )
    if observed_section_ids != expected_section_ids:
        raise ValueError(
            "Approved Executive Summary sections do not match approved templates."
        )

    for section in approved_executive_summary.sections:
        expected_section = (
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.executive_summary_sections[
                section.section_id
            ]
        )
        if (
            section.heading != expected_section.heading
            or section.section_order != expected_section.order
            or section.template_id != expected_section.template_id
            or section.template_version != expected_section.template_version
        ):
            raise ValueError(
                "Approved Executive Summary section does not match approved "
                "template configuration."
            )


def _build_question_evaluation_from_approved_score(
    question_id: str,
    approved_score: ApprovedQuestionScore,
    methodology_config: BusinessDecisionMethodologyConfig,
) -> QuestionEvaluation:
    question = load_question_definition(question_id, methodology_config)

    if approved_score.question_id != question.id:
        raise ValueError(f"Approved question score mismatch: {question_id}")

    return QuestionEvaluation(
        question_id=question.id,
        readiness_dimension=question.readiness_dimension,
        normalized_score=approved_score.score,
        weight=methodology_config.placeholder_question_weights[question.id],
        evidence_category=question.evidence_category,
        weight_category=question.weight_category,
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
