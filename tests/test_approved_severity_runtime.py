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
    SEVERITY_DECISION_TABLE_SET_VERSION,
)
from assessment.approved_overall_assessment_runtime import (  # noqa: E402
    ApprovedOverallAssessmentResult,
    ApprovedOverallDimensionContribution,
    calculate_approved_overall_assessment,
)
from assessment.approved_question_scoring_runtime import (  # noqa: E402
    score_approved_questions,
)
from assessment.approved_readiness_runtime import (  # noqa: E402
    determine_approved_readiness,
)
from assessment.approved_severity_runtime import (  # noqa: E402
    SEVERITY_ASSIGNMENT_METHOD,
    ApprovedSeverityAssessmentResult,
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


def approved_readiness(scale_value=2, numeric_value=50):
    question_scoring = score_approved_questions(
        approved_responses(scale_value, numeric_value),
        METHODOLOGY_VERSION,
    )
    dimension_aggregation = aggregate_approved_dimensions(question_scoring)
    dimension_weighting = weight_approved_dimensions(dimension_aggregation)
    overall_assessment = calculate_approved_overall_assessment(dimension_weighting)
    return determine_approved_readiness(overall_assessment)


def approved_readiness_with_score(score):
    contributions = tuple(
        ApprovedOverallDimensionContribution(
            dimension_id=dimension.id,
            dimension_name=dimension.label,
            raw_aggregated_score=float(score),
            official_weight=dimension.weight,
            weighted_score=float(score) * dimension.weight / 100,
        )
        for dimension in APPROVED_METHODOLOGY_RUNTIME_CONFIG.dimensions.values()
    )
    overall_assessment = ApprovedOverallAssessmentResult(
        overall_assessment_score=sum(
            contribution.weighted_score
            for contribution in contributions
        ),
        weighted_dimension_contributions=contributions,
        methodology_version=METHODOLOGY_VERSION,
        runtime_config_version=(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version
        ),
        weight_set_version=(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG
            .version_manifest
            .official_dimension_weight_set_version
        ),
        calculation_method="weighted-dimension-contribution-sum-v1",
        dimension_count=len(contributions),
        total_official_weight=100,
    )
    return determine_approved_readiness(overall_assessment)


class ApprovedSeverityRuntimeTests(unittest.TestCase):
    def test_assigns_severity_deterministically(self):
        readiness = approved_readiness()

        first = determine_approved_severity(readiness)
        second = determine_approved_severity(readiness)

        self.assertEqual(first, second)
        self.assertIsInstance(first, ApprovedSeverityAssessmentResult)
        self.assertEqual(first.severity_classification, "medium")
        self.assertEqual(first.readiness_classification, "Ready")
        self.assertEqual(first.readiness_score, 50.0)
        self.assertEqual(
            first.severity_decision_identifier,
            "severity-v1-deficiency-medium",
        )
        self.assertEqual(
            first.decision_table_version,
            SEVERITY_DECISION_TABLE_SET_VERSION,
        )
        self.assertEqual(first.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(
            first.runtime_config_version,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version,
        )
        self.assertEqual(first.assignment_method, SEVERITY_ASSIGNMENT_METHOD)

    def test_applies_approved_severity_rules_by_readiness_context(self):
        cases = (
            (0, "critical", "severity-v1-deficiency-critical"),
            (25, "high", "severity-v1-deficiency-high"),
            (50, "medium", "severity-v1-deficiency-medium"),
            (75, "informational", "severity-v1-observation-informational"),
            (100, "informational", "severity-v1-observation-informational"),
        )

        for score, severity, rule_id in cases:
            with self.subTest(score=score):
                result = determine_approved_severity(
                    approved_readiness_with_score(score)
                )

                self.assertEqual(result.severity_classification, severity)
                self.assertEqual(result.severity_decision_identifier, rule_id)
                self.assertEqual(result.readiness_score, float(score))

    def test_result_artifact_is_immutable(self):
        result = determine_approved_severity(approved_readiness())

        with self.assertRaises(FrozenInstanceError):
            result.severity_classification = "critical"

    def test_validation_fails_closed_for_non_readiness_result(self):
        with self.assertRaisesRegex(ValueError, "ApprovedReadinessAssessmentResult"):
            determine_approved_severity(object())

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
            determine_approved_severity(
                approved_readiness(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_severity_table_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            severity_decision_table_set_version="unsupported-severity-table-version",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(
            ValueError,
            "severity_decision_table_set_version",
        ):
            determine_approved_severity(
                approved_readiness(),
                invalid_config,
            )

    def test_validation_fails_closed_for_missing_required_severity_rule(self):
        severity_rules = dict(APPROVED_METHODOLOGY_RUNTIME_CONFIG.severity_decision_rules)
        del severity_rules["severity-v1-deficiency-medium"]
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            severity_decision_rules=MappingProxyType(severity_rules),
        )

        with self.assertRaisesRegex(ValueError, "Missing approved severity"):
            determine_approved_severity(
                approved_readiness(),
                invalid_config,
            )

    def test_validation_fails_closed_for_invalid_severity_rule_output(self):
        severity_rules = dict(APPROVED_METHODOLOGY_RUNTIME_CONFIG.severity_decision_rules)
        severity_rules["severity-v1-deficiency-medium"] = replace(
            severity_rules["severity-v1-deficiency-medium"],
            output="unsupported-severity",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            severity_decision_rules=MappingProxyType(severity_rules),
        )

        with self.assertRaisesRegex(ValueError, "severity decision rule output"):
            determine_approved_severity(
                approved_readiness(),
                invalid_config,
            )

    def test_validation_fails_closed_for_readiness_methodology_version_mismatch(self):
        invalid_readiness = replace(
            approved_readiness(),
            methodology_version="unsupported-methodology-version",
        )

        with self.assertRaisesRegex(ValueError, "methodology version"):
            determine_approved_severity(invalid_readiness)

    def test_validation_fails_closed_for_readiness_runtime_config_version_mismatch(self):
        invalid_readiness = replace(
            approved_readiness(),
            runtime_config_version="unsupported-runtime-config-version",
        )

        with self.assertRaisesRegex(ValueError, "runtime config version"):
            determine_approved_severity(invalid_readiness)

    def test_validation_fails_closed_for_readiness_threshold_version_mismatch(self):
        invalid_readiness = replace(
            approved_readiness(),
            readiness_threshold_version="unsupported-threshold-values-version",
        )

        with self.assertRaisesRegex(ValueError, "threshold values version"):
            determine_approved_severity(invalid_readiness)

    def test_validation_fails_closed_for_readiness_classification_mismatch(self):
        invalid_readiness = replace(
            approved_readiness(),
            readiness_classification="Advanced",
        )

        with self.assertRaisesRegex(ValueError, "classification"):
            determine_approved_severity(invalid_readiness)

    def test_validation_fails_closed_for_readiness_threshold_metadata_mismatch(self):
        invalid_readiness = replace(
            approved_readiness(),
            threshold_lower_bound=0,
        )

        with self.assertRaisesRegex(ValueError, "threshold metadata"):
            determine_approved_severity(invalid_readiness)

    def test_validation_fails_closed_for_invalid_readiness_score(self):
        invalid_readiness = replace(
            approved_readiness(),
            readiness_score=101,
        )

        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            determine_approved_severity(invalid_readiness)

    def test_validation_fails_closed_for_readiness_score_threshold_mismatch(self):
        invalid_readiness = replace(
            approved_readiness(),
            readiness_score=49,
        )

        with self.assertRaisesRegex(ValueError, "threshold range"):
            determine_approved_severity(invalid_readiness)


if __name__ == "__main__":
    unittest.main()
