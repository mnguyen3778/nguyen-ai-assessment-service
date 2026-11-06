"""Synthetic-only D8 methodology checks; no producer integration."""

import itertools
import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.approved_methodology_runtime_config import (  # noqa: E402
    SEVERITY_DECISION_RULES, RECOMMENDATION_DECISION_RULES,
    SEVERITY_DECISION_TABLE_SET_VERSION, RISK_DECISION_TABLE_SET_VERSION,
    CONFIDENCE_DECISION_TABLE_SET_VERSION,
)
from assessment.governed_assessment_input import (  # noqa: E402
    FindingInput, FINDING_CONSEQUENCE_RULES,
)
from assessment.governed_decision_runtime import (  # noqa: E402
    GovernedRecommendationResult, RECOMMENDATION_RULE_BY_FINDING,
)
from assessment.local_priority_assertions import (  # noqa: E402
    ABSENCE_VALUES, APPLICABILITY_RULE_VERSION, ASSERTION_CONTRACT_VERSION,
    AUTHORITY_BY_DRIVER, RecommendationInstance, SyntheticContext,
    SyntheticEvidence,
)
from assessment.local_d8_priority import (  # noqa: E402
    BLOCKED_REQUIRED_EVIDENCE, INSUFFICIENT_CONFIDENCE,
    NO_FINDINGS_MONITOR, PRIORITY_ASSIGNED, PRIORITY_NOT_DETERMINED,
    REJECTED_INVALID_ASSERTION, LocalD8Input, _resolve_level,
    evaluate_local_d8_priority,
)


