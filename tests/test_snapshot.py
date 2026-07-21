import sys
import unittest
from dataclasses import replace
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.decision_engine import (  # noqa: E402
    QuestionEvaluation,
    evaluate_assessment,
    evaluate_decision,
)
from assessment.methodology_config import BUSINESS_DECISION_METHODOLOGY  # noqa: E402
from assessment.snapshot import build_business_readiness_snapshot  # noqa: E402


def valid_configured_answers(scale_value=4, numeric_value=100):
    return {
        question_id: (
            numeric_value
            if question.expected_answer_type == "numeric"
            else scale_value
        )
        for question_id, question in BUSINESS_DECISION_METHODOLOGY.questions.items()
    }


class BusinessReadinessSnapshotTests(unittest.TestCase):
    def test_snapshot_consumes_decision_evaluation_deterministically(self):
        evaluation = evaluate_assessment(
            valid_configured_answers(scale_value=3, numeric_value=80)
        )

        first_snapshot = build_business_readiness_snapshot(
            "nguyen-ai-readiness-v1",
            evaluation,
        )
        second_snapshot = build_business_readiness_snapshot(
            "nguyen-ai-readiness-v1",
            evaluation,
        )

        self.assertEqual(first_snapshot, second_snapshot)
        self.assertEqual(
            first_snapshot.assessment_version,
            "nguyen-ai-readiness-v1",
        )
        self.assertEqual(
            first_snapshot.overall_readiness.score,
            evaluation.overall_score,
        )
        self.assertEqual(
            first_snapshot.overall_readiness.contributing_dimensions,
            tuple(sorted(BUSINESS_DECISION_METHODOLOGY.readiness_dimensions)),
        )

    def test_snapshot_maps_dimension_evaluation_to_domain_readiness(self):
        evaluation = evaluate_assessment(valid_configured_answers())
        snapshot = build_business_readiness_snapshot(
            "nguyen-ai-readiness-v1",
            evaluation,
        )
        domains_by_id = {
            domain.domain_id: domain
            for domain in snapshot.domains
        }

        ai_domain = domains_by_id["ai-readiness"]
        ai_dimension = evaluation.dimensions["ai-readiness"]

        self.assertEqual(ai_domain.label, "AI Readiness")
        self.assertEqual(ai_domain.score, ai_dimension.normalized_score)
        self.assertEqual(ai_domain.question_count, ai_dimension.question_count)
        self.assertEqual(ai_domain.total_weight, ai_dimension.total_weight)
        self.assertEqual(
            ai_domain.contributing_questions,
            ai_dimension.contributing_questions,
        )

    def test_snapshot_includes_reproducible_audit_metadata(self):
        evaluation = evaluate_assessment(valid_configured_answers())

        snapshot = build_business_readiness_snapshot(
            "nguyen-ai-readiness-v1",
            evaluation,
        )

        self.assertEqual(
            snapshot.audit.methodology_version,
            BUSINESS_DECISION_METHODOLOGY.version,
        )
        self.assertEqual(
            snapshot.audit.evaluated_dimensions,
            tuple(sorted(BUSINESS_DECISION_METHODOLOGY.readiness_dimensions)),
        )
        self.assertEqual(snapshot.audit.question_count, evaluation.question_count)
        self.assertEqual(snapshot.audit.total_weight, evaluation.total_weight)

    def test_snapshot_dict_stays_within_foundation_scope(self):
        evaluation = evaluate_assessment(valid_configured_answers())

        snapshot_dict = build_business_readiness_snapshot(
            "nguyen-ai-readiness-v1",
            evaluation,
        ).to_dict()

        self.assertEqual(
            set(snapshot_dict),
            {
                "assessmentVersion",
                "overallReadiness",
                "domains",
                "audit",
            },
        )
        self.assertNotIn("confidence", snapshot_dict)
        self.assertNotIn("executiveSummary", snapshot_dict)
        self.assertNotIn("executiveRecommendations", snapshot_dict)
        self.assertNotIn("recommendedServiceTier", snapshot_dict)

    def test_snapshot_rejects_missing_evaluation_explanation(self):
        evaluation = evaluate_assessment(valid_configured_answers())
        invalid_evaluation = replace(evaluation, explanation=None)

        with self.assertRaisesRegex(ValueError, "explanation is required"):
            build_business_readiness_snapshot(
                "nguyen-ai-readiness-v1",
                invalid_evaluation,
            )

    def test_snapshot_rejects_unknown_readiness_dimension(self):
        evaluation = evaluate_decision(
            (
                QuestionEvaluation(
                    question_id="q.invalid.dimension",
                    readiness_dimension="unknown-readiness",
                    normalized_score=50,
                    weight=1,
                ),
            )
        )

        with self.assertRaisesRegex(ValueError, "Unknown readiness dimension"):
            build_business_readiness_snapshot(
                "nguyen-ai-readiness-v1",
                evaluation,
            )

    def test_snapshot_rejects_mismatched_explanation_metadata(self):
        evaluation = evaluate_assessment(valid_configured_answers())
        invalid_explanation = replace(
            evaluation.explanation,
            evaluated_dimensions=(),
        )
        invalid_evaluation = replace(
            evaluation,
            explanation=invalid_explanation,
        )

        with self.assertRaisesRegex(ValueError, "dimensions do not match"):
            build_business_readiness_snapshot(
                "nguyen-ai-readiness-v1",
                invalid_evaluation,
            )

    def test_snapshot_rejects_empty_assessment_version(self):
        evaluation = evaluate_assessment(valid_configured_answers())

        with self.assertRaisesRegex(ValueError, "Assessment version"):
            build_business_readiness_snapshot("", evaluation)


if __name__ == "__main__":
    unittest.main()
