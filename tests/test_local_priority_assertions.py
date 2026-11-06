"""Synthetic-only checks for the isolated assertion validation boundary."""

import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.local_priority_assertions import (  # noqa: E402
    APPLICABILITY_RULE_VERSION,
    ASSERTION_CONTRACT_VERSION,
    AUTHORITY_PROFILE_VERSION,
    AUTHORITY_BY_DRIVER,
    BLOCKED_PENDING_DATA,
    ABSENCE_VALUES,
    INVALID,
    VALID_EVALUATED,
    VALID_NOT_APPLICABLE,
    LOCAL_AUTHORITY_PROFILE,
    RecommendationInstance,
    SyntheticAuthorityProfile,
    SyntheticContext,
    SyntheticEvidence,
    validate_local_assertions,
)


RECOMMENDATIONS = (
    RecommendationInstance("synthetic-instance-a", "synthetic-finding-a",
                           "recommendation-v1-deficiency-high-priority"),
    RecommendationInstance("synthetic-instance-b", "synthetic-finding-b",
                           "recommendation-v1-deficiency-high-priority"),
)


def fixture(driver="customer-impact", value="impact-present", status="evaluated",
            instance=0, target=None, timing=None):
    recommendation = RECOMMENDATIONS[instance]
    evidence_ref = f"synthetic-evidence-{driver}-{value}-{instance}"
    evidence = SyntheticEvidence(
        evidence_ref, driver, value, recommendation.instance_identity,
        scope_confirmed=(status == "not-applicable" or value in ABSENCE_VALUES),
        timing_basis_reference=timing, target_reference=target,
    )
    context = SyntheticContext(
        "synthetic-snapshot-001", "synthetic-assessment-001", RECOMMENDATIONS,
        {evidence_ref: evidence}, {"synthetic-currentness-001": "synthetic-rev-2"},
    )
    record = {
        "assertionId": f"synthetic-assertion-{driver}-{instance}",
        "assessmentSnapshotIdentity": context.snapshot_identity,
        "assessmentIdentity": context.assessment_identity,
        "recommendationInstanceIdentity": recommendation.instance_identity,
        "findingId": recommendation.finding_id,
        "recommendationDecisionIdentifier": recommendation.decision_identifier,
        "recommendationDecisionTableVersion": recommendation.decision_table_version,
        "driverId": driver,
        "assertedValue": value,
        "applicabilityStatus": status,
        "applicabilityRuleId": f"local-{driver}-{status}-v1",
        "applicabilityRuleVersion": APPLICABILITY_RULE_VERSION,
        "evidenceReferences": [evidence_ref],
        "businessAuthorityReference": AUTHORITY_BY_DRIVER[driver],
        "sourceRevision": "synthetic-rev-2",
        "currentnessReference": "synthetic-currentness-001",
        "assertionContractVersion": ASSERTION_CONTRACT_VERSION,
        "targetReference": target,
        "timingBasisReference": timing,
    }
    return record, context


def outcome(record, context, **kwargs):
    return validate_local_assertions([record], context, **kwargs).outcomes[0].status


