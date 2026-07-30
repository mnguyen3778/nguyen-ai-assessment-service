import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import assessment.executive_snapshot_handoff as handoff_module  # noqa: E402
from assessment.business_decision_package import (  # noqa: E402
    BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS,
    BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BUSINESS_DECISION_PACKAGE_LIMITATIONS,
)
from assessment.executive_orchestration import (  # noqa: E402
    INPUT_CONTRACT_FAILURE as ORCHESTRATION_INPUT_CONTRACT_FAILURE,
    ExecutiveOrchestrationFailure,
    ExecutiveOrchestrationResult,
    ValidatedCanonicalExecutiveAssessmentInput,
)
from assessment.executive_runtime import (  # noqa: E402
    EXECUTIVE_ASSESSMENT_VERSION,
    EXECUTIVE_INTERNAL_ERROR,
    EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
    ExecutiveRuntimeValidationIssue,
    ExecutiveRuntimeValidationResult,
    create_executive_runtime_error_response,
)
from assessment.executive_snapshot_handoff import (  # noqa: E402
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


class ExecutiveSnapshotHandoffTests(unittest.TestCase):
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
