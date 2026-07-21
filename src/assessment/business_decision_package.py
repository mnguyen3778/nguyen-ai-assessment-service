from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from assessment.confidence import ConfidenceEvaluation
from assessment.decision_engine import (
    DecisionEvaluationResult,
    DimensionEvaluation,
    DimensionExplanation,
    EvaluationExplanation,
    QuestionExplanation,
)
from assessment.executive_summary import ExecutiveSummaryFoundation
from assessment.recommendation_priority import RecommendationPriorityEvaluation
from assessment.snapshot import BusinessReadinessSnapshot


BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION = "business-decision-package-v1"
BUSINESS_DECISION_PACKAGE_LIMITATIONS = (
    "final-confidence-formulas-not-implemented",
    "final-confidence-level-assignment-not-implemented",
    "final-recommendation-assignment-not-implemented",
    "recommendation-generation-not-implemented",
    "service-decisions-not-implemented",
    "executive-reporting-not-implemented",
    "executive-narratives-not-implemented",
    "evidence-ingestion-not-implemented",
    "persistence-not-implemented",
    "api-exposure-of-snapshot-consumers-not-implemented",
)
BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS = MappingProxyType(
    {
        "decisionEvaluation": "assessment-decision-engine-v2",
        "businessReadinessSnapshot": "sprint3-snapshot-foundation-v1",
        "confidenceEvaluation": "sprint3-confidence-foundation-v1",
        "recommendationPriorityEvaluation": (
            "sprint3-recommendation-priority-foundation-v1"
        ),
        "executiveSummaryFoundation": "sprint3-executive-summary-foundation-v1",
    }
)
BUSINESS_DECISION_PACKAGE_SOURCE_COMPONENTS = tuple(
    BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS
)


@dataclass(frozen=True)
class BusinessDecisionPackageAudit:
    assessment_version: str
    methodology_version: str
    source_component_ids: tuple[str, ...]
    evaluated_dimensions: tuple[str, ...]
    question_count: int
    total_weight: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "assessmentVersion": self.assessment_version,
            "methodologyVersion": self.methodology_version,
            "sourceComponentIds": list(self.source_component_ids),
            "evaluatedDimensions": list(self.evaluated_dimensions),
            "questionCount": self.question_count,
            "totalWeight": self.total_weight,
        }


@dataclass(frozen=True)
class BusinessDecisionPackageVersionMetadata:
    contract_version: str
    assessment_version: str
    methodology_version: str
    component_versions: Mapping[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "contractVersion": self.contract_version,
            "assessmentVersion": self.assessment_version,
            "methodologyVersion": self.methodology_version,
            "componentVersions": {
                component_id: self.component_versions[component_id]
                for component_id in self.component_versions
            },
        }


@dataclass(frozen=True)
class BusinessDecisionPackage:
    decision_evaluation: DecisionEvaluationResult
    business_readiness_snapshot: BusinessReadinessSnapshot
    confidence_evaluation: ConfidenceEvaluation
    recommendation_priority_evaluation: RecommendationPriorityEvaluation
    executive_summary_foundation: ExecutiveSummaryFoundation
    audit: BusinessDecisionPackageAudit
    limitations: tuple[str, ...]
    version_metadata: BusinessDecisionPackageVersionMetadata

    def to_dict(self) -> dict[str, Any]:
        return {
            "decisionEvaluation": _decision_evaluation_to_dict(
                self.decision_evaluation
            ),
            "businessReadinessSnapshot": self.business_readiness_snapshot.to_dict(),
            "confidenceEvaluation": self.confidence_evaluation.to_dict(),
            "recommendationPriorityEvaluation": (
                self.recommendation_priority_evaluation.to_dict()
            ),
            "executiveSummaryFoundation": (
                self.executive_summary_foundation.to_dict()
            ),
            "audit": self.audit.to_dict(),
            "limitations": list(self.limitations),
            "versionMetadata": self.version_metadata.to_dict(),
        }


def build_business_decision_package(
    decision_evaluation: DecisionEvaluationResult,
    business_readiness_snapshot: BusinessReadinessSnapshot,
    confidence_evaluation: ConfidenceEvaluation,
    recommendation_priority_evaluation: RecommendationPriorityEvaluation,
    executive_summary_foundation: ExecutiveSummaryFoundation,
) -> BusinessDecisionPackage:
    _validate_sources(
        decision_evaluation,
        business_readiness_snapshot,
        confidence_evaluation,
        recommendation_priority_evaluation,
        executive_summary_foundation,
    )

    assessment_version = business_readiness_snapshot.assessment_version
    methodology_version = business_readiness_snapshot.audit.methodology_version

    return BusinessDecisionPackage(
        decision_evaluation=decision_evaluation,
        business_readiness_snapshot=business_readiness_snapshot,
        confidence_evaluation=confidence_evaluation,
        recommendation_priority_evaluation=recommendation_priority_evaluation,
        executive_summary_foundation=executive_summary_foundation,
        audit=BusinessDecisionPackageAudit(
            assessment_version=assessment_version,
            methodology_version=methodology_version,
            source_component_ids=BUSINESS_DECISION_PACKAGE_SOURCE_COMPONENTS,
            evaluated_dimensions=business_readiness_snapshot.audit.evaluated_dimensions,
            question_count=business_readiness_snapshot.audit.question_count,
            total_weight=business_readiness_snapshot.audit.total_weight,
        ),
        limitations=BUSINESS_DECISION_PACKAGE_LIMITATIONS,
        version_metadata=BusinessDecisionPackageVersionMetadata(
            contract_version=BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
            assessment_version=assessment_version,
            methodology_version=methodology_version,
            component_versions=BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS,
        ),
    )