class LocalPriorityAssertionTests(unittest.TestCase):
    def test_valid_driver_values_and_absence_are_evaluated(self):
        cases = (
            ("customer-impact", "impact-present", None, None),
            ("customer-impact", "impact-affirmed-absent", None, None),
            ("executive-urgency", "executive-action-required", None, None),
            ("executive-urgency", "executive-action-affirmed-absent", None, None),
            ("executive-urgency", "time-bound-executive-action", None, "synthetic-timing-1"),
            ("dependency-role", "blocks-related-work", "synthetic-instance-b", None),
            ("dependency-role", "unlocks-related-work", "synthetic-instance-b", None),
            ("dependency-role", "no-dependency-affirmed", None, None),
        )
        for driver, value, target, timing in cases:
            with self.subTest(driver=driver, value=value):
                record, context = fixture(driver, value, target=target, timing=timing)
                self.assertEqual(outcome(record, context), VALID_EVALUATED)

    def test_evidence_backed_exclusion_for_each_driver(self):
        for driver in AUTHORITY_BY_DRIVER:
            with self.subTest(driver=driver):
                record, context = fixture(driver, "not-applicable", "not-applicable")
                self.assertEqual(outcome(record, context), VALID_NOT_APPLICABLE)

    def test_missing_required_assertion_blocks(self):
        _, context = fixture()
        result = validate_local_assertions([], context,
            required_driver_ids=frozenset(("customer-impact",)))
        self.assertEqual(result.outcomes[0].status, BLOCKED_PENDING_DATA)

    def test_invalid_structure_and_values_reject(self):
        changes = (
            {"driverId": "unknown"}, {"assertedValue": "high"},
            {"assertionContractVersion": "unsupported"},
            {"applicabilityRuleVersion": "unsupported"},
            {"applicabilityRuleId": "unsupported"},
            {"assertionId": 12}, {"assertionId": "x" * 129},
            {"evidenceReferences": []}, {"evidenceReferences": "synthetic-evidence"},
            {"evidenceReferences": ["z", "z"]},
            {"applicabilityStatus": "unknown"},
            {"targetReference": "unexpected"},
        )
        for change in changes:
            with self.subTest(change=change):
                record, context = fixture()
                record.update(change)
                self.assertEqual(outcome(record, context), INVALID)
        record, context = fixture()
        record["extra"] = "not supported"
        self.assertEqual(outcome(record, context), INVALID)
        del record["extra"]
        del record["assertionId"]
        self.assertEqual(outcome(record, context), INVALID)

    def test_snapshot_recommendation_and_evidence_binding_reject(self):
        changes = (
            {"assessmentSnapshotIdentity": "other-snapshot"},
            {"assessmentIdentity": "other-assessment"},
            {"recommendationInstanceIdentity": "synthetic-instance-b"},
            {"findingId": "synthetic-finding-b"},
            {"recommendationDecisionIdentifier": "other-rule"},
            {"recommendationDecisionTableVersion": "other-version"},
            {"evidenceReferences": ["missing-evidence"]},
        )
        for change in changes:
            with self.subTest(change=change):
                record, context = fixture()
                record.update(change)
                self.assertEqual(outcome(record, context), INVALID)
        record, context = fixture()
        ref = record["evidenceReferences"][0]
        context = replace(context, evidence={ref: replace(context.evidence[ref],
                                                           supported_value="impact-affirmed-absent")})
        self.assertEqual(outcome(record, context), INVALID)

    def test_authority_and_currentness_reject(self):
        changes = (
            {"businessAuthorityReference": "synthetic-issuer-executive"},
            {"businessAuthorityReference": "self-declared"},
            {"businessAuthorityReference": ""},
            {"sourceRevision": "synthetic-rev-1"},
            {"sourceRevision": "unknown"},
            {"currentnessReference": "unknown"},
        )
        for change in changes:
            with self.subTest(change=change):
                record, context = fixture()
                record.update(change)
                self.assertEqual(outcome(record, context), INVALID)
        record, context = fixture()
        bad_profile = SyntheticAuthorityProfile("unsupported", AUTHORITY_BY_DRIVER)
        self.assertEqual(outcome(record, context, profile=bad_profile), INVALID)
        bad_profile = SyntheticAuthorityProfile(AUTHORITY_PROFILE_VERSION,
                                                {"customer-impact": "self-declared"})
        self.assertEqual(outcome(record, context, profile=bad_profile), INVALID)
        self.assertEqual(outcome(record, context, profile=LOCAL_AUTHORITY_PROFILE),
                         VALID_EVALUATED)

    def test_exclusion_and_time_bound_require_support(self):
        record, context = fixture("customer-impact", "not-applicable", "not-applicable")
        ref = record["evidenceReferences"][0]
        context = replace(context, evidence={ref: replace(context.evidence[ref],
                                                           scope_confirmed=False)})
        self.assertEqual(outcome(record, context), INVALID)
        record, context = fixture("executive-urgency", "time-bound-executive-action",
                                  timing="synthetic-timing-1")
        record["timingBasisReference"] = None
        self.assertEqual(outcome(record, context), INVALID)
        record, context = fixture("customer-impact", "impact-present")
        record["applicabilityStatus"] = "not-applicable"
        record["applicabilityRuleId"] = "local-customer-impact-not-applicable-v1"
        self.assertEqual(outcome(record, context), INVALID)

    def test_dependency_targets_reject(self):
        for target in (None, "synthetic-instance-a", "other-snapshot-instance"):
            with self.subTest(target=target):
                record, context = fixture("dependency-role", "blocks-related-work",
                                          target="synthetic-instance-b")
                record["targetReference"] = target
                self.assertEqual(outcome(record, context), INVALID)
        record, context = fixture("dependency-role", "no-dependency-affirmed")
        record["targetReference"] = "synthetic-instance-b"
        self.assertEqual(outcome(record, context), INVALID)

    def test_duplicates_and_conflicts_reject_atomically(self):
        record, context = fixture()
        self.assertEqual(validate_local_assertions([record, dict(record)], context)
                         .outcomes[0].status, INVALID)
        second = dict(record, assertionId="synthetic-assertion-2",
                      sourceRevision="synthetic-rev-1")
        self.assertEqual(validate_local_assertions([record, second], context)
                         .outcomes[0].status, INVALID)
        second = dict(record, assertionId="synthetic-assertion-2")
        self.assertEqual(validate_local_assertions([record, second], context)
                         .outcomes[0].status, INVALID)

    def test_directed_dependency_cycle_rejects(self):
        first, first_context = fixture("dependency-role", "blocks-related-work",
                                       instance=0, target="synthetic-instance-b")
        second, second_context = fixture("dependency-role", "blocks-related-work",
                                         instance=1, target="synthetic-instance-a")
        context = replace(first_context, evidence={**first_context.evidence,
                                                   **second_context.evidence})
        result = validate_local_assertions([first, second], context)
        self.assertEqual(result.outcomes[0].status, INVALID)
        self.assertIn("cycle", result.outcomes[0].reason)

    def test_determinism_and_no_priority_output(self):
        record, context = fixture()
        first = validate_local_assertions([record], context)
        second = validate_local_assertions([record], context)
        self.assertEqual(first, second)
        self.assertTrue(first.is_valid)
        self.assertFalse(hasattr(first, "priority"))
        self.assertFalse(hasattr(first.outcomes[0], "priority"))

    def test_no_findings_is_not_given_synthetic_driver_assertions(self):
        context = SyntheticContext("synthetic-snapshot-empty", "synthetic-assessment-empty",
            (RecommendationInstance("synthetic-monitor", None,
                                    "recommendation-v1-no-findings-monitor"),), {}, {})
        result = validate_local_assertions([], context,
            required_driver_ids=frozenset(AUTHORITY_BY_DRIVER))
        self.assertTrue(result.is_valid)
        self.assertEqual(result.outcomes, ())


if __name__ == "__main__":
    unittest.main()
