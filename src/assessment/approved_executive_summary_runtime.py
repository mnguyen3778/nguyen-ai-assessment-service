from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from assessment.approved_methodology_runtime_config import (
    APPROVED_CONFIDENCE_LEVEL_ORDER,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    APPROVED_RECOMMENDATION_LABEL_ORDER,
    APPROVED_RISK_LEVEL_ORDER,
    APPROVED_SEVERITY_LEVEL_ORDER,
    EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
    INCOMPLETE_OPERATIONAL_STATE,
    RECOMMENDATION_DECISION_TABLE_SET_VERSION,
    ApprovedMethodologyRuntimeConfig,
    ExecutiveSummarySectionRuntimeConfig,
    validate_approved_methodology_runtime_config,
)
from assessment.approved_recommendation_runtime import (
    RECOMMENDATION_ASSIGNMENT_METHOD,
    ApprovedRecommendationAssessmentResult,
)
from assessment.methodology_config import METHODOLOGY_VERSION


EXECUTIVE_SUMMARY_TEMPLATE_ARTIFACT_VERSION = "executive-summary-templates-v1"
EXECUTIVE_SUMMARY_SUMMARY_ID = "approved-executive-summary-v1"
EXECUTIVE_SUMMARY_VALIDATION_STATUS = "valid"
EXECUTIVE_SUMMARY_EXECUTION_METHOD = "approved-executive-summary-templates-v1"


SECTION_TEMPLATE_TEXT = MappingProxyType(
    {
        "overall-assessment-overview": (
            "The overall assessment result is {overall_assessment_result}. "
            "The assigned readiness state is {readiness}. This summary was "
            "produced under {methodology_version}."
        ),
        "business-capability-highlights": (
            "Business capability results are: {dimension_results}. These "
            "results are summarized from approved Dimension Results and "
            "Evidence Evaluation."
        ),
        "significant-findings": (
            "The assessment produced {finding_count} Findings. Significant "
            "Findings are summarized from Severity-Assigned Findings: "
            "{significant_findings}."
        ),
        "risk-overview": (
            "The assessment-level risk is {risk_assessment}. This Risk "
            "Assessment is summarized from approved Severity-Assigned Findings."
        ),
        "confidence-statement": (
            "The confidence assessment is {confidence_assessment}. This "
            "Confidence Assessment is summarized from approved Evidence "
            "Evaluation and required upstream context."
        ),
        "recommended-actions": (
            "The assessment produced {recommendation_count} Recommendations: "
            "{recommendations}."
        ),
        "closing-assessment-statement": (
            "This Executive Summary presents approved Assessment Service "
            "outputs only. It is bound to {methodology_version} and source "
            "artifact versions {artifact_versions}."
        ),
    }
)

SIGNIFICANT_FINDINGS_EMPTY_TEMPLATE_TEXT = (
    "The assessment produced no Findings."
)

SECTION_PLACEHOLDERS = MappingProxyType(
    {
        "overall-assessment-overview": (
            "overall_assessment_result",
            "readiness",
            "methodology_version",
        ),
        "business-capability-highlights": ("dimension_results",),
        "significant-findings": (
            "finding_count",
            "significant_findings",
        ),
        "risk-overview": ("risk_assessment",),
        "confidence-statement": ("confidence_assessment",),
        "recommended-actions": (
            "recommendation_count",
            "recommendations",
        ),
        "closing-assessment-statement": (
            "methodology_version",
            "artifact_versions",
        ),
    }
)

PLACEHOLDER_SOURCE_MAP = MappingProxyType(
    {
        "overall_assessment_result": (
            "ApprovedRecommendationAssessmentResult.overall_assessment_score"
        ),
        "readiness": (
            "ApprovedRecommendationAssessmentResult.readiness_classification"
        ),
        "dimension_results": (
            "ApprovedRecommendationAssessmentResult.readiness_classification; "
            "ApprovedRecommendationAssessmentResult.overall_assessment_score"
        ),
        "finding_count": (
            "ApprovedRecommendationAssessmentResult.severity_classification"
        ),
        "significant_findings": (
            "ApprovedRecommendationAssessmentResult.severity_classification"
        ),
        "risk_assessment": (
            "ApprovedRecommendationAssessmentResult.risk_classification"
        ),
        "confidence_assessment": (
            "ApprovedRecommendationAssessmentResult.confidence_classification"
        ),
        "recommendation_count": (
            "ApprovedRecommendationAssessmentResult.recommendation_classification"
        ),
        "recommendations": (
            "ApprovedRecommendationAssessmentResult.recommendation_classification"
        ),
        "methodology_version": (
            "ApprovedRecommendationAssessmentResult.methodology_version"
        ),
        "artifact_versions": (
            "ApprovedRecommendationAssessmentResult.methodology_version; "
            "ApprovedRecommendationAssessmentResult.runtime_config_version; "
            "ApprovedRecommendationAssessmentResult."
            "recommendation_decision_table_version"
        ),
    }
)

