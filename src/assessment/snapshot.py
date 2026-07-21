from dataclasses import dataclass
from typing import Any, Mapping

from assessment.decision_engine import (
    DecisionEvaluationResult,
    DimensionEvaluation,
)
from assessment.methodology_config import (
    BUSINESS_DECISION_METHODOLOGY,
    BusinessDecisionMethodologyConfig,
    validate_methodology_config,
)


@dataclass(frozen=True)
class OverallReadinessSnapshot:
    score: float
    contributing_dimensions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "contributingDimensions": list(self.contributing_dimensions),
        }


@dataclass(frozen=True)
class DomainReadinessSnapshot:
    domain_id: str
    label: str
    score: float
    question_count: int
    total_weight: float
    contributing_questions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "domainId": self.domain_id,
            "label": self.label,
            "score": self.score,
            "questionCount": self.question_count,
            "totalWeight": self.total_weight,
            "contributingQuestions": list(self.contributing_questions),
        }


@dataclass(frozen=True)
class SnapshotAudit:
    methodology_version: str
    evaluated_dimensions: tuple[str, ...]
    question_count: int
    total_weight: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "methodologyVersion": self.methodology_version,
            "evaluatedDimensions": list(self.evaluated_dimensions),
            "questionCount": self.question_count,
            "totalWeight": self.total_weight,
        }


@dataclass(frozen=True)
class BusinessReadinessSnapshot:
    assessment_version: str
    overall_readiness: OverallReadinessSnapshot
    domains: tuple[DomainReadinessSnapshot, ...]
    audit: SnapshotAudit

    def to_dict(self) -> dict[str, Any]:
        return {
            "assessmentVersion": self.assessment_version,
            "overallReadiness": self.overall_readiness.to_dict(),
            "domains": [
                domain.to_dict()
                for domain in self.domains
            ],
            "audit": self.audit.to_dict(),
        }


def build_business_readiness_snapshot(
    assessment_version: str,
    evaluation: DecisionEvaluationResult,
    methodology_config: BusinessDecisionMethodologyConfig = (
        BUSINESS_DECISION_METHODOLOGY
    ),
) -> BusinessReadinessSnapshot:
    validate_methodology_config(methodology_config)
    _validate_assessment_version(assessment_version)
    _validate_evaluation_explanation(evaluation)
    _validate_dimensions(evaluation.dimensions, methodology_config)

    domains = tuple(
        _build_domain_snapshot(
            dimension_id,
            dimension,
            methodology_config,
        )
        for dimension_id, dimension in sorted(evaluation.dimensions.items())
    )
    evaluated_dimensions = tuple(domain.domain_id for domain in domains)

    return BusinessReadinessSnapshot(
        assessment_version=assessment_version,
        overall_readiness=OverallReadinessSnapshot(
            score=evaluation.overall_score,
            contributing_dimensions=evaluated_dimensions,
        ),
        domains=domains,
        audit=SnapshotAudit(
            methodology_version=methodology_config.version,
            evaluated_dimensions=evaluated_dimensions,
            question_count=evaluation.question_count,
            total_weight=evaluation.total_weight,
        ),
    )


def _build_domain_snapshot(
    dimension_id: str,
    dimension: DimensionEvaluation,
    methodology_config: BusinessDecisionMethodologyConfig,
) -> DomainReadinessSnapshot:
    dimension_config = methodology_config.readiness_dimensions[dimension_id]

    return DomainReadinessSnapshot(
        domain_id=dimension_id,
        label=dimension_config.label,
        score=dimension.normalized_score,
        question_count=dimension.question_count,
        total_weight=dimension.total_weight,
        contributing_questions=dimension.contributing_questions,
    )


def _validate_assessment_version(assessment_version: str) -> None:
    if not isinstance(assessment_version, str) or not assessment_version.strip():
        raise ValueError("Assessment version must be a non-empty string.")


def _validate_evaluation_explanation(evaluation: DecisionEvaluationResult) -> None:
    if evaluation.explanation is None:
        raise ValueError("Evaluation explanation is required.")

    evaluated_dimensions = tuple(sorted(evaluation.dimensions))
    if evaluation.explanation.evaluated_dimensions != evaluated_dimensions:
        raise ValueError("Evaluation explanation dimensions do not match evaluation.")

    for dimension_id, dimension in evaluation.dimensions.items():
        try:
            dimension_explanation = evaluation.explanation.dimension_explanations[
                dimension_id
            ]
        except KeyError as exc:
            raise ValueError(
                f"Missing dimension explanation: {dimension_id}"
            ) from exc

        if dimension_explanation.contributing_questions != (
            dimension.contributing_questions
        ):
            raise ValueError(
                f"Dimension explanation does not match evaluation: {dimension_id}"
            )


def _validate_dimensions(
    dimensions: Mapping[str, DimensionEvaluation],
    methodology_config: BusinessDecisionMethodologyConfig,
) -> None:
    for dimension_id in dimensions:
        if dimension_id not in methodology_config.readiness_dimensions:
            raise ValueError(f"Unknown readiness dimension: {dimension_id}")
