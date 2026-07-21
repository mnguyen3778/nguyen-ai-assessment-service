from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from assessment.methodology_config import (
    BUSINESS_DECISION_METHODOLOGY,
    BusinessDecisionMethodologyConfig,
    ConfidenceFactorConfig,
    validate_methodology_config,
)
from assessment.snapshot import BusinessReadinessSnapshot


EVALUATED_STATUS = "evaluated"
NOT_EVALUATED_STATUS = "not-evaluated"


@dataclass(frozen=True)
class ConfidenceFactorEvaluation:
    factor_id: str
    label: str
    status: str
    observed_count: int | None = None
    expected_count: int | None = None
    coverage_ratio: float | None = None
    question_refs: tuple[str, ...] = ()
    dimension_refs: tuple[str, ...] = ()
    evidence_categories: tuple[str, ...] = ()
    limitation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "factorId": self.factor_id,
            "label": self.label,
            "status": self.status,
            "observedCount": self.observed_count,
            "expectedCount": self.expected_count,
            "coverageRatio": self.coverage_ratio,
            "questionRefs": list(self.question_refs),
            "dimensionRefs": list(self.dimension_refs),
            "evidenceCategories": list(self.evidence_categories),
            "limitation": self.limitation,
        }


@dataclass(frozen=True)
class ConfidenceEvaluation:
    assessment_version: str
    methodology_version: str
    factors: Mapping[str, ConfidenceFactorEvaluation]
    evaluated_factor_ids: tuple[str, ...]
    not_evaluated_factor_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "assessmentVersion": self.assessment_version,
            "methodologyVersion": self.methodology_version,
            "factors": {
                factor_id: factor.to_dict()
                for factor_id, factor in self.factors.items()
            },
            "evaluatedFactorIds": list(self.evaluated_factor_ids),
            "notEvaluatedFactorIds": list(self.not_evaluated_factor_ids),
        }


def build_confidence_evaluation(
    snapshot: BusinessReadinessSnapshot,
    methodology_config: BusinessDecisionMethodologyConfig = (
        BUSINESS_DECISION_METHODOLOGY
    ),
) -> ConfidenceEvaluation:
    validate_methodology_config(methodology_config)
    _validate_snapshot_methodology(snapshot, methodology_config)

    factors = {
        factor_id: _build_factor_evaluation(
            factor,
            snapshot,
            methodology_config,
        )
        for factor_id, factor in sorted(methodology_config.confidence_factors.items())
    }

    return ConfidenceEvaluation(
        assessment_version=snapshot.assessment_version,
        methodology_version=snapshot.audit.methodology_version,
        factors=MappingProxyType(factors),
        evaluated_factor_ids=tuple(
            factor_id
            for factor_id, factor in factors.items()
            if factor.status == EVALUATED_STATUS
        ),
        not_evaluated_factor_ids=tuple(
            factor_id
            for factor_id, factor in factors.items()
            if factor.status == NOT_EVALUATED_STATUS
        ),
    )


def _build_factor_evaluation(
    factor: ConfidenceFactorConfig,
    snapshot: BusinessReadinessSnapshot,
    methodology_config: BusinessDecisionMethodologyConfig,
) -> ConfidenceFactorEvaluation:
    if factor.id == "assessment-completeness":
        return _build_assessment_completeness(factor, snapshot, methodology_config)
    if factor.id == "evidence-coverage":
        return _build_evidence_coverage(factor, snapshot, methodology_config)

    return ConfidenceFactorEvaluation(
        factor_id=factor.id,
        label=factor.label,
        status=NOT_EVALUATED_STATUS,
        limitation=_limitation_for(factor.id),
    )


def _build_assessment_completeness(
    factor: ConfidenceFactorConfig,
    snapshot: BusinessReadinessSnapshot,
    methodology_config: BusinessDecisionMethodologyConfig,
) -> ConfidenceFactorEvaluation:
    question_refs = _question_refs(snapshot)
    expected_count = len(methodology_config.questions)

    return ConfidenceFactorEvaluation(
        factor_id=factor.id,
        label=factor.label,
        status=EVALUATED_STATUS,
        observed_count=len(question_refs),
        expected_count=expected_count,
        coverage_ratio=_coverage_ratio(len(question_refs), expected_count),
        question_refs=question_refs,
        dimension_refs=snapshot.audit.evaluated_dimensions,
    )


def _build_evidence_coverage(
    factor: ConfidenceFactorConfig,
    snapshot: BusinessReadinessSnapshot,
    methodology_config: BusinessDecisionMethodologyConfig,
) -> ConfidenceFactorEvaluation:
    question_refs = _question_refs(snapshot)
    evidence_categories = tuple(
        sorted(
            {
                methodology_config.questions[question_id].evidence_category
                for question_id in question_refs
            }
        )
    )
    expected_count = len(methodology_config.evidence_categories)

    return ConfidenceFactorEvaluation(
        factor_id=factor.id,
        label=factor.label,
        status=EVALUATED_STATUS,
        observed_count=len(evidence_categories),
        expected_count=expected_count,
        coverage_ratio=_coverage_ratio(len(evidence_categories), expected_count),
        question_refs=question_refs,
        dimension_refs=snapshot.audit.evaluated_dimensions,
        evidence_categories=evidence_categories,
    )


def _question_refs(snapshot: BusinessReadinessSnapshot) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                question_id
                for domain in snapshot.domains
                for question_id in domain.contributing_questions
            }
        )
    )


def _coverage_ratio(observed_count: int, expected_count: int) -> float:
    if expected_count <= 0:
        raise ValueError("Expected count must be greater than zero.")

    return observed_count / expected_count


def _limitation_for(factor_id: str) -> str:
    limitations = {
        "answer-consistency": (
            "Answer consistency requires approved consistency rules before "
            "deterministic evaluation."
        ),
        "response-quality": (
            "Response quality requires approved response quality rules before "
            "deterministic evaluation."
        ),
        "business-certainty": (
            "Business certainty requires approved business certainty rules before "
            "deterministic evaluation."
        ),
    }

    return limitations.get(
        factor_id,
        "This confidence factor requires approved methodology before evaluation.",
    )


def _validate_snapshot_methodology(
    snapshot: BusinessReadinessSnapshot,
    methodology_config: BusinessDecisionMethodologyConfig,
) -> None:
    if snapshot.audit.methodology_version != methodology_config.version:
        raise ValueError("Snapshot methodology version does not match configuration.")

    domain_ids = tuple(domain.domain_id for domain in snapshot.domains)
    if tuple(sorted(domain_ids)) != snapshot.audit.evaluated_dimensions:
        raise ValueError("Snapshot audit dimensions do not match snapshot domains.")

    question_refs = _question_refs(snapshot)
    if len(question_refs) != snapshot.audit.question_count:
        raise ValueError("Snapshot audit question count does not match questions.")

    for domain_id in domain_ids:
        if domain_id not in methodology_config.readiness_dimensions:
            raise ValueError(f"Unknown readiness dimension: {domain_id}")

    for question_id in question_refs:
        if question_id not in methodology_config.questions:
            raise ValueError(f"Unknown question ID: {question_id}")
