import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from types import MappingProxyType


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.approved_dimension_aggregation_runtime import (  # noqa: E402
    aggregate_approved_dimensions,
)
from assessment.approved_dimension_weighting_runtime import (  # noqa: E402
    weight_approved_dimensions,
)
from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    CONFIDENCE_DECISION_TABLE_SET_VERSION,
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
from assessment.approved_risk_runtime import (  # noqa: E402
    determine_approved_risk,
)
from assessment.approved_severity_runtime import (  # noqa: E402
    determine_approved_severity,
)
from assessment.approved_confidence_runtime import (  # noqa: E402
    CONFIDENCE_ASSIGNMENT_METHOD,
    DEFAULT_CONFIDENCE_DECISION_RULE_ID,
    ApprovedConfidenceAssessmentResult,
    determine_approved_confidence,
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


def approved_risk(scale_value=2, numeric_value=50):
    question_scoring = score_approved_questions(
        approved_responses(scale_value, numeric_value),
        METHODOLOGY_VERSION,
    )
    dimension_aggregation = aggregate_approved_dimensions(question_scoring)
    dimension_weighting = weight_approved_dimensions(dimension_aggregation)
    overall_assessment = calculate_approved_overall_assessment(dimension_weighting)
    readiness = determine_approved_readiness(overall_assessment)
    severity = determine_approved_severity(readiness)
    return determine_approved_risk(severity)


class ApprovedConfidenceRuntimeTests(unittest.TestCase):
    def test_assigns_confidence_deterministically(self):
        risk = approved_risk()

        first = determine_approved_confidence(risk)
        second = determine_approved_confidence(risk)

        self.assertEqual(first, second)
        self.assertIsInstance(first, ApprovedConfidenceAssessmentResult)
        self.assertEqual(first.confidence_classification, "moderate-confidence")
        self.assertEqual(first.risk_classification, "moderate-risk")
        self.assertEqual(first.severity_classifications, ("medium",))
        self.assertEqual(first.readiness_classification, "Ready")
        self.assertEqual(first.overall_assessment_score, 50.0)
        self.assertEqual(
            first.confidence_decision_identifier,
            DEFAULT_CONFIDENCE_DECISION_RULE_ID,
        )
        self.assertEqual(
            first.confidence_decision_table_version,
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
        )
        self.assertEqual(first.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(
            first.runtime_config_version,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version,
        )
        self.assertEqual(first.assignment_method, CONFIDENCE_ASSIGNMENT_METHOD)

    def test_result_artifact_is_immutable(self):
        result = determine_approved_confidence(approved_risk())

        with self.assertRaises(FrozenInstanceError):
            result.confidence_classification = "high-confidence"
        with self.assertRaises(TypeError):
            result.severity_classifications[0] = "critical"

    def test_validation_fails_closed_for_non_risk_result(self):
        with self.assertRaisesRegex(ValueError, "ApprovedRiskAssessmentResult"):
            determine_approved_confidence(object())

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
            determine_approved_confidence(
                approved_risk(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_confidence_table_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            confidence_decision_table_set_version=(
                "unsupported-confidence-table-version"
            ),
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(ValueError, "confidence_decision_table_set_version"):
            determine_approved_confidence(
                approved_risk(),
                invalid_config,
            )

    def test_validation_fails_closed_for_missing_required_confidence_rule(self):
        confidence_rules = dict(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.confidence_decision_rules
        )
        del confidence_rules[DEFAULT_CONFIDENCE_DECISION_RULE_ID]
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            confidence_decision_rules=MappingProxyType(confidence_rules),
        )

        with self.assertRaisesRegex(ValueError, "Missing approved confidence"):
            determine_approved_confidence(
                approved_risk(),
                invalid_config,
            )

    def test_validation_fails_closed_for_invalid_confidence_rule_output(self):
        confidence_rules = dict(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.confidence_decision_rules
        )
        confidence_rules[DEFAULT_CONFIDENCE_DECISION_RULE_ID] = replace(
            confidence_rules[DEFAULT_CONFIDENCE_DECISION_RULE_ID],
            output="unsupported-confidence",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            confidence_decision_rules=MappingProxyType(confidence_rules),
        )

        with self.assertRaisesRegex(ValueError, "confidence decision rule output"):
            determine_approved_confidence(
                approved_risk(),
                invalid_config,
            )

    def test_validation_fails_closed_for_risk_methodology_version_mismatch(self):
        invalid_risk = replace(
            approved_risk(),
            methodology_version="unsupported-methodology-version",
        )

        with self.assertRaisesRegex(ValueError, "methodology version"):
            determine_approved_confidence(invalid_risk)

    def test_validation_fails_closed_for_risk_runtime_config_version_mismatch(self):
        invalid_risk = replace(
            approved_risk(),
            runtime_config_version="unsupported-runtime-config-version",
        )

        with self.assertRaisesRegex(ValueError, "runtime config version"):
            determine_approved_confidence(invalid_risk)

    def test_validation_fails_closed_for_risk_decision_table_version_mismatch(self):
        invalid_risk = replace(
            approved_risk(),
            risk_decision_table_version="unsupported-risk-table-version",
        )

        with self.assertRaisesRegex(ValueError, "Risk decision table version"):
            determine_approved_confidence(invalid_risk)

    def test_validation_fails_closed_for_unsupported_risk_classification(self):
        invalid_risk = replace(
            approved_risk(),
            risk_classification="unsupported-risk",
        )

        with self.assertRaisesRegex(ValueError, "Risk classification"):
            determine_approved_confidence(invalid_risk)

    def test_validation_fails_closed_for_missing_severity_classifications(self):
        invalid_risk = replace(
            approved_risk(),
            severity_classifications=(),
        )

        with self.assertRaisesRegex(ValueError, "severity classifications"):
            determine_approved_confidence(invalid_risk)

    def test_validation_fails_closed_for_unsupported_severity_classification(self):
        invalid_risk = replace(
            approved_risk(),
            severity_classifications=("unsupported-severity",),
        )

        with self.assertRaisesRegex(ValueError, "severity classification"):
            determine_approved_confidence(invalid_risk)

    def test_validation_fails_closed_for_invalid_readiness_classification(self):
        invalid_risk = replace(
            approved_risk(),
            readiness_classification="",
        )

        with self.assertRaisesRegex(ValueError, "readiness classification"):
            determine_approved_confidence(invalid_risk)

    def test_validation_fails_closed_for_invalid_overall_assessment_score(self):
        invalid_risk = replace(
            approved_risk(),
            overall_assessment_score=101,
        )

        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            determine_approved_confidence(invalid_risk)

    def test_validation_fails_closed_for_unsupported_risk_decision_identifier(self):
        invalid_risk = replace(
            approved_risk(),
            risk_decision_identifier="unsupported-risk-decision",
        )

        with self.assertRaisesRegex(ValueError, "Risk decision identifier"):
            determine_approved_confidence(invalid_risk)

    def test_validation_fails_closed_for_risk_decision_output_mismatch(self):
        invalid_risk = replace(
            approved_risk(),
            risk_classification="critical-risk",
        )

        with self.assertRaisesRegex(ValueError, "Risk classification"):
            determine_approved_confidence(invalid_risk)


if __name__ == "__main__":
    unittest.main()