SECTION_SOURCE_REFERENCES = MappingProxyType(
    {
        "overall-assessment-overview": (
            "recommendation.overall_assessment_score",
            "recommendation.readiness_classification",
            "recommendation.methodology_version",
        ),
        "business-capability-highlights": (
            "recommendation.readiness_classification",
            "recommendation.overall_assessment_score",
        ),
        "significant-findings": (
            "recommendation.severity_classification",
        ),
        "risk-overview": (
            "recommendation.risk_classification",
            "recommendation.severity_classification",
        ),
        "confidence-statement": (
            "recommendation.confidence_classification",
        ),
        "recommended-actions": (
            "recommendation.recommendation_classification",
            "recommendation.recommendation_decision_identifier",
        ),
        "closing-assessment-statement": (
            "recommendation.methodology_version",
            "recommendation.runtime_config_version",
            "recommendation.recommendation_decision_table_version",
        ),
    }
)


@dataclass(frozen=True)
class ApprovedExecutiveSummarySection:
    section_id: str
    heading: str
    section_order: int
    template_id: str
    template_version: str
    executive_summary_text: str
    source_artifact_references: tuple[str, ...]
    placeholder_source_map: Mapping[str, str]
    validation_status: str

    def __post_init__(self) -> None:
        if isinstance(self.placeholder_source_map, Mapping):
            object.__setattr__(
                self,
                "placeholder_source_map",
                MappingProxyType(dict(self.placeholder_source_map)),
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "sectionId": self.section_id,
            "heading": self.heading,
            "sectionOrder": self.section_order,
            "templateId": self.template_id,
            "templateVersion": self.template_version,
            "executiveSummaryText": self.executive_summary_text,
            "sourceArtifactReferences": list(self.source_artifact_references),
            "placeholderSourceMap": dict(self.placeholder_source_map),
            "validationStatus": self.validation_status,
        }


@dataclass(frozen=True)
class ApprovedExecutiveSummaryResult:
    summary_id: str
    executive_summary_text: str
    recommendation_classification: str
    confidence_classification: str
    risk_classification: str
    severity_classification: str
    readiness_classification: str
    overall_assessment_score: float
    executive_summary_template_identifier: str
    executive_summary_template_version: str
    methodology_version: str
    runtime_config_version: str
    execution_metadata: Mapping[str, Any]
    sections: tuple[ApprovedExecutiveSummarySection, ...]

    def __post_init__(self) -> None:
        if isinstance(self.execution_metadata, Mapping):
            object.__setattr__(
                self,
                "execution_metadata",
                MappingProxyType(dict(self.execution_metadata)),
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "summaryId": self.summary_id,
            "executiveSummaryText": self.executive_summary_text,
            "recommendationClassification": self.recommendation_classification,
            "confidenceClassification": self.confidence_classification,
            "riskClassification": self.risk_classification,
            "severityClassification": self.severity_classification,
            "readinessClassification": self.readiness_classification,
            "overallAssessmentScore": self.overall_assessment_score,
            "executiveSummaryTemplateIdentifier": (
                self.executive_summary_template_identifier
            ),
            "executiveSummaryTemplateVersion": (
                self.executive_summary_template_version
            ),
            "methodologyVersion": self.methodology_version,
            "runtimeConfigVersion": self.runtime_config_version,
            "executionMetadata": _metadata_to_dict(self.execution_metadata),
            "sections": [section.to_dict() for section in self.sections],
        }


