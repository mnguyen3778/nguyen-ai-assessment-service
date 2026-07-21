import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.business_decision_package import (  # noqa: E402
    BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS,
    BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BUSINESS_DECISION_PACKAGE_LIMITATIONS,
    BUSINESS_DECISION_PACKAGE_SOURCE_COMPONENTS,
    _decision_evaluation_to_dict,
    build_business_decision_package,
)
from assessment.confidence import build_confidence_evaluation  # noqa: E402
from assessment.decision_engine import evaluate_assessment  # noqa: E402
from assessment.executive_summary import (  # noqa: E402
    build_executive_summary_foundation,
)
from assessment.methodology_config import (  # noqa: E402
    BUSINESS_DECISION_METHODOLOGY,
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
    decision_evaluation = evaluate_assessment(
        valid_configured_answers(scale_value, numeric_value)
    )
    snapshot = build_business_readiness_snapshot(
        "nguyen-ai-readiness-v1",
        decision_evaluation,
    )
    confidence = build_confidence_evaluation(snapshot)
    priority = build_recommendation_priority_evaluation(snapshot, confidence)
    executive_summary = build_executive_summary_foundation(
        snapshot,
        confidence,
        priority,
    )

    return (
        decision_evaluation,
        snapshot,
        confidence,
        priority,
        executive_summary,
    )


class BusinessDecisionPackageTests(unittest.TestCase):
    def test_package_assembly_is_deterministic(self):
        sources = valid_sources(scale_value=3, numeric_value=80)

        first_package = build_business_decision_package(*sources)
        second_package = build_business_decision_package(*sources)

        self.assertEqual(first_package, second_package)
        self.assertEqual(first_package.to_dict(), second_package.to_dict())

    def test_package_preserves_sprint3_output_objects(self):
        sources = valid_sources()

        package = build_business_decision_package(*sources)

        self.assertIs(package.decision_evaluation, sources[0])
        self.assertIs(package.business_readiness_snapshot, sources[1])
        self.assertIs(package.confidence_evaluation, sources[2])
        self.assertIs(package.recommendation_priority_evaluation, sources[3])
        self.assertIs(package.executive_summary_foundation, sources[4])

    def test_package_is_immutable_where_practical(self):
        package = build_business_decision_package(*valid_sources())

        with self.assertRaises(FrozenInstanceError):
            package.audit = None
        with self.assertRaises(FrozenInstanceError):
            package.limitations = ()
        with self.assertRaises(TypeError):
            package.version_metadata.component_versions["newComponent"] = "v1"

    def test_package_does_not_mutate_contained_outputs(self):
        sources = valid_sources(scale_value=2, numeric_value=50)
        decision_evaluation = sources[0]
        snapshot = sources[1]
        confidence = sources[2]
        priority = sources[3]
        executive_summary = sources[4]
        decision_dict_before = _decision_evaluation_to_dict(decision_evaluation)
        snapshot_dict_before = snapshot.to_dict()
        confidence_dict_before = confidence.to_dict()
        priority_dict_before = priority.to_dict()
        executive_summary_dict_before = executive_summary.to_dict()

        build_business_decision_package(*sources)

        self.assertEqual(
            _decision_evaluation_to_dict(decision_evaluation),
            decision_dict_before,
        )
        self.assertEqual(snapshot.to_dict(), snapshot_dict_before)
        self.assertEqual(confidence.to_dict(), confidence_dict_before)
        self.assertEqual(priority.to_dict(), priority_dict_before)
        self.assertEqual(executive_summary.to_dict(), executive_summary_dict_before)

    def test_package_to_dict_preserves_existing_outputs(self):
        sources = valid_sources(scale_value=1, numeric_value=25)
        package = build_business_decision_package(*sources)
        package_dict = package.to_dict()

        self.assertEqual(
            package_dict["decisionEvaluation"],
            _decision_evaluation_to_dict(sources[0]),
        )
        self.assertEqual(
            package_dict["businessReadinessSnapshot"],
            sources[1].to_dict(),
        )
        self.assertEqual(package_dict["confidenceEvaluation"], sources[2].to_dict())
        self.assertEqual(
            package_dict["recommendationPriorityEvaluation"],
            sources[3].to_dict(),
        )
        self.assertEqual(
            package_dict["executiveSummaryFoundation"],
            sources[4].to_dict(),
        )

    def test_package_uses_stable_ordering(self):
        package = build_business_decision_package(*valid_sources())
        package_dict = package.to_dict()
        decision_dict = package_dict["decisionEvaluation"]
        explanation = decision_dict["explanation"]

        self.assertEqual(
            list(decision_dict["dimensions"]),
            sorted(decision_dict["dimensions"]),
        )
        self.assertEqual(
            list(explanation["questionExplanations"]),
            sorted(explanation["questionExplanations"]),
        )
        self.assertEqual(
            list(explanation["dimensionExplanations"]),
            sorted(explanation["dimensionExplanations"]),
        )
        self.assertEqual(
            list(package_dict["versionMetadata"]["componentVersions"]),
            list(BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS),
        )

    def test_version_metadata_integrity(self):
        decision_evaluation, snapshot, confidence, priority, summary = valid_sources()
        package = build_business_decision_package(
            decision_evaluation,
            snapshot,
            confidence,
            priority,
            summary,
        )

        self.assertEqual(
            package.version_metadata.contract_version,
            BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
        )
        self.assertEqual(
            package.version_metadata.assessment_version,
            snapshot.assessment_version,
        )
        self.assertEqual(
            package.version_metadata.methodology_version,
            snapshot.audit.methodology_version,
        )
        self.assertEqual(
            package.version_metadata.component_versions,
            BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS,
        )

    def test_audit_object_integrity(self):
        decision_evaluation, snapshot, confidence, priority, summary = valid_sources()

        package = build_business_decision_package(
            decision_evaluation,
            snapshot,
            confidence,
            priority,
            summary,
        )

        self.assertEqual(package.audit.assessment_version, snapshot.assessment_version)
        self.assertEqual(
            package.audit.methodology_version,
            snapshot.audit.methodology_version,
        )
        self.assertEqual(
            package.audit.source_component_ids,
            BUSINESS_DECISION_PACKAGE_SOURCE_COMPONENTS,
        )
        self.assertEqual(
            package.audit.evaluated_dimensions,
            snapshot.audit.evaluated_dimensions,
        )
        self.assertEqual(package.audit.question_count, snapshot.audit.question_count)
        self.assertEqual(package.audit.total_weight, snapshot.audit.total_weight)

    def test_limitations_are_preserved_without_mutating_package(self):
        package = build_business_decision_package(*valid_sources())
        package_dict = package.to_dict()

        self.assertEqual(package.limitations, BUSINESS_DECISION_PACKAGE_LIMITATIONS)
        self.assertEqual(
            package_dict["limitations"],
            list(BUSINESS_DECISION_PACKAGE_LIMITATIONS),
        )

        package_dict["limitations"].append("local-dict-mutation")

        self.assertNotIn("local-dict-mutation", package.limitations)

    def test_mismatched_assessment_versions_are_rejected(self):
        decision_evaluation, snapshot, confidence, priority, summary = valid_sources()
        invalid_summary = replace(
            summary,
            assessment_version="other-assessment-version",
        )

        with self.assertRaisesRegex(ValueError, "assessment versions"):
            build_business_decision_package(
                decision_evaluation,
                snapshot,
                confidence,
                priority,
                invalid_summary,
            )

    def test_mismatched_methodology_versions_are_rejected(self):
        decision_evaluation, snapshot, confidence, priority, summary = valid_sources()
        invalid_priority = replace(
            priority,
            methodology_version="other-methodology-version",
        )

        with self.assertRaisesRegex(ValueError, "methodology versions"):
            build_business_decision_package(
                decision_evaluation,
                snapshot,
                confidence,
                invalid_priority,
                summary,
            )

    def test_decision_snapshot_score_mismatch_is_rejected(self):
        decision_evaluation, snapshot, confidence, priority, summary = valid_sources()
        invalid_snapshot = replace(
            snapshot,
            overall_readiness=replace(snapshot.overall_readiness, score=0),
        )

        with self.assertRaisesRegex(ValueError, "score"):
            build_business_decision_package(
                decision_evaluation,
                invalid_snapshot,
                confidence,
                priority,
                summary,
            )

    def test_decision_snapshot_audit_mismatch_is_rejected(self):
        decision_evaluation, snapshot, confidence, priority, summary = valid_sources()
        invalid_snapshot = replace(
            snapshot,
            audit=replace(snapshot.audit, question_count=0),
        )

        with self.assertRaisesRegex(ValueError, "question count"):
            build_business_decision_package(
                decision_evaluation,
                invalid_snapshot,
                confidence,
                priority,
                summary,
            )

    def test_package_contract_stays_within_assembly_scope(self):
        package_dict = build_business_decision_package(*valid_sources()).to_dict()

        self.assertEqual(
            set(package_dict),
            {
                "decisionEvaluation",
                "businessReadinessSnapshot",
                "confidenceEvaluation",
                "recommendationPriorityEvaluation",
                "executiveSummaryFoundation",
                "audit",
                "limitations",
                "versionMetadata",
            },
        )
        self.assertNotIn("recommendations", package_dict)
        self.assertNotIn("serviceRouting", package_dict)
        self.assertNotIn("serviceDecision", package_dict)
        self.assertNotIn("executiveReport", package_dict)
        self.assertNotIn("executiveNarrative", package_dict)
        self.assertNotIn("generatedAt", package_dict)
        self.assertNotIn("runtimeTimestamp", package_dict)
        self.assertNotIn("requestId", package_dict)


if __name__ == "__main__":
    unittest.main()