PAIRS = (
    ("Deficiency", "material current breach"),
    ("Deficiency", "significant gap"),
    ("Deficiency", "clear deficiency"),
    ("Deficiency", "limited weakness"),
    ("Observation", "observation"),
    ("Strength", "strength"),
    ("Opportunity", "opportunity"),
)
DRIVERS = ("customer-impact", "executive-urgency", "dependency-role")
VALUES = (
    {"P": "impact-present", "A": "impact-affirmed-absent"},
    {"T": "time-bound-executive-action", "U": "executive-action-required",
     "A": "executive-action-affirmed-absent"},
    {"P": "blocks-related-work", "A": "no-dependency-affirmed"},
)
# Independent transcription of Document 43 Section 12; never derived from evaluator.
ORACLE = (
    ("C+H1", "H1", "H1", "H1", "-", "-", "C", "-", "-", "-", "-", "-"),
    ("H2", "H2", "H2", "H2", "H2", "-", "H2", "-", "-", "-", "-", "-"),
    ("H3", "H3", "-", "-", "-", "-", "-", "-", "-", "-", "-", "M1"),
    ("-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "L1"),
    ("H7", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "L1"),
    ("H7", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "L1"),
    ("H7", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "L1"),
)
ELIGIBLE_IDS = (
    ("B-C1", "G-H1"), ("G-H2",), ("B-H3", "B-M1"),
    ("G-L1",), ("N-H7", "G-L1"), ("N-H7", "G-L1"),
    ("N-H7", "G-L1"),
)
RULE = {"C": ("critical", "B-C1"), "H1": ("high", "G-H1"),
        "H2": ("high", "G-H2"), "H3": ("high", "B-H3"),
        "H7": ("high", "N-H7"), "M1": ("medium", "B-M1"),
        "L1": ("low", "G-L1")}


def fixture(pair=PAIRS[0], states=("P", "T", "P")):
    severity = SEVERITY_DECISION_RULES[FINDING_CONSEQUENCE_RULES[pair]].output
    rule_id = RECOMMENDATION_RULE_BY_FINDING[(pair[0], severity)]
    rec_rule = RECOMMENDATION_DECISION_RULES[rule_id]
    findings = tuple(FindingInput(f"finding-{i}", "Synthetic finding", "POC", (),
                                  "synthetic-trigger", pair[0], pair[1],
                                  ("synthetic-source",)) for i in (1, 2))
    recommendations = tuple(GovernedRecommendationResult(
        f"finding-{i}", rec_rule.output, rec_rule.id, rec_rule.table_version
    ) for i in (1, 2))
    instances = tuple(RecommendationInstance(f"instance-{i}", f"finding-{i}",
                                              rule_id) for i in (1, 2))
    records, evidence = [], {}
    for driver, vocabulary, state in zip(DRIVERS, VALUES, states):
        if state is None:
            continue
        value = vocabulary[state]
        ref = f"evidence-{driver}"
        target = "instance-2" if driver == "dependency-role" and state == "P" else None
        timing = "synthetic-timing" if driver == "executive-urgency" and state == "T" else None
        evidence[ref] = SyntheticEvidence(ref, driver, value, "instance-1",
                                          scope_confirmed=value in ABSENCE_VALUES,
                                          timing_basis_reference=timing,
                                          target_reference=target)
        records.append({
            "assertionId": f"assertion-{driver}",
            "assessmentSnapshotIdentity": "snapshot-1",
            "assessmentIdentity": "assessment-1",
            "recommendationInstanceIdentity": "instance-1",
            "findingId": "finding-1",
            "recommendationDecisionIdentifier": rule_id,
            "recommendationDecisionTableVersion": rec_rule.table_version,
            "driverId": driver, "assertedValue": value,
            "applicabilityStatus": "evaluated",
            "applicabilityRuleId": f"local-{driver}-evaluated-v1",
            "applicabilityRuleVersion": APPLICABILITY_RULE_VERSION,
            "evidenceReferences": [ref],
            "businessAuthorityReference": AUTHORITY_BY_DRIVER[driver],
            "sourceRevision": "rev-1", "currentnessReference": "current-1",
            "assertionContractVersion": ASSERTION_CONTRACT_VERSION,
            "targetReference": target, "timingBasisReference": timing,
        })
    context = SyntheticContext("snapshot-1", "assessment-1", instances,
                               evidence, {"current-1": "rev-1"})
    return LocalD8Input(findings, recommendations, "instance-1", context,
                        records, (severity, severity), "moderate-risk",
                        "high-confidence",
                        (FINDING_CONSEQUENCE_RULES[pair],) * 2,
                        SEVERITY_DECISION_TABLE_SET_VERSION,
                        "risk-v1-moderate-single-high",
                        RISK_DECISION_TABLE_SET_VERSION,
                        "confidence-v1-high-strong-present",
                        CONFIDENCE_DECISION_TABLE_SET_VERSION)


def without(data, driver):
    return replace(data, records=[r for r in data.records if r["driverId"] != driver])


class LocalD8Tests(unittest.TestCase):
    def test_all_84_document_43_cases(self):
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "PND": 0}
        tuples = tuple(itertools.product("PA", "TUA", "PA"))
        for pair, expected_row, eligible_ids in zip(PAIRS, ORACLE, ELIGIBLE_IDS):
            for states, expected in zip(tuples, expected_row):
                with self.subTest(pair=pair, states=states):
                    result = evaluate_local_d8_priority(fixture(pair, states))
                    if expected == "-":
                        self.assertEqual(result.outcome, PRIORITY_NOT_DETERMINED)
                        self.assertIsNone(result.priority)
                        self.assertTrue(result.review_required)
                        self.assertEqual(
                            (result.governed_finding_type, result.governed_consequence_basis),
                            pair)
                        self.assertEqual(result.evaluated_driver_values,
                                         tuple((driver, vocabulary[state])
                                               for driver, vocabulary, state in
                                               zip(DRIVERS, VALUES, states)))
                        self.assertEqual(result.excluded_rule_ids,
                                         tuple(sorted(eligible_ids)))
                        self.assertEqual(result.methodology_version,
                                         "founder-d8-methodology-approval-v1-local-synthetic")
                        self.assertEqual(result.rule_table_version,
                                         "local-synthetic-d8-rule-table-v1")
                        self.assertEqual(result.snapshot_identity, "snapshot-1")
                        self.assertEqual(result.assessment_identity, "assessment-1")
                        self.assertEqual(result.recommendation_instance_identity, "instance-1")
                        self.assertEqual(result.finding_id, "finding-1")
                        self.assertEqual(result.validated_assertion_ids,
                                         tuple(sorted(f"assertion-{driver}" for driver in DRIVERS)))
                        self.assertRegex(result.review_reference or "",
                                         r"^local-synthetic-d8-review-v1:[0-9a-f]{64}$")
                        counts["PND"] += 1
                    else:
                        ids = [RULE[code] for code in expected.split("+")]
                        winning = ids[0][0]
                        self.assertEqual(result.outcome, PRIORITY_ASSIGNED)
                        self.assertEqual(result.priority, winning)
                        self.assertEqual(result.matched_rule_ids, (ids[0][1],))
                        counts[winning] += 1
        self.assertEqual(counts, {"critical": 2, "high": 14,
                                  "medium": 1, "low": 4, "PND": 63})

    def test_rule_dependent_missing_and_short_circuit(self):
        cases = (
            (PAIRS[0], (None, "T", "P"), PRIORITY_ASSIGNED, "critical"),
            (PAIRS[0], ("P", "T", None), BLOCKED_REQUIRED_EVIDENCE, None),
            (PAIRS[0], (None, "A", None), PRIORITY_NOT_DETERMINED, None),
            (PAIRS[0], (None, None, "P"), BLOCKED_REQUIRED_EVIDENCE, None),
            (PAIRS[1], ("P", None, "P"), PRIORITY_ASSIGNED, "high"),
            (PAIRS[1], ("P", "U", None), PRIORITY_ASSIGNED, "high"),
            (PAIRS[1], (None, "T", "P"), PRIORITY_ASSIGNED, "high"),
            (PAIRS[1], ("P", None, "A"), BLOCKED_REQUIRED_EVIDENCE, None),
            (PAIRS[2], ("A", "A", None), BLOCKED_REQUIRED_EVIDENCE, None),
            (PAIRS[3], ("P", None, None), PRIORITY_NOT_DETERMINED, None),
        )
        for pair, states, outcome, level in cases:
            with self.subTest(pair=pair, states=states):
                result = evaluate_local_d8_priority(fixture(pair, states))
                self.assertEqual((result.outcome, result.priority), (outcome, level))

    def test_invalid_supplied_assertions_reject_even_when_unneeded(self):
        base = fixture(PAIRS[0], ("P", "T", "P"))
        for change in (
            {"businessAuthorityReference": "wrong"},
            {"sourceRevision": "stale"},
            {"assessmentSnapshotIdentity": "other"},
            {"recommendationInstanceIdentity": "instance-2"},
            {"recommendationDecisionTableVersion": "wrong"},
            {"assertedValue": "unknown"},
        ):
            with self.subTest(change=change):
                records = [dict(r) for r in base.records]
                records[0].update(change)
                self.assertEqual(evaluate_local_d8_priority(
                    replace(base, records=records)).outcome, REJECTED_INVALID_ASSERTION)
        duplicate = replace(base, records=base.records + [dict(base.records[0])])
        self.assertEqual(evaluate_local_d8_priority(duplicate).outcome,
                         REJECTED_INVALID_ASSERTION)
        unneeded = fixture(PAIRS[1], ("P", "U", "A"))
        records = [dict(r) for r in unneeded.records]
        records[-1]["businessAuthorityReference"] = "wrong"
        self.assertEqual(evaluate_local_d8_priority(
            replace(unneeded, records=records)).outcome, REJECTED_INVALID_ASSERTION)

    def test_not_applicable_rejected_by_d8(self):
        data = fixture()
        records = [dict(r) for r in data.records]
        records[0].update(assertedValue="not-applicable",
                          applicabilityStatus="not-applicable",
                          applicabilityRuleId="local-customer-impact-not-applicable-v1")
        ref = records[0]["evidenceReferences"][0]
        evidence = dict(data.context.evidence)
        evidence[ref] = replace(evidence[ref], supported_value="not-applicable",
                                scope_confirmed=True)
        data = replace(data, records=records, context=replace(data.context, evidence=evidence))
        self.assertEqual(evaluate_local_d8_priority(data).outcome,
                         REJECTED_INVALID_ASSERTION)

    def test_governed_binding_and_context_reject(self):
        data = fixture()
        changes = (
            replace(data, recommendation_instance_identity="other"),
            replace(data, risk_classification="unknown"),
            replace(data, confidence_classification="unknown"),
            replace(data, severity_classifications=("low", "low")),
            replace(data, severity_decision_identifiers=("wrong", "wrong")),
            replace(data, risk_decision_table_version="wrong"),
            replace(data, confidence_decision_identifier="wrong"),
            replace(data, recommendations=(replace(data.recommendations[0],
                     recommendation_decision_identifier="wrong"), data.recommendations[1])),
            replace(data, recommendations=(replace(data.recommendations[0],
                     recommendation_classification="monitor"), data.recommendations[1])),
            replace(data, context=replace(data.context, snapshot_identity="other")),
            replace(data, context=replace(data.context, recommendations=(
                replace(data.context.recommendations[0], finding_id="finding-2"),
                data.context.recommendations[1]))),
        )
        for changed in changes:
            with self.subTest(changed=changed):
                self.assertEqual(evaluate_local_d8_priority(changed).outcome,
                                 REJECTED_INVALID_ASSERTION)
        self.assertEqual(evaluate_local_d8_priority(
            replace(data, confidence_classification="insufficient-confidence",
                    confidence_decision_identifier="confidence-v1-insufficient-unassertable")).outcome,
            INSUFFICIENT_CONFIDENCE)
        self.assertEqual(evaluate_local_d8_priority(
            replace(data, risk_classification="critical-risk",
                    risk_decision_identifier="risk-v1-critical-any-critical")).priority, "critical")
        records = [dict(r) for r in data.records]
        records[-1]["targetReference"] = "missing-instance"
        self.assertEqual(evaluate_local_d8_priority(
            replace(data, records=records)).outcome, REJECTED_INVALID_ASSERTION)
        malformed_finding = object.__new__(FindingInput)
        object.__setattr__(malformed_finding, "finding_id", "finding-1")
        object.__setattr__(malformed_finding, "finding_type", "Unsupported")
        object.__setattr__(malformed_finding, "business_consequence_basis", "unknown")
        self.assertEqual(evaluate_local_d8_priority(
            replace(data, findings=(malformed_finding, data.findings[1]))).outcome,
            REJECTED_INVALID_ASSERTION)

    def test_d7_monitor(self):
        rule = RECOMMENDATION_DECISION_RULES["recommendation-v1-no-findings-monitor"]
        rec = GovernedRecommendationResult(None, rule.output, rule.id, rule.table_version)
        instance = RecommendationInstance("instance-monitor", None, rule.id)
        context = SyntheticContext("snapshot-1", "assessment-1", (instance,), {}, {})
        data = LocalD8Input((), (rec,), "instance-monitor", context, [], (),
                            "minimal-informational", "high-confidence", (),
                            SEVERITY_DECISION_TABLE_SET_VERSION,
                            "risk-v1-minimal-informational-only",
                            RISK_DECISION_TABLE_SET_VERSION,
                            "confidence-v1-high-strong-present",
                            CONFIDENCE_DECISION_TABLE_SET_VERSION)
        result = evaluate_local_d8_priority(data)
        self.assertEqual(result.outcome, NO_FINDINGS_MONITOR)
        self.assertIsNone(result.priority)
        self.assertEqual(evaluate_local_d8_priority(
            replace(data, risk_classification="critical-risk",
                    risk_decision_identifier="risk-v1-critical-any-critical")).outcome,
            REJECTED_INVALID_ASSERTION)
        self.assertEqual(evaluate_local_d8_priority(
            replace(data, recommendations=(replace(rec, finding_id="wrong"),))).outcome,
            REJECTED_INVALID_ASSERTION)

    def test_peer_resolution_and_repeatability(self):
        self.assertEqual(_resolve_level((("Z", "TRUE"), ("A", "TRUE"),
                                         ("P", "PENDING_REQUIRED_EVIDENCE"))),
                         (("A", "Z"), ("P",)))
        data = fixture(PAIRS[0], ("P", "T", "P"))
        self.assertEqual(evaluate_local_d8_priority(data), evaluate_local_d8_priority(data))
        result = evaluate_local_d8_priority(data)
        self.assertEqual(result.matched_rule_ids, ("B-C1",))
        self.assertEqual(result.priority, "critical")

    def test_pnd_review_reference_binding_and_missing_distinction(self):
        data = fixture(PAIRS[0], ("A", "A", "A"))
        result = evaluate_local_d8_priority(data)
        self.assertEqual(result.outcome, PRIORITY_NOT_DETERMINED)
        self.assertEqual(result.review_reference,
                         evaluate_local_d8_priority(data).review_reference)
        self.assertTrue(result.review_required)
        self.assertIsNone(result.priority)

        missing = fixture(PAIRS[0], (None, "A", None))
        missing_result = evaluate_local_d8_priority(missing)
        self.assertEqual(missing_result.outcome, PRIORITY_NOT_DETERMINED)
        self.assertEqual(missing_result.evaluated_driver_values,
                         (("customer-impact", None),
                          ("executive-urgency", "executive-action-affirmed-absent"),
                          ("dependency-role", None)))
        self.assertEqual(result.evaluated_driver_values,
                         (("customer-impact", "impact-affirmed-absent"),
                          ("executive-urgency", "executive-action-affirmed-absent"),
                          ("dependency-role", "no-dependency-affirmed")))

        second_records = [dict(record,
                               recommendationInstanceIdentity="instance-2",
                               findingId="finding-2")
                          for record in data.records]
        second_evidence = {
            reference: replace(evidence, instance_identity="instance-2")
            for reference, evidence in data.context.evidence.items()
        }
        second = replace(data, recommendation_instance_identity="instance-2",
                         records=second_records,
                         context=replace(data.context, evidence=second_evidence))
        second_result = evaluate_local_d8_priority(second)
        self.assertEqual(second_result.outcome, PRIORITY_NOT_DETERMINED)
        self.assertEqual(second_result.finding_id, "finding-2")
        self.assertNotEqual(result.review_reference, second_result.review_reference)


if __name__ == "__main__":
    unittest.main()
