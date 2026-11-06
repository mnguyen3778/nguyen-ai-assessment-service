import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import assessment.executive_orchestration as orchestration_module  # noqa: E402
from assessment.business_decision_package import (  # noqa: E402
    ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS,
    BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BUSINESS_DECISION_PACKAGE_LIMITATIONS,
    GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
)
from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_RECOMMENDATION_ACTION_TEXT_BY_RULE,
)
from assessment.business_decision_package_validation import (  # noqa: E402
    BusinessDecisionPackageValidationIssue,
    BusinessDecisionPackageValidationResult,
)
from assessment.executive_orchestration import (  # noqa: E402
    DETERMINISTIC_EVALUATION_FAILURE,
    INPUT_CONTRACT_FAILURE,
    PACKAGE_INTEGRITY_FAILURE,
    VERSION_COMPATIBILITY_FAILURE,
    ExecutiveOrchestrationResult,
    ValidatedCanonicalExecutiveAssessmentInput,
    orchestrate_executive_assessment,
)
from assessment.executive_runtime import EXECUTIVE_ASSESSMENT_VERSION  # noqa: E402
from assessment.methodology_config import (  # noqa: E402
    BUSINESS_DECISION_METHODOLOGY,
    METHODOLOGY_VERSION,
)
from assessment.models import AssessmentRequest  # noqa: E402
from assessment.governed_assessment_input import FindingInput  # noqa: E402
from test_golden_fixture_regression import request  # noqa: E402


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


