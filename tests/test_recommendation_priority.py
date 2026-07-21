import sys
import unittest
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.confidence import (  # noqa: E402
    ConfidenceFactorEvaluation,
    build_confidence_evaluation,
)
from assessment.decision_engine import evaluate_assessment  # noqa: E402
from assessment.methodology_config import (  # noqa: E402
    BUSINESS_DECISION_METHODOLOGY,
    RecommendationPriorityFactorConfig,
)
from assessment.recommendation_priority import (  # noqa: E402
    NOT_EVALUATED_STATUS,
    PRIORITY_FOUNDATION_LIMITATION,
    build_recommendation_priority_evaluation,
)
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


def valid_confidence(snapshot):
    return build_confidence_evaluation(snapshot)


class RecommendationPriorityEvaluationTests(unittest.TestCase):
    def test_priority_evaluation_consumes_sources_deterministically(self):
        snapshot = valid_snapshot(scale_value=3, numeric_value=80)
        confidence = valid_confidence(snapshot)

        first_evaluation = build_recommendation_priority_evaluation(
            snapshot,
            confidence,
        )
        second_evaluation = build_recommendation_priority_evaluation(
            snapshot,
            confidence,
        )

        self.assertEqual(first_evaluation, second_evaluation)
        self.assertEqual(
            first_evaluation.assessment_version,
            snapshot.assessment_version,
        )
        self.assertEqual(
            first_evaluation.methodology_version,
            BUSINESS_DECISION_METHODOLOGY.version,
        )

    def test_priority_evaluation_uses_configured_priority_level_catalog(self):
        snapshot = valid_snapshot()
        confidence = valid_confidence(snapshot)

        priority = build_recommendation_priority_evaluation(snapshot, confidence)

        self.assertEqual(
            list(priority.configured_priority_levels),
            ["critical", "high", "medium", "low"],
        )
        self.assertEqual(
            priority.configured_priority_levels["critical"].rank,
            1,
        )
        self.assertEqual(
            priority.configured_priority_levels["low"].rank,
            4,
        )

    def test_priority_evaluation_uses_configured_priority_factor_catalog(self):
        snapshot = valid_snapshot()
        confidence = valid_confidence(snapshot)

        priority = build_recommendation_priority_evaluation(snapshot, confidence)

        self.assertEqual(
            set(priority.configured_priority_factors),
            set(BUSINESS_DECISION_METHODOLOGY.recommendation_priority_factors),
        )
        self.assertEqual(priority.evaluated_factor_ids, ())
        self.assertEqual(
            priority.not_evaluated_factor_ids,
            tuple(sorted(BUSINESS_DECISION_METHODOLOGY.recommendation_priority_factors)),
        )

    def test_all_priority_factors_are_explicitly_not_evaluated(self):
        snapshot = valid_snapshot()
        confidence = valid_confidence(snapshot)

        priority = build_recommendation_priority_evaluation(snapshot, confidence)

        for factor in priority.configured_priority_factors.values():
            self.assertEqual(factor.status, NOT_EVALUATED_STATUS)
            self.assertEqual(factor.limitation, PRIORITY_FOUNDATION_LIMITATION)
            self.assertIn("snapshot.audit", factor.snapshot_source_refs)
            self.assertIn(
                "confidence.factors.assessment-completeness",
                factor.confidence_source_refs,
            )

    def test_priority_evaluation_preserves_readiness_outputs(self):
        snapshot = valid_snapshot(scale_value=2, numeric_value=50)
        confidence = valid_confidence(snapshot)
        snapshot_dict_before = snapshot.to_dict()

        build_recommendation_priority_evaluation(snapshot, confidence)

        self.assertEqual(snapshot.to_dict(), snapshot_dict_before)
        self.assertEqual(snapshot.overall_readiness.score, 50)

    def test_priority_evaluation_preserves_confidence_outputs(self):
        snapshot = valid_snapshot()
        confidence = valid_confidence(snapshot)
        confidence_dict_before = confidence.to_dict()

        build_recommendation_priority_evaluation(snapshot, confidence)

        self.assertEqual(confidence.to_dict(), confidence_dict_before)

    def test_priority_evaluation_is_immutable_where_practical(self):
        snapshot = valid_snapshot()
        confidence = valid_confidence(snapshot)

        priority = build_recommendation_priority_evaluation(snapshot, confidence)

        with self.assertRaises(TypeError):
            priority.configured_priority_factors["business-impact"] = None
        with self.assertRaises(TypeError):
            priority.source_snapshot_metadata["questionCount"] = 0

    def test_priority_evaluation_rejects_mismatched_assessment_versions(self):
        snapshot = valid_snapshot()
        confidence = replace(
            valid_confidence(snapshot),
            assessment_version="other-assessment-version",
        )

        with self.assertRaisesRegex(ValueError, "assessment versions"):
            build_recommendation_priority_evaluation(snapshot, confidence)

    def test_priority_evaluation_rejects_mismatched_methodology_versions(self):
        snapshot = valid_snapshot()
        confidence = replace(
            valid_confidence(snapshot),
            methodology_version="other-methodology",
        )

        with self.assertRaisesRegex(ValueError, "methodology versions"):
            build_recommendation_priority_evaluation(snapshot, confidence)

    def test_priority_evaluation_rejects_invalid_priority_ranks(self):
        snapshot = valid_snapshot()
        confidence = valid_confidence(snapshot)
        config = BUSINESS_DECISION_METHODOLOGY
        priorities = dict(config.recommendation_priorities)
        priorities["low"] = replace(priorities["low"], rank=5)
        invalid_config = replace(
            config,
            recommendation_priorities=MappingProxyType(priorities),
        )

        with self.assertRaisesRegex(ValueError, "priority ranks"):
            build_recommendation_priority_evaluation(
                snapshot,
                confidence,
                invalid_config,
            )

    def test_priority_evaluation_rejects_invalid_factor_ids(self):
        snapshot = valid_snapshot()
        confidence = valid_confidence(snapshot)
        config = BUSINESS_DECISION_METHODOLOGY
        factors = dict(config.recommendation_priority_factors)
        factors["unknown-factor"] = RecommendationPriorityFactorConfig(
            "unknown-factor",
            "Unknown Factor",
        )
        invalid_config = replace(
            config,
            recommendation_priority_factors=MappingProxyType(factors),
        )

        with self.assertRaisesRegex(
            ValueError,
            "Unknown recommendation priority factor",
        ):
            build_recommendation_priority_evaluation(
                snapshot,
                confidence,
                invalid_config,
            )

    def test_priority_evaluation_rejects_incomplete_confidence_input(self):
        snapshot = valid_snapshot()
        confidence = valid_confidence(snapshot)
        factors = dict(confidence.factors)
        del factors["assessment-completeness"]
        incomplete_confidence = replace(
            confidence,
            factors=MappingProxyType(factors),
        )

        with self.assertRaisesRegex(ValueError, "Missing confidence factor"):
            build_recommendation_priority_evaluation(
                snapshot,
                incomplete_confidence,
            )

    def test_priority_evaluation_rejects_unknown_confidence_factor(self):
        snapshot = valid_snapshot()
        confidence = valid_confidence(snapshot)
        factors = dict(confidence.factors)
        factors["unknown-factor"] = ConfidenceFactorEvaluation(
            factor_id="unknown-factor",
            label="Unknown Factor",
            status=NOT_EVALUATED_STATUS,
        )
        invalid_confidence = replace(
            confidence,
            factors=MappingProxyType(factors),
        )

        with self.assertRaisesRegex(ValueError, "Unknown confidence factor"):
            build_recommendation_priority_evaluation(snapshot, invalid_confidence)

    def test_priority_evaluation_dict_stays_within_foundation_scope(self):
        snapshot = valid_snapshot()
        confidence = valid_confidence(snapshot)

        priority_dict = build_recommendation_priority_evaluation(
            snapshot,
            confidence,
        ).to_dict()

        self.assertEqual(
            set(priority_dict),
            {
                "assessmentVersion",
                "methodologyVersion",
                "configuredPriorityLevels",
                "configuredPriorityFactors",
                "evaluatedFactorIds",
                "notEvaluatedFactorIds",
                "sourceSnapshotMetadata",
                "sourceConfidenceMetadata",
            },
        )
        self.assertNotIn("recommendations", priority_dict)
        self.assertNotIn("executiveRecommendations", priority_dict)
        self.assertNotIn("recommendedServiceTier", priority_dict)
        self.assertNotIn("executiveSummary", priority_dict)
        self.assertNotIn("priorityAssignment", priority_dict)
        self.assertNotIn("serviceRouting", priority_dict)


if __name__ == "__main__":
    unittest.main()
