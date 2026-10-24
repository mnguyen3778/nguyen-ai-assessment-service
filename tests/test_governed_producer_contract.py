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
from assessment.decision_engine import evaluate_assessment_v2
from assessment.executive_assessment_snapshot import (
    validate_executive_assessment_snapshot_serialization,
)
from assessment.executive_orchestration import orchestrate_executive_assessment
from assessment.executive_snapshot_handoff import produce_executive_assessment_snapshot
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


class GovernedProducerContractTests(unittest.TestCase):
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
