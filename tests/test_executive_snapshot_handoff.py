import copy
import json
import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from unittest.mock import patch

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import assessment.executive_snapshot_handoff as handoff_module  # noqa: E402
from assessment.business_decision_package import (  # noqa: E402
    ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS,
    BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BUSINESS_DECISION_PACKAGE_LIMITATIONS,
)
from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_RECOMMENDATION_ACTION_TEXT_BY_RULE,
)
from assessment.executive_orchestration import (  # noqa: E402
    INPUT_CONTRACT_FAILURE as ORCHESTRATION_INPUT_CONTRACT_FAILURE,
    ExecutiveOrchestrationFailure,
    ExecutiveOrchestrationResult,
    ValidatedCanonicalExecutiveAssessmentInput,
    orchestrate_executive_assessment,
)
from assessment.executive_assessment_snapshot import (  # noqa: E402
    validate_executive_assessment_snapshot_serialization,
)
from assessment.executive_runtime import (  # noqa: E402
    EXECUTIVE_ASSESSMENT_VERSION,
    EXECUTIVE_INTERNAL_ERROR,
    EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
    NOT_PRODUCTION_AUTHORITATIVE,
    PRODUCTION_AUTHORITATIVE,
    ExecutiveRuntimeValidationIssue,
    ExecutiveRuntimeValidationResult,
    create_executive_runtime_error_response,
)
from assessment.executive_snapshot_handoff import (  # noqa: E402
    ATTESTATION_FAILURE,
    INPUT_CONTRACT_FAILURE,
    ORCHESTRATION_FAILURE,
    RUNTIME_FAILURE,
    SNAPSHOT_CREATION_FAILURE,
    SNAPSHOT_SERIALIZATION_FAILURE,
    SNAPSHOT_SERIALIZATION_VALIDATION_FAILURE,
    UNEXPECTED_INTERNAL_FAILURE,
    ExecutiveSnapshotProductionResult,
    produce_executive_assessment_snapshot,
)
from assessment.governed_assessment_input import FindingInput  # noqa: E402
from assessment.producer_snapshot_attestation import (  # noqa: E402
    AttestationError, ProducerSnapshotIssuer, ProducerSnapshotVerifier,
    V3_VERIFICATION_CONTRACT_VERSION,
)
from test_golden_fixture_regression import request  # noqa: E402
from assessment.methodology_config import (  # noqa: E402
    BUSINESS_DECISION_METHODOLOGY,
    METHODOLOGY_VERSION,
)
from assessment.models import AssessmentRequest  # noqa: E402


def valid_configured_answers(scale_value=4, numeric_value=100):
    return {
        question_id: (
            numeric_value
            if question.expected_answer_type == "numeric"
            else scale_value
        )
        for question_id, question in BUSINESS_DECISION_METHODOLOGY.questions.items()
    }


def valid_canonical_input(scale_value=4, numeric_value=100):
    return ValidatedCanonicalExecutiveAssessmentInput(
        assessment_version=EXECUTIVE_ASSESSMENT_VERSION,
        methodology_version=METHODOLOGY_VERSION,
        answers=valid_configured_answers(scale_value, numeric_value),
    )


def local_v3_authorities():
    key = Ed25519PrivateKey.generate()
    release = "a075a679a053ee9d0eb9a32d7f0ffa2dc796f0da"
    issuer = ProducerSnapshotIssuer(
        key, issuer_id="nguyen-ai-assessment", key_id="local-v3-handoff-test",
        producer_release_commit=release,
        verification_contract_version=V3_VERIFICATION_CONTRACT_VERSION,
    )
    verifier = ProducerSnapshotVerifier(
        trusted_issuer_id="nguyen-ai-assessment",
        trusted_keys={"local-v3-handoff-test": key.public_key()},
        expected_release_commit=release,
        verification_contract_version=V3_VERIFICATION_CONTRACT_VERSION,
    )
    return issuer, verifier


