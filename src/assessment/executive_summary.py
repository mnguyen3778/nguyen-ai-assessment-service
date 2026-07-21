from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from assessment.confidence import ConfidenceEvaluation
from assessment.methodology_config import (
    BUSINESS_DECISION_METHODOLOGY,
    BusinessDecisionMethodologyConfig,
    ExecutiveSummarySectionConfig,
    validate_methodology_config,
)
from assessment.recommendation_priority import RecommendationPriorityEvaluation
from assessment.snapshot import BusinessReadinessSnapshot


NOT_EVALUATED_STATUS = "not-evaluated"
EXECUTIVE_SUMMARY_FOUNDATION_LIMITATION = (
    "Narrative generation, executive reporting rules, recommendation "
    "generation, and service decisions are not yet approved for this "
    "foundation."
)


@dataclass(frozen=True)
class ExecutiveSummarySectionEvaluation:
    section_id: str
    label: str
    status: str
    snapshot_source_refs: tuple[str, ...] = ()
    confidence_source_refs: tuple[str, ...] = ()
    priority_source_refs: tuple[str, ...] = ()
    limitation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "sectionId": self.section_id,
            "label": self.label,
            "status": self.status,
            "snapshotSourceRefs": list(self.snapshot_source_refs),
            "confidenceSourceRefs": list(self.confidence_source_refs),
            "prioritySourceRefs": list(self.priority_source_refs),
            "limitation": self.limitation,
        }


@dataclass(frozen=True)
class ExecutiveSummaryFoundation:
    assessment_version: str
    methodology_version: str
    configured_summary_sections: Mapping[str, ExecutiveSummarySectionEvaluation]
    evaluated_section_ids: tuple[str, ...]
    not_evaluated_section_ids: tuple[str, ...]
    source_snapshot_metadata: Mapping[str, Any]
    source_confidence_metadata: Mapping[str, Any]
    source_priority_metadata: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "assessmentVersion": self.assessment_version,
            "methodologyVersion": self.methodology_version,
            "configuredSummarySections": {
                section_id: section.to_dict()
                for section_id, section in self.configured_summary_sections.items()
            },
            "evaluatedSectionIds": list(self.evaluated_section_ids),
            "notEvaluatedSectionIds": list(self.not_evaluated_section_ids),
            "sourceSnapshotMetadata": _metadata_to_dict(
                self.source_snapshot_metadata,
            ),
            "sourceConfidenceMetadata": _metadata_to_dict(
                self.source_confidence_metadata,
            ),
            "sourcePriorityMetadata": _metadata_to_dict(
                self.source_priority_metadata,
            ),
        }


def build_executive_summary_foundation(
    snapshot: BusinessReadinessSnapshot,
    confidence: ConfidenceEvaluation,
    priority: RecommendationPriorityEvaluation,
    methodology_config: BusinessDecisionMethodologyConfig = (
        BUSINESS_DECISION_METHODOLOGY
    ),
) -> ExecutiveSummaryFoundation:
    validate_methodology_config(methodology_config)
    _validate_sources(snapshot, confidence, priority, methodology_config)

    sections = {
        section_id: _build_section_evaluation(
            section,
            snapshot,
            confidence,
            priority,
        )
        for section_id, section in sorted(
            methodology_config.executive_summary_sections.items()
        )
    }

    return ExecutiveSummaryFoundation(
        assessment_version=snapshot.assessment_version,
        methodology_version=snapshot.audit.methodology_version,
        configured_summary_sections=MappingProxyType(sections),
        evaluated_section_ids=(),
        not_evaluated_section_ids=tuple(sections),
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
        source_priority_metadata=MappingProxyType(
            {
                "assessmentVersion": priority.assessment_version,
                "methodologyVersion": priority.methodology_version,
                "configuredPriorityLevelIds": tuple(
                    priority.configured_priority_levels
                ),
                "configuredPriorityFactorIds": tuple(
                    priority.configured_priority_factors
                ),
                "evaluatedFactorIds": priority.evaluated_factor_ids,
                "notEvaluatedFactorIds": priority.not_evaluated_factor_ids,
            }
        ),
    )


def _build_section_evaluation(
    section: ExecutiveSummarySectionConfig,
    snapshot: BusinessReadinessSnapshot,
    confidence: ConfidenceEvaluation,
    priority: RecommendationPriorityEvaluation,
) -> ExecutiveSummarySectionEvaluation:
    return ExecutiveSummarySectionEvaluation(
        section_id=section.id,
        label=section.label,
        status=NOT_EVALUATED_STATUS,
        snapshot_source_refs=_snapshot_source_refs(snapshot),
        confidence_source_refs=_confidence_source_refs(confidence),
        priority_source_refs=_priority_source_refs(priority),
        limitation=EXECUTIVE_SUMMARY_FOUNDATION_LIMITATION,
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


def _priority_source_refs(
    priority: RecommendationPriorityEvaluation,
) -> tuple[str, ...]:
    return (
        "priority.configuredPriorityLevels",
        *(
            f"priority.configuredPriorityFactors.{factor_id}"
            for factor_id in sorted(priority.configured_priority_factors)
        ),
    )


def _validate_sources(
    snapshot: BusinessReadinessSnapshot,
    confidence: ConfidenceEvaluation,
    priority: RecommendationPriorityEvaluation,
    methodology_config: BusinessDecisionMethodologyConfig,
) -> None:
    assessment_versions = {
        snapshot.assessment_version,
        confidence.assessment_version,
        priority.assessment_version,
    }
    if len(assessment_versions) != 1:
        raise ValueError(
            "Snapshot, confidence, and priority assessment versions do not match."
        )

    methodology_versions = {
        snapshot.audit.methodology_version,
        confidence.methodology_version,
        priority.methodology_version,
    }
    if len(methodology_versions) != 1:
        raise ValueError(
            "Snapshot, confidence, and priority methodology versions do not match."
        )

    if snapshot.audit.methodology_version != methodology_config.version:
        raise ValueError("Snapshot methodology version does not match configuration.")


def _metadata_to_dict(metadata: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: list(value) if isinstance(value, tuple) else value
        for key, value in metadata.items()
    }
