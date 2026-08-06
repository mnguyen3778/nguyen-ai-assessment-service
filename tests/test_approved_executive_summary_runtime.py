import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from types import MappingProxyType


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.approved_confidence_runtime import (  # noqa: E402
    determine_approved_confidence,
)
from assessment.approved_dimension_aggregation_runtime import (  # noqa: E402
    aggregate_approved_dimensions,
)
from assessment.approved_dimension_weighting_runtime import (  # noqa: E402
    weight_approved_dimensions,
)
from assessment.approved_executive_summary_runtime import (  # noqa: E402
    EXECUTIVE_SUMMARY_EXECUTION_METHOD,
    EXECUTIVE_SUMMARY_SUMMARY_ID,
    EXECUTIVE_SUMMARY_TEMPLATE_ARTIFACT_VERSION,
    ApprovedExecutiveSummaryResult,
    generate_approved_executive_summary,
)
from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
    RECOMMENDATION_DECISION_TABLE_SET_VERSION,
)
from assessment.approved_overall_assessment_runtime import (  # noqa: E402
    calculate_approved_overall_assessment,
)
from assessment.approved_question_scoring_runtime import (  # noqa: E402
    score_approved_questions,
)
from assessment.approved_readiness_runtime import (  # noqa: E402
    determine_approved_readiness,
)
from assessment.approved_recommendation_runtime import (  # noqa: E402
    RECOMMENDATION_ASSIGNMENT_METHOD,
    determine_approved_recommendation,
)
from assessment.approved_risk_runtime import (  # noqa: E402
    determine_approved_risk,
)
from assessment.approved_severity_runtime import (  # noqa: E402
    determine_approved_severity,
)
from assessment.methodology_config import METHODOLOGY_VERSION  # noqa: E402


def approved_responses(scale_value=2, numeric_value=50):
    return {
        question_id: (
            numeric_value
            if question.response_model_id == "numeric-0-100"
            else scale_value
        )
        for question_id, question in (
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.questions.items()
        )
    }


def approved_recommendation(scale_value=2, numeric_value=50):
    question_scoring = score_approved_questions(
        approved_responses(scale_value, numeric_value),
        METHODOLOGY_VERSION,
    )
    dimension_aggregation = aggregate_approved_dimensions(question_scoring)
    dimension_weighting = weight_approved_dimensions(dimension_aggregation)
    overall_assessment = calculate_approved_overall_assessment(dimension_weighting)
    readiness = determine_approved_readiness(overall_assessment)
    severity = determine_approved_severity(readiness)
    risk = determine_approved_risk(severity)
    confidence = determine_approved_confidence(risk)
    return determine_approved_recommendation(confidence)


