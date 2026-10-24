import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.decision_engine import evaluate_assessment_v2  # noqa: E402
from assessment.executive_orchestration import (  # noqa: E402
    ValidatedCanonicalExecutiveAssessmentInput,
    orchestrate_executive_assessment,
)
from assessment.executive_runtime import EXECUTIVE_ASSESSMENT_VERSION  # noqa: E402
from assessment.governed_assessment_input import (  # noqa: E402
    EXECUTIVE_ASSESSMENT_VERSION_V2,
    EvidenceProfileInput,
    EvidenceQualityInput,
    FindingInput,
    ValidatedCanonicalExecutiveAssessmentInputV2,
)
from assessment.methodology_config import METHODOLOGY_VERSION  # noqa: E402
from test_golden_fixture_regression import answers, evidence, finding, request  # noqa: E402


class GovernedInputContractTests(unittest.TestCase):
    def test_valid_input_is_frozen_and_canonically_ordered(self):
        high_b = finding("b", "Deficiency", "TISM", "significant gap")
        high_a = finding("a", "Deficiency", "GCR", "significant gap")
        canonical = ValidatedCanonicalExecutiveAssessmentInputV2(
            EXECUTIVE_ASSESSMENT_VERSION_V2, METHODOLOGY_VERSION,
            answers(50), evidence("adequate"), (high_b, high_a))
        self.assertEqual(tuple(x.finding_id for x in canonical.findings), ("a", "b"))
        self.assertEqual(tuple(canonical.answers), tuple(sorted(canonical.answers)))
        with self.assertRaises(FrozenInstanceError):
            canonical.findings = ()
        with self.assertRaises(TypeError):
            canonical.answers["q.ai.governance.owner"] = 4

    def test_required_fields_cannot_be_omitted(self):
        with self.assertRaises(TypeError):
            ValidatedCanonicalExecutiveAssessmentInputV2(
                EXECUTIVE_ASSESSMENT_VERSION_V2, METHODOLOGY_VERSION,
                answers(50), evidence("adequate"))
        with self.assertRaises(TypeError):
            ValidatedCanonicalExecutiveAssessmentInputV2(
                EXECUTIVE_ASSESSMENT_VERSION_V2, METHODOLOGY_VERSION,
                answers(50))

    def test_none_evidence_rejected(self):
        with self.assertRaises(ValueError):
            replace(request(50, "adequate", "none"), evidence_profile=None)

    def test_none_findings_rejected(self):
        with self.assertRaises(ValueError):
            replace(request(50, "adequate", "none"), findings=None)

    def test_empty_findings_are_valid_and_distinct_from_missing(self):
        result = evaluate_assessment_v2(request(50, "adequate", "none"))
        self.assertEqual(result.findings, ())
        self.assertEqual(result.severity_assignments, ())
        self.assertEqual(result.risk.risk_classification, "minimal-informational")
        self.assertEqual(result.recommendations[0].recommendation_decision_identifier,
                         "recommendation-v1-no-findings-monitor")

    def test_missing_required_evidence_rejected(self):
        with self.assertRaises(ValueError):
            EvidenceProfileInput(False, (EvidenceQualityInput("e", "Basic", None),))

    def test_empty_evidence_rejected(self):
        with self.assertRaises(ValueError):
            EvidenceProfileInput(True, ())

    def test_unsupported_quality_rejected(self):
        with self.assertRaises(ValueError):
            EvidenceQualityInput("e", "Excellent", None)

    def test_unsupported_limitation_rejected(self):
        with self.assertRaises(ValueError):
            EvidenceQualityInput("e", "Adequate", "uncertain")

    def test_duplicate_evidence_reference_rejected(self):
        with self.assertRaises(ValueError):
            EvidenceProfileInput(True, (
                EvidenceQualityInput("e", "Basic", None),
                EvidenceQualityInput("e", "Strong", None),
            ))

    def test_malformed_evidence_reference_rejected(self):
        with self.assertRaises(ValueError):
            EvidenceQualityInput(" ", "Adequate", None)

    def test_duplicate_finding_id_rejected(self):
        duplicate = finding("same", "Deficiency", "GCR", "significant gap")
        with self.assertRaises(ValueError):
            replace(request(50, "adequate", "none"), findings=(duplicate, duplicate))

    def test_unsupported_finding_type_rejected(self):
        with self.assertRaises(ValueError):
            finding("a", "Other", "GCR", "significant gap")

    def test_unsupported_dimension_rejected(self):
        with self.assertRaises(ValueError):
            finding("a", "Deficiency", "INVALID", "significant gap")

    def test_unsupported_consequence_rejected(self):
        with self.assertRaises(ValueError):
            finding("a", "Deficiency", "GCR", "not a governed basis")

    def test_type_consequence_mismatch_rejected(self):
        with self.assertRaises(ValueError):
            finding("a", "Strength", "POC", "material current breach")

    def test_malformed_finding_reference_rejected(self):
        with self.assertRaises(ValueError):
            replace(finding("a", "Strength", "POC", "strength"),
                    source_references=(" ",))

    def test_finding_reference_must_resolve_to_evidence(self):
        bad = replace(finding("a", "Strength", "POC", "strength"),
                      source_references=("unknown-evidence",))
        with self.assertRaises(ValueError):
            replace(request(50, "adequate", "none"), findings=(bad,))

    def test_wrong_assessment_version_rejected(self):
        with self.assertRaises(ValueError):
            replace(request(50, "adequate", "none"), assessment_version="other")

    def test_wrong_methodology_version_rejected(self):
        with self.assertRaises(ValueError):
            replace(request(50, "adequate", "none"), methodology_version="other")

    def test_v1_input_cannot_enter_v2_engine(self):
        legacy = ValidatedCanonicalExecutiveAssessmentInput(
            EXECUTIVE_ASSESSMENT_VERSION, METHODOLOGY_VERSION, answers(50))
        with self.assertRaises(ValueError):
            evaluate_assessment_v2(legacy)


