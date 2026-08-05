import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.approved_dimension_aggregation_runtime import (  # noqa: E402
    aggregate_approved_dimensions,
)
from assessment.approved_dimension_weighting_runtime import (  # noqa: E402
    weight_approved_dimensions,
)
from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    READINESS_BOUNDARY_CONVENTION_VERSION,
    READINESS_THRESHOLD_SET_VERSION,
    READINESS_THRESHOLD_VALUES_VERSION,
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
    READINESS_ASSIGNMENT_METHOD,
    ApprovedReadinessAssessmentResult,
    determine_approved_readiness,
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


def approved_overall_assessment(scale_value=2, numeric_value=50):
    question_scoring = score_approved_questions(
        approved_responses(scale_value, numeric_value),
        METHODOLOGY_VERSION,
    )
    dimension_aggregation = aggregate_approved_dimensions(question_scoring)
    dimension_weighting = weight_approved_dimensions(dimension_aggregation)
    return calculate_approved_overall_assessment(dimension_weighting)


def approved_overall_assessment_with_score(score):
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

    return ApprovedOverallAssessmentResult(
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


class ApprovedReadinessRuntimeTests(unittest.TestCase):
    def test_assigns_readiness_deterministically(self):
        overall_assessment = approved_overall_assessment()

        first = determine_approved_readiness(overall_assessment)
        second = determine_approved_readiness(overall_assessment)

        self.assertEqual(first, second)
        self.assertIsInstance(first, ApprovedReadinessAssessmentResult)
        self.assertEqual(first.readiness_classification, "Ready")
        self.assertEqual(first.readiness_score, 50.0)
        self.assertEqual(first.readiness_threshold_id, "ready")
        self.assertEqual(first.threshold_lower_bound, 50)
        self.assertEqual(first.threshold_upper_bound, 75)
        self.assertTrue(first.threshold_lower_inclusive)
        self.assertFalse(first.threshold_upper_inclusive)
        self.assertEqual(first.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(
            first.runtime_config_version,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version,
        )
        self.assertEqual(
            first.readiness_threshold_version,
            READINESS_THRESHOLD_VALUES_VERSION,
        )
        self.assertEqual(
            first.readiness_threshold_set_version,
            READINESS_THRESHOLD_SET_VERSION,
        )
        self.assertEqual(
            first.readiness_boundary_convention_version,
            READINESS_BOUNDARY_CONVENTION_VERSION,
        )
        self.assertEqual(first.assignment_method, READINESS_ASSIGNMENT_METHOD)

    def test_applies_approved_boundary_convention(self):
        cases = (
            (0, "Not Ready", "not-ready"),
            (25, "Developing", "developing"),
            (50, "Ready", "ready"),
            (75, "Advanced", "advanced"),
            (100, "Advanced", "advanced"),
        )

        for score, classification, threshold_id in cases:
            with self.subTest(score=score):
                result = determine_approved_readiness(
                    approved_overall_assessment_with_score(score)
                )

                self.assertEqual(result.readiness_classification, classification)
                self.assertEqual(result.readiness_threshold_id, threshold_id)
                self.assertEqual(result.readiness_score, float(score))

    def test_result_artifact_is_immutable(self):
        result = determine_approved_readiness(approved_overall_assessment())

        with self.assertRaises(FrozenInstanceError):
            result.readiness_classification = "Advanced"

    def test_validation_fails_closed_for_non_overall_result(self):
        with self.assertRaisesRegex(ValueError, "ApprovedOverallAssessmentResult"):
            determine_approved_readiness(object())

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
            determine_approved_readiness(
                approved_overall_assessment(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_threshold_values_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            readiness_threshold_values_version="unsupported-threshold-values-version",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(ValueError, "readiness_threshold_values_version"):
            determine_approved_readiness(
                approved_overall_assessment(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_threshold_set_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            readiness_threshold_set_version="unsupported-threshold-set-version",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(ValueError, "readiness_threshold_set_version"):
            determine_approved_readiness(
                approved_overall_assessment(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_boundary_convention_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            readiness_boundary_convention_version="unsupported-boundary-version",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(
            ValueError,
            "readiness_boundary_convention_version",
        ):
            determine_approved_readiness(
                approved_overall_assessment(),
                invalid_config,
            )

    def test_validation_fails_closed_for_methodology_version_mismatch(self):
        invalid_overall = replace(
            approved_overall_assessment(),
            methodology_version="unsupported-methodology-version",
        )

        with self.assertRaisesRegex(ValueError, "methodology version"):
            determine_approved_readiness(invalid_overall)

    def test_validation_fails_closed_for_runtime_config_version_mismatch(self):
        invalid_overall = replace(
            approved_overall_assessment(),
            runtime_config_version="unsupported-runtime-config-version",
        )

        with self.assertRaisesRegex(ValueError, "runtime config version"):
            determine_approved_readiness(invalid_overall)

    def test_validation_fails_closed_for_missing_dimension_contribution(self):
        overall = approved_overall_assessment()
        invalid_overall = replace(
            overall,
            dimension_count=4,
            weighted_dimension_contributions=(
                overall.weighted_dimension_contributions[:-1]
            ),
        )

        with self.assertRaisesRegex(ValueError, "5 dimension contributions"):
            determine_approved_readiness(invalid_overall)

    def test_validation_fails_closed_for_invalid_overall_score(self):
        invalid_overall = replace(
            approved_overall_assessment(),
            overall_assessment_score=101,
        )

        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            determine_approved_readiness(invalid_overall)

    def test_validation_fails_closed_for_contribution_mismatch(self):
        invalid_overall = replace(
            approved_overall_assessment(),
            overall_assessment_score=49,
        )

        with self.assertRaisesRegex(ValueError, "does not match contributions"):
            determine_approved_readiness(invalid_overall)


if __name__ == "__main__":
    unittest.main()
