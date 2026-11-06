"""Gap 2 producer truth, convergence, and fail-closed representation tests."""

import copy
import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.business_decision_package_validation import (
    validate_business_decision_package,
    validate_business_decision_package_serialization,
)
from assessment.approved_methodology_runtime_config import (
    APPROVED_RECOMMENDATION_ACTION_TEXT_BY_RULE,
)
from assessment.business_decision_package import (
    ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    build_business_decision_package,
)
from assessment.decision_engine import evaluate_assessment_v2
from assessment.executive_assessment_snapshot import (
    validate_executive_assessment_snapshot_serialization,
)
from assessment.executive_orchestration import orchestrate_executive_assessment
from assessment.executive_snapshot_handoff import produce_executive_assessment_snapshot
from assessment.governed_assessment_input import FindingInput
from test_golden_fixture_regression import request


def package_and_snapshot(score, profile, findings):
    canonical = request(score, profile, findings)
    engine = evaluate_assessment_v2(canonical)
    orchestration = orchestrate_executive_assessment(canonical)
    assert orchestration.is_success, orchestration.failure
    package = orchestration.business_decision_package
    produced = produce_executive_assessment_snapshot(canonical)
    assert produced.is_success, produced.failure
    return engine, package, produced.serialized_snapshot


def local_v3_package(canonical):
    orchestration = orchestrate_executive_assessment(canonical)
    assert orchestration.is_success, orchestration.failure
    v2 = orchestration.business_decision_package
    v3 = build_business_decision_package(
        v2.decision_evaluation,
        v2.business_readiness_snapshot,
        v2.confidence_evaluation,
        v2.recommendation_priority_evaluation,
        v2.executive_summary_foundation,
        governed_result=v2.governed_conclusions,
        governed_package_contract_version=ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    )
    return v2, v3


