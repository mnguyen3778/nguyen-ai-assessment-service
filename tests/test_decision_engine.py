import sys
import unittest
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.decision_engine import (  # noqa: E402
    QuestionEvaluation,
    build_question_evaluations,
    evaluate_assessment,
    evaluate_decision,
)
from assessment.methodology_config import BUSINESS_DECISION_METHODOLOGY  # noqa: E402


def valid_configured_answers(scale_value=4, numeric_value=100):
    return {
        question_id: (
            numeric_value
            if question.expected_answer_type == "numeric"
            else scale_value
        )
        for question_id, question in BUSINESS_DECISION_METHODOLOGY.questions.items()
    }


class DecisionEngineTests(unittest.TestCase):
    def test_evaluate_assessment_maps_answers_through_methodology_config(self):
        result = evaluate_assessment(valid_configured_answers())

        self.assertEqual(
            result.question_count,
            len(BUSINESS_DECISION_METHODOLOGY.questions),
        )
        self.assertEqual(
            set(result.dimensions),
            set(BUSINESS_DECISION_METHODOLOGY.readiness_dimensions),
        )
        self.assertAlmostEqual(result.overall_score, 100)
        self.assertEqual(
            result.dimensions["ai-readiness"].question_count,
            6,
        )

    def test_build_question_evaluations_resolves_configured_metadata(self):
        evaluations = build_question_evaluations(valid_configured_answers(3))
        evaluation_by_id = {
            evaluation.question_id: evaluation
            for evaluation in evaluations
        }
        question = BUSINESS_DECISION_METHODOLOGY.questions["q.ai.governance.owner"]
        evaluation = evaluation_by_id["q.ai.governance.owner"]

        self.assertEqual(evaluation.readiness_dimension, question.readiness_dimension)
        self.assertEqual(evaluation.evidence_category, question.evidence_category)
        self.assertEqual(evaluation.weight_category, question.weight_category)
        self.assertEqual(
            evaluation.weight,
            BUSINESS_DECISION_METHODOLOGY.placeholder_question_weights[question.id],
        )
        self.assertEqual(evaluation.normalized_score, 75)

    def test_build_question_evaluations_normalizes_numeric_answers(self):
        evaluations = build_question_evaluations(
            valid_configured_answers(scale_value=0, numeric_value=50)
        )
        evaluation_by_id = {
            evaluation.question_id: evaluation
            for evaluation in evaluations
        }

        self.assertEqual(
            evaluation_by_id["q.automation.manual-volume"].normalized_score,
            50,
        )

    def test_evaluate_assessment_includes_traceable_explanation_metadata(self):
        result = evaluate_assessment(
            valid_configured_answers(scale_value=3, numeric_value=80)
        )
        explanation = result.explanation

        self.assertIsNotNone(explanation)
        self.assertEqual(
            explanation.evaluated_dimensions,
            tuple(sorted(BUSINESS_DECISION_METHODOLOGY.readiness_dimensions)),
        )
        self.assertEqual(
            len(explanation.contributing_questions),
            len(BUSINESS_DECISION_METHODOLOGY.questions),
        )
        self.assertIn(
            "q.ai.governance.owner",
            explanation.contributing_questions,
        )
        self.assertEqual(
            explanation.applied_weights["q.ai.governance.owner"],
            BUSINESS_DECISION_METHODOLOGY.placeholder_question_weights[
                "q.ai.governance.owner"
            ],
        )

        question = BUSINESS_DECISION_METHODOLOGY.questions["q.ai.governance.owner"]
        question_explanation = explanation.question_explanations[
            "q.ai.governance.owner"
        ]
        self.assertEqual(question_explanation.question_id, question.id)
        self.assertEqual(
            question_explanation.readiness_dimension,
            question.readiness_dimension,
        )
        self.assertEqual(
            question_explanation.evidence_category,
            question.evidence_category,
        )
        self.assertEqual(
            question_explanation.weight_category,
            question.weight_category,
        )
        self.assertEqual(question_explanation.normalized_score, 75)

        dimension = result.dimensions["ai-readiness"]
        dimension_explanation = explanation.dimension_explanations["ai-readiness"]
        self.assertEqual(
            dimension_explanation.contributing_questions,
            dimension.contributing_questions,
        )
        self.assertEqual(
            dimension_explanation.applied_weights["q.ai.governance.owner"],
            question_explanation.applied_weight,
        )
        self.assertAlmostEqual(
            dimension_explanation.normalized_score,
            dimension.normalized_score,
        )

    def test_evaluation_explanation_is_immutable(self):
        result = evaluate_assessment(valid_configured_answers())
        explanation = result.explanation

        self.assertIsNotNone(explanation)
        with self.assertRaises(TypeError):
            explanation.applied_weights["q.ai.governance.owner"] = 2
        with self.assertRaises(TypeError):
            explanation.question_explanations["q.ai.governance.owner"] = None

    def test_evaluate_assessment_rejects_unknown_question_id(self):
        answers = valid_configured_answers()
        answers["q.unknown"] = 100

        with self.assertRaisesRegex(ValueError, "Unknown question ID"):
            evaluate_assessment(answers)

    def test_evaluate_assessment_rejects_missing_required_question(self):
        answers = valid_configured_answers()
        del answers["q.ai.governance.owner"]

        with self.assertRaisesRegex(ValueError, "Missing required question"):
            evaluate_assessment(answers)

    def test_evaluate_assessment_rejects_invalid_answer_type(self):
        answers = valid_configured_answers()
        answers["q.ai.governance.owner"] = "ready"

        with self.assertRaisesRegex(ValueError, "must be numeric"):
            evaluate_assessment(answers)

    def test_evaluate_assessment_rejects_out_of_range_answer(self):
        answers = valid_configured_answers()
        answers["q.ai.governance.owner"] = 5

        with self.assertRaisesRegex(ValueError, "between 0 and 4"):
            evaluate_assessment(answers)

    def test_evaluate_assessment_rejects_invalid_configured_weight(self):
        weights = dict(BUSINESS_DECISION_METHODOLOGY.placeholder_question_weights)
        weights["q.ai.governance.owner"] = 0
        invalid_config = replace(
            BUSINESS_DECISION_METHODOLOGY,
            placeholder_question_weights=MappingProxyType(weights),
        )

        with self.assertRaisesRegex(ValueError, "weight"):
            evaluate_assessment(valid_configured_answers(), invalid_config)

    def test_evaluate_assessment_rejects_invalid_configured_readiness_dimension(self):
        questions = dict(BUSINESS_DECISION_METHODOLOGY.questions)
        questions["q.ai.governance.owner"] = replace(
            questions["q.ai.governance.owner"],
            readiness_dimension="unknown",
        )
        invalid_config = replace(
            BUSINESS_DECISION_METHODOLOGY,
            questions=MappingProxyType(questions),
        )

        with self.assertRaisesRegex(ValueError, "Unknown readiness dimension"):
            evaluate_assessment(valid_configured_answers(), invalid_config)

    def test_evaluate_assessment_is_deterministic_for_same_answers(self):
        answers = valid_configured_answers(scale_value=3, numeric_value=80)

        self.assertEqual(evaluate_assessment(answers), evaluate_assessment(answers))

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

        explanation = result.explanation
        self.assertIsNotNone(explanation)
        self.assertEqual(
            explanation.evaluated_dimensions,
            ("ai-readiness", "security-readiness"),
        )
        self.assertEqual(
            explanation.applied_weights,
            {
                "q.ai.governance.owner": 3,
                "q.ai.strategy.business-goals": 1,
                "q.security.identity.mfa": 2,
            },
        )
        self.assertEqual(
            explanation.dimension_explanations[
                "ai-readiness"
            ].contributing_questions,
            (
                "q.ai.governance.owner",
                "q.ai.strategy.business-goals",
            ),
        )

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
