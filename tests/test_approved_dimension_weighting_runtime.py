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
    ApprovedDimensionWeightingResult,
    weight_approved_dimensions,
)
from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_DIMENSION_ORDER,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    OFFICIAL_DIMENSION_WEIGHT_SET_VERSION,
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


def approved_dimension_aggregation(scale_value=2, numeric_value=50):
    question_scoring = score_approved_questions(
        approved_responses(scale_value, numeric_value),
        METHODOLOGY_VERSION,
    )
    return aggregate_approved_dimensions(question_scoring)


class ApprovedDimensionWeightingRuntimeTests(unittest.TestCase):
    def test_weights_approved_dimensions_deterministically(self):
        dimension_aggregation = approved_dimension_aggregation()

        first = weight_approved_dimensions(dimension_aggregation)
        second = weight_approved_dimensions(dimension_aggregation)

        self.assertEqual(first, second)
        self.assertIsInstance(first, ApprovedDimensionWeightingResult)
        self.assertEqual(first.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(
            first.runtime_config_version,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version,
        )
        self.assertEqual(
            first.weight_set_version,
            OFFICIAL_DIMENSION_WEIGHT_SET_VERSION,
        )
        self.assertEqual(first.dimension_count, 5)
        self.assertEqual(first.total_official_weight, 100)
        self.assertEqual(
            tuple(dimension.dimension_id for dimension in first.dimensions),
            APPROVED_DIMENSION_ORDER,
        )
        self.assertEqual(
            {
                dimension.dimension_id: dimension.official_weight
                for dimension in first.dimensions
            },
            {
                "POC": 18,
                "GCR": 24,
                "TISM": 22,
                "DPSC": 20,
                "RVCI": 16,
            },
        )
        self.assertTrue(
            all(
                dimension.raw_aggregated_score == 50.0
                for dimension in first.dimensions
            )
        )
        self.assertEqual(
            {
                dimension.dimension_id: dimension.weighted_score
                for dimension in first.dimensions
            },
            {
                "POC": 9.0,
                "GCR": 12.0,
                "TISM": 11.0,
                "DPSC": 10.0,
                "RVCI": 8.0,
            },
        )

    def test_preserves_weighted_dimension_metadata(self):
        result = weight_approved_dimensions(
            approved_dimension_aggregation(scale_value=3, numeric_value=75)
        )
        dimensions = {
            dimension.dimension_id: dimension
            for dimension in result.dimensions
        }

        governance = dimensions["GCR"]
        self.assertEqual(
            governance.dimension_name,
            "Governance, Compliance & Regulatory Readiness",
        )
        self.assertEqual(governance.raw_aggregated_score, 75.0)
        self.assertEqual(governance.official_weight, 24)
        self.assertEqual(governance.weighted_score, 18.0)
        self.assertEqual(governance.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(
            governance.runtime_config_version,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version,
        )
        self.assertEqual(
            governance.weight_set_version,
            OFFICIAL_DIMENSION_WEIGHT_SET_VERSION,
        )

    def test_result_and_weighted_dimension_artifacts_are_immutable(self):
        result = weight_approved_dimensions(approved_dimension_aggregation())

        with self.assertRaises(FrozenInstanceError):
            result.dimension_count = 0
        with self.assertRaises(TypeError):
            result.dimensions[0] = None
        with self.assertRaises(FrozenInstanceError):
            result.dimensions[0].weighted_score = 0

    def test_validation_fails_closed_for_non_aggregation_result(self):
        with self.assertRaisesRegex(ValueError, "ApprovedDimensionAggregationResult"):
            weight_approved_dimensions(object())

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
            weight_approved_dimensions(
                approved_dimension_aggregation(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_weight_set_version(self):
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
            weight_approved_dimensions(
                approved_dimension_aggregation(),
                invalid_config,
            )

    def test_validation_fails_closed_for_weight_total_mismatch(self):
        dimensions = dict(APPROVED_METHODOLOGY_RUNTIME_CONFIG.dimensions)
        dimensions["POC"] = replace(dimensions["POC"], weight=19)
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            dimensions=MappingProxyType(dimensions),
        )

        with self.assertRaisesRegex(ValueError, "weights must sum to 100"):
            weight_approved_dimensions(
                approved_dimension_aggregation(),
                invalid_config,
            )

    def test_validation_fails_closed_for_methodology_version_mismatch(self):
        invalid_aggregation = replace(
            approved_dimension_aggregation(),
            methodology_version="unsupported-methodology-version",
        )

        with self.assertRaisesRegex(ValueError, "methodology version"):
            weight_approved_dimensions(invalid_aggregation)

    def test_validation_fails_closed_for_runtime_config_version_mismatch(self):
        invalid_aggregation = replace(
            approved_dimension_aggregation(),
            runtime_config_version="unsupported-runtime-config-version",
        )

        with self.assertRaisesRegex(ValueError, "runtime config version"):
            weight_approved_dimensions(invalid_aggregation)

    def test_validation_fails_closed_for_missing_dimension(self):
        aggregation = approved_dimension_aggregation()
        invalid_aggregation = replace(
            aggregation,
            dimension_count=4,
            dimensions=aggregation.dimensions[:-1],
        )

        with self.assertRaisesRegex(ValueError, "5 dimensions"):
            weight_approved_dimensions(invalid_aggregation)

    def test_validation_fails_closed_for_duplicate_dimension(self):
        aggregation = approved_dimension_aggregation()
        invalid_aggregation = replace(
            aggregation,
            dimensions=(
                aggregation.dimensions[0],
                aggregation.dimensions[0],
                *aggregation.dimensions[2:],
            ),
        )

        with self.assertRaisesRegex(ValueError, "Duplicate approved dimension"):
            weight_approved_dimensions(invalid_aggregation)

    def test_validation_fails_closed_for_unknown_dimension(self):
        aggregation = approved_dimension_aggregation()
        unknown_dimension = replace(
            aggregation.dimensions[0],
            dimension_id="UNKNOWN",
        )
        invalid_aggregation = replace(
            aggregation,
            dimensions=(unknown_dimension, *aggregation.dimensions[1:]),
        )

        with self.assertRaisesRegex(ValueError, "Unknown approved dimension"):
            weight_approved_dimensions(invalid_aggregation)

    def test_validation_fails_closed_for_dimension_metadata_mismatch(self):
        aggregation = approved_dimension_aggregation()
        mismatched_dimension = replace(
            aggregation.dimensions[0],
            dimension_name="Unsupported Dimension",
        )
        invalid_aggregation = replace(
            aggregation,
            dimensions=(mismatched_dimension, *aggregation.dimensions[1:]),
        )

        with self.assertRaisesRegex(ValueError, "dimension name mismatch"):
            weight_approved_dimensions(invalid_aggregation)

    def test_validation_fails_closed_for_invalid_dimension_score(self):
        aggregation = approved_dimension_aggregation()
        invalid_dimension = replace(
            aggregation.dimensions[0],
            score=101,
        )
        invalid_aggregation = replace(
            aggregation,
            dimensions=(invalid_dimension, *aggregation.dimensions[1:]),
        )

        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            weight_approved_dimensions(invalid_aggregation)


if __name__ == "__main__":
    unittest.main()
