import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from types import MappingProxyType


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.approved_dimension_aggregation_runtime import (  # noqa: E402
    DIMENSION_AGGREGATION_METHOD,
    ApprovedDimensionAggregationResult,
    aggregate_approved_dimensions,
)
from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_DIMENSION_ORDER,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    SCORING_SCALE_VERSION,
)
from assessment.approved_question_scoring_runtime import (  # noqa: E402
    ApprovedQuestionScore,
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


def approved_question_scoring(scale_value=2, numeric_value=50):
    return score_approved_questions(
        approved_responses(scale_value, numeric_value),
        METHODOLOGY_VERSION,
    )


class ApprovedDimensionAggregationRuntimeTests(unittest.TestCase):
    def test_aggregates_approved_question_scores_deterministically(self):
        question_scoring = approved_question_scoring(scale_value=2, numeric_value=50)

        first = aggregate_approved_dimensions(question_scoring)
        second = aggregate_approved_dimensions(question_scoring)

        self.assertEqual(first, second)
        self.assertIsInstance(first, ApprovedDimensionAggregationResult)
        self.assertEqual(first.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(first.aggregation_method, DIMENSION_AGGREGATION_METHOD)
        self.assertEqual(first.dimension_count, 5)
        self.assertEqual(
            tuple(dimension.dimension_id for dimension in first.dimensions),
            APPROVED_DIMENSION_ORDER,
        )
        self.assertTrue(
            all(dimension.score == 50.0 for dimension in first.dimensions)
        )

    def test_preserves_dimension_metadata_and_contributing_scores(self):
        result = aggregate_approved_dimensions(
            approved_question_scoring(scale_value=3, numeric_value=75)
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
        self.assertEqual(governance.question_count, 12)
        self.assertEqual(governance.expected_question_count, 12)
        self.assertEqual(governance.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(
            governance.runtime_config_version,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version,
        )
        self.assertEqual(governance.scoring_scale_version, SCORING_SCALE_VERSION)
        self.assertEqual(
            governance.contributing_question_ids,
            tuple(sorted(governance.contributing_scores)),
        )
        self.assertIn(
            "q.ai.governance.owner",
            governance.contributing_question_ids,
        )
        self.assertEqual(
            governance.contributing_scores["q.ai.governance.owner"],
            75.0,
        )

    def test_dimension_question_counts_match_approved_distribution(self):
        result = aggregate_approved_dimensions(approved_question_scoring())

        self.assertEqual(
            {
                dimension.dimension_id: dimension.question_count
                for dimension in result.dimensions
            },
            {
                "POC": 14,
                "GCR": 12,
                "TISM": 12,
                "DPSC": 4,
                "RVCI": 6,
            },
        )

    def test_result_and_dimension_artifacts_are_immutable(self):
        result = aggregate_approved_dimensions(approved_question_scoring())

        with self.assertRaises(FrozenInstanceError):
            result.dimension_count = 0
        with self.assertRaises(TypeError):
            result.dimensions[0] = None
        with self.assertRaises(FrozenInstanceError):
            result.dimensions[0].score = 0
        with self.assertRaises(TypeError):
            result.dimensions[0].contributing_scores["q.unknown"] = 0

    def test_validation_fails_closed_for_non_scoring_result(self):
        with self.assertRaisesRegex(ValueError, "ApprovedQuestionScoringResult"):
            aggregate_approved_dimensions(object())

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
            aggregate_approved_dimensions(
                approved_question_scoring(),
                invalid_config,
            )

    def test_validation_fails_closed_for_methodology_version_mismatch(self):
        invalid_scoring = replace(
            approved_question_scoring(),
            methodology_version="unsupported-methodology-version",
        )

        with self.assertRaisesRegex(ValueError, "methodology version"):
            aggregate_approved_dimensions(invalid_scoring)

    def test_validation_fails_closed_for_runtime_config_version_mismatch(self):
        invalid_scoring = replace(
            approved_question_scoring(),
            runtime_config_version="unsupported-runtime-config-version",
        )

        with self.assertRaisesRegex(ValueError, "runtime config version"):
            aggregate_approved_dimensions(invalid_scoring)

    def test_validation_fails_closed_for_missing_question_score(self):
        scoring = approved_question_scoring()
        invalid_scoring = replace(
            scoring,
            question_count=47,
            question_scores=scoring.question_scores[:-1],
        )

        with self.assertRaisesRegex(ValueError, "48 question scores"):
            aggregate_approved_dimensions(invalid_scoring)

    def test_validation_fails_closed_for_duplicate_question_score(self):
        scoring = approved_question_scoring()
        invalid_scoring = replace(
            scoring,
            question_scores=(
                scoring.question_scores[0],
                *scoring.question_scores[:-1],
            ),
        )

        with self.assertRaisesRegex(ValueError, "Duplicate question score"):
            aggregate_approved_dimensions(invalid_scoring)

    def test_validation_fails_closed_for_unknown_question_score(self):
        scoring = approved_question_scoring()
        unknown_score = replace(
            scoring.question_scores[0],
            question_id="q.unknown",
        )
        invalid_scoring = replace(
            scoring,
            question_scores=(unknown_score, *scoring.question_scores[1:]),
        )

        with self.assertRaisesRegex(ValueError, "Unknown question score"):
            aggregate_approved_dimensions(invalid_scoring)

    def test_validation_fails_closed_for_question_metadata_mismatch(self):
        scoring = approved_question_scoring()
        mismatched_score = replace(
            scoring.question_scores[0],
            primary_dimension="POC",
        )
        invalid_scoring = replace(
            scoring,
            question_scores=(mismatched_score, *scoring.question_scores[1:]),
        )

        with self.assertRaisesRegex(ValueError, "Primary Dimension mismatch"):
            aggregate_approved_dimensions(invalid_scoring)

    def test_validation_fails_closed_for_invalid_question_score_value(self):
        scoring = approved_question_scoring()
        invalid_score = replace(
            scoring.question_scores[0],
            score=101,
        )
        invalid_scoring = replace(
            scoring,
            question_scores=(invalid_score, *scoring.question_scores[1:]),
        )

        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            aggregate_approved_dimensions(invalid_scoring)

    def test_validation_fails_closed_for_missing_dimension_representation(self):
        scoring = approved_question_scoring()
        altered_scores: list[ApprovedQuestionScore] = []
        for question_score in scoring.question_scores:
            if question_score.primary_dimension == "DPSC":
                altered_scores.append(
                    replace(question_score, primary_dimension="POC")
                )
            else:
                altered_scores.append(question_score)
        invalid_scoring = replace(
            scoring,
            question_scores=tuple(altered_scores),
        )

        with self.assertRaisesRegex(ValueError, "Primary Dimension mismatch"):
            aggregate_approved_dimensions(invalid_scoring)


if __name__ == "__main__":
    unittest.main()