class ApprovedExecutiveSummaryRuntimeTests(unittest.TestCase):
    def test_generates_executive_summary_deterministically(self):
        recommendation = approved_recommendation()

        first = generate_approved_executive_summary(recommendation)
        second = generate_approved_executive_summary(recommendation)

        self.assertEqual(first, second)
        self.assertIsInstance(first, ApprovedExecutiveSummaryResult)
        self.assertEqual(first.summary_id, EXECUTIVE_SUMMARY_SUMMARY_ID)
        self.assertEqual(first.recommendation_classification, "planned-improvement")
        self.assertEqual(first.confidence_classification, "moderate-confidence")
        self.assertEqual(first.risk_classification, "moderate-risk")
        self.assertEqual(first.severity_classification, "medium")
        self.assertEqual(first.readiness_classification, "Ready")
        self.assertEqual(first.overall_assessment_score, 50.0)
        self.assertEqual(
            first.executive_summary_template_identifier,
            EXECUTIVE_SUMMARY_TEMPLATE_ARTIFACT_VERSION,
        )
        self.assertEqual(
            first.executive_summary_template_version,
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
        )
        self.assertEqual(first.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(
            first.runtime_config_version,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version,
        )
        self.assertEqual(len(first.sections), 7)
        self.assertEqual(
            first.execution_metadata["executionMethod"],
            EXECUTIVE_SUMMARY_EXECUTION_METHOD,
        )
        self.assertEqual(
            first.execution_metadata["sectionOrdering"],
            (
                "overall-assessment-overview",
                "business-capability-highlights",
                "significant-findings",
                "risk-overview",
                "confidence-statement",
                "recommended-actions",
                "closing-assessment-statement",
            ),
        )

    def test_executes_only_approved_template_text(self):
        summary = generate_approved_executive_summary(approved_recommendation())
        sections = {
            section.section_id: section
            for section in summary.sections
        }

        self.assertEqual(
            sections["overall-assessment-overview"].executive_summary_text,
            "The overall assessment result is 50. The assigned readiness state "
            "is Ready. This summary was produced under "
            "business-decision-methodology-v1.",
        )
        self.assertEqual(
            sections["business-capability-highlights"].executive_summary_text,
            "Business capability results are: readiness=Ready; "
            "overall_assessment_score=50. These results are summarized from "
            "approved Dimension Results and Evidence Evaluation.",
        )
        self.assertEqual(
            sections["significant-findings"].executive_summary_text,
            "The assessment produced 1 Findings. Significant Findings are "
            "summarized from Severity-Assigned Findings: medium.",
        )
        self.assertEqual(
            sections["risk-overview"].executive_summary_text,
            "The assessment-level risk is moderate-risk. This Risk Assessment "
            "is summarized from approved Severity-Assigned Findings.",
        )
        self.assertEqual(
            sections["confidence-statement"].executive_summary_text,
            "The confidence assessment is moderate-confidence. This Confidence "
            "Assessment is summarized from approved Evidence Evaluation and "
            "required upstream context.",
        )
        self.assertEqual(
            sections["recommended-actions"].executive_summary_text,
            "The assessment produced 1 Recommendations: planned-improvement.",
        )
        self.assertIn(
            "This Executive Summary presents approved Assessment Service "
            "outputs only.",
            sections["closing-assessment-statement"].executive_summary_text,
        )

    def test_sections_preserve_template_metadata_and_traceability(self):
        summary = generate_approved_executive_summary(approved_recommendation())

        for index, section in enumerate(summary.sections, start=1):
            self.assertEqual(section.section_order, index)
            self.assertEqual(
                section.template_id,
                f"executive-summary-v1-{section.section_id}",
            )
            self.assertEqual(
                section.template_version,
                EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
            )
            self.assertTrue(section.source_artifact_references)
            self.assertTrue(section.placeholder_source_map)
            self.assertEqual(section.validation_status, "valid")

    def test_result_artifacts_are_immutable(self):
        summary = generate_approved_executive_summary(approved_recommendation())

        with self.assertRaises(FrozenInstanceError):
            summary.recommendation_classification = "monitor"
        with self.assertRaises(TypeError):
            summary.execution_metadata["validationStatus"] = "invalid"
        with self.assertRaises(FrozenInstanceError):
            summary.sections[0].executive_summary_text = "changed"
        with self.assertRaises(TypeError):
            summary.sections[0].placeholder_source_map["readiness"] = "changed"

    def test_to_dict_preserves_contract_values(self):
        summary = generate_approved_executive_summary(approved_recommendation())

        payload = summary.to_dict()

        self.assertEqual(payload["summaryId"], EXECUTIVE_SUMMARY_SUMMARY_ID)
        self.assertEqual(payload["recommendationClassification"], "planned-improvement")
        self.assertEqual(payload["confidenceClassification"], "moderate-confidence")
        self.assertEqual(payload["riskClassification"], "moderate-risk")
        self.assertEqual(payload["severityClassification"], "medium")
        self.assertEqual(payload["readinessClassification"], "Ready")
        self.assertEqual(payload["overallAssessmentScore"], 50.0)
        self.assertEqual(
            payload["executiveSummaryTemplateIdentifier"],
            EXECUTIVE_SUMMARY_TEMPLATE_ARTIFACT_VERSION,
        )
        self.assertEqual(
            payload["executiveSummaryTemplateVersion"],
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
        )
        self.assertEqual(payload["methodologyVersion"], METHODOLOGY_VERSION)
        self.assertEqual(len(payload["sections"]), 7)

    def test_validation_fails_closed_for_non_recommendation_result(self):
        with self.assertRaisesRegex(ValueError, "ApprovedRecommendation"):
            generate_approved_executive_summary(object())

    def test_validation_fails_closed_for_unsupported_methodology_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            methodology_version="unsupported-methodology-version",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(ValueError, "methodology_version"):
            generate_approved_executive_summary(
                approved_recommendation(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_runtime_config_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            runtime_config_version="unsupported-runtime-config-version",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(ValueError, "runtime_config_version"):
            generate_approved_executive_summary(
                approved_recommendation(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_template_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            executive_summary_template_set_version="unsupported-template-version",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(
            ValueError,
            "executive_summary_template_set_version",
        ):
            generate_approved_executive_summary(
                approved_recommendation(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_section_template(self):
        sections = dict(APPROVED_METHODOLOGY_RUNTIME_CONFIG.executive_summary_sections)
        sections["risk-overview"] = replace(
            sections["risk-overview"],
            template_id="unsupported-risk-overview-template",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            executive_summary_sections=MappingProxyType(sections),
        )

        with self.assertRaisesRegex(ValueError, "section template"):
            generate_approved_executive_summary(
                approved_recommendation(),
                invalid_config,
            )

    def test_validation_fails_closed_for_recommendation_methodology_mismatch(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            methodology_version="unsupported-methodology-version",
        )

        with self.assertRaisesRegex(ValueError, "methodology version"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_fails_closed_for_recommendation_runtime_config_mismatch(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            runtime_config_version="unsupported-runtime-config-version",
        )

        with self.assertRaisesRegex(ValueError, "runtime config version"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_fails_closed_for_recommendation_table_version_mismatch(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            recommendation_decision_table_version=(
                "unsupported-recommendation-table-version"
            ),
        )

        with self.assertRaisesRegex(ValueError, "decision table version"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_fails_closed_for_unsupported_recommendation_classification(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            recommendation_classification="unsupported-recommendation",
        )

        with self.assertRaisesRegex(ValueError, "Recommendation classification"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_fails_closed_for_unsupported_confidence_classification(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            confidence_classification="unsupported-confidence",
        )

        with self.assertRaisesRegex(ValueError, "confidence classification"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_fails_closed_for_unsupported_risk_classification(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            risk_classification="unsupported-risk",
        )

        with self.assertRaisesRegex(ValueError, "risk classification"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_fails_closed_for_unsupported_severity_classification(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            severity_classification="unsupported-severity",
        )

        with self.assertRaisesRegex(ValueError, "severity classification"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_fails_closed_for_unsupported_readiness_classification(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            readiness_classification="Incomplete",
        )

        with self.assertRaisesRegex(ValueError, "readiness classification"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_fails_closed_for_invalid_overall_assessment_score(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            overall_assessment_score=101,
        )

        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_fails_closed_for_unsupported_assignment_method(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            assignment_method="unsupported-assignment-method",
        )

        with self.assertRaisesRegex(ValueError, "assignment method"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_fails_closed_for_unsupported_decision_identifier(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            recommendation_decision_identifier="unsupported-recommendation-decision",
        )

        with self.assertRaisesRegex(ValueError, "decision identifier"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_fails_closed_for_recommendation_decision_output_mismatch(self):
        invalid_recommendation = replace(
            approved_recommendation(),
            recommendation_classification="monitor",
        )

        with self.assertRaisesRegex(ValueError, "does not match decision table"):
            generate_approved_executive_summary(invalid_recommendation)

    def test_validation_preserves_source_recommendation_metadata(self):
        summary = generate_approved_executive_summary(approved_recommendation())

        self.assertEqual(
            summary.execution_metadata["sourceRecommendationDecisionTableVersion"],
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        )
        self.assertEqual(
            summary.execution_metadata["sourceRecommendationAssignmentMethod"],
            RECOMMENDATION_ASSIGNMENT_METHOD,
        )


if __name__ == "__main__":
    unittest.main()
