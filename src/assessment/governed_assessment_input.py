"""Canonical governed executive assessment input for the v2 decision path."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from assessment.approved_methodology_runtime_config import APPROVED_DIMENSION_ORDER
from assessment.methodology_config import METHODOLOGY_VERSION


EXECUTIVE_ASSESSMENT_VERSION_V2 = "nguyen-ai-executive-assessment-v2"
EVIDENCE_QUALITIES = frozenset(("Basic", "Adequate", "Strong"))
ASSERTABILITY_LIMITATIONS = frozenset(("authenticity", "traceability"))
FINDING_CONSEQUENCE_RULES = MappingProxyType({
    ("Deficiency", "material current breach"): "severity-v1-deficiency-critical",
    ("Deficiency", "significant gap"): "severity-v1-deficiency-high",
    ("Deficiency", "clear deficiency"): "severity-v1-deficiency-medium",
    ("Deficiency", "limited weakness"): "severity-v1-deficiency-low",
    ("Observation", "observation"): "severity-v1-observation-informational",
    ("Strength", "strength"): "severity-v1-strength-informational",
    ("Opportunity", "opportunity"): "severity-v1-opportunity-informational",
})


def _text(name: str, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text.")
    return value


@dataclass(frozen=True)
class EvidenceQualityInput:
    source_reference: str
    quality: str
    assertability_limitation: str | None

    def __post_init__(self) -> None:
        _text("Evidence source reference", self.source_reference)
        if self.quality not in EVIDENCE_QUALITIES:
            raise ValueError("Unsupported evidence quality.")
        if (self.assertability_limitation is not None and
                self.assertability_limitation not in ASSERTABILITY_LIMITATIONS):
            raise ValueError("Unsupported evidence assertability limitation.")


@dataclass(frozen=True)
class EvidenceProfileInput:
    required_evidence_present: bool
    items: tuple[EvidenceQualityInput, ...]

    def __post_init__(self) -> None:
        if self.required_evidence_present is not True:
            raise ValueError("Required evidence must be present.")
        if not isinstance(self.items, tuple) or not self.items:
            raise ValueError("Evidence items must be a nonempty tuple.")
        if any(not isinstance(item, EvidenceQualityInput) for item in self.items):
            raise ValueError("Evidence items must be governed quality inputs.")
        references = [item.source_reference for item in self.items]
        if len(references) != len(set(references)):
            raise ValueError("Duplicate evidence source reference.")
        object.__setattr__(self, "items", tuple(sorted(
            self.items, key=lambda item: item.source_reference
        )))


@dataclass(frozen=True)
class FindingInput:
    finding_id: str
    title: str
    primary_dimension: str
    related_dimensions: tuple[str, ...]
    trigger_source: str
    finding_type: str
    business_consequence_basis: str
    source_references: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("finding_id", "title", "trigger_source"):
            _text(name, getattr(self, name))
        if self.primary_dimension not in APPROVED_DIMENSION_ORDER:
            raise ValueError("Unsupported finding primary dimension.")
        if not isinstance(self.related_dimensions, tuple) or any(
            dimension not in APPROVED_DIMENSION_ORDER or
            dimension == self.primary_dimension
            for dimension in self.related_dimensions
        ) or len(self.related_dimensions) != len(set(self.related_dimensions)):
            raise ValueError("Unsupported finding related dimensions.")
        if (self.finding_type, self.business_consequence_basis) not in FINDING_CONSEQUENCE_RULES:
            raise ValueError("Unsupported finding type or business consequence basis.")
        if not isinstance(self.source_references, tuple) or not self.source_references:
            raise ValueError("Finding source references are required.")
        for reference in self.source_references:
            _text("Finding source reference", reference)
        if len(self.source_references) != len(set(self.source_references)):
            raise ValueError("Duplicate finding source reference.")
        object.__setattr__(self, "related_dimensions", tuple(sorted(self.related_dimensions)))
        object.__setattr__(self, "source_references", tuple(sorted(self.source_references)))


@dataclass(frozen=True)
class ValidatedCanonicalExecutiveAssessmentInputV2:
    assessment_version: str
    methodology_version: str
    answers: Mapping[str, object]
    evidence_profile: EvidenceProfileInput
    findings: tuple[FindingInput, ...]

    def __post_init__(self) -> None:
        if self.assessment_version != EXECUTIVE_ASSESSMENT_VERSION_V2:
            raise ValueError("Unsupported v2 executive assessment version.")
        if self.methodology_version != METHODOLOGY_VERSION:
            raise ValueError("Unsupported v2 methodology version.")
        if not isinstance(self.answers, Mapping):
            raise ValueError("Canonical answers must be a mapping.")
        if any(not isinstance(key, str) for key in self.answers):
            raise ValueError("Canonical answer IDs must be text.")
        object.__setattr__(self, "answers", MappingProxyType({
            key: self.answers[key] for key in sorted(self.answers)
        }))
        if not isinstance(self.evidence_profile, EvidenceProfileInput):
            raise ValueError("Governed evidence profile is required.")
        if not isinstance(self.findings, tuple) or any(
            not isinstance(finding, FindingInput) for finding in self.findings
        ):
            raise ValueError("Complete governed finding tuple is required.")
        ids = [finding.finding_id for finding in self.findings]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate finding ID.")
        evidence_refs = {
            item.source_reference for item in self.evidence_profile.items
        }
        for finding in self.findings:
            if not set(finding.source_references) <= evidence_refs:
                raise ValueError("Finding source references must identify evaluated evidence.")
        object.__setattr__(self, "findings", tuple(sorted(
            self.findings, key=lambda finding: finding.finding_id
        )))
