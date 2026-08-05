import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from types import MappingProxyType


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    QUESTION_SCORING_TABLES_VERSION,
)
from assessment.approved_question_scoring_runtime import (  # noqa: E402
    ApprovedQuestionScoringResult,
    CanonicalQuestionResponse,
    score_approved_questions,
)
from assessment.methodology_config import METHODOLOGY_VERSION  # noqa: E402


def valid_approved_responses(scale_value=4, numeric_value=50):
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


class ApprovedQuestionScoringRuntimeTests(unittest.TestCase):
    def test_scores_all_approved_questions_deterministically(self):
        responses = valid_approved_responses(scale_value=3, numeric_value=64)

        first = score_approved_questions(responses, METHODOLOGY_VERSION)
        second = score_approved_questions(responses, METHODOLOGY_VERSION)

        self.assertEqual(first, second)
        self.assertIsInstance(first, ApprovedQuestionScoringResult)
        self.assertEqual(first.question_count, 48)
        self.assertEqual(
            tuple(score.question_id for score in first.question_scores),
            tuple(APPROVED_METHODOLOGY_RUNTIME_CONFIG.questions),
        )

    def test_executes_approved_response_to_score_mappings(self):
        responses = valid_approved_responses(scale_value=2, numeric_value=37)

        result = score_approved_questions(responses, METHODOLOGY_VERSION)
        scores = {
            question_score.question_id: question_score.score
            for question_score in result.question_scores
        }

        self.assertEqual(scores["q.ai.governance.owner"], 50.0)
        self.assertEqual(scores["q.automation.manual-volume"], 37.0)

    def test_preserves_approved_question_metadata(self):
        result = score_approved_questions(
            valid_approved_responses(scale_value=1, numeric_value=25),
            METHODOLOGY_VERSION,
        )
        scores = {
            question_score.question_id: question_score
            for question_score in result.question_scores
        }
        score = scores["q.ai.strategy.business-goals"]

        self.assertEqual(score.question_id, "q.ai.strategy.business-goals")
        self.assertEqual(score.primary_dimension, "GCR")
        self.assertEqual(score.secondary_dimensions, ("TISM",))
        self.assertEqual(score.response_model_id, "scale-0-4")
        self.assertEqual(score.scoring_table_version, QUESTION_SCORING_TABLES_VERSION)
        self.assertEqual(score.taxonomy_version, "business-capability-taxonomy-v1")
        self.assertEqual(
            score.runtime_config_version,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
        )
        self.assertEqual(score.score, 25.0)

    def test_result_and_score_artifacts_are_immutable(self):
        result = score_approved_questions(
            valid_approved_responses(),
            METHODOLOGY_VERSION,
        )

        with self.assertRaises(FrozenInstanceError):
            result.question_count = 0
        with self.assertRaises(TypeError):
            result.question_scores[0] = None
        with self.assertRaises(FrozenInstanceError):
            result.question_scores[0].score = 0

    def test_accepts_canonical_response_entries_and_rejects_duplicates(self):
        responses = tuple(
            CanonicalQuestionResponse(question_id, value)
            for question_id, value in valid_approved_responses().items()
        )

        result = score_approved_questions(responses, METHODOLOGY_VERSION)

        self.assertEqual(result.question_count, 48)

        duplicate_responses = (
            *responses,
            CanonicalQuestionResponse("q.ai.governance.owner", 4),
        )
        with self.assertRaisesRegex(ValueError, "Duplicate question response"):
            score_approved_questions(duplicate_responses, METHODOLOGY_VERSION)

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
            score_approved_questions(
                valid_approved_responses(),
                METHODOLOGY_VERSION,
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_methodology_version(self):
        with self.assertRaisesRegex(ValueError, "Unsupported methodology version"):
            score_approved_questions(
                valid_approved_responses(),
                "unsupported-methodology-version",
            )

    def test_validation_fails_closed_for_missing_question(self):
        responses = valid_approved_responses()
        del responses["q.ai.governance.owner"]

        with self.assertRaisesRegex(ValueError, "Missing question response"):
            score_approved_questions(responses, METHODOLOGY_VERSION)

    def test_validation_fails_closed_for_unknown_question(self):
        responses = valid_approved_responses()
        responses["q.unknown"] = 4

        with self.assertRaisesRegex(ValueError, "Unknown question response"):
            score_approved_questions(responses, METHODOLOGY_VERSION)

    def test_validation_fails_closed_for_malformed_response_container(self):
        with self.assertRaisesRegex(ValueError, "Canonical question responses"):
            score_approved_questions("not-canonical", METHODOLOGY_VERSION)

        with self.assertRaisesRegex(
            ValueError,
            "Malformed canonical question response",
        ):
            score_approved_questions(
                (("q.ai.governance.owner", 4, "extra"),),
                METHODOLOGY_VERSION,
            )

    def test_validation_fails_closed_for_malformed_scale_response(self):
        responses = valid_approved_responses()
        responses["q.ai.governance.owner"] = 1.0

        with self.assertRaisesRegex(ValueError, "Malformed response"):
            score_approved_questions(responses, METHODOLOGY_VERSION)

    def test_validation_fails_closed_for_out_of_range_scale_response(self):
        responses = valid_approved_responses()
        responses["q.ai.governance.owner"] = 5

        with self.assertRaisesRegex(ValueError, "Out-of-range response"):
            score_approved_questions(responses, METHODOLOGY_VERSION)

    def test_validation_fails_closed_for_out_of_range_numeric_response(self):
        responses = valid_approved_responses()
        responses["q.automation.manual-volume"] = 101

        with self.assertRaisesRegex(ValueError, "Out-of-range response"):
            score_approved_questions(responses, METHODOLOGY_VERSION)

    def test_validation_fails_closed_for_unsupported_response_model(self):
        questions = dict(APPROVED_METHODOLOGY_RUNTIME_CONFIG.questions)
        questions["q.ai.governance.owner"] = replace(
            questions["q.ai.governance.owner"],
            response_model_id="unsupported-response-model",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            questions=MappingProxyType(questions),
        )

        with self.assertRaisesRegex(ValueError, "Unknown response model"):
            score_approved_questions(
                valid_approved_responses(),
                METHODOLOGY_VERSION,
                invalid_config,
            )


if __name__ == "__main__":
    unittest.main()