def _validate_sources(
    decision_evaluation: DecisionEvaluationResult,
    business_readiness_snapshot: BusinessReadinessSnapshot,
    confidence_evaluation: ConfidenceEvaluation,
    recommendation_priority_evaluation: RecommendationPriorityEvaluation,
    executive_summary_foundation: ExecutiveSummaryFoundation,
) -> None:
    assessment_versions = {
        business_readiness_snapshot.assessment_version,
        confidence_evaluation.assessment_version,
        recommendation_priority_evaluation.assessment_version,
        executive_summary_foundation.assessment_version,
    }
    if len(assessment_versions) != 1:
        raise ValueError("Business decision package assessment versions do not match.")

    methodology_versions = {
        business_readiness_snapshot.audit.methodology_version,
        confidence_evaluation.methodology_version,
        recommendation_priority_evaluation.methodology_version,
        executive_summary_foundation.methodology_version,
    }
    if len(methodology_versions) != 1:
        raise ValueError("Business decision package methodology versions do not match.")

    _validate_decision_evaluation_snapshot_alignment(
        decision_evaluation,
        business_readiness_snapshot,
    )


def _validate_decision_evaluation_snapshot_alignment(
    decision_evaluation: DecisionEvaluationResult,
    business_readiness_snapshot: BusinessReadinessSnapshot,
) -> None:
    if (
        decision_evaluation.overall_score
        != business_readiness_snapshot.overall_readiness.score
    ):
        raise ValueError("Decision evaluation score does not match snapshot.")

    if decision_evaluation.question_count != (
        business_readiness_snapshot.audit.question_count
    ):
        raise ValueError(
            "Decision evaluation question count does not match snapshot audit."
        )

    if decision_evaluation.total_weight != business_readiness_snapshot.audit.total_weight:
        raise ValueError(
            "Decision evaluation total weight does not match snapshot audit."
        )

    evaluated_dimensions = tuple(sorted(decision_evaluation.dimensions))
    if evaluated_dimensions != business_readiness_snapshot.audit.evaluated_dimensions:
        raise ValueError(
            "Decision evaluation dimensions do not match snapshot audit."
        )


def _decision_evaluation_to_dict(
    evaluation: DecisionEvaluationResult,
) -> dict[str, Any]:
    return {
        "overallScore": evaluation.overall_score,
        "totalWeight": evaluation.total_weight,
        "questionCount": evaluation.question_count,
        "dimensions": {
            dimension_id: _dimension_evaluation_to_dict(dimension)
            for dimension_id, dimension in sorted(evaluation.dimensions.items())
        },
        "explanation": (
            _evaluation_explanation_to_dict(evaluation.explanation)
            if evaluation.explanation is not None
            else None
        ),
    }


def _dimension_evaluation_to_dict(
    dimension: DimensionEvaluation,
) -> dict[str, Any]:
    return {
        "dimensionId": dimension.dimension_id,
        "normalizedScore": dimension.normalized_score,
        "totalWeight": dimension.total_weight,
        "questionCount": dimension.question_count,
        "contributingQuestions": list(dimension.contributing_questions),
    }


def _evaluation_explanation_to_dict(
    explanation: EvaluationExplanation,
) -> dict[str, Any]:
    return {
        "evaluatedDimensions": list(explanation.evaluated_dimensions),
        "contributingQuestions": list(explanation.contributing_questions),
        "appliedWeights": {
            question_id: explanation.applied_weights[question_id]
            for question_id in sorted(explanation.applied_weights)
        },
        "questionExplanations": {
            question_id: _question_explanation_to_dict(question_explanation)
            for question_id, question_explanation in sorted(
                explanation.question_explanations.items()
            )
        },
        "dimensionExplanations": {
            dimension_id: _dimension_explanation_to_dict(dimension_explanation)
            for dimension_id, dimension_explanation in sorted(
                explanation.dimension_explanations.items()
            )
        },
    }


def _question_explanation_to_dict(
    explanation: QuestionExplanation,
) -> dict[str, Any]:
    return {
        "questionId": explanation.question_id,
        "readinessDimension": explanation.readiness_dimension,
        "evidenceCategory": explanation.evidence_category,
        "weightCategory": explanation.weight_category,
        "appliedWeight": explanation.applied_weight,
        "normalizedScore": explanation.normalized_score,
    }


def _dimension_explanation_to_dict(
    explanation: DimensionExplanation,
) -> dict[str, Any]:
    return {
        "dimensionId": explanation.dimension_id,
        "contributingQuestions": list(explanation.contributing_questions),
        "appliedWeights": {
            question_id: explanation.applied_weights[question_id]
            for question_id in sorted(explanation.applied_weights)
        },
        "normalizedScore": explanation.normalized_score,
        "totalWeight": explanation.total_weight,
    }
