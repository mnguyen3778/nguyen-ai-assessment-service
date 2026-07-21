import sys
import unittest
from dataclasses import replace
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.confidence import (  # noqa: E402
    EVALUATED_STATUS,
    NOT_EVALUATED_STATUS,
    build_confidence_evaluation,
)
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


def valid_snapshot(scale_value=4, numeric_value=100):
    evaluation = evaluate_assessment(
        valid_configured_answers(scale_value, numeric_value)
    )
    return build_business_readiness_snapshot(
        "nguyen-ai-readiness-v1",
        evaluation,
    )


class ConfidenceEvaluationTests(unittest.TestCase):
    def test_confidence_evaluation_consumes_snapshot_deterministically(self):
        snapshot = valid_snapshot(scale_value=3, numeric_value=80)

        first_evaluation = build_confidence_evaluation(snapshot)
        second_evaluation = build_confidence_evaluation(snapshot)

        self.assertEqual(first_evaluation, second_evaluation)
        self.assertEqual(
            first_evaluation.assessment_version,
            snapshot.assessment_version,
        )
        self.assertEqual(
            first_evaluation.methodology_version,
            BUSINESS_DECISION_METHODOLOGY.version,
        )

    def test_confidence_evaluation_preserves_snapshot_scores(self):
        snapshot = valid_snapshot(scale_value=2, numeric_value=50)
        snapshot_dict_before = snapshot.to_dict()

        build_confidence_evaluation(snapshot)

        self.assertEqual(snapshot.to_dict(), snapshot_dict_before)
        self.assertEqual(snapshot.overall_readiness.score, 50)

    def test_confidence_evaluation_uses_configured_factor_catalog(self):
        snapshot = valid_snapshot()
        confidence = build_confidence_evaluation(snapshot)

        self.assertEqual(
            set(confidence.factors),
            set(BUSINESS_DECISION_METHODOLOGY.confidence_factors),
        )
        self.assertEqual(
            confidence.evaluated_factor_ids,
            ("assessment-completeness", "evidence-coverage"),
        )
        self.assertEqual(
            confidence.not_evaluated_factor_ids,
            ("answer-consistency", "business-certainty", "response-quality"),
        )

    def test_assessment_completeness_uses_snapshot_audit_question_count(self):
        snapshot = valid_snapshot()

        confidence = build_confidence_evaluation(snapshot)
        completeness = confidence.factors["assessment-completeness"]

        self.assertEqual(completeness.status, EVALUATED_STATUS)
        self.assertEqual(
            completeness.observed_count,
            snapshot.audit.question_count,
        )
        self.assertEqual(
            completeness.expected_count,
            len(BUSINESS_DECISION_METHODOLOGY.questions),
        )
        self.assertEqual(completeness.coverage_ratio, 1)
        self.assertEqual(
            completeness.dimension_refs,
            snapshot.audit.evaluated_dimensions,
        )

    def test_evidence_coverage_uses_contributing_questions_and_methodology(self):
        snapshot = valid_snapshot()

        confidence = build_confidence_evaluation(snapshot)
        evidence_coverage = confidence.factors["evidence-coverage"]

        self.assertEqual(evidence_coverage.status, EVALUATED_STATUS)
        self.assertEqual(
            evidence_coverage.evidence_categories,
            tuple(sorted(BUSINESS_DECISION_METHODOLOGY.evidence_categories)),
        )
        self.assertEqual(
            evidence_coverage.observed_count,
            len(BUSINESS_DECISION_METHODOLOGY.evidence_categories),
        )
        self.assertEqual(
            evidence_coverage.expected_count,
            len(BUSINESS_DECISION_METHODOLOGY.evidence_categories),
        )
        self.assertEqual(evidence_coverage.coverage_ratio, 1)

    def test_not_yet_evaluated_factors_expose_limitations(self):
        snapshot = valid_snapshot()

        confidence = build_confidence_evaluation(snapshot)

        for factor_id in confidence.not_evaluated_factor_ids:
            factor = confidence.factors[factor_id]
            self.assertEqual(factor.status, NOT_EVALUATED_STATUS)
            self.assertIsNotNone(factor.limitation)
            self.assertIsNone(factor.coverage_ratio)

    def test_confidence_evaluation_dict_stays_within_foundation_scope(self):
        snapshot = valid_snapshot()

        confidence_dict = build_confidence_evaluation(snapshot).to_dict()

        self.assertEqual(
            set(confidence_dict),
            {
                "assessmentVersion",
                "methodologyVersion",
                "factors",
                "evaluatedFactorIds",
                "notEvaluatedFactorIds",
            },
        )
        self.assertNotIn("recommendations", confidence_dict)
        self.assertNotIn("executiveSummary", confidence_dict)
        self.assertNotIn("recommendedServiceTier", confidence_dict)

    def test_confidence_evaluation_is_immutable(self):
        snapshot = valid_snapshot()
        confidence = build_confidence_evaluation(snapshot)

        with self.assertRaises(TypeError):
            confidence.factors["assessment-completeness"] = None

    def test_confidence_evaluation_rejects_mismatched_methodology_version(self):
        snapshot = valid_snapshot()
        invalid_snapshot = replace(
            snapshot,
            audit=replace(
                snapshot.audit,
                methodology_version="other-methodology",
            ),
        )

        with self.assertRaisesRegex(ValueError, "methodology version"):
            build_confidence_evaluation(invalid_snapshot)

    def test_confidence_evaluation_rejects_unknown_question_id(self):
        evaluation = evaluate_decision(
            (
                QuestionEvaluation(
                    question_id="q.unknown",
                    readiness_dimension="ai-readiness",
                    normalized_score=50,
                    weight=1,
                ),
            )
        )
        snapshot = build_business_readiness_snapshot(
            "nguyen-ai-readiness-v1",
            evaluation,
        )

        with self.assertRaisesRegex(ValueError, "Unknown question ID"):
            build_confidence_evaluation(snapshot)


if __name__ == "__main__":
    unittest.main()
