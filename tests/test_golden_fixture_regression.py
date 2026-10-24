"""Golden Fixture payloads exercised through the governed v2 engine."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_METHODOLOGY_RUNTIME_CONFIG as CONFIG,
)
from assessment.approved_question_scoring_runtime import score_approved_questions  # noqa: E402
from assessment.approved_dimension_aggregation_runtime import aggregate_approved_dimensions  # noqa: E402
from assessment.approved_dimension_weighting_runtime import weight_approved_dimensions  # noqa: E402
from assessment.approved_overall_assessment_runtime import calculate_approved_overall_assessment  # noqa: E402
from assessment.business_decision_package import (  # noqa: E402
    BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BUSINESS_DECISION_PACKAGE_LIMITATIONS,
)
from assessment.decision_engine import evaluate_assessment_v2  # noqa: E402
from assessment.executive_orchestration import (  # noqa: E402
    ValidatedCanonicalExecutiveAssessmentInput,
    orchestrate_executive_assessment,
)
from assessment.executive_runtime import (  # noqa: E402
    EXECUTIVE_ASSESSMENT_VERSION,
    EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
    NOT_PRODUCTION_AUTHORITATIVE,
)
from assessment.executive_snapshot_handoff import produce_executive_assessment_snapshot  # noqa: E402
from assessment.governed_assessment_input import (  # noqa: E402
    EXECUTIVE_ASSESSMENT_VERSION_V2,
    EvidenceProfileInput,
    EvidenceQualityInput,
    FindingInput,
    ValidatedCanonicalExecutiveAssessmentInputV2,
)
from assessment.methodology_config import METHODOLOGY_VERSION  # noqa: E402


READINESS_BY_SCORE = {
    0: "Not Ready", 25: "Developing", 50: "Ready",
    75: "Advanced", 100: "Advanced",
}


# The distinct expected outputs below are from Golden Fixture Payloads v1, §5.
# They are intentionally keyed by fixture ID rather than by score.
FIXTURES = (
    ("fixture-v1-complete-minimal-risk", 100, "strong", "strength", ("informational",), "minimal-informational", "very-high-confidence", ("best-practice",), ("recommendation-v1-strength-best-practice",)),
    ("fixture-v1-complete-not-ready-readiness", 0, "adequate", "none", (), "minimal-informational", "moderate-confidence", ("monitor",), ("recommendation-v1-no-findings-monitor",)),
    ("fixture-v1-complete-developing-readiness", 25, "adequate", "none", (), "minimal-informational", "moderate-confidence", ("monitor",), ("recommendation-v1-no-findings-monitor",)),
    ("fixture-v1-complete-ready-readiness", 50, "adequate", "none", (), "minimal-informational", "moderate-confidence", ("monitor",), ("recommendation-v1-no-findings-monitor",)),
    ("fixture-v1-complete-advanced-readiness", 75, "adequate", "none", (), "minimal-informational", "moderate-confidence", ("monitor",), ("recommendation-v1-no-findings-monitor",)),
    ("fixture-v1-critical-finding-risk", 75, "adequate", "critical", ("critical",), "critical-risk", "moderate-confidence", ("immediate-action",), ("recommendation-v1-deficiency-critical-immediate",)),
    ("fixture-v1-high-concentration-risk", 75, "mixed-strong", "two-high", ("high", "high"), "elevated-risk", "high-confidence", ("priority-action", "priority-action"), ("recommendation-v1-deficiency-high-priority",) * 2),
    ("fixture-v1-medium-risk", 50, "adequate", "medium", ("medium",), "moderate-risk", "moderate-confidence", ("planned-improvement",), ("recommendation-v1-deficiency-medium-planned",)),
    ("fixture-v1-low-risk", 50, "adequate", "low", ("low",), "low-risk", "moderate-confidence", ("planned-improvement",), ("recommendation-v1-deficiency-low-planned",)),
    ("fixture-v1-evidence-basic-confidence", 50, "basic", "none", (), "minimal-informational", "low-confidence", ("monitor",), ("recommendation-v1-no-findings-monitor",)),
    ("fixture-v1-evidence-strong-confidence", 75, "strong", "none", (), "minimal-informational", "very-high-confidence", ("monitor",), ("recommendation-v1-no-findings-monitor",)),
    ("fixture-v1-evidence-assertability-limitation", 50, "limitation", "none", (), "minimal-informational", "insufficient-confidence", ("monitor",), ("recommendation-v1-no-findings-monitor",)),
    ("fixture-v1-no-findings-recommendation", 100, "adequate", "none", (), "minimal-informational", "moderate-confidence", ("monitor",), ("recommendation-v1-no-findings-monitor",)),
)


def answers(score):
    return {
        question_id: (score if question.response_model_id == "numeric-0-100" else score // 25)
        for question_id, question in CONFIG.questions.items()
    }


def evidence(profile):
    if profile == "mixed-strong":
        items = (EvidenceQualityInput("fixture-input", "Strong", None),
                 EvidenceQualityInput("fixture-input-2", "Adequate", None))
    elif profile == "limitation":
        items = (EvidenceQualityInput("fixture-input", "Adequate", "traceability"),)
    else:
        items = (EvidenceQualityInput("fixture-input", {
            "basic": "Basic", "adequate": "Adequate", "strong": "Strong"
        }[profile], None),)
    return EvidenceProfileInput(True, items)


def finding(identifier, kind, dimension, basis):
    return FindingInput(identifier, identifier, dimension, (), "fixture-input",
                        kind, basis, ("fixture-input",))


def findings(payload):
    return {
        "none": (),
        "strength": (finding("finding-v1-strength-operating-practice", "Strength", "POC", "strength"),),
        "critical": (finding("finding-v1-critical-governance-breach", "Deficiency", "GCR", "material current breach"),),
        "two-high": (
            finding("finding-v1-high-governance-gap", "Deficiency", "GCR", "significant gap"),
            finding("finding-v1-high-technology-gap", "Deficiency", "TISM", "significant gap"),
        ),
        "medium": (finding("finding-v1-medium-process-deficiency", "Deficiency", "POC", "clear deficiency"),),
        "low": (finding("finding-v1-low-control-weakness", "Deficiency", "RVCI", "limited weakness"),),
    }[payload]


def request(score, profile, payload):
    return ValidatedCanonicalExecutiveAssessmentInputV2(
        EXECUTIVE_ASSESSMENT_VERSION_V2, METHODOLOGY_VERSION,
        answers(score), evidence(profile), findings(payload)
    )


class GoldenFixtureRegressionTests(unittest.TestCase):
    def test_catalog_is_complete_and_ordered(self):
        self.assertEqual(tuple(row[0] for row in FIXTURES) + (
            "fixture-v1-invalid-input-fail-closed",
            "fixture-v1-version-mismatch-fail-closed",
        ), tuple(CONFIG.golden_fixtures))

    def test_complete_fixtures_execute_real_v2_path(self):
        for (fixture_id, score, profile, payload, severities, risk, confidence,
             actions, rule_ids) in FIXTURES:
            with self.subTest(fixture_id=fixture_id):
                canonical = request(score, profile, payload)
                scored = score_approved_questions(canonical.answers, METHODOLOGY_VERSION)
                self.assertEqual(scored.question_count, 48)
                self.assertTrue(all(item.score == score for item in scored.question_scores))
                aggregated = aggregate_approved_dimensions(scored)
                self.assertTrue(all(item.score == score for item in aggregated.dimensions))
                weighted = weight_approved_dimensions(aggregated)
                self.assertEqual(calculate_approved_overall_assessment(weighted).overall_assessment_score,
                                 score)
                result = evaluate_assessment_v2(canonical)
                self.assertEqual(result.decision_evaluation.overall_score, score)
                self.assertEqual(result.readiness.readiness_score, score)
                self.assertEqual(result.readiness.readiness_classification,
                                 READINESS_BY_SCORE[score])
                self.assertEqual(len(result.decision_evaluation.explanation.contributing_questions), 48)
                self.assertEqual(result.findings, canonical.findings)
                self.assertEqual(tuple(x.finding.finding_id for x in result.severity_assigned_findings),
                                 tuple(x.finding_id for x in canonical.findings))
                self.assertEqual(tuple(x.sequence_identifier for x in result.severity_assigned_findings),
                                 tuple(range(1, len(canonical.findings) + 1)))
                self.assertTrue(all(x.linked_readiness == result.readiness.readiness_classification
                                    for x in result.severity_assigned_findings))
                self.assertTrue(all(x.evidence_qualities for x in result.severity_assigned_findings))
                self.assertEqual(tuple(x.severity_classification for x in result.severity_assignments), severities)
                self.assertTrue(all(x.decision_table_version ==
                                    CONFIG.version_manifest.severity_decision_table_set_version
                                    for x in result.severity_assignments))
                self.assertEqual(result.risk.risk_classification, risk)
                self.assertEqual(result.risk.risk_decision_table_version,
                                 CONFIG.version_manifest.risk_decision_table_set_version)
                self.assertEqual(result.confidence.confidence_classification, confidence)
                self.assertEqual(result.confidence.confidence_decision_table_version,
                                 CONFIG.version_manifest.confidence_decision_table_set_version)
                self.assertEqual(tuple(x.recommendation_classification for x in result.recommendations), actions)
                self.assertEqual(tuple(x.recommendation_decision_identifier for x in result.recommendations), rule_ids)
                self.assertTrue(all(x.recommendation_decision_table_version ==
                                    CONFIG.version_manifest.recommendation_decision_table_set_version
                                    for x in result.recommendations))
                summary = result.executive_summary_inputs
                self.assertEqual(tuple(summary.section_text), tuple(CONFIG.executive_summary_sections))
                self.assertEqual(summary.finding_count, len(canonical.findings))
                self.assertEqual(summary.severity_classifications, severities)
                self.assertEqual(summary.risk_classification, risk)
                self.assertEqual(summary.confidence_classification, confidence)
                self.assertEqual(summary.recommendation_classifications, actions)
                self.assertIn(risk, summary.section_text["risk-overview"])
                self.assertIn(confidence, summary.section_text["confidence-statement"])
                if not canonical.findings:
                    self.assertEqual(summary.section_text["significant-findings"],
                                     "The assessment produced no Findings.")
                orchestration = orchestrate_executive_assessment(canonical)
                self.assertTrue(orchestration.is_success, orchestration.failure)
                package = orchestration.business_decision_package
                self.assertEqual(package.version_metadata.contract_version,
                                 BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION)
                self.assertEqual(package.version_metadata.assessment_version,
                                 EXECUTIVE_ASSESSMENT_VERSION_V2)
                self.assertEqual(package.limitations, BUSINESS_DECISION_PACKAGE_LIMITATIONS)

    def test_existing_v1_package_snapshot_contract_remains_intact(self):
        # This tests the frozen producer boundary only. Governed conclusions
        # are verified through v2 above and remain internal until Gap 2.
        for score in READINESS_BY_SCORE:
            with self.subTest(score=score):
                legacy = ValidatedCanonicalExecutiveAssessmentInput(
                    EXECUTIVE_ASSESSMENT_VERSION, METHODOLOGY_VERSION,
                    answers(score))
                produced = produce_executive_assessment_snapshot(legacy)
                self.assertTrue(produced.is_success, produced.failure)
                serialized = produced.serialized_snapshot
                self.assertEqual(serialized["responseContractVersion"],
                                 EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION)
                self.assertEqual(serialized["responseStatus"]["productionAuthority"],
                                 NOT_PRODUCTION_AUTHORITATIVE)
                package = serialized["businessDecisionPackage"]
                self.assertEqual(package["versionMetadata"]["contractVersion"],
                                 BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION)
                self.assertEqual(package["decisionEvaluation"]["overallScore"], score)
                self.assertEqual(package["businessReadinessSnapshot"]["overallReadiness"]["score"],
                                 score)

    def test_same_score_distinct_profiles(self):
        adequate = evaluate_assessment_v2(request(50, "adequate", "none"))
        basic = evaluate_assessment_v2(request(50, "basic", "none"))
        medium = evaluate_assessment_v2(request(50, "adequate", "medium"))
        low = evaluate_assessment_v2(request(50, "adequate", "low"))
        self.assertEqual(adequate.decision_evaluation, basic.decision_evaluation)
        self.assertNotEqual(adequate.confidence.confidence_classification,
                            basic.confidence.confidence_classification)
        self.assertEqual(medium.decision_evaluation, low.decision_evaluation)
        self.assertNotEqual(medium.severity_assignments[0].severity_classification,
                            low.severity_assignments[0].severity_classification)
        self.assertNotEqual(medium.risk.risk_classification, low.risk.risk_classification)
        self.assertNotEqual(medium.recommendations[0].recommendation_decision_identifier,
                            low.recommendations[0].recommendation_decision_identifier)
        critical = evaluate_assessment_v2(request(75, "adequate", "critical"))
        no_findings = evaluate_assessment_v2(request(75, "adequate", "none"))
        self.assertEqual(critical.decision_evaluation, no_findings.decision_evaluation)
        self.assertNotEqual(critical.recommendations[0].recommendation_classification,
                            no_findings.recommendations[0].recommendation_classification)

    def test_invalid_question_fixture_fails_closed(self):
        incomplete = answers(50)
        del incomplete["q.ai.governance.owner"]
        canonical = ValidatedCanonicalExecutiveAssessmentInputV2(
            EXECUTIVE_ASSESSMENT_VERSION_V2, METHODOLOGY_VERSION,
            incomplete, evidence("adequate"), ())
        with self.assertRaises(ValueError):
            evaluate_assessment_v2(canonical)

    def test_version_mismatch_fixture_fails_closed(self):
        with self.assertRaises(ValueError):
            ValidatedCanonicalExecutiveAssessmentInputV2(
                EXECUTIVE_ASSESSMENT_VERSION_V2, "unsupported-methodology-version",
                answers(50), evidence("adequate"), ())


if __name__ == "__main__":
    unittest.main()
