import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.business_decision_package import (  # noqa: E402
    BUSINESS_DECISION_PACKAGE_LIMITATIONS,
    BusinessDecisionPackageAudit,
    BusinessDecisionPackageVersionMetadata,
    build_business_decision_package,
)
from assessment.business_decision_package_validation import (  # noqa: E402
    ROOT_FIELD_ORDER,
    validate_business_decision_package,
    validate_business_decision_package_serialization,
)
from assessment.confidence import build_confidence_evaluation  # noqa: E402
from assessment.decision_engine import evaluate_assessment  # noqa: E402
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


def valid_package(scale_value=4, numeric_value=100):
    decision_evaluation = evaluate_assessment(
        valid_configured_answers(scale_value, numeric_value)
    )
    snapshot = build_business_readiness_snapshot(
        "nguyen-ai-readiness-v1",
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


def issue_codes(validation_result):
    return tuple(issue.code for issue in validation_result.issues)


class BusinessDecisionPackageValidationTests(unittest.TestCase):
    def test_valid_package_is_accepted(self):
        package = valid_package()

        validation_result = validate_business_decision_package(package)

        self.assertTrue(validation_result.is_valid)
        self.assertEqual(validation_result.issues, ())

    def test_validation_result_is_immutable(self):
        validation_result = validate_business_decision_package(valid_package())

        with self.assertRaises(FrozenInstanceError):
            validation_result.is_valid = False

    def test_missing_component_is_rejected(self):
        package = replace(
            valid_package(),
            confidence_evaluation=None,
        )

        validation_result = validate_business_decision_package(package)

        self.assertFalse(validation_result.is_valid)
        self.assertIn("missing-component", issue_codes(validation_result))

    def test_version_mismatch_is_detected(self):
        package = valid_package()
        invalid_version_metadata = replace(
            package.version_metadata,
            methodology_version="other-methodology-version",
        )

        validation_result = validate_business_decision_package(
            replace(package, version_metadata=invalid_version_metadata)
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "audit-methodology-version-mismatch",
            issue_codes(validation_result),
        )
        self.assertIn(
            "serialized-audit-methodology-version-mismatch",
            issue_codes(validation_result),
        )

    def test_component_version_mismatch_is_detected(self):
        package = valid_package()
        invalid_version_metadata = BusinessDecisionPackageVersionMetadata(
            contract_version=package.version_metadata.contract_version,
            assessment_version=package.version_metadata.assessment_version,
            methodology_version=package.version_metadata.methodology_version,
            component_versions={"decisionEvaluation": "unexpected-version"},
        )

        validation_result = validate_business_decision_package(
            replace(package, version_metadata=invalid_version_metadata)
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn("component-version-mismatch", issue_codes(validation_result))
        self.assertIn(
            "serialized-component-version-mismatch",
            issue_codes(validation_result),
        )

    def test_serialization_contract_violation_is_detected(self):
        serialized_package = valid_package().to_dict()
        serialized_package.pop("audit")

        validation_result = validate_business_decision_package_serialization(
            serialized_package
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn("root-field-order-mismatch", issue_codes(validation_result))
        self.assertIn("missing-serialized-field", issue_codes(validation_result))

    def test_unexpected_serialized_field_is_detected(self):
        serialized_package = valid_package().to_dict()
        serialized_package["generatedAt"] = "2026-07-21T00:00:00Z"

        validation_result = validate_business_decision_package_serialization(
            serialized_package
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn("root-field-order-mismatch", issue_codes(validation_result))
        self.assertIn("unexpected-serialized-field", issue_codes(validation_result))

    def test_serialized_root_order_is_validated(self):
        serialized_package = valid_package().to_dict()
        reordered_package = {
            "versionMetadata": serialized_package["versionMetadata"],
            **{
                field: serialized_package[field]
                for field in ROOT_FIELD_ORDER
                if field != "versionMetadata"
            },
        }

        validation_result = validate_business_decision_package_serialization(
            reordered_package
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn("root-field-order-mismatch", issue_codes(validation_result))

    def test_audit_violation_is_detected(self):
        package = valid_package()
        invalid_audit = BusinessDecisionPackageAudit(
            assessment_version=package.audit.assessment_version,
            methodology_version=package.audit.methodology_version,
            source_component_ids=("decisionEvaluation",),
            evaluated_dimensions=package.audit.evaluated_dimensions,
            question_count=package.audit.question_count,
            total_weight=package.audit.total_weight,
        )

        validation_result = validate_business_decision_package(
            replace(package, audit=invalid_audit)
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn("source-components-mismatch", issue_codes(validation_result))
        self.assertIn(
            "serialized-source-components-mismatch",
            issue_codes(validation_result),
        )

    def test_limitation_violation_is_detected(self):
        package = replace(
            valid_package(),
            limitations=(
                *BUSINESS_DECISION_PACKAGE_LIMITATIONS,
                BUSINESS_DECISION_PACKAGE_LIMITATIONS[0],
            ),
        )

        validation_result = validate_business_decision_package(package)

        self.assertFalse(validation_result.is_valid)
        self.assertIn("limitations-mismatch", issue_codes(validation_result))
        self.assertIn("duplicate-limitations", issue_codes(validation_result))
        self.assertIn(
            "serialized-duplicate-limitations",
            issue_codes(validation_result),
        )

    def test_validation_behavior_is_deterministic(self):
        package = valid_package(scale_value=3, numeric_value=80)

        first_result = validate_business_decision_package(package)
        second_result = validate_business_decision_package(package)

        self.assertEqual(first_result, second_result)
        self.assertEqual(first_result.to_dict(), second_result.to_dict())

    def test_validation_preserves_package_immutability_and_contents(self):
        package = valid_package(scale_value=2, numeric_value=50)
        package_dict_before = package.to_dict()

        validate_business_decision_package(package)

        self.assertEqual(package.to_dict(), package_dict_before)
        with self.assertRaises(FrozenInstanceError):
            package.audit = None

    def test_serialized_invariant_violation_is_detected(self):
        serialized_package = valid_package().to_dict()
        serialized_package["businessReadinessSnapshot"]["overallReadiness"][
            "score"
        ] = 0

        validation_result = validate_business_decision_package_serialization(
            serialized_package
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn(
            "serialized-decision-snapshot-score-mismatch",
            issue_codes(validation_result),
        )

    def test_invalid_package_type_is_rejected(self):
        validation_result = validate_business_decision_package(
            {"not": "a package"}
        )

        self.assertFalse(validation_result.is_valid)
        self.assertIn("invalid-package-type", issue_codes(validation_result))


if __name__ == "__main__":
    unittest.main()