class GovernedDecisionBehaviorTests(unittest.TestCase):
    def test_approved_finding_consequence_drives_severity(self):
        result = evaluate_assessment_v2(request(75, "adequate", "critical"))
        self.assertEqual(result.severity_assignments[0].severity_decision_identifier,
                         "severity-v1-deficiency-critical")
        self.assertEqual(result.severity_assignments[0].severity_classification,
                         "critical")

    def test_two_high_findings_drive_elevated_risk(self):
        result = evaluate_assessment_v2(request(75, "mixed-strong", "two-high"))
        self.assertEqual(len(result.severity_assignments), 2)
        self.assertEqual(len(result.severity_assigned_findings), 2)
        self.assertEqual(tuple(x.finding.finding_id for x in result.severity_assigned_findings),
                         ("finding-v1-high-governance-gap", "finding-v1-high-technology-gap"))
        self.assertEqual(result.risk.risk_decision_identifier,
                         "risk-v1-elevated-high-concentration")
        self.assertEqual(result.risk.risk_classification, "elevated-risk")

    def test_evidence_quality_drives_confidence(self):
        expected = {
            "basic": "low-confidence",
            "adequate": "moderate-confidence",
            "mixed-strong": "high-confidence",
            "strong": "very-high-confidence",
            "limitation": "insufficient-confidence",
        }
        for profile, confidence in expected.items():
            with self.subTest(profile=profile):
                result = evaluate_assessment_v2(request(50, profile, "none"))
                self.assertEqual(result.confidence.confidence_classification,
                                 confidence)

    def test_strength_and_no_findings_use_distinct_recommendation_rules(self):
        strength = evaluate_assessment_v2(request(100, "strong", "strength"))
        empty = evaluate_assessment_v2(request(100, "strong", "none"))
        self.assertEqual(strength.decision_evaluation, empty.decision_evaluation)
        self.assertEqual(strength.recommendations[0].recommendation_decision_identifier,
                         "recommendation-v1-strength-best-practice")
        self.assertEqual(empty.recommendations[0].recommendation_decision_identifier,
                         "recommendation-v1-no-findings-monitor")

    def test_governed_summary_uses_finding_count_and_actions(self):
        result = evaluate_assessment_v2(request(75, "mixed-strong", "two-high"))
        summary = result.executive_summary_inputs
        self.assertEqual(summary.finding_count, 2)
        self.assertIn("2 Findings", summary.section_text["significant-findings"])
        self.assertIn("2 Recommendations", summary.section_text["recommended-actions"])
        self.assertIn("elevated-risk", summary.section_text["risk-overview"])
        self.assertIn("high-confidence", summary.section_text["confidence-statement"])

    def test_v2_orchestration_forwards_governed_input(self):
        governed = request(75, "adequate", "critical")
        result = orchestrate_executive_assessment(governed)
        self.assertTrue(result.is_success, result.failure)
        self.assertEqual(result.business_decision_package.version_metadata.assessment_version,
                         EXECUTIVE_ASSESSMENT_VERSION_V2)


if __name__ == "__main__":
    unittest.main()
