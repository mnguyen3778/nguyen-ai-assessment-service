import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from types import MappingProxyType


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.approved_dimension_aggregation_runtime import (  # noqa: E402
    aggregate_approved_dimensions,
)
from assessment.approved_dimension_weighting_runtime import (  # noqa: E402
    weight_approved_dimensions,
)
from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    RISK_DECISION_TABLE_SET_VERSION,
)
from assessment.approved_overall_assessment_runtime import (  # noqa: E402
    ApprovedOverallAssessmentResult,
    ApprovedOverallDimensionContribution,
    calculate_approved_overall_assessment,
)
from assessment.approved_question_scoring_runtime import (  # noqa: E402
    score_approved_questions,
)
from assessment.approved_readiness_runtime import (  # noqa: E402
    determine_approved_readiness,
)
from assessment.approved_risk_runtime import (  # noqa: E402
    RISK_ASSIGNMENT_METHOD,
    ApprovedRiskAssessmentResult,
    determine_approved_risk,
)
from assessment.approved_severity_runtime import (  # noqa: E402
    determine_approved_severity,
)
from assessment.methodology_config import METHODOLOGY_VERSION  # noqa: E402


def approved_responses(scale_value=2, numeric_value=50):
    return {
        question_id: (
            numeric_value
            if question.response_model_id == "numeric-0-100"
            else scale_value
        )
        for question_id, question in (
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.questions.items()
        )
    }


def approved_severity(scale_value=2, numeric_value=50):
    question_scoring = score_approved_questions(
        approved_responses(scale_value, numeric_value),
        METHODOLOGY_VERSION,
    )
    dimension_aggregation = aggregate_approved_dimensions(question_scoring)
    dimension_weighting = weight_approved_dimensions(dimension_aggregation)
    overall_assessment = calculate_approved_overall_assessment(dimension_weighting)
    readiness = determine_approved_readiness(overall_assessment)
    return determine_approved_severity(readiness)


def approved_severity_with_score(score):
    contributions = tuple(
        ApprovedOverallDimensionContribution(
            dimension_id=dimension.id,
            dimension_name=dimension.label,
            raw_aggregated_score=float(score),
            official_weight=dimension.weight,
            weighted_score=float(score) * dimension.weight / 100,
        )
        for dimension in APPROVED_METHODOLOGY_RUNTIME_CONFIG.dimensions.values()
    )
    overall_assessment = ApprovedOverallAssessmentResult(
        overall_assessment_score=sum(
            contribution.weighted_score
            for contribution in contributions
        ),
        weighted_dimension_contributions=contributions,
        methodology_version=METHODOLOGY_VERSION,
        runtime_config_version=(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version
        ),
        weight_set_version=(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG
            .version_manifest
            .official_dimension_weight_set_version
        ),
        calculation_method="weighted-dimension-contribution-sum-v1",
        dimension_count=len(contributions),
        total_official_weight=100,
    )
    readiness = determine_approved_readiness(overall_assessment)
    return determine_approved_severity(readiness)