def encode(snapshot):
    return json.dumps(snapshot, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


class ExecutiveSnapshotHandoffTests(unittest.TestCase):
    def test_explicit_local_v3_handoff_preserves_eight_governed_scenarios(self):
        issuer, verifier = local_v3_authorities()
        cases = [
            request(75, "adequate", "critical"),
            request(75, "mixed-strong", "two-high"),
            request(50, "adequate", "medium"),
            request(50, "adequate", "low"),
            request(100, "strong", "strength"),
            request(50, "adequate", "none"),
        ]
        for kind, basis in (("Observation", "observation"),
                            ("Opportunity", "opportunity")):
            finding = FindingInput(
                "finding-local-" + kind.lower(), "Local finding", "POC", (),
                "fixture-input", kind, basis, ("fixture-input",),
            )
            cases.append(replace(request(50, "adequate", "none"), findings=(finding,)))

        four_fields = (
            "findingId", "recommendationClassification",
            "recommendationDecisionIdentifier", "recommendationDecisionTableVersion",
        )
        seen = set()
        for canonical in cases:
            with self.subTest(findings=canonical.findings):
                v2 = produce_executive_assessment_snapshot(canonical)
                v3 = produce_executive_assessment_snapshot(
                    canonical,
                    local_package_contract_version=ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
                    local_v3_issuer=issuer, local_v3_verifier=verifier,
                )
                self.assertTrue(v2.is_success, v2.failure)
                self.assertTrue(v3.is_success, v3.failure)
                self.assertIsNone(v2.attestation_sidecar)
                self.assertEqual(v3.serialized_snapshot["responseContractVersion"],
                                 "executive-runtime-response-v1")
                self.assertEqual(v3.serialized_snapshot["responseStatus"]["productionAuthority"],
                                 NOT_PRODUCTION_AUTHORITATIVE)
                self.assertEqual(v3.attestation_sidecar["verificationContractVersion"],
                                 V3_VERIFICATION_CONTRACT_VERSION)
                self.assertIsNone(verifier.verify(encode(v3.serialized_snapshot),
                                                  v3.attestation_sidecar))
                old = v2.serialized_snapshot["businessDecisionPackage"]
                new = copy.deepcopy(v3.serialized_snapshot["businessDecisionPackage"])
                self.assertEqual(new["versionMetadata"]["assessmentVersion"],
                                 "nguyen-ai-executive-assessment-v2")
                new["versionMetadata"]["contractVersion"] = "business-decision-package-v2"
                for row in new["governedConclusions"]["recommendations"]:
                    self.assertEqual(tuple(row), four_fields + ("recommendationActionText",))
                    rule = row["recommendationDecisionIdentifier"]
                    self.assertEqual(row["recommendationActionText"],
                                     APPROVED_RECOMMENDATION_ACTION_TEXT_BY_RULE[rule])
                    seen.add(rule)
                    del row["recommendationActionText"]
                self.assertEqual(new, old)
                self.assertTrue(all(tuple(row) == four_fields for row in
                                    old["governedConclusions"]["recommendations"]))
                if not canonical.findings:
                    self.assertIsNone(new["governedConclusions"]["recommendations"][0]["findingId"])
        self.assertEqual(seen, set(APPROVED_RECOMMENDATION_ACTION_TEXT_BY_RULE))

    def test_local_v3_requires_explicit_valid_selection_and_attestation(self):
        canonical = request(50, "adequate", "none")
        issuer, verifier = local_v3_authorities()
        with patch.object(handoff_module, "orchestrate_executive_assessment") as run:
            for selection, signer, checker in (
                (None, issuer, verifier),
                (3, issuer, verifier),
                (False, issuer, verifier),
                ("business-decision-package-v4", issuer, verifier),
                (ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION, None, verifier),
                (ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION, issuer, None),
            ):
                with self.subTest(selection=selection, signer=signer, checker=checker):
                    result = produce_executive_assessment_snapshot(
                        canonical, local_package_contract_version=selection,
                        local_v3_issuer=signer, local_v3_verifier=checker,
                    )
                    self.assertFalse(result.is_success)
                    self.assertEqual(result.failure.category, INPUT_CONTRACT_FAILURE)
            legacy = produce_executive_assessment_snapshot(
                valid_canonical_input(),
                local_package_contract_version=ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
                local_v3_issuer=issuer, local_v3_verifier=verifier,
            )
            self.assertFalse(legacy.is_success)
            self.assertEqual(legacy.failure.category, INPUT_CONTRACT_FAILURE)
            run.assert_not_called()

    def test_local_v3_handoff_rejects_invalid_evidence_and_cross_version_profiles(self):
        canonical = request(75, "mixed-strong", "two-high")
        issuer, verifier = local_v3_authorities()
        selected = {
            "local_package_contract_version": ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
            "local_v3_issuer": issuer, "local_v3_verifier": verifier,
        }
        valid = produce_executive_assessment_snapshot(canonical, **selected)
        self.assertTrue(valid.is_success, valid.failure)
        raw = encode(valid.serialized_snapshot)
        altered = copy.deepcopy(valid.serialized_snapshot)
        altered["businessDecisionPackage"]["governedConclusions"]["recommendations"][0]["recommendationActionText"] = "changed"
        with self.assertRaises(AttestationError):
            verifier.verify(encode(altered), valid.attestation_sidecar)
        altered = copy.deepcopy(valid.serialized_snapshot)
        altered["businessDecisionPackage"]["governedConclusions"]["recommendations"].reverse()
        with self.assertRaises(AttestationError):
            verifier.verify(encode(altered), valid.attestation_sidecar)
        altered = copy.deepcopy(valid.serialized_snapshot)
        altered["businessDecisionPackage"]["governedConclusions"]["recommendations"][0]["findingId"] = "changed"
        with self.assertRaises(AttestationError):
            verifier.verify(encode(altered), valid.attestation_sidecar)
        for edit in (
            lambda s: s.update({"snapshotDigest": "0" * 64}),
            lambda s: s.update({"signature": "AAAA"}),
            lambda s: s.update({"canonicalizationId": "governed-conclusions-json-v1"}),
            lambda s: s.update({"verificationContractVersion": "producer-snapshot-attestation-v1"}),
        ):
            sidecar = dict(valid.attestation_sidecar)
            edit(sidecar)
            with self.assertRaises(AttestationError):
                verifier.verify(raw, sidecar)
        with patch.object(issuer, "issue", return_value=None):
            missing = produce_executive_assessment_snapshot(canonical, **selected)
        self.assertFalse(missing.is_success)
        self.assertEqual(missing.failure.category, ATTESTATION_FAILURE)
        v2_issuer = ProducerSnapshotIssuer(
            Ed25519PrivateKey.generate(), issuer_id="nguyen-ai-assessment",
            key_id="local-v3-handoff-test",
            producer_release_commit="a075a679a053ee9d0eb9a32d7f0ffa2dc796f0da",
        )
        wrong = produce_executive_assessment_snapshot(
            canonical, **dict(selected, local_v3_issuer=v2_issuer))
        self.assertFalse(wrong.is_success)
        self.assertEqual(wrong.failure.category, ATTESTATION_FAILURE)

        genuine_issue = issuer.issue
        for field, bad_value in (("snapshotDigest", "0" * 64),
                                 ("signature", "AAAA")):
            def corrupted_issue(snapshot_bytes, field=field, bad_value=bad_value):
                sidecar = genuine_issue(snapshot_bytes)
                sidecar[field] = bad_value
                return sidecar

            with patch.object(issuer, "issue", side_effect=corrupted_issue):
                rejected = produce_executive_assessment_snapshot(canonical, **selected)
            self.assertFalse(rejected.is_success)
            self.assertEqual(rejected.failure.category, ATTESTATION_FAILURE)
            self.assertIsNone(rejected.serialized_snapshot)

    def test_local_v3_handoff_rejects_substituted_or_invalid_snapshot_content(self):
        canonical = request(50, "adequate", "medium")
        issuer, verifier = local_v3_authorities()
        selected = {
            "local_package_contract_version": ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
            "local_v3_issuer": issuer, "local_v3_verifier": verifier,
        }
        v2_orchestration = orchestrate_executive_assessment(canonical)
        with patch.object(handoff_module, "orchestrate_executive_assessment",
                          return_value=v2_orchestration):
            substituted = produce_executive_assessment_snapshot(canonical, **selected)
        self.assertFalse(substituted.is_success)
        self.assertEqual(substituted.failure.category, RUNTIME_FAILURE)

        original_to_dict = handoff_module.ExecutiveAssessmentSnapshot.to_dict

        def altered_text(snapshot):
            serialized = original_to_dict(snapshot)
            serialized["businessDecisionPackage"]["governedConclusions"]["recommendations"][0]["recommendationActionText"] = "unapproved"
            return serialized

        with patch.object(handoff_module.ExecutiveAssessmentSnapshot, "to_dict",
                          altered_text), patch.object(issuer, "issue") as sign:
            invalid = produce_executive_assessment_snapshot(canonical, **selected)
        self.assertFalse(invalid.is_success)
        self.assertEqual(invalid.failure.category, SNAPSHOT_SERIALIZATION_VALIDATION_FAILURE)
        sign.assert_not_called()

        valid = produce_executive_assessment_snapshot(canonical, **selected)
        self.assertTrue(valid.is_success, valid.failure)
        serialized = copy.deepcopy(valid.serialized_snapshot)
        serialized["responseStatus"]["productionAuthority"] = PRODUCTION_AUTHORITATIVE
        self.assertFalse(validate_executive_assessment_snapshot_serialization(serialized).is_valid)
        with self.assertRaises(AttestationError):
            issuer.issue(encode(serialized))

    def test_local_v3_handoff_rejects_production_authority(self):
        canonical = request(50, "adequate", "none")
        issuer, verifier = local_v3_authorities()
        real_execute = handoff_module.ExecutiveRuntime.execute

        def authoritative(runtime, *args, **kwargs):
            result = real_execute(runtime, *args, **kwargs)
            success = replace(result.success, response_status=replace(
                result.success.response_status,
                production_authority=PRODUCTION_AUTHORITATIVE,
            ))
            return replace(result, success=success)

        with patch.object(handoff_module.ExecutiveRuntime, "execute", authoritative):
            result = produce_executive_assessment_snapshot(
                canonical,
                local_package_contract_version=ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
                local_v3_issuer=issuer, local_v3_verifier=verifier,
            )
        self.assertFalse(result.is_success)
        self.assertEqual(result.failure.category, RUNTIME_FAILURE)
        self.assertIsNone(result.serialized_snapshot)

    def test_snapshot_production_is_deterministic(self):
        canonical_input = valid_canonical_input(scale_value=3, numeric_value=80)

        first_result = produce_executive_assessment_snapshot(canonical_input)
        second_result = produce_executive_assessment_snapshot(canonical_input)

        self.assertTrue(first_result.is_success)
        self.assertTrue(second_result.is_success)
        self.assertEqual(
            first_result.serialized_snapshot,
            second_result.serialized_snapshot,
        )
        self.assertIsNone(first_result.failure)

    def test_snapshot_production_invokes_components_in_approved_order(self):
        canonical_input = valid_canonical_input()
        observed_sequence = []
        snapshot_class = handoff_module.ExecutiveAssessmentSnapshot

        def wrapped(name, function):
            def wrapper(*args, **kwargs):
                observed_sequence.append(name)
                return function(*args, **kwargs)

            return wrapper

        with patch.object(
            handoff_module,
            "orchestrate_executive_assessment",
            side_effect=wrapped(
                "orchestration",
                handoff_module.orchestrate_executive_assessment,
            ),
        ), patch.object(
            handoff_module.ExecutiveRuntime,
            "execute",
            side_effect=wrapped(
                "runtime",
                handoff_module.ExecutiveRuntime.execute,
            ),
            autospec=True,
        ), patch.object(
            handoff_module,
            "ExecutiveAssessmentSnapshot",
            side_effect=wrapped(
                "snapshot",
                snapshot_class,
            ),
        ), patch.object(
            snapshot_class,
            "to_dict",
            side_effect=wrapped(
                "serialization",
                snapshot_class.to_dict,
            ),
            autospec=True,
        ), patch.object(
            handoff_module,
            "validate_executive_assessment_snapshot_serialization",
            side_effect=wrapped(
                "serialization-validation",
                handoff_module.validate_executive_assessment_snapshot_serialization,
            ),
        ):
            result = produce_executive_assessment_snapshot(canonical_input)

        self.assertTrue(result.is_success)
        self.assertEqual(
            observed_sequence,
            [
                "orchestration",
                "runtime",
                "snapshot",
                "serialization",
                "serialization-validation",
            ],
        )

    def test_snapshot_production_returns_only_serialized_snapshot_on_success(self):
        result = produce_executive_assessment_snapshot(valid_canonical_input())

        self.assertTrue(result.is_success)
        self.assertIsNotNone(result.serialized_snapshot)
        self.assertFalse(hasattr(result, "executive_assessment_snapshot"))
        self.assertFalse(hasattr(result, "business_decision_package"))

    def test_snapshot_production_preserves_versions_and_limitations(self):
        result = produce_executive_assessment_snapshot(valid_canonical_input())
        serialized_snapshot = result.serialized_snapshot
        package = serialized_snapshot["businessDecisionPackage"]
        version_metadata = package["versionMetadata"]

        self.assertEqual(
            serialized_snapshot["responseContractVersion"],
            EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
        )
        self.assertEqual(
            version_metadata["contractVersion"],
            BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
        )
        self.assertEqual(
            version_metadata["assessmentVersion"],
            EXECUTIVE_ASSESSMENT_VERSION,
        )
        self.assertEqual(
            version_metadata["methodologyVersion"],
            METHODOLOGY_VERSION,
        )
        self.assertEqual(
            version_metadata["componentVersions"],
            dict(BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS),
        )
        self.assertEqual(
            package["limitations"],
            list(BUSINESS_DECISION_PACKAGE_LIMITATIONS),
        )

    def test_snapshot_production_rejects_public_payload_before_orchestration(self):
        public_payload = {
            "assessmentVersion": "nguyen-ai-readiness-v1",
            "organization": {"name": "Nguyen AI"},
            "respondent": {"email": "owner@example.com"},
            "answers": {"public-question-1": 4},
        }

        with patch.object(
            handoff_module,
            "orchestrate_executive_assessment",
        ) as orchestration_mock:
            result = produce_executive_assessment_snapshot(public_payload)

        self.assertFalse(result.is_success)
        self.assertIsNone(result.serialized_snapshot)
        self.assertEqual(result.failure.category, INPUT_CONTRACT_FAILURE)
        orchestration_mock.assert_not_called()

    def test_snapshot_production_rejects_public_assessment_request(self):
        public_request = AssessmentRequest(
            assessment_version="nguyen-ai-readiness-v1",
            organization={"name": "Nguyen AI"},
            respondent={"email": "owner@example.com"},
            answers={"public-question-1": 4},
        )

        result = produce_executive_assessment_snapshot(public_request)

        self.assertFalse(result.is_success)
        self.assertIsNone(result.serialized_snapshot)
        self.assertEqual(result.failure.category, INPUT_CONTRACT_FAILURE)

    def test_snapshot_production_fails_closed_on_orchestration_failure(self):
        orchestration_failure = ExecutiveOrchestrationFailure(
            category=ORCHESTRATION_INPUT_CONTRACT_FAILURE,
            code="unsupported-assessment-version",
            stage="version-binding",
            message="Unsupported assessment version.",
        )

        with patch.object(
            handoff_module,
            "orchestrate_executive_assessment",
            return_value=ExecutiveOrchestrationResult(
                failure=orchestration_failure,
            ),
        ), patch.object(
            handoff_module.ExecutiveRuntime,
            "execute",
        ) as runtime_mock:
            result = produce_executive_assessment_snapshot(valid_canonical_input())

        self.assertFalse(result.is_success)
        self.assertIsNone(result.serialized_snapshot)
        self.assertEqual(result.failure.category, ORCHESTRATION_FAILURE)
        self.assertIs(result.failure.orchestration_failure, orchestration_failure)
        runtime_mock.assert_not_called()

    def test_snapshot_production_fails_closed_on_runtime_failure(self):
        with patch.object(
            handoff_module.ExecutiveRuntime,
            "execute",
            return_value=create_executive_runtime_error_response(
                EXECUTIVE_INTERNAL_ERROR,
            ),
        ), patch.object(
            handoff_module,
            "ExecutiveAssessmentSnapshot",
        ) as snapshot_mock:
            result = produce_executive_assessment_snapshot(valid_canonical_input())

        self.assertFalse(result.is_success)
        self.assertIsNone(result.serialized_snapshot)
        self.assertEqual(result.failure.category, RUNTIME_FAILURE)
        snapshot_mock.assert_not_called()

    def test_snapshot_production_fails_closed_on_snapshot_validation_failure(self):
        with patch.object(
            handoff_module,
            "ExecutiveAssessmentSnapshot",
            side_effect=ValueError("snapshot validation failed"),
        ):
            result = produce_executive_assessment_snapshot(valid_canonical_input())

        self.assertFalse(result.is_success)
        self.assertIsNone(result.serialized_snapshot)
        self.assertEqual(result.failure.category, SNAPSHOT_CREATION_FAILURE)
        self.assertEqual(result.failure.code, "snapshot-creation-failed")

    def test_snapshot_production_fails_closed_on_serialization_failure(self):
        with patch.object(
            handoff_module.ExecutiveAssessmentSnapshot,
            "to_dict",
            side_effect=ValueError("serialization failed"),
        ):
            result = produce_executive_assessment_snapshot(valid_canonical_input())

        self.assertFalse(result.is_success)
        self.assertIsNone(result.serialized_snapshot)
        self.assertEqual(result.failure.category, SNAPSHOT_SERIALIZATION_FAILURE)

    def test_snapshot_production_validates_serialization(self):
        with patch.object(
            handoff_module,
            "validate_executive_assessment_snapshot_serialization",
            wraps=handoff_module.validate_executive_assessment_snapshot_serialization,
        ) as validation_mock:
            result = produce_executive_assessment_snapshot(valid_canonical_input())

        self.assertTrue(result.is_success)
        validation_mock.assert_called_once_with(result.serialized_snapshot)

    def test_snapshot_production_fails_closed_on_serialization_validation_failure(self):
        validation_issue = ExecutiveRuntimeValidationIssue(
            code="unexpected-serialized-snapshot-field",
            path="$.generatedAt",
            message="Serialized snapshot contains unexpected field.",
        )

        with patch.object(
            handoff_module,
            "validate_executive_assessment_snapshot_serialization",
            return_value=ExecutiveRuntimeValidationResult(
                is_valid=False,
                issues=(validation_issue,),
            ),
        ):
            result = produce_executive_assessment_snapshot(valid_canonical_input())

        self.assertFalse(result.is_success)
        self.assertIsNone(result.serialized_snapshot)
        self.assertEqual(
            result.failure.category,
            SNAPSHOT_SERIALIZATION_VALIDATION_FAILURE,
        )
        self.assertEqual(
            result.failure.code,
            "snapshot-serialization-validation-failed",
        )

    def test_snapshot_production_fails_closed_on_serialization_validation_exception(self):
        with patch.object(
            handoff_module,
            "validate_executive_assessment_snapshot_serialization",
            side_effect=RuntimeError("validator crashed"),
        ):
            result = produce_executive_assessment_snapshot(valid_canonical_input())

        self.assertFalse(result.is_success)
        self.assertIsNone(result.serialized_snapshot)
        self.assertEqual(result.failure.category, UNEXPECTED_INTERNAL_FAILURE)
        self.assertEqual(
            result.failure.code,
            "unexpected-snapshot-serialization-validation-failure",
        )

    def test_snapshot_production_preserves_immutable_input_and_evidence(self):
        answers = valid_configured_answers(scale_value=2, numeric_value=50)
        canonical_input = ValidatedCanonicalExecutiveAssessmentInput(
            assessment_version=EXECUTIVE_ASSESSMENT_VERSION,
            methodology_version=METHODOLOGY_VERSION,
            answers=answers,
        )
        input_answers_before = dict(canonical_input.answers)

        result = produce_executive_assessment_snapshot(canonical_input)
        result.serialized_snapshot["businessDecisionPackage"]["limitations"] = []
        second_result = produce_executive_assessment_snapshot(canonical_input)

        self.assertEqual(dict(canonical_input.answers), input_answers_before)
        self.assertEqual(
            second_result.serialized_snapshot["businessDecisionPackage"][
                "limitations"
            ],
            list(BUSINESS_DECISION_PACKAGE_LIMITATIONS),
        )
        with self.assertRaises(TypeError):
            canonical_input.answers[next(iter(canonical_input.answers))] = 1
        with self.assertRaises(FrozenInstanceError):
            canonical_input.assessment_version = "changed"

    def test_snapshot_production_result_rejects_partial_outcomes(self):
        with self.assertRaisesRegex(ValueError, "exactly one outcome"):
            ExecutiveSnapshotProductionResult()

        successful_result = produce_executive_assessment_snapshot(
            valid_canonical_input()
        )
        failed_result = produce_executive_assessment_snapshot({})

        with self.assertRaisesRegex(ValueError, "exactly one outcome"):
            ExecutiveSnapshotProductionResult(
                serialized_snapshot=successful_result.serialized_snapshot,
                failure=failed_result.failure,
            )


if __name__ == "__main__":
    unittest.main()
