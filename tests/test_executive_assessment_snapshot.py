import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.business_decision_package import (  # noqa: E402
    build_business_decision_package,
)
from assessment.confidence import build_confidence_evaluation  # noqa: E402
from assessment.decision_engine import evaluate_assessment  # noqa: E402
from assessment.executive_assessment_snapshot import (  # noqa: E402
    ExecutiveAssessmentSnapshot,
    create_executive_assessment_snapshot,
)
from assessment.executive_runtime import (  # noqa: E402
    EXECUTIVE_ASSESSMENT_VERSION,
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


if __name__ == "__main__":
    unittest.main()