class GovernedProducerContractTests(unittest.TestCase):
    def test_local_v3_serialization_is_explicit_exact_and_deterministic(self):
        cases = (
            request(75, "adequate", "critical"),
            request(75, "mixed-strong", "two-high"),
            request(50, "adequate", "medium"),
            request(50, "adequate", "low"),
            request(100, "strong", "strength"),
            request(50, "adequate", "none"),
        )
        for kind, basis in (("Observation", "observation"),
                            ("Opportunity", "opportunity")):
            finding = FindingInput(
                "finding-local-" + kind.lower(), "Local finding", "POC", (),
                "fixture-input", kind, basis, ("fixture-input",),
            )
            cases += (replace(request(50, "adequate", "none"),
                              findings=(finding,)),)

        observed_rules = set()
        fields_v2 = (
            "findingId", "recommendationClassification",
            "recommendationDecisionIdentifier", "recommendationDecisionTableVersion",
        )
        for canonical in cases:
            with self.subTest(findings=canonical.findings):
                v2, v3 = local_v3_package(canonical)
                old = v2.to_dict()
                new = v3.to_dict()
                self.assertEqual(v2.version_metadata.contract_version,
                                 GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION)
                self.assertEqual(v3.version_metadata.contract_version,
                                 ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION)
                self.assertEqual(new, v3.to_dict())
                self.assertEqual(old, v2.to_dict())
                self.assertEqual(v2.governed_conclusions, v3.governed_conclusions)
                old_rows = old["governedConclusions"]["recommendations"]
                new_rows = new["governedConclusions"]["recommendations"]
                self.assertEqual(len(old_rows), len(new_rows))
                for old_row, new_row in zip(old_rows, new_rows):
                    self.assertEqual(tuple(old_row), fields_v2)
                    self.assertEqual(tuple(new_row), fields_v2 + ("recommendationActionText",))
                    self.assertEqual({key: new_row[key] for key in fields_v2}, old_row)
                    self.assertEqual(new_row["recommendationActionText"],
                                     APPROVED_RECOMMENDATION_ACTION_TEXT_BY_RULE[
                                         old_row["recommendationDecisionIdentifier"]])
                    observed_rules.add(old_row["recommendationDecisionIdentifier"])
                self.assertFalse(validate_business_decision_package_serialization(new).is_valid)
        self.assertEqual(observed_rules, set(APPROVED_RECOMMENDATION_ACTION_TEXT_BY_RULE))

    def test_no_findings_v3_is_local_and_v2_snapshot_has_no_action_text(self):
        canonical = request(50, "adequate", "none")
        v2, v3 = local_v3_package(canonical)
        row = v3.to_dict()["governedConclusions"]["recommendations"][0]
        self.assertIsNone(row["findingId"])
        self.assertEqual(row["recommendationClassification"], "monitor")
        self.assertEqual(row["recommendationDecisionIdentifier"],
                         "recommendation-v1-no-findings-monitor")
        produced = produce_executive_assessment_snapshot(canonical)
        self.assertTrue(produced.is_success)
        self.assertEqual(produced.serialized_snapshot["businessDecisionPackage"], v2.to_dict())
        self.assertNotIn("recommendationActionText",
                         produced.serialized_snapshot["businessDecisionPackage"][
                             "governedConclusions"]["recommendations"][0])

    def test_local_v3_selection_and_serialization_fail_closed(self):
        canonical = request(75, "adequate", "critical")
        v2, v3 = local_v3_package(canonical)
        sources = (
            v2.decision_evaluation, v2.business_readiness_snapshot,
            v2.confidence_evaluation, v2.recommendation_priority_evaluation,
            v2.executive_summary_foundation,
        )
        with self.assertRaisesRegex(ValueError, "Unsupported governed package"):
            build_business_decision_package(*sources, governed_result=v2.governed_conclusions,
                                            governed_package_contract_version="unsupported")
        with self.assertRaisesRegex(ValueError, "requires a governed"):
            build_business_decision_package(*sources,
                                            governed_package_contract_version=ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION)
        item = v3.governed_conclusions.recommendations[0]
        for changed in (
            replace(item, recommendation_decision_identifier="unknown-rule"),
            replace(item, recommendation_decision_identifier="recommendation-v1-reject-missing-risk"),
            replace(item, recommendation_classification="monitor"),
            replace(item, recommendation_decision_table_version="unsupported-version"),
            replace(item, finding_id="other-finding"),
        ):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                altered = replace(v3, governed_conclusions=replace(
                    v3.governed_conclusions, recommendations=(changed,)))
                altered.to_dict()
        _, medium_v3 = local_v3_package(request(50, "adequate", "medium"))
        medium_item = medium_v3.governed_conclusions.recommendations[0]
        wrong_rule_same_classification = replace(
            medium_item,
            recommendation_decision_identifier="recommendation-v1-deficiency-low-planned",
        )
        with self.assertRaisesRegex(ValueError, "does not match its finding"):
            replace(medium_v3, governed_conclusions=replace(
                medium_v3.governed_conclusions,
                recommendations=(wrong_rule_same_classification,),
            )).to_dict()

    def test_package_snapshot_converge_and_empty_findings_are_explicit(self):
        engine, package, snapshot = package_and_snapshot(50, "adequate", "none")
        truth = package.to_dict()["governedConclusions"]
        self.assertEqual(truth["severityAssignedFindings"], [])
        self.assertEqual(truth["assessmentRisk"]["riskClassification"], engine.risk.risk_classification)
        self.assertEqual(truth["confidence"]["confidenceClassification"], engine.confidence.confidence_classification)
        self.assertEqual(truth["recommendations"][0]["recommendationDecisionIdentifier"],
                         "recommendation-v1-no-findings-monitor")
        self.assertEqual(snapshot["businessDecisionPackage"], package.to_dict())
        self.assertTrue(validate_business_decision_package(package).is_valid)
        self.assertTrue(validate_executive_assessment_snapshot_serialization(snapshot).is_valid)

    def test_same_score_evidence_and_findings_survive_both_producer_layers(self):
        adequate = package_and_snapshot(50, "adequate", "none")
        basic = package_and_snapshot(50, "basic", "none")
        medium = package_and_snapshot(50, "adequate", "medium")
        low = package_and_snapshot(50, "adequate", "low")
        for left, right, path in (
            (adequate, basic, ("confidence", "confidenceClassification")),
            (medium, low, ("severityAssignedFindings", 0, "severityClassification")),
            (medium, low, ("assessmentRisk", "riskClassification")),
            (medium, low, ("recommendations", 0, "recommendationDecisionIdentifier")),
        ):
            self.assertEqual(left[0].decision_evaluation, right[0].decision_evaluation)
            for result in (left, right):
                self.assertEqual(result[1].to_dict()["governedConclusions"],
                                 result[2]["businessDecisionPackage"]["governedConclusions"])
            def value(result):
                item = result[1].to_dict()["governedConclusions"]
                for key in path:
                    item = item[key]
                return item
            self.assertNotEqual(value(left), value(right))

    def test_malformed_serialized_truth_fails_closed(self):
        _, package, snapshot = package_and_snapshot(75, "adequate", "critical")
        base = package.to_dict()
        changes = (
            lambda d: d["governedConclusions"].pop("confidence"),
            lambda d: d["governedConclusions"]["severityAssignedFindings"][0].__setitem__("severityClassification", "unknown"),
            lambda d: d["governedConclusions"]["assessmentRisk"].__setitem__("riskClassification", "unknown"),
            lambda d: d["governedConclusions"]["confidence"].__setitem__("confidenceClassification", "unknown"),
            lambda d: d["governedConclusions"]["recommendations"][0].__setitem__("recommendationDecisionIdentifier", "unknown"),
            lambda d: d["governedConclusions"]["severityAssignedFindings"].append(copy.deepcopy(d["governedConclusions"]["severityAssignedFindings"][0])),
            lambda d: d["governedConclusions"]["recommendations"].reverse() or d["governedConclusions"]["recommendations"].append(copy.deepcopy(d["governedConclusions"]["recommendations"][0])),
            lambda d: d["versionMetadata"].__setitem__("methodologyVersion", "unknown"),
            lambda d: d["versionMetadata"].__setitem__("contractVersion", "business-decision-package-v1"),
        )
        for change in changes:
            with self.subTest(change=change):
                altered = copy.deepcopy(base)
                change(altered)
                self.assertFalse(validate_business_decision_package_serialization(altered).is_valid)
                altered_snapshot = copy.deepcopy(snapshot)
                altered_snapshot["businessDecisionPackage"] = altered
                self.assertFalse(validate_executive_assessment_snapshot_serialization(altered_snapshot).is_valid)
        self.assertFalse(validate_business_decision_package(replace(package, governed_conclusions=None)).is_valid)

    def test_malformed_empty_findings_is_rejected(self):
        _, package, _ = package_and_snapshot(50, "adequate", "none")
        altered = package.to_dict()
        altered["governedConclusions"]["recommendations"] = []
        self.assertFalse(validate_business_decision_package_serialization(altered).is_valid)

    def test_noncanonical_finding_and_recommendation_order_is_rejected(self):
        _, package, _ = package_and_snapshot(75, "mixed-strong", "two-high")
        for field in ("severityAssignedFindings", "recommendations"):
            with self.subTest(field=field):
                altered = package.to_dict()
                altered["governedConclusions"][field].reverse()
                self.assertFalse(validate_business_decision_package_serialization(altered).is_valid)

    def test_missing_internal_governed_result_fails_closed(self):
        _, package, _ = package_and_snapshot(50, "adequate", "none")
        malformed = replace(package, governed_conclusions=replace(
            package.governed_conclusions, risk=None))
        self.assertFalse(validate_business_decision_package(malformed).is_valid)
