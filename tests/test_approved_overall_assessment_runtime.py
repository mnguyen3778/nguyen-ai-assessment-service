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
    APPROVED_DIMENSION_ORDER,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    OFFICIAL_DIMENSION_WEIGHT_SET_VERSION,
)
from assessment.approved_overall_assessment_runtime import (  # noqa: E402
    OVERALL_ASSESSMENT_CALCULATION_METHOD,
    ApprovedOverallAssessmentResult,
    calculate_approved_overall_assessment,
)
from assessment.approved_question_scoring_runtime import (  # noqa: E402
    score_approved_questions,
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


def approved_dimension_weighting(scale_value=2, numeric_value=50):
    question_scoring = score_approved_questions(
        approved_responses(scale_value, numeric_value),
        METHODOLOGY_VERSION,
    )
    dimension_aggregation = aggregate_approved_dimensions(question_scoring)
    return weight_approved_dimensions(dimension_aggregation)


class ApprovedOverallAssessmentRuntimeTests(unittest.TestCase):
    def test_calculates_overall_assessment_deterministically(self):
        dimension_weighting = approved_dimension_weighting()

        first = calculate_approved_overall_assessment(dimension_weighting)
        second = calculate_approved_overall_assessment(dimension_weighting)

        self.assertEqual(first, second)
        self.assertIsInstance(first, ApprovedOverallAssessmentResult)
        self.assertEqual(first.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(
            first.runtime_config_version,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version,
        )
        self.assertEqual(
            first.weight_set_version,
            OFFICIAL_DIMENSION_WEIGHT_SET_VERSION,
        )
        self.assertEqual(
            first.calculation_method,
            OVERALL_ASSESSMENT_CALCULATION_METHOD,
        )
        self.assertEqual(first.dimension_count, 5)
        self.assertEqual(first.total_official_weight, 100)
        self.assertEqual(first.overall_assessment_score, 50.0)
        self.assertEqual(
            tuple(
                contribution.dimension_id
                for contribution in first.weighted_dimension_contributions
            ),
            APPROVED_DIMENSION_ORDER,
        )

    def test_preserves_weighted_dimension_contributions(self):
        result = calculate_approved_overall_assessment(
            approved_dimension_weighting(scale_value=3, numeric_value=75)
        )
        contributions = {
            contribution.dimension_id: contribution
            for contribution in result.weighted_dimension_contributions
        }

        governance = contributions["GCR"]
        self.assertEqual(
            governance.dimension_name,
            "Governance, Compliance & Regulatory Readiness",
        )
        self.assertEqual(governance.raw_aggregated_score, 75.0)
        self.assertEqual(governance.official_weight, 24)
        self.assertEqual(governance.weighted_score, 18.0)
        self.assertEqual(result.overall_assessment_score, 75.0)

    def test_result_and_contribution_artifacts_are_immutable(self):
        result = calculate_approved_overall_assessment(
            approved_dimension_weighting()
        )

        with self.assertRaises(FrozenInstanceError):
            result.overall_assessment_score = 0
        with self.assertRaises(TypeError):
            result.weighted_dimension_contributions[0] = None
        with self.assertRaises(FrozenInstanceError):
            result.weighted_dimension_contributions[0].weighted_score = 0

    def test_validation_fails_closed_for_non_weighting_result(self):
        with self.assertRaisesRegex(ValueError, "ApprovedDimensionWeightingResult"):
            calculate_approved_overall_assessment(object())

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
            calculate_approved_overall_assessment(
                approved_dimension_weighting(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_config_weight_set_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            official_dimension_weight_set_version="unsupported-weight-set-version",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(
            ValueError,
            "official_dimension_weight_set_version",
        ):
            calculate_approved_overall_assessment(
                approved_dimension_weighting(),
                invalid_config,
            )

    def test_validation_fails_closed_for_methodology_version_mismatch(self):
        invalid_weighting = replace(
            approved_dimension_weighting(),
            methodology_version="unsupported-methodology-version",
        )

        with self.assertRaisesRegex(ValueError, "methodology version"):
            calculate_approved_overall_assessment(invalid_weighting)

    def test_validation_fails_closed_for_runtime_config_version_mismatch(self):
        invalid_weighting = replace(
            approved_dimension_weighting(),
            runtime_config_version="unsupported-runtime-config-version",
        )

        with self.assertRaisesRegex(ValueError, "runtime config version"):
            calculate_approved_overall_assessment(invalid_weighting)

    def test_validation_fails_closed_for_weight_set_version_mismatch(self):
        invalid_weighting = replace(
            approved_dimension_weighting(),
            weight_set_version="unsupported-weight-set-version",
        )

        with self.assertRaisesRegex(ValueError, "weight set version"):
            calculate_approved_overall_assessment(invalid_weighting)

    def test_validation_fails_closed_for_missing_dimension(self):
        weighting = approved_dimension_weighting()
        invalid_weighting = replace(
            weighting,
            dimension_count=4,
            dimensions=weighting.dimensions[:-1],
        )

        with self.assertRaisesRegex(ValueError, "5 dimensions"):
            calculate_approved_overall_assessment(invalid_weighting)

    def test_validation_fails_closed_for_duplicate_dimension(self):
        weighting = approved_dimension_weighting()
        invalid_weighting = replace(
            weighting,
            dimensions=(
                weighting.dimensions[0],
                weighting.dimensions[0],
                *weighting.dimensions[2:],
            ),
        )

        with self.assertRaisesRegex(ValueError, "Duplicate approved weighted dimension"):
            calculate_approved_overall_assessment(invalid_weighting)

    def test_validation_fails_closed_for_unknown_dimension(self):
        weighting = approved_dimension_weighting()
        unknown_dimension = replace(
            weighting.dimensions[0],
            dimension_id="UNKNOWN",
        )
        invalid_weighting = replace(
            weighting,
            dimensions=(unknown_dimension, *weighting.dimensions[1:]),
        )

        with self.assertRaisesRegex(ValueError, "Unknown approved weighted dimension"):
            calculate_approved_overall_assessment(invalid_weighting)

    def test_validation_fails_closed_for_dimension_metadata_mismatch(self):
        weighting = approved_dimension_weighting()
        mismatched_dimension = replace(
            weighting.dimensions[0],
            dimension_name="Unsupported Dimension",
        )
        invalid_weighting = replace(
            weighting,
            dimensions=(mismatched_dimension, *weighting.dimensions[1:]),
        )

        with self.assertRaisesRegex(ValueError, "dimension name mismatch"):
            calculate_approved_overall_assessment(invalid_weighting)

    def test_validation_fails_closed_for_weight_mismatch(self):
        weighting = approved_dimension_weighting()
        mismatched_dimension = replace(
            weighting.dimensions[0],
            official_weight=99,
        )
        invalid_weighting = replace(
            weighting,
            dimensions=(mismatched_dimension, *weighting.dimensions[1:]),
        )

        with self.assertRaisesRegex(ValueError, "dimension weight mismatch"):
            calculate_approved_overall_assessment(invalid_weighting)

    def test_validation_fails_closed_for_total_weight_mismatch(self):
        invalid_weighting = replace(
            approved_dimension_weighting(),
            total_official_weight=99,
        )

        with self.assertRaisesRegex(ValueError, "total weight of 100"):
            calculate_approved_overall_assessment(invalid_weighting)

    def test_validation_fails_closed_for_invalid_raw_score(self):
        weighting = approved_dimension_weighting()
        invalid_dimension = replace(
            weighting.dimensions[0],
            raw_aggregated_score=101,
        )
        invalid_weighting = replace(
            weighting,
            dimensions=(invalid_dimension, *weighting.dimensions[1:]),
        )

        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            calculate_approved_overall_assessment(invalid_weighting)

    def test_validation_fails_closed_for_contribution_mismatch(self):
        weighting = approved_dimension_weighting()
        invalid_dimension = replace(
            weighting.dimensions[0],
            weighted_score=weighting.dimensions[0].weighted_score + 1,
        )
        invalid_weighting = replace(
            weighting,
            dimensions=(invalid_dimension, *weighting.dimensions[1:]),
        )

        with self.assertRaisesRegex(ValueError, "contribution mismatch"):
            calculate_approved_overall_assessment(invalid_weighting)


if __name__ == "__main__":
    unittest.main()