def generate_approved_executive_summary(
    recommendation: object,
    runtime_config: ApprovedMethodologyRuntimeConfig = (
        APPROVED_METHODOLOGY_RUNTIME_CONFIG
    ),
) -> ApprovedExecutiveSummaryResult:
    validate_approved_methodology_runtime_config(runtime_config)
    _validate_methodology_version(runtime_config)
    _validate_runtime_config_version(runtime_config)
    _validate_executive_summary_template_version(runtime_config)
    _validate_executive_summary_templates(runtime_config)
    _validate_recommendation_artifact(recommendation, runtime_config)

    placeholders = _build_placeholder_values(recommendation, runtime_config)
    sections = tuple(
        _render_section(section_config, placeholders)
        for section_config in runtime_config.executive_summary_sections.values()
    )
    summary_text = "\n\n".join(
        f"{section.heading}\n{section.executive_summary_text}"
        for section in sections
    )

    return ApprovedExecutiveSummaryResult(
        summary_id=EXECUTIVE_SUMMARY_SUMMARY_ID,
        executive_summary_text=summary_text,
        recommendation_classification=(
            recommendation.recommendation_classification
        ),
        confidence_classification=recommendation.confidence_classification,
        risk_classification=recommendation.risk_classification,
        severity_classification=recommendation.severity_classification,
        readiness_classification=recommendation.readiness_classification,
        overall_assessment_score=float(recommendation.overall_assessment_score),
        executive_summary_template_identifier=(
            EXECUTIVE_SUMMARY_TEMPLATE_ARTIFACT_VERSION
        ),
        executive_summary_template_version=(
            runtime_config.version_manifest.executive_summary_template_set_version
        ),
        methodology_version=recommendation.methodology_version,
        runtime_config_version=recommendation.runtime_config_version,
        execution_metadata=MappingProxyType(
            {
                "executionMethod": EXECUTIVE_SUMMARY_EXECUTION_METHOD,
                "sectionCount": len(sections),
                "sectionOrdering": tuple(
                    section.section_id
                    for section in sections
                ),
                "sourceRecommendationDecisionIdentifier": (
                    recommendation.recommendation_decision_identifier
                ),
                "sourceRecommendationDecisionTableVersion": (
                    recommendation.recommendation_decision_table_version
                ),
                "sourceRecommendationAssignmentMethod": (
                    recommendation.assignment_method
                ),
                "validationStatus": EXECUTIVE_SUMMARY_VALIDATION_STATUS,
            }
        ),
        sections=sections,
    )


def _validate_methodology_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if runtime_config.version_manifest.methodology_version != METHODOLOGY_VERSION:
        raise ValueError("Unsupported methodology version.")


def _validate_runtime_config_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.runtime_config_version
        != APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION
    ):
        raise ValueError("Unsupported approved methodology runtime config version.")


