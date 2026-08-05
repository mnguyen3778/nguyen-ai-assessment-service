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
from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
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
    ApprovedRecommendationAssessmentResult,
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


def approved_confidence(scale_value=2, numeric_value=50):
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
    return determine_approved_confidence(risk)


class ApprovedRecommendationRuntimeTests(unittest.TestCase):
    def test_assigns_recommendation_deterministically(self):
        confidence = approved_confidence()

        first = determine_approved_recommendation(confidence)
        second = determine_approved_recommendation(confidence)

        self.assertEqual(first, second)
        self.assertIsInstance(first, ApprovedRecommendationAssessmentResult)
        self.assertEqual(first.recommendation_classification, "planned-improvement")
        self.assertEqual(first.confidence_classification, "moderate-confidence")
        self.assertEqual(first.risk_classification, "moderate-risk")
        self.assertEqual(first.severity_classification, "medium")
        self.assertEqual(first.readiness_classification, "Ready")
        self.assertEqual(first.overall_assessment_score, 50.0)
        self.assertEqual(
            first.recommendation_decision_identifier,
            "recommendation-v1-deficiency-medium-planned",
        )
        self.assertEqual(
            first.recommendation_decision_table_version,
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        )
        self.assertEqual(first.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(
            first.runtime_config_version,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version,
        )
        self.assertEqual(first.assignment_method, RECOMMENDATION_ASSIGNMENT_METHOD)

    def test_applies_approved_recommendation_rules_by_severity(self):
        confidence = approved_confidence()
        cases = (
            (
                "critical",
                "immediate-action",
                "recommendation-v1-deficiency-critical-immediate",
            ),
            ("high", "priority-action", "recommendation-v1-deficiency-high-priority"),
            (
                "medium",
                "planned-improvement",
                "recommendation-v1-deficiency-medium-planned",
            ),
            (
                "low",
                "planned-improvement",
                "recommendation-v1-deficiency-low-planned",
            ),
            (
                "informational",
                "monitor",
                "recommendation-v1-observation-monitor",
            ),
        )

        for severity, recommendation, rule_id in cases:
            with self.subTest(rule_id=rule_id):
                result = determine_approved_recommendation(
                    replace(
                        confidence,
                        severity_classifications=(severity,),
                    )
                )

                self.assertEqual(result.recommendation_classification, recommendation)
                self.assertEqual(result.recommendation_decision_identifier, rule_id)
                self.assertEqual(result.severity_classification, severity)

    def test_result_artifact_is_immutable(self):
        result = determine_approved_recommendation(approved_confidence())

        with self.assertRaises(FrozenInstanceError):
            result.recommendation_classification = "monitor"

    def test_validation_fails_closed_for_non_confidence_result(self):
        with self.assertRaisesRegex(ValueError, "ApprovedConfidenceAssessmentResult"):
            determine_approved_recommendation(object())

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
            determine_approved_recommendation(
                approved_confidence(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_recommendation_table_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            recommendation_decision_table_set_version=(
                "unsupported-recommendation-table-version"
            ),
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(
            ValueError,
            "recommendation_decision_table_set_version",
        ):
            determine_approved_recommendation(
                approved_confidence(),
                invalid_config,
            )

    def test_validation_fails_closed_for_missing_required_recommendation_rule(self):
        recommendation_rules = dict(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.recommendation_decision_rules
        )
        del recommendation_rules["recommendation-v1-deficiency-medium-planned"]
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            recommendation_decision_rules=MappingProxyType(recommendation_rules),
        )

        with self.assertRaisesRegex(ValueError, "Missing approved recommendation"):
            determine_approved_recommendation(
                approved_confidence(),
                invalid_config,
            )

    def test_validation_fails_closed_for_invalid_recommendation_rule_output(self):
        recommendation_rules = dict(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.recommendation_decision_rules
        )
        recommendation_rules["recommendation-v1-deficiency-medium-planned"] = replace(
            recommendation_rules["recommendation-v1-deficiency-medium-planned"],
            output="unsupported-recommendation",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            recommendation_decision_rules=MappingProxyType(recommendation_rules),
        )

        with self.assertRaisesRegex(ValueError, "recommendation decision rule output"):
            determine_approved_recommendation(
                approved_confidence(),
                invalid_config,
            )

    def test_validation_fails_closed_for_confidence_methodology_version_mismatch(self):
        invalid_confidence = replace(
            approved_confidence(),
            methodology_version="unsupported-methodology-version",
        )

        with self.assertRaisesRegex(ValueError, "methodology version"):
            determine_approved_recommendation(invalid_confidence)

    def test_validation_fails_closed_for_confidence_runtime_config_version_mismatch(self):
        invalid_confidence = replace(
            approved_confidence(),
            runtime_config_version="unsupported-runtime-config-version",
        )

        with self.assertRaisesRegex(ValueError, "runtime config version"):
            determine_approved_recommendation(invalid_confidence)

    def test_validation_fails_closed_for_confidence_decision_table_version_mismatch(self):
        invalid_confidence = replace(
            approved_confidence(),
            confidence_decision_table_version="unsupported-confidence-table-version",
        )

        with self.assertRaisesRegex(ValueError, "Confidence decision table version"):
            determine_approved_recommendation(invalid_confidence)

    def test_validation_fails_closed_for_unsupported_confidence_classification(self):
        invalid_confidence = replace(
            approved_confidence(),
            confidence_classification="unsupported-confidence",
        )

        with self.assertRaisesRegex(ValueError, "Confidence classification"):
            determine_approved_recommendation(invalid_confidence)

    def test_validation_fails_closed_for_unsupported_risk_classification(self):
        invalid_confidence = replace(
            approved_confidence(),
            risk_classification="unsupported-risk",
        )

        with self.assertRaisesRegex(ValueError, "risk classification"):
            determine_approved_recommendation(invalid_confidence)

    def test_validation_fails_closed_for_ambiguous_severity_classification(self):
        invalid_confidence = replace(
            approved_confidence(),
            severity_classifications=("high", "high"),
        )

        with self.assertRaisesRegex(ValueError, "exactly one"):
            determine_approved_recommendation(invalid_confidence)

    def test_validation_fails_closed_for_unsupported_severity_classification(self):
        invalid_confidence = replace(
            approved_confidence(),
            severity_classifications=("unsupported-severity",),
        )

        with self.assertRaisesRegex(ValueError, "severity classification"):
            determine_approved_recommendation(invalid_confidence)

    def test_validation_fails_closed_for_invalid_readiness_classification(self):
        invalid_confidence = replace(
            approved_confidence(),
            readiness_classification="",
        )

        with self.assertRaisesRegex(ValueError, "readiness classification"):
            determine_approved_recommendation(invalid_confidence)

    def test_validation_fails_closed_for_invalid_overall_assessment_score(self):
        invalid_confidence = replace(
            approved_confidence(),
            overall_assessment_score=101,
        )

        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            determine_approved_recommendation(invalid_confidence)

    def test_validation_fails_closed_for_unsupported_confidence_decision_identifier(self):
        invalid_confidence = replace(
            approved_confidence(),
            confidence_decision_identifier="unsupported-confidence-decision",
        )

        with self.assertRaisesRegex(ValueError, "Confidence decision identifier"):
            determine_approved_recommendation(invalid_confidence)

    def test_validation_fails_closed_for_confidence_decision_output_mismatch(self):
        invalid_confidence = replace(
            approved_confidence(),
            confidence_classification="very-high-confidence",
        )

        with self.assertRaisesRegex(ValueError, "Confidence classification"):
            determine_approved_recommendation(invalid_confidence)


if __name__ == "__main__":
    unittest.main()
