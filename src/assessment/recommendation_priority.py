from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from assessment.confidence import ConfidenceEvaluation
from assessment.methodology_config import (
    BUSINESS_DECISION_METHODOLOGY,
    BusinessDecisionMethodologyConfig,
    RecommendationPriorityConfig,
    RecommendationPriorityFactorConfig,
    validate_methodology_config,
)
from assessment.snapshot import BusinessReadinessSnapshot


NOT_EVALUATED_STATUS = "not-evaluated"
PRIORITY_FOUNDATION_LIMITATION = (
    "Executable recommendation priority formulas and recommendation targets "
    "are not yet approved for this foundation."
)


@dataclass(frozen=True)
class RecommendationPriorityFactorEvaluation:
    factor_id: str
    label: str
    status: str
    snapshot_source_refs: tuple[str, ...] = ()
    confidence_source_refs: tuple[str, ...] = ()
    limitation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "factorId": self.factor_id,
            "label": self.label,
            "status": self.status,
            "snapshotSourceRefs": list(self.snapshot_source_refs),
            "confidenceSourceRefs": list(self.confidence_source_refs),
            "limitation": self.limitation,
        }


@dataclass(frozen=True)
class RecommendationPriorityEvaluation:
    assessment_version: str
    methodology_version: str
    configured_priority_levels: Mapping[str, RecommendationPriorityConfig]
    configured_priority_factors: Mapping[str, RecommendationPriorityFactorEvaluation]
    evaluated_factor_ids: tuple[str, ...]
    not_evaluated_factor_ids: tuple[str, ...]
    source_snapshot_metadata: Mapping[str, Any]
    source_confidence_metadata: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "assessmentVersion": self.assessment_version,
            "methodologyVersion": self.methodology_version,
            "configuredPriorityLevels": {
                priority_id: _priority_level_to_dict(priority)
                for priority_id, priority in self.configured_priority_levels.items()
            },
            "configuredPriorityFactors": {
                factor_id: factor.to_dict()
                for factor_id, factor in self.configured_priority_factors.items()
            },
            "evaluatedFactorIds": list(self.evaluated_factor_ids),
            "notEvaluatedFactorIds": list(self.not_evaluated_factor_ids),
            "sourceSnapshotMetadata": _metadata_to_dict(
                self.source_snapshot_metadata,
            ),
            "sourceConfidenceMetadata": _metadata_to_dict(
                self.source_confidence_metadata,
            ),
        }


def build_recommendation_priority_evaluation(
    snapshot: BusinessReadinessSnapshot,
    confidence: ConfidenceEvaluation,
    methodology_config: BusinessDecisionMethodologyConfig = (
        BUSINESS_DECISION_METHODOLOGY
    ),
) -> RecommendationPriorityEvaluation:
    validate_methodology_config(methodology_config)
    _validate_sources(snapshot, confidence, methodology_config)

    factors = {
        factor_id: _build_factor_evaluation(
            factor,
            snapshot,
            confidence,
        )
        for factor_id, factor in sorted(
            methodology_config.recommendation_priority_factors.items()
        )
    }

    return RecommendationPriorityEvaluation(
        assessment_version=snapshot.assessment_version,
        methodology_version=snapshot.audit.methodology_version,
        configured_priority_levels=MappingProxyType(
            {
                priority.id: priority
                for priority in sorted(
                    methodology_config.recommendation_priorities.values(),
                    key=lambda priority: priority.rank,
                )
            }
        ),
        configured_priority_factors=MappingProxyType(factors),
        evaluated_factor_ids=(),
        not_evaluated_factor_ids=tuple(factors),
        source_snapshot_metadata=MappingProxyType(
            {
                "assessmentVersion": snapshot.assessment_version,
                "methodologyVersion": snapshot.audit.methodology_version,
                "overallReadinessScore": snapshot.overall_readiness.score,
                "evaluatedDimensions": snapshot.audit.evaluated_dimensions,
                "questionCount": snapshot.audit.question_count,
                "totalWeight": snapshot.audit.total_weight,
            }
        ),
        source_confidence_metadata=MappingProxyType(
            {
                "assessmentVersion": confidence.assessment_version,
                "methodologyVersion": confidence.methodology_version,
                "evaluatedFactorIds": confidence.evaluated_factor_ids,
                "notEvaluatedFactorIds": confidence.not_evaluated_factor_ids,
            }
        ),
    )


def _build_factor_evaluation(
    factor: RecommendationPriorityFactorConfig,
    snapshot: BusinessReadinessSnapshot,
    confidence: ConfidenceEvaluation,
) -> RecommendationPriorityFactorEvaluation:
    return RecommendationPriorityFactorEvaluation(
        factor_id=factor.id,
        label=factor.label,
        status=NOT_EVALUATED_STATUS,
        snapshot_source_refs=_snapshot_source_refs(snapshot),
        confidence_source_refs=_confidence_source_refs(confidence),
        limitation=PRIORITY_FOUNDATION_LIMITATION,
    )


def _snapshot_source_refs(
    snapshot: BusinessReadinessSnapshot,
) -> tuple[str, ...]:
    return (
        "snapshot.overallReadiness",
        "snapshot.audit",
        *(
            f"snapshot.domains.{domain.domain_id}"
            for domain in snapshot.domains
        ),
    )


def _confidence_source_refs(
    confidence: ConfidenceEvaluation,
) -> tuple[str, ...]:
    return tuple(
        f"confidence.factors.{factor_id}"
        for factor_id in sorted(confidence.factors)
    )


def _validate_sources(
    snapshot: BusinessReadinessSnapshot,
    confidence: ConfidenceEvaluation,
    methodology_config: BusinessDecisionMethodologyConfig,
) -> None:
    if snapshot.assessment_version != confidence.assessment_version:
        raise ValueError("Snapshot and confidence assessment versions do not match.")

    if snapshot.audit.methodology_version != confidence.methodology_version:
        raise ValueError("Snapshot and confidence methodology versions do not match.")

    if snapshot.audit.methodology_version != methodology_config.version:
        raise ValueError("Snapshot methodology version does not match configuration.")

    unknown_confidence_factors = set(confidence.factors) - set(
        methodology_config.confidence_factors
    )
    if unknown_confidence_factors:
        raise ValueError(
            "Unknown confidence factor: "
            f"{sorted(unknown_confidence_factors)[0]}"
        )

    expected_confidence_factors = set(methodology_config.confidence_factors)
    observed_confidence_factors = set(confidence.factors)
    if observed_confidence_factors != expected_confidence_factors:
        missing_factor = sorted(
            expected_confidence_factors - observed_confidence_factors
        )[0]
        raise ValueError(f"Missing confidence factor: {missing_factor}")


def _priority_level_to_dict(
    priority: RecommendationPriorityConfig,
) -> dict[str, Any]:
    return {
        "priorityId": priority.id,
        "label": priority.label,
        "rank": priority.rank,
    }


def _metadata_to_dict(metadata: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: list(value) if isinstance(value, tuple) else value
        for key, value in metadata.items()
    }