class ApprovedRiskRuntimeTests(unittest.TestCase):
    def test_assigns_risk_deterministically(self):
        severity = approved_severity()

        first = determine_approved_risk(severity)
        second = determine_approved_risk(severity)

        self.assertEqual(first, second)
        self.assertIsInstance(first, ApprovedRiskAssessmentResult)
        self.assertEqual(first.risk_classification, "moderate-risk")
        self.assertEqual(first.severity_classifications, ("medium",))
        self.assertEqual(first.readiness_classification, "Ready")
        self.assertEqual(first.overall_assessment_score, 50.0)
        self.assertEqual(
            first.risk_decision_identifier,
            "risk-v1-moderate-any-medium",
        )
        self.assertEqual(
            first.risk_decision_table_version,
            RISK_DECISION_TABLE_SET_VERSION,
        )
        self.assertEqual(first.methodology_version, METHODOLOGY_VERSION)
        self.assertEqual(
            first.runtime_config_version,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.runtime_config_version,
        )
        self.assertEqual(first.assignment_method, RISK_ASSIGNMENT_METHOD)

    def test_applies_approved_risk_rules_by_severity_distribution(self):
        critical = approved_severity_with_score(0)
        high = approved_severity_with_score(25)
        medium = approved_severity_with_score(50)
        low = replace(medium, severity_classification="low")
        informational = approved_severity_with_score(75)

        cases = (
            ((critical,), "critical-risk", "risk-v1-critical-any-critical"),
            ((high, high), "elevated-risk", "risk-v1-elevated-high-concentration"),
            ((high,), "moderate-risk", "risk-v1-moderate-single-high"),
            ((medium,), "moderate-risk", "risk-v1-moderate-any-medium"),
            ((low,), "low-risk", "risk-v1-low-low-only-defects"),
            (
                (informational,),
                "minimal-informational",
                "risk-v1-minimal-informational-only",
            ),
        )

        for severities, risk, rule_id in cases:
            with self.subTest(rule_id=rule_id):
                result = determine_approved_risk(severities)

                self.assertEqual(result.risk_classification, risk)
                self.assertEqual(result.risk_decision_identifier, rule_id)

    def test_result_artifact_is_immutable(self):
        result = determine_approved_risk(approved_severity())

        with self.assertRaises(FrozenInstanceError):
            result.risk_classification = "critical-risk"
        with self.assertRaises(TypeError):
            result.severity_classifications[0] = "critical"

    def test_validation_fails_closed_for_non_severity_result(self):
        with self.assertRaisesRegex(ValueError, "ApprovedSeverityAssessmentResult"):
            determine_approved_risk(object())

    def test_validation_fails_closed_for_empty_severity_collection(self):
        with self.assertRaisesRegex(ValueError, "at least one severity"):
            determine_approved_risk(())

    def test_validation_fails_closed_for_unsupported_runtime_config_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            runtime_config_version="unsupported-runtime-config-version",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(ValueError, "runtime_config_version"):
            determine_approved_risk(
                approved_severity(),
                invalid_config,
            )

    def test_validation_fails_closed_for_unsupported_risk_table_version(self):
        manifest = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest,
            risk_decision_table_set_version="unsupported-risk-table-version",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            version_manifest=manifest,
        )

        with self.assertRaisesRegex(ValueError, "risk_decision_table_set_version"):
            determine_approved_risk(
                approved_severity(),
                invalid_config,
            )

    def test_validation_fails_closed_for_missing_required_risk_rule(self):
        risk_rules = dict(APPROVED_METHODOLOGY_RUNTIME_CONFIG.risk_decision_rules)
        del risk_rules["risk-v1-moderate-any-medium"]
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            risk_decision_rules=MappingProxyType(risk_rules),
        )

        with self.assertRaisesRegex(ValueError, "Missing approved risk"):
            determine_approved_risk(
                approved_severity(),
                invalid_config,
            )

    def test_validation_fails_closed_for_invalid_risk_rule_output(self):
        risk_rules = dict(APPROVED_METHODOLOGY_RUNTIME_CONFIG.risk_decision_rules)
        risk_rules["risk-v1-moderate-any-medium"] = replace(
            risk_rules["risk-v1-moderate-any-medium"],
            output="unsupported-risk",
        )
        invalid_config = replace(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG,
            risk_decision_rules=MappingProxyType(risk_rules),
        )

        with self.assertRaisesRegex(ValueError, "risk decision rule output"):
            determine_approved_risk(
                approved_severity(),
                invalid_config,
            )

    def test_validation_fails_closed_for_severity_methodology_version_mismatch(self):
        invalid_severity = replace(
            approved_severity(),
            methodology_version="unsupported-methodology-version",
        )

        with self.assertRaisesRegex(ValueError, "methodology version"):
            determine_approved_risk(invalid_severity)

    def test_validation_fails_closed_for_severity_runtime_config_version_mismatch(self):
        invalid_severity = replace(
            approved_severity(),
            runtime_config_version="unsupported-runtime-config-version",
        )

        with self.assertRaisesRegex(ValueError, "runtime config version"):
            determine_approved_risk(invalid_severity)

    def test_validation_fails_closed_for_severity_decision_table_version_mismatch(self):
        invalid_severity = replace(
            approved_severity(),
            decision_table_version="unsupported-severity-table-version",
        )

        with self.assertRaisesRegex(ValueError, "Severity decision table version"):
            determine_approved_risk(invalid_severity)

    def test_validation_fails_closed_for_unsupported_severity_classification(self):
        invalid_severity = replace(
            approved_severity(),
            severity_classification="unsupported-severity",
        )

        with self.assertRaisesRegex(ValueError, "Severity classification"):
            determine_approved_risk(invalid_severity)

    def test_validation_fails_closed_for_mixed_readiness_context(self):
        ready = approved_severity_with_score(50)
        advanced = approved_severity_with_score(75)

        with self.assertRaisesRegex(ValueError, "readiness classifications"):
            determine_approved_risk((ready, advanced))

    def test_validation_fails_closed_for_invalid_overall_assessment_score(self):
        invalid_severity = replace(
            approved_severity(),
            readiness_score=101,
        )

        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            determine_approved_risk(invalid_severity)


if __name__ == "__main__":
    unittest.main()
