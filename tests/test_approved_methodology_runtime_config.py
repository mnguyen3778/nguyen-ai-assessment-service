import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from types import MappingProxyType


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_CONFIDENCE_LEVEL_ORDER,
    APPROVED_DIMENSION_ORDER,
    APPROVED_FINDING_TYPE_ORDER,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_RECOMMENDATION_LABEL_ORDER,
    APPROVED_RISK_LEVEL_ORDER,
    APPROVED_SEVERITY_LEVEL_ORDER,
    CONFIDENCE_DECISION_TABLE_SET_VERSION,
    EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
    QUESTION_SCORING_TABLES_VERSION,
    RECOMMENDATION_DECISION_TABLE_SET_VERSION,
    RISK_DECISION_TABLE_SET_VERSION,
    SEVERITY_DECISION_TABLE_SET_VERSION,
    DecisionRuleRuntimeConfig,
    validate_approved_methodology_runtime_config,
)
from assessment.methodology_config import METHODOLOGY_VERSION  # noqa: E402


class ApprovedMethodologyRuntimeConfigTests(unittest.TestCase):
    def test_approved_runtime_config_validates(self):
        validate_approved_methodology_runtime_config(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG
        )

    def test_version_manifest_is_bound_to_approved_artifacts(self):
        manifest = APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest

        self.assertEqual(manifest.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(
            manifest.production_authority_release_version,
            "production-authority-release-v1",
        )
        self.assertEqual(
            manifest.runtime_config_version,
            "approved-methodology-runtime-config-v1",
        )
        self.assertEqual(manifest.scoring_scale_version, "scoring-scale-v1")
        self.assertEqual(
            manifest.question_scoring_tables_version,
            QUESTION_SCORING_TABLES_VERSION,
        )
        self.assertEqual(
            manifest.severity_decision_table_set_version,
            SEVERITY_DECISION_TABLE_SET_VERSION,
        )
        self.assertEqual(
            manifest.risk_decision_table_set_version,
            RISK_DECISION_TABLE_SET_VERSION,
        )
        self.assertEqual(
            manifest.confidence_decision_table_set_version,
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
        )
        self.assertEqual(
            manifest.recommendation_decision_table_set_version,
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        )
        self.assertEqual(
            manifest.executive_summary_template_set_version,
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
        )

    def test_dimensions_match_approved_weights_and_question_distribution(self):
        config = APPROVED_METHODOLOGY_RUNTIME_CONFIG
        dimensions = config.dimensions

        self.assertEqual(tuple(dimensions), APPROVED_DIMENSION_ORDER)
        self.assertEqual(
            {
                dimension_id: dimensions[dimension_id].weight
                for dimension_id in dimensions
            },
            {
                "POC": 18,
                "GCR": 24,
                "TISM": 22,
                "DPSC": 20,
                "RVCI": 16,
            },
        )
        self.assertEqual(sum(dimension.weight for dimension in dimensions.values()), 100)

        observed_counts = {
            dimension_id: 0
            for dimension_id in dimensions
        }
        for question in config.questions.values():
            observed_counts[question.primary_dimension] += 1

        self.assertEqual(
            observed_counts,
            {
                "POC": 14,
                "GCR": 12,
                "TISM": 12,
                "DPSC": 4,
                "RVCI": 6,
            },
        )

    def test_all_48_questions_have_approved_mapping_and_scoring_metadata(self):
        config = APPROVED_METHODOLOGY_RUNTIME_CONFIG

        self.assertEqual(len(config.questions), 48)
        self.assertEqual(
            config.questions["q.ai.strategy.business-goals"].primary_dimension,
            "GCR",
        )
        self.assertEqual(
            config.questions["q.ai.strategy.business-goals"].secondary_dimensions,
            ("TISM",),
        )
        self.assertEqual(
            config.questions["q.automation.manual-volume"].response_model_id,
            "numeric-0-100",
        )
        self.assertEqual(
            config.questions["q.business.decision-cadence"].secondary_dimensions,
            ("POC",),
        )
        self.assertTrue(
            all(
                question.scoring_table_version == QUESTION_SCORING_TABLES_VERSION
                for question in config.questions.values()
            )
        )

    def test_response_models_match_approved_scoring_scale(self):
        response_models = APPROVED_METHODOLOGY_RUNTIME_CONFIG.response_models

        self.assertEqual(
            dict(response_models["scale-0-4"].allowed_response_scores),
            {
                0: 0,
                1: 25,
                2: 50,
                3: 75,
                4: 100,
            },
        )
        self.assertEqual(response_models["numeric-0-100"].numeric_minimum, 0)
        self.assertEqual(response_models["numeric-0-100"].numeric_maximum, 100)
        self.assertTrue(response_models["numeric-0-100"].identity_numeric_mapping)

    def test_readiness_thresholds_are_deterministic_and_complete(self):
        thresholds = APPROVED_METHODOLOGY_RUNTIME_CONFIG.readiness_thresholds

        self.assertEqual(tuple(thresholds), ("not-ready", "developing", "ready", "advanced"))
        self.assertEqual(
            [
                (
                    threshold.label,
                    threshold.lower_bound,
                    threshold.upper_bound,
                    threshold.lower_inclusive,
                    threshold.upper_inclusive,
                )
                for threshold in thresholds.values()
            ],
            [
                ("Not Ready", 0, 25, True, False),
                ("Developing", 25, 50, True, False),
                ("Ready", 50, 75, True, False),
                ("Advanced", 75, 100, True, True),
            ],
        )

    def test_taxonomies_and_decision_rule_metadata_are_approved(self):
        config = APPROVED_METHODOLOGY_RUNTIME_CONFIG

        self.assertEqual(config.severity_levels, APPROVED_SEVERITY_LEVEL_ORDER)
        self.assertEqual(config.finding_types, APPROVED_FINDING_TYPE_ORDER)
        self.assertEqual(config.risk_levels, APPROVED_RISK_LEVEL_ORDER)
        self.assertEqual(config.confidence_levels, APPROVED_CONFIDENCE_LEVEL_ORDER)
        self.assertEqual(
            config.recommendation_labels,
            APPROVED_RECOMMENDATION_LABEL_ORDER,
        )
        self.assertEqual(
            config.severity_decision_rules[
                "severity-v1-deficiency-critical"
            ].output,
            "critical",
        )
        self.assertEqual(
            config.risk_decision_rules["risk-v1-critical-any-critical"].output,
            "critical-risk",
        )
        self.assertEqual(
            config.confidence_decision_rules[
                "confidence-v1-very-high-strong-only"
            ].output,
            "very-high-confidence",
        )
        self.assertEqual(
            config.recommendation_decision_rules[
                "recommendation-v1-deficiency-critical-immediate"
            ].output,
            "immediate-action",
        )

    def test_summary_sections_golden_fixtures_and_inventory_are_complete(self):
        config = APPROVED_METHODOLOGY_RUNTIME_CONFIG

        self.assertEqual(
            tuple(config.executive_summary_sections),
            (
                "overall-assessment-overview",
                "business-capability-highlights",
                "significant-findings",
                "risk-overview",
                "confidence-statement",
                "recommended-actions",
                "closing-assessment-statement",
            ),
        )
        self.assertEqual(len(config.golden_fixtures), 15)
        self.assertIn(
            "fixture-v1-version-mismatch-fail-closed",
            config.golden_fixtures,
        )
        self.assertEqual(len(config.artifact_inventory), 23)
        self.assertIn("production-authority-release-v1", config.artifact_inventory)

    def test_runtime_config_is_immutable(self):
        config = APPROVED_METHODOLOGY_RUNTIME_CONFIG

        with self.assertRaises(FrozenInstanceError):
            config.severity_levels = ()
        with self.assertRaises(TypeError):
            config.questions["q.ai.governance.owner"] = None
        with self.assertRaises(TypeError):
            config.response_models["scale-0-4"].allowed_response_scores[0] = 1

    def test_validation_fails_closed_for_unsupported_methodology_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            methodology_version="unsupported-methodology-version",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(ValueError, "Unsupported methodology version"):
            validate_approved_methodology_runtime_config(invalid_config)

    def test_validation_fails_closed_for_missing_question(self):
        questions = dict(APPROVED_METHODOLOGY_RUNTIME_CONFIG.questions)
        del questions["q.ai.governance.owner"]
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            questions=MappingProxyType(questions),
        )

        with self.assertRaisesRegex(ValueError, "48 canonical questions"):
            validate_approved_methodology_runtime_config(invalid_config)

    def test_validation_fails_closed_for_dimension_weight_mismatch(self):
        dimensions = dict(APPROVED_METHODOLOGY_RUNTIME_CONFIG.dimensions)
        dimensions["POC"] = replace(dimensions["POC"], weight=19)
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            dimensions=MappingProxyType(dimensions),
        )

        with self.assertRaisesRegex(ValueError, "weights must sum to 100"):
            validate_approved_methodology_runtime_config(invalid_config)

    def test_validation_fails_closed_for_invalid_decision_rule_output(self):
        rules = dict(APPROVED_METHODOLOGY_RUNTIME_CONFIG.risk_decision_rules)
        rules["risk-v1-critical-any-critical"] = DecisionRuleRuntimeConfig(
            "risk-v1-critical-any-critical",
            "unsupported-risk",
            RISK_DECISION_TABLE_SET_VERSION,
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            risk_decision_rules=MappingProxyType(rules),
        )

        with self.assertRaisesRegex(ValueError, "Unsupported risk decision rule output"):
            validate_approved_methodology_runtime_config(invalid_config)

    def test_validation_fails_closed_for_missing_artifact_inventory_entry(self):
        inventory = dict(APPROVED_METHODOLOGY_RUNTIME_CONFIG.artifact_inventory)
        del inventory["production-authority-release-v1"]
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            artifact_inventory=MappingProxyType(inventory),
        )

        with self.assertRaisesRegex(ValueError, "artifact inventory"):
            validate_approved_methodology_runtime_config(invalid_config)


if __name__ == "__main__":
    unittest.main()
