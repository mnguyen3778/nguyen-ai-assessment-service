import sys
import unittest
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.methodology_config import (  # noqa: E402
    AnswerTypeConfig,
    BUSINESS_DECISION_METHODOLOGY,
    METHODOLOGY_VERSION,
    QuestionConfig,
    validate_methodology_config,
)


class MethodologyConfigTests(unittest.TestCase):
    def test_methodology_version_matches_approved_baseline(self):
        self.assertEqual(
            BUSINESS_DECISION_METHODOLOGY.version,
            "business-decision-methodology-v1",
        )
        self.assertEqual(METHODOLOGY_VERSION, BUSINESS_DECISION_METHODOLOGY.version)

    def test_canonical_vocabulary_counts_match_methodology_catalogs(self):
        config = BUSINESS_DECISION_METHODOLOGY

        self.assertEqual(len(config.readiness_dimensions), 8)
        self.assertEqual(len(config.evidence_categories), 10)
        self.assertEqual(len(config.questions), 48)
        self.assertEqual(len(config.services), 6)
        self.assertEqual(len(config.recommendation_priorities), 4)

    def test_question_catalog_maps_every_question_to_known_vocabulary(self):
        config = BUSINESS_DECISION_METHODOLOGY

        for question in config.questions.values():
            self.assertIn(question.evidence_category, config.evidence_categories)
            self.assertIn(question.readiness_dimension, config.readiness_dimensions)
            self.assertIn(question.expected_answer_type, config.answer_types)
            self.assertIn(question.weight_category, config.weight_categories)

    def test_answer_type_ranges_define_normalizable_inputs(self):
        answer_types = BUSINESS_DECISION_METHODOLOGY.answer_types

        self.assertEqual(answer_types["scale-0-4"].minimum, 0)
        self.assertEqual(answer_types["scale-0-4"].maximum, 4)
        self.assertTrue(answer_types["scale-0-4"].is_normalizable)
        self.assertEqual(answer_types["numeric"].minimum, 0)
        self.assertEqual(answer_types["numeric"].maximum, 100)
        self.assertTrue(answer_types["numeric"].is_normalizable)
        self.assertFalse(answer_types["text-evidence"].is_normalizable)

    def test_required_methodology_identifiers_are_present(self):
        config = BUSINESS_DECISION_METHODOLOGY

        self.assertIn("ai-readiness", config.readiness_dimensions)
        self.assertIn("security-readiness", config.readiness_dimensions)
        self.assertIn("operational-readiness", config.readiness_dimensions)
        self.assertIn("business-readiness", config.readiness_dimensions)
        self.assertIn("leadership", config.evidence_categories)
        self.assertIn("governance", config.evidence_categories)
        self.assertIn("q.ai.governance.owner", config.questions)
        self.assertIn("q.business.executive-alignment", config.questions)
        self.assertIn("service.assessment-only", config.services)
        self.assertIn("service.managed-ai-services", config.services)

    def test_recommendation_priorities_are_deterministically_ordered(self):
        priorities = BUSINESS_DECISION_METHODOLOGY.recommendation_priorities

        self.assertEqual(priorities["critical"].rank, 1)
        self.assertEqual(priorities["high"].rank, 2)
        self.assertEqual(priorities["medium"].rank, 3)
        self.assertEqual(priorities["low"].rank, 4)

    def test_placeholder_thresholds_cover_full_score_range(self):
        thresholds = sorted(
            BUSINESS_DECISION_METHODOLOGY.placeholder_thresholds.values(),
            key=lambda threshold: threshold.minimum,
        )

        self.assertEqual(thresholds[0].minimum, 0)
        self.assertEqual(thresholds[-1].maximum, 100)
        for left, right in zip(thresholds, thresholds[1:]):
            self.assertEqual(left.maximum + 1, right.minimum)

    def test_output_schema_tracks_current_and_future_contract_fields(self):
        output_schema = BUSINESS_DECISION_METHODOLOGY.output_schema

        self.assertIn("overallScore", output_schema.current_response_fields)
        self.assertIn("readinessLevel", output_schema.current_response_fields)
        self.assertIn("overallReadiness", output_schema.snapshot_response_fields)
        self.assertIn("executiveSummary", output_schema.snapshot_response_fields)
        self.assertIn("recommendedServiceTier", output_schema.snapshot_response_fields)

    def test_validation_rejects_question_with_unknown_evidence_category(self):
        config = BUSINESS_DECISION_METHODOLOGY
        questions = dict(config.questions)
        questions["q.ai.governance.owner"] = replace(
            questions["q.ai.governance.owner"],
            evidence_category="unknown",
        )
        invalid_config = replace(
            config,
            questions=MappingProxyType(questions),
        )

        with self.assertRaisesRegex(ValueError, "Unknown evidence category"):
            validate_methodology_config(invalid_config)

    def test_validation_rejects_question_with_unknown_readiness_dimension(self):
        config = BUSINESS_DECISION_METHODOLOGY
        questions = dict(config.questions)
        questions["q.ai.governance.owner"] = replace(
            questions["q.ai.governance.owner"],
            readiness_dimension="unknown",
        )
        invalid_config = replace(
            config,
            questions=MappingProxyType(questions),
        )

        with self.assertRaisesRegex(ValueError, "Unknown readiness dimension"):
            validate_methodology_config(invalid_config)

    def test_validation_rejects_non_contiguous_priority_ranks(self):
        config = BUSINESS_DECISION_METHODOLOGY
        priorities = dict(config.recommendation_priorities)
        priorities["low"] = replace(priorities["low"], rank=5)
        invalid_config = replace(
            config,
            recommendation_priorities=MappingProxyType(priorities),
        )

        with self.assertRaisesRegex(ValueError, "priority ranks"):
            validate_methodology_config(invalid_config)

    def test_validation_rejects_mismatched_mapping_key(self):
        config = BUSINESS_DECISION_METHODOLOGY
        questions = dict(config.questions)
        questions["q.invalid.alias"] = QuestionConfig(
            id="q.invalid.real",
            business_capability="Invalid alias.",
            evidence_category="strategy",
            readiness_dimension="business-readiness",
            expected_answer_type="scale-0-4",
            weight_category="strategic-alignment",
        )
        invalid_config = replace(
            config,
            questions=MappingProxyType(questions),
        )

        with self.assertRaisesRegex(ValueError, "key must match object id"):
            validate_methodology_config(invalid_config)

    def test_validation_rejects_invalid_answer_type_range(self):
        config = BUSINESS_DECISION_METHODOLOGY
        answer_types = dict(config.answer_types)
        answer_types["scale-0-4"] = AnswerTypeConfig(
            id="scale-0-4",
            label="Scale 0-4",
            minimum=4,
            maximum=0,
        )
        invalid_config = replace(
            config,
            answer_types=MappingProxyType(answer_types),
        )

        with self.assertRaisesRegex(ValueError, "maximum"):
            validate_methodology_config(invalid_config)


if __name__ == "__main__":
    unittest.main()
