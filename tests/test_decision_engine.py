import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.decision_engine import (  # noqa: E402
    QuestionEvaluation,
    evaluate_decision,
)


class DecisionEngineTests(unittest.TestCase):
    def test_evaluate_decision_aggregates_scores_by_dimension(self):
        result = evaluate_decision(
            (
                QuestionEvaluation(
                    question_id="q.ai.strategy.business-goals",
                    readiness_dimension="ai-readiness",
                    normalized_score=50,
                    weight=1,
                ),
                QuestionEvaluation(
                    question_id="q.ai.governance.owner",
                    readiness_dimension="ai-readiness",
                    normalized_score=100,
                    weight=3,
                ),
                QuestionEvaluation(
                    question_id="q.security.identity.mfa",
                    readiness_dimension="security-readiness",
                    normalized_score=25,
                    weight=2,
                ),
            )
        )

        self.assertEqual(result.question_count, 3)
        self.assertEqual(result.total_weight, 6)
        self.assertAlmostEqual(result.overall_score, 66.66666666666667)
        self.assertEqual(
            tuple(result.dimensions),
            ("ai-readiness", "security-readiness"),
        )

        ai_dimension = result.dimensions["ai-readiness"]
        self.assertEqual(ai_dimension.dimension_id, "ai-readiness")
        self.assertEqual(ai_dimension.question_count, 2)
        self.assertEqual(ai_dimension.total_weight, 4)
        self.assertAlmostEqual(ai_dimension.normalized_score, 87.5)
        self.assertEqual(
            ai_dimension.contributing_questions,
            (
                "q.ai.governance.owner",
                "q.ai.strategy.business-goals",
            ),
        )

        security_dimension = result.dimensions["security-readiness"]
        self.assertEqual(security_dimension.question_count, 1)
        self.assertAlmostEqual(security_dimension.normalized_score, 25)

    def test_evaluate_decision_is_deterministic_for_same_inputs(self):
        evaluations = (
            QuestionEvaluation(
                question_id="q.business.outcomes-defined",
                readiness_dimension="business-readiness",
                normalized_score=70,
                weight=2,
            ),
            QuestionEvaluation(
                question_id="q.business.executive-alignment",
                readiness_dimension="business-readiness",
                normalized_score=90,
                weight=1,
            ),
        )

        self.assertEqual(evaluate_decision(evaluations), evaluate_decision(evaluations))

    def test_evaluate_decision_rejects_empty_input(self):
        with self.assertRaisesRegex(ValueError, "At least one"):
            evaluate_decision(())

    def test_evaluate_decision_rejects_duplicate_questions(self):
        evaluations = (
            QuestionEvaluation(
                question_id="q.ai.governance.owner",
                readiness_dimension="ai-readiness",
                normalized_score=50,
            ),
            QuestionEvaluation(
                question_id="q.ai.governance.owner",
                readiness_dimension="ai-readiness",
                normalized_score=75,
            ),
        )

        with self.assertRaisesRegex(ValueError, "Duplicate question"):
            evaluate_decision(evaluations)

    def test_evaluate_decision_rejects_invalid_scores(self):
        invalid_scores = (-1, 101, True, "high")

        for score in invalid_scores:
            with self.subTest(score=score):
                with self.assertRaisesRegex(ValueError, "normalized_score"):
                    evaluate_decision(
                        (
                            QuestionEvaluation(
                                question_id="q.ai.governance.owner",
                                readiness_dimension="ai-readiness",
                                normalized_score=score,
                            ),
                        )
                    )

    def test_evaluate_decision_rejects_invalid_weights(self):
        invalid_weights = (0, -1, True, "high")

        for weight in invalid_weights:
            with self.subTest(weight=weight):
                with self.assertRaisesRegex(ValueError, "weight"):
                    evaluate_decision(
                        (
                            QuestionEvaluation(
                                question_id="q.ai.governance.owner",
                                readiness_dimension="ai-readiness",
                                normalized_score=50,
                                weight=weight,
                            ),
                        )
                    )


if __name__ == "__main__":
    unittest.main()
