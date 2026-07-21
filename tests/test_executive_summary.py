import sys
import unittest
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.confidence import build_confidence_evaluation  # noqa: E402
from assessment.decision_engine import evaluate_assessment  # noqa: E402
from assessment.executive_summary import (  # noqa: E402
    EXECUTIVE_SUMMARY_FOUNDATION_LIMITATION,
    NOT_EVALUATED_STATUS,
    build_executive_summary_foundation,
)
from assessment.methodology_config import (  # noqa: E402
    BUSINESS_DECISION_METHODOLOGY,
    ExecutiveSummarySectionConfig,
    _map_by_id,
)
from assessment.recommendation_priority import (  # noqa: E402
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


def valid_sources(scale_value=4, numeric_value=100):
    evaluation = evaluate_assessment(
        valid_configured_answers(scale_value, numeric_value)
    )
    snapshot = build_business_readiness_snapshot(
        "nguyen-ai-readiness-v1",
        evaluation,
    )
    confidence = build_confidence_evaluation(snapshot)
    priority = build_recommendation_priority_evaluation(snapshot, confidence)

    return snapshot, confidence, priority


class ExecutiveSummaryFoundationTests(unittest.TestCase):
    def test_summary_foundation_consumes_sources_deterministically(self):
        snapshot, confidence, priority = valid_sources(scale_value=3, numeric_value=80)

        first_summary = build_executive_summary_foundation(
            snapshot,
            confidence,
            priority,
        )
        second_summary = build_executive_summary_foundation(
            snapshot,
            confidence,
            priority,
        )

        self.assertEqual(first_summary, second_summary)
        self.assertEqual(first_summary.assessment_version, snapshot.assessment_version)
        self.assertEqual(
            first_summary.methodology_version,
            BUSINESS_DECISION_METHODOLOGY.version,
        )

    def test_summary_foundation_uses_configured_section_catalog(self):
        snapshot, confidence, priority = valid_sources()

        summary = build_executive_summary_foundation(
            snapshot,
            confidence,
            priority,
        )

        self.assertEqual(
            set(summary.configured_summary_sections),
            set(BUSINESS_DECISION_METHODOLOGY.executive_summary_sections),
        )
        self.assertEqual(summary.evaluated_section_ids, ())
        self.assertEqual(
            summary.not_evaluated_section_ids,
            tuple(sorted(BUSINESS_DECISION_METHODOLOGY.executive_summary_sections)),
        )

    def test_all_sections_are_explicitly_not_evaluated(self):
        snapshot, confidence, priority = valid_sources()

        summary = build_executive_summary_foundation(
            snapshot,
            confidence,
            priority,
        )

        for section in summary.configured_summary_sections.values():
            self.assertEqual(section.status, NOT_EVALUATED_STATUS)
            self.assertEqual(
                section.limitation,
                EXECUTIVE_SUMMARY_FOUNDATION_LIMITATION,
            )
            self.assertIn("snapshot.audit", section.snapshot_source_refs)
            self.assertIn(
                "confidence.factors.assessment-completeness",
                section.confidence_source_refs,
            )
            self.assertIn(
                "priority.configuredPriorityLevels",
                section.priority_source_refs,
            )

    def test_summary_foundation_is_immutable_where_practical(self):
        snapshot, confidence, priority = valid_sources()

        summary = build_executive_summary_foundation(
            snapshot,
            confidence,
            priority,
        )

        with self.assertRaises(TypeError):
            summary.configured_summary_sections["readiness-overview"] = None
        with self.assertRaises(TypeError):
            summary.source_snapshot_metadata["questionCount"] = 0

    def test_summary_foundation_rejects_mismatched_assessment_versions(self):
        snapshot, confidence, priority = valid_sources()
        invalid_priority = replace(
            priority,
            assessment_version="other-assessment-version",
        )

        with self.assertRaisesRegex(ValueError, "assessment versions"):
            build_executive_summary_foundation(
                snapshot,
                confidence,
                invalid_priority,
            )

    def test_summary_foundation_rejects_mismatched_methodology_versions(self):
        snapshot, confidence, priority = valid_sources()
        invalid_confidence = replace(
            confidence,
            methodology_version="other-methodology",
        )

        with self.assertRaisesRegex(ValueError, "methodology versions"):
            build_executive_summary_foundation(
                snapshot,
                invalid_confidence,
                priority,
            )

    def test_summary_foundation_rejects_invalid_section_ids(self):
        snapshot, confidence, priority = valid_sources()
        config = BUSINESS_DECISION_METHODOLOGY
        sections = dict(config.executive_summary_sections)
        sections["unknown-section"] = ExecutiveSummarySectionConfig(
            "unknown-section",
            "Unknown Section",
        )
        invalid_config = replace(
            config,
            executive_summary_sections=MappingProxyType(sections),
        )

        with self.assertRaisesRegex(
            ValueError,
            "Unknown executive summary section",
        ):
            build_executive_summary_foundation(
                snapshot,
                confidence,
                priority,
                invalid_config,
            )

    def test_duplicate_section_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate methodology id"):
            _map_by_id(
                (
                    ExecutiveSummarySectionConfig(
                        "readiness-overview",
                        "Readiness Overview",
                    ),
                    ExecutiveSummarySectionConfig(
                        "readiness-overview",
                        "Duplicate Readiness Overview",
                    ),
                )
            )

    def test_summary_foundation_preserves_readiness_outputs(self):
        snapshot, confidence, priority = valid_sources(scale_value=2, numeric_value=50)
        snapshot_dict_before = snapshot.to_dict()

        build_executive_summary_foundation(snapshot, confidence, priority)

        self.assertEqual(snapshot.to_dict(), snapshot_dict_before)
        self.assertEqual(snapshot.overall_readiness.score, 50)

    def test_summary_foundation_preserves_confidence_outputs(self):
        snapshot, confidence, priority = valid_sources()
        confidence_dict_before = confidence.to_dict()

        build_executive_summary_foundation(snapshot, confidence, priority)

        self.assertEqual(confidence.to_dict(), confidence_dict_before)

    def test_summary_foundation_preserves_priority_outputs(self):
        snapshot, confidence, priority = valid_sources()
        priority_dict_before = priority.to_dict()

        build_executive_summary_foundation(snapshot, confidence, priority)

        self.assertEqual(priority.to_dict(), priority_dict_before)

    def test_summary_foundation_dict_stays_within_foundation_scope(self):
        snapshot, confidence, priority = valid_sources()

        summary_dict = build_executive_summary_foundation(
            snapshot,
            confidence,
            priority,
        ).to_dict()

        self.assertEqual(
            set(summary_dict),
            {
                "assessmentVersion",
                "methodologyVersion",
                "configuredSummarySections",
                "evaluatedSectionIds",
                "notEvaluatedSectionIds",
                "sourceSnapshotMetadata",
                "sourceConfidenceMetadata",
                "sourcePriorityMetadata",
            },
        )
        self.assertNotIn("narrative", summary_dict)
        self.assertNotIn("summaryText", summary_dict)
        self.assertNotIn("executiveReport", summary_dict)
        self.assertNotIn("recommendations", summary_dict)
        self.assertNotIn("executiveRecommendations", summary_dict)
        self.assertNotIn("serviceRouting", summary_dict)
        self.assertNotIn("recommendedServiceTier", summary_dict)
        self.assertNotIn("priorityAssignment", summary_dict)


if __name__ == "__main__":
    unittest.main()