def _validate_executive_summary_template_version(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if (
        runtime_config.version_manifest.executive_summary_template_set_version
        != EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION
    ):
        raise ValueError("Unsupported Executive Summary template version.")


def _validate_executive_summary_templates(
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    expected_section_ids = tuple(SECTION_TEMPLATE_TEXT)
    if tuple(runtime_config.executive_summary_sections) != expected_section_ids:
        raise ValueError("Executive Summary section order is unsupported.")

    for index, section in enumerate(
        runtime_config.executive_summary_sections.values(),
        start=1,
    ):
        _validate_section_template(index, section)


def _validate_section_template(
    expected_order: int,
    section: ExecutiveSummarySectionRuntimeConfig,
) -> None:
    if section.order != expected_order:
        raise ValueError(f"Executive Summary section order mismatch: {section.id}")
    if section.template_version != EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION:
        raise ValueError(
            f"Unsupported Executive Summary section template version: {section.id}"
        )
    expected_template_id = f"executive-summary-v1-{section.id}"
    if section.template_id != expected_template_id:
        raise ValueError(
            f"Unsupported Executive Summary section template: {section.id}"
        )
    if section.id not in SECTION_TEMPLATE_TEXT:
        raise ValueError(f"Unapproved Executive Summary section: {section.id}")


def _validate_recommendation_artifact(
    recommendation: object,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    if not isinstance(recommendation, ApprovedRecommendationAssessmentResult):
        raise ValueError(
            "Approved Executive Summary requires "
            "ApprovedRecommendationAssessmentResult."
        )
    if (
        recommendation.methodology_version
        != runtime_config.version_manifest.methodology_version
    ):
        raise ValueError("Recommendation methodology version is unsupported.")
    if (
        recommendation.runtime_config_version
        != runtime_config.version_manifest.runtime_config_version
    ):
        raise ValueError("Recommendation runtime config version is unsupported.")
    if (
        recommendation.recommendation_decision_table_version
        != RECOMMENDATION_DECISION_TABLE_SET_VERSION
    ):
        raise ValueError("Recommendation decision table version is unsupported.")
    if (
        recommendation.recommendation_classification
        not in APPROVED_RECOMMENDATION_LABEL_ORDER
    ):
        raise ValueError("Recommendation classification is unsupported.")
    if (
        recommendation.confidence_classification
        not in APPROVED_CONFIDENCE_LEVEL_ORDER
    ):
        raise ValueError("Recommendation confidence classification is unsupported.")
    if recommendation.risk_classification not in APPROVED_RISK_LEVEL_ORDER:
        raise ValueError("Recommendation risk classification is unsupported.")
    if recommendation.severity_classification not in APPROVED_SEVERITY_LEVEL_ORDER:
        raise ValueError("Recommendation severity classification is unsupported.")
    if not _approved_readiness_label(recommendation, runtime_config):
        raise ValueError("Recommendation readiness classification is unsupported.")
    if not isinstance(
        recommendation.overall_assessment_score,
        (int, float),
    ) or isinstance(recommendation.overall_assessment_score, bool):
        raise ValueError("Recommendation overall assessment score must be numeric.")
    if not 0 <= float(recommendation.overall_assessment_score) <= 100:
        raise ValueError(
            "Recommendation overall assessment score must be between 0 and 100."
        )
    if recommendation.assignment_method != RECOMMENDATION_ASSIGNMENT_METHOD:
        raise ValueError("Recommendation assignment method is unsupported.")

    _validate_recommendation_decision_alignment(recommendation, runtime_config)


def _approved_readiness_label(
    recommendation: ApprovedRecommendationAssessmentResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> bool:
    if not isinstance(recommendation.readiness_classification, str):
        return False
    if recommendation.readiness_classification == INCOMPLETE_OPERATIONAL_STATE:
        return False
    approved_labels = tuple(
        threshold.label
        for threshold in runtime_config.readiness_thresholds.values()
    )
    return recommendation.readiness_classification in approved_labels


def _validate_recommendation_decision_alignment(
    recommendation: ApprovedRecommendationAssessmentResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> None:
    try:
        rule = runtime_config.recommendation_decision_rules[
            recommendation.recommendation_decision_identifier
        ]
    except KeyError as exc:
        raise ValueError("Recommendation decision identifier is unsupported.") from exc

    if rule.table_version != RECOMMENDATION_DECISION_TABLE_SET_VERSION:
        raise ValueError("Recommendation decision table version is unsupported.")
    if rule.output != recommendation.recommendation_classification:
        raise ValueError(
            "Recommendation classification does not match decision table."
        )


def _build_placeholder_values(
    recommendation: ApprovedRecommendationAssessmentResult,
    runtime_config: ApprovedMethodologyRuntimeConfig,
) -> Mapping[str, str]:
    artifact_versions = (
        f"methodology_version={recommendation.methodology_version}; "
        f"runtime_config_version={recommendation.runtime_config_version}; "
        "recommendation_decision_table_version="
        f"{recommendation.recommendation_decision_table_version}; "
        "executive_summary_template_version="
        f"{runtime_config.version_manifest.executive_summary_template_set_version}"
    )
    return MappingProxyType(
        {
            "overall_assessment_result": _format_score(
                recommendation.overall_assessment_score
            ),
            "readiness": recommendation.readiness_classification,
            "dimension_results": (
                f"readiness={recommendation.readiness_classification}; "
                "overall_assessment_score="
                f"{_format_score(recommendation.overall_assessment_score)}"
            ),
            "finding_count": "1",
            "significant_findings": recommendation.severity_classification,
            "risk_assessment": recommendation.risk_classification,
            "confidence_assessment": recommendation.confidence_classification,
            "recommendation_count": "1",
            "recommendations": recommendation.recommendation_classification,
            "methodology_version": recommendation.methodology_version,
            "artifact_versions": artifact_versions,
        }
    )


def _render_section(
    section_config: ExecutiveSummarySectionRuntimeConfig,
    placeholders: Mapping[str, str],
) -> ApprovedExecutiveSummarySection:
    if section_config.id == "significant-findings":
        template_text = (
            SIGNIFICANT_FINDINGS_EMPTY_TEMPLATE_TEXT
            if placeholders["finding_count"] == "0"
            else SECTION_TEMPLATE_TEXT[section_config.id]
        )
    else:
        template_text = SECTION_TEMPLATE_TEXT[section_config.id]

    section_placeholders = SECTION_PLACEHOLDERS[section_config.id]
    placeholder_values = {
        placeholder: placeholders[placeholder]
        for placeholder in section_placeholders
    }
    placeholder_sources = {
        placeholder: PLACEHOLDER_SOURCE_MAP[placeholder]
        for placeholder in section_placeholders
    }
    return ApprovedExecutiveSummarySection(
        section_id=section_config.id,
        heading=section_config.heading,
        section_order=section_config.order,
        template_id=section_config.template_id,
        template_version=section_config.template_version,
        executive_summary_text=template_text.format(**placeholder_values),
        source_artifact_references=SECTION_SOURCE_REFERENCES[section_config.id],
        placeholder_source_map=MappingProxyType(placeholder_sources),
        validation_status=EXECUTIVE_SUMMARY_VALIDATION_STATUS,
    )


def _format_score(score: float) -> str:
    normalized = float(score)
    if normalized.is_integer():
        return str(int(normalized))
    return str(normalized)


def _metadata_to_dict(metadata: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: list(value) if isinstance(value, tuple) else value
        for key, value in metadata.items()
    }
