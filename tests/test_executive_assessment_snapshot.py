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
from assessment.executive_assessment_snapshot import (  # noqa: E402
    ExecutiveAssessmentSnapshot,
    create_executive_assessment_snapshot,
    validate_executive_assessment_snapshot,
)
from assessment.executive_runtime import (  # noqa: E402
    EXECUTIVE_ASSESSMENT_VERSION,
    EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
    ExecutiveRuntimeResponseStatus,
    EXECUTIVE_RESULT_UNAVAILABLE,
    NOT_PRODUCTION_AUTHORITATIVE,
    PRODUCTION_AUTHORITATIVE,
    ExecutiveRuntime,
    ExecutiveRuntimeMetadata,
    create_executive_runtime_error_response,
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


def runtime_metadata(
    request_id="snapshot-request-1",
    correlation_id="snapshot-correlation-1",
    trace_id="snapshot-trace-1",
):
    return ExecutiveRuntimeMetadata(
        request_id=request_id,
        correlation_id=correlation_id,
        trace_id=trace_id,
    )


def successful_runtime_result(
    package=None,
    metadata=None,
    *,
    production_authoritative=False,
):
    return ExecutiveRuntime().execute(
        package if package is not None else valid_executive_package(),
        metadata if metadata is not None else runtime_metadata(),
        production_authoritative=production_authoritative,
    )


def issue_codes(validation_result):
    return tuple(issue.code for issue in validation_result.issues)


class ExecutiveAssessmentSnapshotTests(unittest.TestCase):
    def test_successful_snapshot_creation_from_runtime_result(self):
        package = valid_executive_package(scale_value=3, numeric_value=75)
        result = successful_runtime_result(package)

        snapshot = ExecutiveAssessmentSnapshot(result)

        self.assertIs(snapshot.business_decision_package, package)
        self.assertIs(snapshot.response_status, result.success.response_status)
        self.assertEqual(
            snapshot.response_contract_version,
            result.success.response_contract_version,
        )

    def test_factory_creates_same_snapshot_as_constructor(self):
        result = successful_runtime_result(
            valid_executive_package(scale_value=2, numeric_value=60)
        )

        self.assertEqual(
            create_executive_assessment_snapshot(result),
            ExecutiveAssessmentSnapshot(result),
        )

    def test_failed_runtime_result_is_rejected(self):
        result = create_executive_runtime_error_response(
            EXECUTIVE_RESULT_UNAVAILABLE,
        )

        with self.assertRaisesRegex(
            ValueError,
            "requires a successful ExecutiveRuntimeResult",
        ):
            ExecutiveAssessmentSnapshot(result)

    def test_snapshot_creation_rejects_invalid_success_contract_version(self):
        result = successful_runtime_result()
        object.__setattr__(
            result.success,
            "response_contract_version",
            "unsupported-response-contract",
        )

        with self.assertRaisesRegex(
            ValueError,
            "invalid-response-contract-version",
        ):
            ExecutiveAssessmentSnapshot(result)

    def test_snapshot_creation_rejects_invalid_success_package(self):
        result = successful_runtime_result()
        object.__setattr__(
            result.success,
            "business_decision_package",
            object(),
        )

        with self.assertRaisesRegex(
            ValueError,
            "invalid-business-decision-package",
        ):
            ExecutiveAssessmentSnapshot(result)

    def test_non_runtime_result_is_rejected(self):
        with self.assertRaisesRegex(
            ValueError,
            "requires an ExecutiveRuntimeResult",
        ):
            ExecutiveAssessmentSnapshot(None)

    def test_snapshot_is_immutable(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())

        with self.assertRaises(FrozenInstanceError):
            snapshot.response_contract_version = "changed"

    def test_repeated_construction_is_deterministic(self):
        package = valid_executive_package(scale_value=3, numeric_value=80)
        first = successful_runtime_result(
            package,
            runtime_metadata(
                request_id="request-1",
                correlation_id="correlation-1",
                trace_id="trace-1",
            ),
        )
        second = successful_runtime_result(
            package,
            runtime_metadata(
                request_id="request-2",
                correlation_id="correlation-2",
                trace_id="trace-2",
            ),
        )

        self.assertEqual(
            ExecutiveAssessmentSnapshot(first),
            ExecutiveAssessmentSnapshot(second),
        )

    def test_business_decision_package_is_preserved_without_mutation(self):
        package = valid_executive_package(scale_value=1, numeric_value=30)
        package_before = package.to_dict()

        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result(package))

        self.assertIs(snapshot.business_decision_package, package)
        self.assertEqual(package.to_dict(), package_before)
        self.assertEqual(snapshot.business_decision_package.to_dict(), package_before)

    def test_runtime_metadata_is_excluded_from_snapshot_state(self):
        metadata = runtime_metadata(
            request_id="metadata-request",
            correlation_id="metadata-correlation",
            trace_id="metadata-trace",
        )
        snapshot = ExecutiveAssessmentSnapshot(
            successful_runtime_result(metadata=metadata)
        )

        self.assertEqual(
            tuple(snapshot.__dict__),
            (
                "business_decision_package",
                "response_status",
                "response_contract_version",
            ),
        )
        self.assertFalse(hasattr(snapshot, "runtime_metadata"))
        self.assertFalse(hasattr(snapshot, "request_id"))
        self.assertFalse(hasattr(snapshot, "correlation_id"))
        self.assertFalse(hasattr(snapshot, "trace_id"))

    def test_response_status_is_preserved_without_authority_upgrade(self):
        non_authoritative = ExecutiveAssessmentSnapshot(
            successful_runtime_result(production_authoritative=False)
        )
        authoritative = ExecutiveAssessmentSnapshot(
            successful_runtime_result(production_authoritative=True)
        )

        self.assertEqual(
            non_authoritative.response_status.production_authority,
            NOT_PRODUCTION_AUTHORITATIVE,
        )
        self.assertEqual(
            authoritative.response_status.production_authority,
            PRODUCTION_AUTHORITATIVE,
        )

    def test_factory_fails_closed_for_unsuccessful_results(self):
        result = create_executive_runtime_error_response(
            EXECUTIVE_RESULT_UNAVAILABLE,
        )

        with self.assertRaisesRegex(
            ValueError,
            "requires a successful ExecutiveRuntimeResult",
        ):
            create_executive_assessment_snapshot(result)

    def test_snapshot_validation_accepts_valid_snapshot(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertTrue(validation_result.is_valid)
        self.assertEqual(validation_result.issues, ())
        self.assertEqual(
            validation_result.to_dict(),
            {
                "isValid": True,
                "issues": [],
            },
        )

    def test_snapshot_validation_rejects_non_snapshot(self):
        validation_result = validate_executive_assessment_snapshot(None)

        self.assertFalse(validation_result.is_valid)
        self.assertEqual(issue_codes(validation_result), ("invalid-snapshot-type",))

    def test_snapshot_validation_rejects_missing_snapshot_field(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__delattr__(snapshot, "response_contract_version")

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn("missing-snapshot-field", issue_codes(validation_result))
        self.assertIn(
            "invalid-response-contract-version",
            issue_codes(validation_result),
        )

    def test_snapshot_validation_rejects_runtime_metadata_inside_snapshot(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(
            snapshot,
            "runtime_metadata",
            runtime_metadata(),
        )

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "runtime-metadata-in-snapshot",
            issue_codes(validation_result),
        )

    def test_snapshot_validation_rejects_error_response_inside_snapshot(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(
            snapshot,
            "error",
            create_executive_runtime_error_response(EXECUTIVE_RESULT_UNAVAILABLE),
        )

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn("error-response-in-snapshot", issue_codes(validation_result))

    def test_snapshot_validation_rejects_public_assessment_response_field(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(snapshot, "assessment_response", object())

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "public-assessment-response-in-snapshot",
            issue_codes(validation_result),
        )

    def test_snapshot_validation_rejects_downstream_enrichment_field(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(snapshot, "dashboard_layout", "summary")

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn("unexpected-snapshot-field", issue_codes(validation_result))

    def test_snapshot_validation_delegates_package_validation(self):
        package = valid_executive_package()
        invalid_version_metadata = BusinessDecisionPackageVersionMetadata(
            contract_version=BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
            assessment_version=EXECUTIVE_ASSESSMENT_VERSION,
            methodology_version=METHODOLOGY_VERSION,
            component_versions={"decisionEvaluation": "unexpected-version"},
        )
        invalid_package = replace(
            package,
            version_metadata=invalid_version_metadata,
        )
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(
            snapshot,
            "business_decision_package",
            invalid_package,
        )

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "package-component-version-mismatch",
            issue_codes(validation_result),
        )
        self.assertIn("invalid-component-versions", issue_codes(validation_result))

    def test_snapshot_validation_rejects_invalid_package_contract_version(self):
        package = valid_executive_package()
        invalid_package = replace(
            package,
            version_metadata=replace(
                package.version_metadata,
                contract_version="business-decision-package-v2",
            ),
        )
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(
            snapshot,
            "business_decision_package",
            invalid_package,
        )

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "invalid-package-contract-version",
            issue_codes(validation_result),
        )

    def test_snapshot_validation_rejects_public_assessment_version(self):
        package = valid_executive_package()
        invalid_package = replace(
            package,
            version_metadata=replace(
                package.version_metadata,
                assessment_version="nguyen-ai-readiness-v1",
            ),
        )
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(
            snapshot,
            "business_decision_package",
            invalid_package,
        )

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "invalid-executive-assessment-version",
            issue_codes(validation_result),
        )

    def test_snapshot_validation_rejects_invalid_methodology_version(self):
        package = valid_executive_package()
        invalid_package = replace(
            package,
            version_metadata=replace(
                package.version_metadata,
                methodology_version="other-methodology-version",
            ),
        )
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(
            snapshot,
            "business_decision_package",
            invalid_package,
        )

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn("invalid-methodology-version", issue_codes(validation_result))

    def test_snapshot_validation_rejects_missing_business_decision_package(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(snapshot, "business_decision_package", None)

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "missing-business-decision-package",
            issue_codes(validation_result),
        )

    def test_snapshot_validation_rejects_invalid_business_decision_package(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(snapshot, "business_decision_package", object())

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "invalid-business-decision-package",
            issue_codes(validation_result),
        )

    def test_snapshot_validation_rejects_invalid_response_contract_version(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(
            snapshot,
            "response_contract_version",
            "unsupported-response-contract",
        )

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "invalid-response-contract-version",
            issue_codes(validation_result),
        )

    def test_snapshot_validation_rejects_invalid_response_status_type(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(snapshot, "response_status", object())

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn("invalid-response-status", issue_codes(validation_result))

    def test_snapshot_validation_rejects_unsupported_response_status_value(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())
        object.__setattr__(
            snapshot,
            "response_status",
            ExecutiveRuntimeResponseStatus(
                package_validation="PENDING",
                runtime_eligibility="RUNTIME_ELIGIBLE",
                exposure="EXPOSURE_ELIGIBLE",
                production_authority=NOT_PRODUCTION_AUTHORITATIVE,
            ),
        )

        validation_result = validate_executive_assessment_snapshot(snapshot)

        self.assertFalse(validation_result.is_valid)
        self.assertIn("invalid-response-status", issue_codes(validation_result))

    def test_snapshot_validation_accepts_both_authority_status_values(self):
        non_authoritative = ExecutiveAssessmentSnapshot(
            successful_runtime_result(production_authoritative=False)
        )
        authoritative = ExecutiveAssessmentSnapshot(
            successful_runtime_result(production_authoritative=True)
        )

        self.assertTrue(
            validate_executive_assessment_snapshot(non_authoritative).is_valid
        )
        self.assertTrue(
            validate_executive_assessment_snapshot(authoritative).is_valid
        )

    def test_snapshot_validation_does_not_mutate_snapshot_or_package(self):
        package = valid_executive_package(scale_value=2, numeric_value=50)
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result(package))
        snapshot_state_before = dict(snapshot.__dict__)
        package_state_before = package.to_dict()

        validate_executive_assessment_snapshot(snapshot)

        self.assertEqual(snapshot.__dict__, snapshot_state_before)
        self.assertEqual(package.to_dict(), package_state_before)

    def test_snapshot_validation_does_not_use_runtime_metadata_for_identity(self):
        package = valid_executive_package(scale_value=3, numeric_value=80)
        first = ExecutiveAssessmentSnapshot(
            successful_runtime_result(
                package,
                runtime_metadata(
                    request_id="request-1",
                    correlation_id="correlation-1",
                    trace_id="trace-1",
                ),
            )
        )
        second = ExecutiveAssessmentSnapshot(
            successful_runtime_result(
                package,
                runtime_metadata(
                    request_id="request-2",
                    correlation_id="correlation-2",
                    trace_id="trace-2",
                ),
            )
        )

        self.assertEqual(
            validate_executive_assessment_snapshot(first),
            validate_executive_assessment_snapshot(second),
        )

    def test_snapshot_response_contract_version_remains_preserved(self):
        snapshot = ExecutiveAssessmentSnapshot(successful_runtime_result())

        self.assertEqual(
            snapshot.response_contract_version,
            EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
        )


if __name__ == "__main__":
    unittest.main()