class ExecutiveOrchestrationTests(unittest.TestCase):
    def test_explicit_local_v3_preserves_every_governed_decision(self):
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
            cases.append(replace(request(50, "adequate", "none"),
                                 findings=(finding,)))
        seen = set()
        fields = (
            "findingId", "recommendationClassification",
            "recommendationDecisionIdentifier", "recommendationDecisionTableVersion",
        )
        for canonical in cases:
            with self.subTest(findings=canonical.findings):
                v2 = orchestrate_executive_assessment(canonical)
                v3 = orchestrate_executive_assessment(
                    canonical,
                    governed_package_contract_version=ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
                )
                self.assertTrue(v2.is_success, v2.failure)
                self.assertTrue(v3.is_success, v3.failure)
                old = v2.business_decision_package.to_dict()
                new = v3.business_decision_package.to_dict()
                self.assertEqual(old["versionMetadata"]["contractVersion"],
                                 GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION)
                self.assertEqual(new["versionMetadata"]["contractVersion"],
                                 ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION)
                self.assertEqual(v2.business_decision_package.governed_conclusions,
                                 v3.business_decision_package.governed_conclusions)
                self.assertEqual(v3.business_decision_package.to_dict(), new)
                normalized = dict(new)
                normalized["versionMetadata"] = dict(new["versionMetadata"],
                    contractVersion=GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION)
                normalized["governedConclusions"] = dict(new["governedConclusions"])
                rows = []
                for row in new["governedConclusions"]["recommendations"]:
                    self.assertEqual(tuple(row), fields + ("recommendationActionText",))
                    self.assertEqual(row["recommendationActionText"],
                        APPROVED_RECOMMENDATION_ACTION_TEXT_BY_RULE[
                            row["recommendationDecisionIdentifier"]])
                    seen.add(row["recommendationDecisionIdentifier"])
                    rows.append({field: row[field] for field in fields})
                normalized["governedConclusions"]["recommendations"] = rows
                self.assertEqual(normalized, old)
                self.assertTrue(all(tuple(row) == fields for row in
                                    old["governedConclusions"]["recommendations"]))
                if not canonical.findings:
                    self.assertIsNone(rows[0]["findingId"])
        self.assertEqual(seen, set(APPROVED_RECOMMENDATION_ACTION_TEXT_BY_RULE))

    def test_v3_selection_rejects_unsupported_invalid_and_legacy_requests(self):
        governed = request(50, "adequate", "none")
        for selected in (None, 3, False, "business-decision-package-v4"):
            with self.subTest(selected=selected):
                result = orchestrate_executive_assessment(
                    governed, governed_package_contract_version=selected)
                self.assertFalse(result.is_success)
                self.assertEqual(result.failure.category, VERSION_COMPATIBILITY_FAILURE)
                self.assertFalse(result.failure.deterministic_evaluation_started)
        legacy = orchestrate_executive_assessment(
            valid_canonical_input(),
            governed_package_contract_version=ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
        )
        self.assertFalse(legacy.is_success)
        self.assertEqual(legacy.failure.code, "legacy-v3-package-version")
        self.assertFalse(legacy.failure.deterministic_evaluation_started)

    def test_orchestration_produces_deterministic_validated_package(self):
        canonical_input = valid_canonical_input(scale_value=3, numeric_value=80)

        first_result = orchestrate_executive_assessment(canonical_input)
        second_result = orchestrate_executive_assessment(canonical_input)

        self.assertTrue(first_result.is_success)
        self.assertTrue(second_result.is_success)
        self.assertEqual(
            first_result.business_decision_package.to_dict(),
            second_result.business_decision_package.to_dict(),
        )
        self.assertIsNone(first_result.failure)

    def test_orchestration_invokes_components_in_approved_sequence(self):
        canonical_input = valid_canonical_input()
        observed_sequence = []

        def wrapped(name, function):
            def wrapper(*args, **kwargs):
                observed_sequence.append(name)
                return function(*args, **kwargs)

            return wrapper

        with patch.object(
            orchestration_module,
            "evaluate_assessment",
            side_effect=wrapped(
                "decision",
                orchestration_module.evaluate_assessment,
            ),
        ), patch.object(
            orchestration_module,
            "build_business_readiness_snapshot",
            side_effect=wrapped(
                "snapshot",
                orchestration_module.build_business_readiness_snapshot,
            ),
        ), patch.object(
            orchestration_module,
            "build_confidence_evaluation",
            side_effect=wrapped(
                "confidence",
                orchestration_module.build_confidence_evaluation,
            ),
        ), patch.object(
            orchestration_module,
            "build_recommendation_priority_evaluation",
            side_effect=wrapped(
                "priority",
                orchestration_module.build_recommendation_priority_evaluation,
            ),
        ), patch.object(
            orchestration_module,
            "build_executive_summary_foundation",
            side_effect=wrapped(
                "summary",
                orchestration_module.build_executive_summary_foundation,
            ),
        ), patch.object(
            orchestration_module,
            "build_business_decision_package",
            side_effect=wrapped(
                "package",
                orchestration_module.build_business_decision_package,
            ),
        ), patch.object(
            orchestration_module,
            "validate_business_decision_package",
            side_effect=wrapped(
                "package-validation",
                orchestration_module.validate_business_decision_package,
            ),
        ):
            result = orchestrate_executive_assessment(canonical_input)

        self.assertTrue(result.is_success)
        self.assertEqual(
            observed_sequence,
            [
                "decision",
                "snapshot",
                "confidence",
                "priority",
                "summary",
                "package",
                "package-validation",
            ],
        )

    def test_orchestration_fails_fast_when_decision_engine_fails(self):
        canonical_input = valid_canonical_input()

        with patch.object(
            orchestration_module,
            "evaluate_assessment",
            side_effect=ValueError("deterministic evaluation failed"),
        ) as decision_mock, patch.object(
            orchestration_module,
            "build_business_readiness_snapshot",
        ) as snapshot_mock, patch.object(
            orchestration_module,
            "build_business_decision_package",
        ) as package_mock:
            result = orchestrate_executive_assessment(canonical_input)

        self.assertFalse(result.is_success)
        self.assertIsNone(result.business_decision_package)
        self.assertEqual(result.failure.category, DETERMINISTIC_EVALUATION_FAILURE)
        self.assertTrue(result.failure.deterministic_evaluation_started)
        self.assertFalse(result.failure.package_validation_ran)
        decision_mock.assert_called_once()
        snapshot_mock.assert_not_called()
        package_mock.assert_not_called()

    def test_orchestration_fails_fast_when_confidence_fails(self):
        canonical_input = valid_canonical_input()

        with patch.object(
            orchestration_module,
            "build_confidence_evaluation",
            side_effect=ValueError("confidence failed"),
        ) as confidence_mock, patch.object(
            orchestration_module,
            "build_recommendation_priority_evaluation",
        ) as priority_mock, patch.object(
            orchestration_module,
            "build_executive_summary_foundation",
        ) as summary_mock, patch.object(
            orchestration_module,
            "build_business_decision_package",
        ) as package_mock:
            result = orchestrate_executive_assessment(canonical_input)

        self.assertFalse(result.is_success)
        self.assertEqual(result.failure.category, DETERMINISTIC_EVALUATION_FAILURE)
        confidence_mock.assert_called_once()
        priority_mock.assert_not_called()
        summary_mock.assert_not_called()
        package_mock.assert_not_called()

    def test_orchestration_enforces_package_validation(self):
        canonical_input = valid_canonical_input()
        validation_issue = BusinessDecisionPackageValidationIssue(
            code="component-version-mismatch",
            path="$.versionMetadata.componentVersions",
            message="Component versions do not match.",
        )

        with patch.object(
            orchestration_module,
            "validate_business_decision_package",
            return_value=BusinessDecisionPackageValidationResult(
                is_valid=False,
                issues=(validation_issue,),
            ),
        ) as validation_mock:
            result = orchestrate_executive_assessment(canonical_input)

        self.assertFalse(result.is_success)
        self.assertIsNone(result.business_decision_package)
        self.assertEqual(result.failure.category, PACKAGE_INTEGRITY_FAILURE)
        self.assertEqual(result.failure.code, "package-validation-failed")
        self.assertEqual(result.failure.validation_issues, (validation_issue,))
        self.assertTrue(result.failure.package_validation_ran)
        validation_mock.assert_called_once()

    def test_package_assembly_failure_does_not_return_partial_success(self):
        canonical_input = valid_canonical_input()

        with patch.object(
            orchestration_module,
            "build_business_decision_package",
            side_effect=ValueError("package assembly failed"),
        ), patch.object(
            orchestration_module,
            "validate_business_decision_package",
        ) as validation_mock:
            result = orchestrate_executive_assessment(canonical_input)

        self.assertFalse(result.is_success)
        self.assertIsNone(result.business_decision_package)
        self.assertEqual(result.failure.category, PACKAGE_INTEGRITY_FAILURE)
        self.assertEqual(result.failure.code, "package-assembly-failed")
        self.assertIsNotNone(result.failure)
        validation_mock.assert_not_called()

    def test_orchestration_preserves_input_immutability(self):
        answers = valid_configured_answers(scale_value=2, numeric_value=50)
        canonical_input = ValidatedCanonicalExecutiveAssessmentInput(
            assessment_version=EXECUTIVE_ASSESSMENT_VERSION,
            methodology_version=METHODOLOGY_VERSION,
            answers=answers,
        )
        input_answers_before = dict(canonical_input.answers)

        answers[next(iter(answers))] = 0
        result = orchestrate_executive_assessment(canonical_input)

        self.assertTrue(result.is_success)
        self.assertEqual(dict(canonical_input.answers), input_answers_before)
        with self.assertRaises(TypeError):
            canonical_input.answers[next(iter(canonical_input.answers))] = 1
        with self.assertRaises(FrozenInstanceError):
            canonical_input.assessment_version = "changed"

    def test_orchestration_preserves_package_versions_and_limitations(self):
        result = orchestrate_executive_assessment(valid_canonical_input())

        package = result.business_decision_package

        self.assertTrue(result.is_success)
        self.assertEqual(
            package.version_metadata.contract_version,
            BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
        )
        self.assertEqual(
            package.version_metadata.assessment_version,
            EXECUTIVE_ASSESSMENT_VERSION,
        )
        self.assertEqual(
            package.version_metadata.methodology_version,
            METHODOLOGY_VERSION,
        )
        self.assertEqual(
            package.version_metadata.component_versions,
            BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS,
        )
        self.assertEqual(package.limitations, BUSINESS_DECISION_PACKAGE_LIMITATIONS)

    def test_orchestration_rejects_unsupported_assessment_version_before_evaluation(self):
        canonical_input = ValidatedCanonicalExecutiveAssessmentInput(
            assessment_version="nguyen-ai-readiness-v1",
            methodology_version=METHODOLOGY_VERSION,
            answers=valid_configured_answers(),
        )

        with patch.object(
            orchestration_module,
            "evaluate_assessment",
        ) as decision_mock:
            result = orchestrate_executive_assessment(canonical_input)

        self.assertFalse(result.is_success)
        self.assertEqual(result.failure.category, VERSION_COMPATIBILITY_FAILURE)
        self.assertEqual(result.failure.code, "unsupported-assessment-version")
        self.assertFalse(result.failure.deterministic_evaluation_started)
        decision_mock.assert_not_called()

    def test_orchestration_rejects_methodology_binding_mismatch_before_evaluation(self):
        canonical_input = ValidatedCanonicalExecutiveAssessmentInput(
            assessment_version=EXECUTIVE_ASSESSMENT_VERSION,
            methodology_version="other-methodology-version",
            answers=valid_configured_answers(),
        )

        with patch.object(
            orchestration_module,
            "evaluate_assessment",
        ) as decision_mock:
            result = orchestrate_executive_assessment(canonical_input)

        self.assertFalse(result.is_success)
        self.assertEqual(result.failure.category, VERSION_COMPATIBILITY_FAILURE)
        self.assertEqual(result.failure.code, "unsupported-methodology-version")
        decision_mock.assert_not_called()

    def test_orchestration_rejects_invalid_answer_representation_before_evaluation(self):
        canonical_input = ValidatedCanonicalExecutiveAssessmentInput(
            assessment_version=EXECUTIVE_ASSESSMENT_VERSION,
            methodology_version=METHODOLOGY_VERSION,
            answers=[],
        )

        with patch.object(
            orchestration_module,
            "evaluate_assessment",
        ) as decision_mock:
            result = orchestrate_executive_assessment(canonical_input)

        self.assertFalse(result.is_success)
        self.assertEqual(result.failure.category, INPUT_CONTRACT_FAILURE)
        self.assertEqual(result.failure.code, "invalid-answer-representation")
        decision_mock.assert_not_called()

    def test_orchestration_rejects_public_payloads_before_evaluation(self):
        public_payload = {
            "assessmentVersion": "nguyen-ai-readiness-v1",
            "organization": {"name": "Nguyen AI"},
            "respondent": {"email": "owner@example.com"},
            "answers": {"public-question-1": 4},
        }

        with patch.object(
            orchestration_module,
            "evaluate_assessment",
        ) as decision_mock:
            result = orchestrate_executive_assessment(public_payload)

        self.assertFalse(result.is_success)
        self.assertEqual(result.failure.category, INPUT_CONTRACT_FAILURE)
        self.assertEqual(result.failure.code, "invalid-canonical-input")
        decision_mock.assert_not_called()

    def test_orchestration_rejects_public_assessment_request_before_evaluation(self):
        public_request = AssessmentRequest(
            assessment_version="nguyen-ai-readiness-v1",
            organization={"name": "Nguyen AI"},
            respondent={"email": "owner@example.com"},
            answers={"public-question-1": 4},
        )

        with patch.object(
            orchestration_module,
            "evaluate_assessment",
        ) as decision_mock:
            result = orchestrate_executive_assessment(public_request)

        self.assertFalse(result.is_success)
        self.assertEqual(result.failure.category, INPUT_CONTRACT_FAILURE)
        self.assertIsNone(result.business_decision_package)
        decision_mock.assert_not_called()

    def test_orchestration_result_rejects_partial_outcomes(self):
        with self.assertRaisesRegex(ValueError, "exactly one outcome"):
            ExecutiveOrchestrationResult()

        successful_result = orchestrate_executive_assessment(valid_canonical_input())
        failed_result = orchestrate_executive_assessment({})

        with self.assertRaisesRegex(ValueError, "exactly one outcome"):
            ExecutiveOrchestrationResult(
                business_decision_package=(
                    successful_result.business_decision_package
                ),
                failure=failed_result.failure,
            )


if __name__ == "__main__":
    unittest.main()
