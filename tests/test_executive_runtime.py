import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.business_decision_package import (  # noqa: E402
    BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BusinessDecisionPackageVersionMetadata,
    build_business_decision_package,
)
from assessment.confidence import build_confidence_evaluation  # noqa: E402
from assessment.decision_engine import evaluate_assessment  # noqa: E402
from assessment.executive_runtime import (  # noqa: E402
    EXECUTIVE_ASSESSMENT_VERSION,
    EXECUTIVE_INTERNAL_ERROR,
    EXECUTIVE_PACKAGE_INTEGRITY_FAILED,
    EXECUTIVE_REQUEST_INVALID,
    EXECUTIVE_RESULT_UNAVAILABLE,
    EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
    EXECUTIVE_VERSION_INCOMPATIBLE,
    NOT_PRODUCTION_AUTHORITATIVE,
    PRODUCTION_AUTHORITATIVE,
    ExecutiveRuntime,
    ExecutiveRuntimeMetadata,
    ExecutiveRuntimeResult,
    create_executive_runtime_error_response,
    create_executive_runtime_success_response,
    validate_executive_runtime_input,
    validate_executive_runtime_response_payload,
)
from assessment.executive_summary import (  # noqa: E402
    build_executive_summary_foundation,
)
from assessment.methodology_config import (  # noqa: E402
    BUSINESS_DECISION_METHODOLOGY,
    METHODOLOGY_VERSION,
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


def valid_executive_package(scale_value=4, numeric_value=100):
    decision_evaluation = evaluate_assessment(
        valid_configured_answers(scale_value, numeric_value)
    )
    snapshot = build_business_readiness_snapshot(
        EXECUTIVE_ASSESSMENT_VERSION,
        decision_evaluation,
    )
    confidence = build_confidence_evaluation(snapshot)
    priority = build_recommendation_priority_evaluation(snapshot, confidence)
    executive_summary = build_executive_summary_foundation(
        snapshot,
        confidence,
        priority,
    )

    return build_business_decision_package(
        decision_evaluation,
        snapshot,
        confidence,
        priority,
        executive_summary,
    )


def valid_runtime_metadata():
    return ExecutiveRuntimeMetadata(
        request_id="runtime-request-1",
        correlation_id="runtime-correlation-1",
        trace_id="runtime-trace-1",
    )


def issue_codes(validation_result):
    return tuple(issue.code for issue in validation_result.issues)


class ExecutiveRuntimeFoundationTests(unittest.TestCase):
    def test_executive_runtime_execute_returns_success_response(self):
        package = valid_executive_package(scale_value=3, numeric_value=75)
        runtime = ExecutiveRuntime()

        result = runtime.execute(
            package,
            valid_runtime_metadata(),
        )

        self.assertTrue(result.is_success)
        self.assertEqual(
            result.to_dict()["businessDecisionPackage"],
            package.to_dict(),
        )

    def test_executive_runtime_execute_is_equivalent_to_procedural_success(self):
        package = valid_executive_package(scale_value=2, numeric_value=60)
        metadata = valid_runtime_metadata()

        class_result = ExecutiveRuntime().execute(
            package,
            metadata,
            production_authoritative=True,
        )
        procedural_result = create_executive_runtime_success_response(
            package,
            metadata,
            production_authoritative=True,
        )

        self.assertEqual(class_result, procedural_result)
        self.assertEqual(class_result.to_dict(), procedural_result.to_dict())

    def test_executive_runtime_execute_is_equivalent_to_procedural_error(self):
        package = valid_executive_package()

        class_result = ExecutiveRuntime().execute(
            package,
            None,
        )
        procedural_result = create_executive_runtime_success_response(
            package,
            None,
        )

        self.assertEqual(class_result, procedural_result)
        self.assertEqual(class_result.to_dict(), procedural_result.to_dict())

    def test_executive_runtime_is_immutable_and_stateless(self):
        runtime = ExecutiveRuntime()

        with self.assertRaises(FrozenInstanceError):
            runtime.mutable_state = "not-allowed"

        package = valid_executive_package(scale_value=3, numeric_value=80)
        first = runtime.execute(
            package,
            ExecutiveRuntimeMetadata(
                request_id="request-1",
                correlation_id="correlation-1",
            ),
        )
        second = runtime.execute(
            package,
            ExecutiveRuntimeMetadata(
                request_id="request-2",
                correlation_id="correlation-2",
            ),
        )

        self.assertEqual(first.to_dict(), second.to_dict())

    def test_executive_runtime_execute_does_not_mutate_inputs(self):
        package = valid_executive_package(scale_value=1, numeric_value=40)
        metadata = valid_runtime_metadata()
        package_dict_before = package.to_dict()
        metadata_before = replace(metadata)

        ExecutiveRuntime().execute(package, metadata)

        self.assertEqual(package.to_dict(), package_dict_before)
        self.assertEqual(metadata, metadata_before)

    def test_successful_runtime_creation_returns_success_response(self):
        package = valid_executive_package(scale_value=3, numeric_value=75)

        result = create_executive_runtime_success_response(
            package,
            valid_runtime_metadata(),
        )
        response = result.to_dict()

        self.assertTrue(result.is_success)
        self.assertEqual(
            list(response),
            [
                "responseContractVersion",
                "responseStatus",
                "businessDecisionPackage",
            ],
        )
        self.assertEqual(
            response["responseContractVersion"],
            EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
        )
        self.assertEqual(
            response["businessDecisionPackage"],
            package.to_dict(),
        )

    def test_success_response_uses_contract_status_defaults(self):
        result = create_executive_runtime_success_response(
            valid_executive_package(),
            valid_runtime_metadata(),
        )

        self.assertEqual(
            result.to_dict()["responseStatus"],
            {
                "packageValidation": "VALIDATED",
                "runtimeEligibility": "RUNTIME_ELIGIBLE",
                "exposure": "EXPOSURE_ELIGIBLE",
                "productionAuthority": NOT_PRODUCTION_AUTHORITATIVE,
            },
        )

    def test_success_response_can_state_production_authority_when_requested(self):
        result = create_executive_runtime_success_response(
            valid_executive_package(),
            valid_runtime_metadata(),
            production_authoritative=True,
        )

        self.assertEqual(
            result.to_dict()["responseStatus"]["productionAuthority"],
            PRODUCTION_AUTHORITATIVE,
        )

    def test_success_response_is_immutable(self):
        result = create_executive_runtime_success_response(
            valid_executive_package(),
            valid_runtime_metadata(),
        )

        with self.assertRaises(FrozenInstanceError):
            result.success.response_contract_version = "other-version"

    def test_error_response_creation_uses_safe_contract_message(self):
        result = create_executive_runtime_error_response(
            EXECUTIVE_RESULT_UNAVAILABLE,
        )
        response = result.to_dict()

        self.assertFalse(result.is_success)
        self.assertEqual(result.error.http_status, 409)
        self.assertEqual(
            response,
            {
                "responseContractVersion": (
                    EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION
                ),
                "error": {
                    "code": EXECUTIVE_RESULT_UNAVAILABLE,
                    "category": "governance-error",
                    "message": (
                        "The executive result is not available under the current "
                        "governance state."
                    ),
                    "details": [],
                },
            },
        )

    def test_unknown_error_code_fails_closed(self):
        result = create_executive_runtime_error_response(
            "RAW_INTERNAL_EXCEPTION_NAME",
        )

        self.assertFalse(result.is_success)
        self.assertEqual(result.error.http_status, 500)
        self.assertEqual(result.to_dict()["error"]["code"], EXECUTIVE_INTERNAL_ERROR)
        self.assertNotIn("RAW_INTERNAL_EXCEPTION_NAME", str(result.to_dict()))

    def test_runtime_result_rejects_simultaneous_success_and_error(self):
        success = create_executive_runtime_success_response(
            valid_executive_package(),
            valid_runtime_metadata(),
        ).success
        error = create_executive_runtime_error_response(
            EXECUTIVE_RESULT_UNAVAILABLE,
        ).error

        with self.assertRaisesRegex(ValueError, "exactly one"):
            ExecutiveRuntimeResult(success=success, error=error)

    def test_runtime_result_rejects_missing_terminal_response(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            ExecutiveRuntimeResult()

    def test_validate_runtime_input_accepts_valid_package_and_metadata(self):
        validation_result = validate_executive_runtime_input(
            valid_executive_package(),
            valid_runtime_metadata(),
        )

        self.assertTrue(validation_result.is_valid)
        self.assertEqual(validation_result.issues, ())

    def test_missing_business_decision_package_is_rejected(self):
        validation_result = validate_executive_runtime_input(
            None,
            valid_runtime_metadata(),
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "missing-business-decision-package",
            issue_codes(validation_result),
        )

    def test_missing_runtime_metadata_is_rejected(self):
        result = create_executive_runtime_success_response(
            valid_executive_package(),
            None,
        )

        self.assertFalse(result.is_success)
        self.assertEqual(result.error.error.code, EXECUTIVE_REQUEST_INVALID)
        self.assertIn(
            "missing-runtime-metadata",
            [detail.code for detail in result.error.error.details],
        )

    def test_missing_runtime_identifiers_are_rejected(self):
        validation_result = validate_executive_runtime_input(
            valid_executive_package(),
            ExecutiveRuntimeMetadata(
                request_id="",
                correlation_id=" ",
            ),
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "missing-runtime-request-id",
            issue_codes(validation_result),
        )
        self.assertIn(
            "missing-runtime-correlation-id",
            issue_codes(validation_result),
        )

    def test_invalid_contract_version_is_rejected(self):
        package = valid_executive_package()
        invalid_metadata = replace(
            package.version_metadata,
            contract_version="business-decision-package-v2",
        )

        result = create_executive_runtime_success_response(
            replace(package, version_metadata=invalid_metadata),
            valid_runtime_metadata(),
        )

        self.assertFalse(result.is_success)
        self.assertEqual(result.error.error.code, EXECUTIVE_VERSION_INCOMPATIBLE)

    def test_invalid_assessment_version_is_rejected(self):
        package = valid_executive_package()
        invalid_metadata = replace(
            package.version_metadata,
            assessment_version="nguyen-ai-readiness-v1",
        )

        validation_result = validate_executive_runtime_input(
            replace(package, version_metadata=invalid_metadata),
            valid_runtime_metadata(),
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "invalid-executive-assessment-version",
            issue_codes(validation_result),
        )

    def test_invalid_methodology_version_is_rejected(self):
        package = valid_executive_package()
        invalid_metadata = replace(
            package.version_metadata,
            methodology_version="other-methodology-version",
        )

        result = create_executive_runtime_success_response(
            replace(package, version_metadata=invalid_metadata),
            valid_runtime_metadata(),
        )

        self.assertFalse(result.is_success)
        self.assertEqual(result.error.error.code, EXECUTIVE_VERSION_INCOMPATIBLE)

    def test_package_validation_failure_rejects_success_response(self):
        package = valid_executive_package()
        invalid_version_metadata = BusinessDecisionPackageVersionMetadata(
            contract_version=BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
            assessment_version=EXECUTIVE_ASSESSMENT_VERSION,
            methodology_version=METHODOLOGY_VERSION,
            component_versions={"decisionEvaluation": "unexpected-version"},
        )

        result = create_executive_runtime_success_response(
            replace(package, version_metadata=invalid_version_metadata),
            valid_runtime_metadata(),
        )

        self.assertFalse(result.is_success)
        self.assertEqual(result.error.error.code, EXECUTIVE_PACKAGE_INTEGRITY_FAILED)

    def test_business_decision_package_is_not_mutated_by_runtime(self):
        package = valid_executive_package(scale_value=2, numeric_value=50)
        package_dict_before = package.to_dict()

        result = create_executive_runtime_success_response(
            package,
            valid_runtime_metadata(),
        )
        result_dict = result.to_dict()
        result_dict["businessDecisionPackage"]["limitations"].append(
            "runtime-mutation-attempt"
        )

        self.assertEqual(package.to_dict(), package_dict_before)

    def test_runtime_metadata_does_not_enter_success_response_or_package(self):
        metadata = ExecutiveRuntimeMetadata(
            request_id="request-not-business-truth",
            correlation_id="correlation-not-business-truth",
            trace_id="trace-not-business-truth",
        )

        result = create_executive_runtime_success_response(
            valid_executive_package(),
            metadata,
        )
        response_text = str(result.to_dict())

        self.assertNotIn(metadata.request_id, response_text)
        self.assertNotIn(metadata.correlation_id, response_text)
        self.assertNotIn(metadata.trace_id, response_text)

    def test_runtime_metadata_does_not_affect_deterministic_output(self):
        package = valid_executive_package(scale_value=3, numeric_value=80)
        first = create_executive_runtime_success_response(
            package,
            ExecutiveRuntimeMetadata(
                request_id="request-1",
                correlation_id="correlation-1",
            ),
        ).to_dict()
        second = create_executive_runtime_success_response(
            package,
            ExecutiveRuntimeMetadata(
                request_id="request-2",
                correlation_id="correlation-2",
            ),
        ).to_dict()

        self.assertEqual(first, second)

    def test_response_payload_validation_rejects_success_and_error(self):
        success_payload = create_executive_runtime_success_response(
            valid_executive_package(),
            valid_runtime_metadata(),
        ).to_dict()
        success_payload["error"] = {
            "code": EXECUTIVE_PACKAGE_INTEGRITY_FAILED,
            "category": "integrity-error",
            "message": "The executive package failed integrity validation.",
            "details": [],
        }

        validation_result = validate_executive_runtime_response_payload(
            success_payload
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn("success-error-conflict", issue_codes(validation_result))

    def test_response_payload_validation_accepts_success(self):
        payload = create_executive_runtime_success_response(
            valid_executive_package(),
            valid_runtime_metadata(),
        ).to_dict()

        validation_result = validate_executive_runtime_response_payload(payload)

        self.assertTrue(validation_result.is_valid)

    def test_response_payload_validation_accepts_error(self):
        payload = create_executive_runtime_error_response(
            EXECUTIVE_PACKAGE_INTEGRITY_FAILED,
        ).to_dict()

        validation_result = validate_executive_runtime_response_payload(payload)

        self.assertTrue(validation_result.is_valid)

    def test_error_response_never_contains_business_decision_package(self):
        result = create_executive_runtime_error_response(
            EXECUTIVE_PACKAGE_INTEGRITY_FAILED,
        )

        self.assertNotIn("businessDecisionPackage", result.to_dict())


if __name__ == "__main__":
    unittest.main()
