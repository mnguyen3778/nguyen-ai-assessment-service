import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.approved_confidence_runtime import (  # noqa: E402
    CONFIDENCE_DECISION_TABLE_SET_VERSION,
    determine_approved_confidence,
)
from assessment.approved_dimension_aggregation_runtime import (  # noqa: E402
    aggregate_approved_dimensions,
)
from assessment.approved_dimension_weighting_runtime import (  # noqa: E402
    OFFICIAL_DIMENSION_WEIGHT_SET_VERSION,
    weight_approved_dimensions,
)
from assessment.approved_executive_summary_runtime import (  # noqa: E402
    EXECUTIVE_SUMMARY_TEMPLATE_ARTIFACT_VERSION,
    generate_approved_executive_summary,
)
from assessment.approved_methodology_runtime_config import (  # noqa: E402
    APPROVED_DIMENSION_ORDER,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
    GOLDEN_FIXTURE_CATALOG_VERSION,
    GOLDEN_FIXTURE_PAYLOADS_VERSION,
    RECOMMENDATION_DECISION_TABLE_SET_VERSION,
    RISK_DECISION_TABLE_SET_VERSION,
    SCORING_SCALE_VERSION,
    SEVERITY_DECISION_TABLE_SET_VERSION,
)
from assessment.approved_overall_assessment_runtime import (  # noqa: E402
    calculate_approved_overall_assessment,
)
from assessment.approved_question_scoring_runtime import (  # noqa: E402
    score_approved_questions,
)
from assessment.approved_readiness_runtime import (  # noqa: E402
    READINESS_THRESHOLD_VALUES_VERSION,
    determine_approved_readiness,
)
from assessment.approved_recommendation_runtime import (  # noqa: E402
    determine_approved_recommendation,
)
from assessment.approved_risk_runtime import determine_approved_risk  # noqa: E402
from assessment.approved_severity_runtime import (  # noqa: E402
    determine_approved_severity,
)
from assessment.business_decision_package import (  # noqa: E402
    BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS,
    BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BUSINESS_DECISION_PACKAGE_LIMITATIONS,
)
from assessment.business_decision_package_validation import (  # noqa: E402
    validate_business_decision_package,
)
from assessment.decision_engine import evaluate_assessment  # noqa: E402
from assessment.executive_orchestration import (  # noqa: E402
    DETERMINISTIC_EVALUATION_FAILURE,
    VERSION_COMPATIBILITY_FAILURE,
    ValidatedCanonicalExecutiveAssessmentInput,
    orchestrate_executive_assessment,
)
from assessment.executive_runtime import (  # noqa: E402
    EXECUTIVE_ASSESSMENT_VERSION,
    EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
    EXPOSURE_ELIGIBLE,
    NOT_PRODUCTION_AUTHORITATIVE,
    PACKAGE_VALIDATION_VALIDATED,
    RUNTIME_ELIGIBILITY_ELIGIBLE,
)
from assessment.executive_snapshot_handoff import (  # noqa: E402
    ORCHESTRATION_FAILURE,
    produce_executive_assessment_snapshot,
)
from assessment.methodology_config import (  # noqa: E402
    METHODOLOGY_VERSION,
)


QUESTION_SCORE_PROFILES = {
    "question-score-profile-all-0": (0, 0, 0.0),
    "question-score-profile-all-25": (1, 25, 25.0),
    "question-score-profile-all-50": (2, 50, 50.0),
    "question-score-profile-all-75": (3, 75, 75.0),
    "question-score-profile-all-100": (4, 100, 100.0),
}

RELEASED_EXPECTED_STAGE_OUTPUTS = {
    0.0: {
        "readiness": "Not Ready",
        "severity": "critical",
        "risk": "critical-risk",
        "confidence": "moderate-confidence",
        "recommendation": "immediate-action",
        "recommendation_rule": "recommendation-v1-deficiency-critical-immediate",
    },
    25.0: {
        "readiness": "Developing",
        "severity": "high",
        "risk": "moderate-risk",
        "confidence": "moderate-confidence",
        "recommendation": "priority-action",
        "recommendation_rule": "recommendation-v1-deficiency-high-priority",
    },
    50.0: {
        "readiness": "Ready",
        "severity": "medium",
        "risk": "moderate-risk",
        "confidence": "moderate-confidence",
        "recommendation": "planned-improvement",
        "recommendation_rule": "recommendation-v1-deficiency-medium-planned",
    },
    75.0: {
        "readiness": "Advanced",
        "severity": "informational",
        "risk": "minimal-informational",
        "confidence": "moderate-confidence",
        "recommendation": "monitor",
        "recommendation_rule": "recommendation-v1-observation-monitor",
    },
    100.0: {
        "readiness": "Advanced",
        "severity": "informational",
        "risk": "minimal-informational",
        "confidence": "moderate-confidence",
        "recommendation": "monitor",
        "recommendation_rule": "recommendation-v1-observation-monitor",
    },
}


@dataclass(frozen=True)
class GoldenFixture:
    fixture_id: str
    question_score_profile: str
    evidence_profile: str
    finding_payload: str
    expected_failure_category: str | None = None
    unsupported_methodology_version: bool = False

    @property
    def is_fail_closed(self) -> bool:
        return self.expected_failure_category is not None


@dataclass(frozen=True)
class GoldenFixtureExecution:
    question_scoring: object
    dimension_aggregation: object
    dimension_weighting: object
    overall_assessment: object
    readiness: object
    severity: object
    risk: object
    confidence: object
    recommendation: object
    executive_summary: object
    decision_evaluation: object
    business_decision_package: object
    serialized_snapshot: Mapping[str, Any]


COMPLETE_VALID_FIXTURES = (
    GoldenFixture(
        "fixture-v1-complete-minimal-risk",
        "question-score-profile-all-100",
        "evidence-profile-strong",
        "finding-payload-strength-informational",
    ),
    GoldenFixture(
        "fixture-v1-complete-not-ready-readiness",
        "question-score-profile-all-0",
        "evidence-profile-adequate",
        "finding-payload-none",
    ),
    GoldenFixture(
        "fixture-v1-complete-developing-readiness",
        "question-score-profile-all-25",
        "evidence-profile-adequate",
        "finding-payload-none",
    ),
    GoldenFixture(
        "fixture-v1-complete-ready-readiness",
        "question-score-profile-all-50",
        "evidence-profile-adequate",
        "finding-payload-none",
    ),
    GoldenFixture(
        "fixture-v1-complete-advanced-readiness",
        "question-score-profile-all-75",
        "evidence-profile-adequate",
        "finding-payload-none",
    ),
    GoldenFixture(
        "fixture-v1-critical-finding-risk",
        "question-score-profile-all-75",
        "evidence-profile-adequate",
        "finding-payload-critical-deficiency",
    ),
    GoldenFixture(
        "fixture-v1-high-concentration-risk",
        "question-score-profile-all-75",
        "evidence-profile-mixed-strong",
        "finding-payload-two-high-deficiencies",
    ),
    GoldenFixture(
        "fixture-v1-medium-risk",
        "question-score-profile-all-50",
        "evidence-profile-adequate",
        "finding-payload-medium-deficiency",
    ),
    GoldenFixture(
        "fixture-v1-low-risk",
        "question-score-profile-all-50",
        "evidence-profile-adequate",
        "finding-payload-low-deficiency",
    ),
    GoldenFixture(
        "fixture-v1-evidence-basic-confidence",
        "question-score-profile-all-50",
        "evidence-profile-basic",
        "finding-payload-none",
    ),
    GoldenFixture(
        "fixture-v1-evidence-strong-confidence",
        "question-score-profile-all-75",
        "evidence-profile-strong",
        "finding-payload-none",
    ),
    GoldenFixture(
        "fixture-v1-evidence-assertability-limitation",
        "question-score-profile-all-50",
        "evidence-profile-assertability-limitation",
        "finding-payload-none",
    ),
    GoldenFixture(
        "fixture-v1-no-findings-recommendation",
        "question-score-profile-all-100",
        "evidence-profile-adequate",
        "finding-payload-none",
    ),
)

FAIL_CLOSED_FIXTURES = (
    GoldenFixture(
        "fixture-v1-invalid-input-fail-closed",
        "question-score-profile-invalid-missing-response",
        "evidence-profile-adequate",
        "finding-payload-none",
        expected_failure_category=DETERMINISTIC_EVALUATION_FAILURE,
    ),
    GoldenFixture(
        "fixture-v1-version-mismatch-fail-closed",
        "question-score-profile-all-50",
        "evidence-profile-adequate",
        "finding-payload-none",
        expected_failure_category=VERSION_COMPATIBILITY_FAILURE,
        unsupported_methodology_version=True,
    ),
)

GOLDEN_FIXTURES = COMPLETE_VALID_FIXTURES + FAIL_CLOSED_FIXTURES


class GoldenFixtureRegressionRunner:
    def validate_complete_fixture(self, fixture: GoldenFixture) -> None:
        execution = self._execute_complete_fixture(fixture)
        _, _, expected_score = QUESTION_SCORE_PROFILES[
            fixture.question_score_profile
        ]
        expected_stage_outputs = RELEASED_EXPECTED_STAGE_OUTPUTS[expected_score]

        self._validate_fixture_metadata(fixture)
        self._validate_question_scoring(fixture, execution, expected_score)
        self._validate_dimension_aggregation(fixture, execution, expected_score)
        self._validate_dimension_weighting(fixture, execution, expected_score)
        self._validate_overall_assessment(fixture, execution, expected_score)
        self._validate_readiness(fixture, execution, expected_stage_outputs)
        self._validate_severity(fixture, execution, expected_stage_outputs)
        self._validate_risk(fixture, execution, expected_stage_outputs)
        self._validate_confidence(fixture, execution, expected_stage_outputs)
        self._validate_recommendation(fixture, execution, expected_stage_outputs)
        self._validate_executive_summary(
            fixture,
            execution,
            expected_stage_outputs,
            expected_score,
        )
        self._validate_business_decision_package(
            fixture,
            execution,
            expected_score,
        )
        self._validate_executive_assessment_snapshot(
            fixture,
            execution,
            expected_score,
        )

    def validate_fail_closed_fixture(self, fixture: GoldenFixture) -> None:
        self._validate_fixture_metadata(fixture)
        answers = _answers_for_fixture(fixture)
        methodology_version = (
            "unsupported-methodology-version"
            if fixture.unsupported_methodology_version
            else METHODOLOGY_VERSION
        )

        if fixture.unsupported_methodology_version:
            with self._expected_failure(fixture, "question_scoring"):
                score_approved_questions(answers, methodology_version)
        else:
            with self._expected_failure(fixture, "question_scoring"):
                score_approved_questions(answers, methodology_version)

        canonical_input = ValidatedCanonicalExecutiveAssessmentInput(
            assessment_version=EXECUTIVE_ASSESSMENT_VERSION,
            methodology_version=methodology_version,
            answers=answers,
        )
        orchestration_result = orchestrate_executive_assessment(canonical_input)
        _assert_equal(
            fixture,
            "orchestration.is_success",
            False,
            orchestration_result.is_success,
        )
        _assert_equal(
            fixture,
            "orchestration.failure.category",
            fixture.expected_failure_category,
            orchestration_result.failure.category,
        )
        _assert_equal(
            fixture,
            "orchestration.business_decision_package",
            None,
            orchestration_result.business_decision_package,
        )

        snapshot_result = produce_executive_assessment_snapshot(canonical_input)
        _assert_equal(
            fixture,
            "snapshot_production.is_success",
            False,
            snapshot_result.is_success,
        )
        _assert_equal(
            fixture,
            "snapshot_production.failure.category",
            ORCHESTRATION_FAILURE,
            snapshot_result.failure.category,
        )
        _assert_equal(
            fixture,
            "snapshot_production.serialized_snapshot",
            None,
            snapshot_result.serialized_snapshot,
        )

    def _execute_complete_fixture(
        self,
        fixture: GoldenFixture,
    ) -> GoldenFixtureExecution:
        answers = _answers_for_fixture(fixture)
        question_scoring = score_approved_questions(answers, METHODOLOGY_VERSION)
        dimension_aggregation = aggregate_approved_dimensions(question_scoring)
        dimension_weighting = weight_approved_dimensions(dimension_aggregation)
        overall_assessment = calculate_approved_overall_assessment(
            dimension_weighting
        )
        readiness = determine_approved_readiness(overall_assessment)
        severity = determine_approved_severity(readiness)
        risk = determine_approved_risk(severity)
        confidence = determine_approved_confidence(risk)
        recommendation = determine_approved_recommendation(confidence)
        executive_summary = generate_approved_executive_summary(recommendation)
        decision_evaluation = evaluate_assessment(answers)
        canonical_input = ValidatedCanonicalExecutiveAssessmentInput(
            assessment_version=EXECUTIVE_ASSESSMENT_VERSION,
            methodology_version=METHODOLOGY_VERSION,
            answers=answers,
        )
        orchestration_result = orchestrate_executive_assessment(canonical_input)
        if not orchestration_result.is_success:
            raise AssertionError(
                _mismatch_message(
                    fixture,
                    "orchestration",
                    "success",
                    orchestration_result.failure,
                )
            )
        snapshot_result = produce_executive_assessment_snapshot(canonical_input)
        if not snapshot_result.is_success:
            raise AssertionError(
                _mismatch_message(
                    fixture,
                    "snapshot_production",
                    "success",
                    snapshot_result.failure,
                )
            )

        return GoldenFixtureExecution(
            question_scoring=question_scoring,
            dimension_aggregation=dimension_aggregation,
            dimension_weighting=dimension_weighting,
            overall_assessment=overall_assessment,
            readiness=readiness,
            severity=severity,
            risk=risk,
            confidence=confidence,
            recommendation=recommendation,
            executive_summary=executive_summary,
            decision_evaluation=decision_evaluation,
            business_decision_package=orchestration_result.business_decision_package,
            serialized_snapshot=snapshot_result.serialized_snapshot,
        )

    def _validate_fixture_metadata(self, fixture: GoldenFixture) -> None:
        _assert_equal(
            fixture,
            "golden_fixture_catalog_version",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.golden_fixtures[
                fixture.fixture_id
            ].catalog_version,
        )
        _assert_equal(
            fixture,
            "golden_fixture_payload_version",
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.golden_fixtures[
                fixture.fixture_id
            ].payload_version,
        )
        _assert_equal(
            fixture,
            "methodology_version",
            METHODOLOGY_VERSION,
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.golden_fixtures[
                fixture.fixture_id
            ].methodology_version,
        )

    def _validate_question_scoring(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected_score: float,
    ) -> None:
        scoring = execution.question_scoring
        _assert_equal(fixture, "question_scoring.question_count", 48, scoring.question_count)
        _assert_equal(
            fixture,
            "question_scoring.runtime_config_version",
            APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
            scoring.runtime_config_version,
        )
        for question_score in scoring.question_scores:
            _assert_equal(
                fixture,
                f"question_scores.{question_score.question_id}",
                expected_score,
                question_score.score,
            )
            _assert_equal(
                fixture,
                f"question_scores.{question_score.question_id}.scoring_scale",
                SCORING_SCALE_VERSION,
                APPROVED_METHODOLOGY_RUNTIME_CONFIG.version_manifest.scoring_scale_version,
            )

    def _validate_dimension_aggregation(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected_score: float,
    ) -> None:
        aggregation = execution.dimension_aggregation
        _assert_equal(
            fixture,
            "dimension_aggregation.dimension_order",
            APPROVED_DIMENSION_ORDER,
            tuple(dimension.dimension_id for dimension in aggregation.dimensions),
        )
        for dimension in aggregation.dimensions:
            _assert_equal(
                fixture,
                f"dimension_aggregation.{dimension.dimension_id}.score",
                expected_score,
                dimension.score,
            )
            _assert_equal(
                fixture,
                f"dimension_aggregation.{dimension.dimension_id}.question_count",
                APPROVED_METHODOLOGY_RUNTIME_CONFIG.dimensions[
                    dimension.dimension_id
                ].expected_primary_question_count,
                dimension.question_count,
            )
            _assert_equal(
                fixture,
                f"dimension_aggregation.{dimension.dimension_id}.scores",
                {
                    question_id: expected_score
                    for question_id in dimension.contributing_question_ids
                },
                dict(dimension.contributing_scores),
            )

    def _validate_dimension_weighting(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected_score: float,
    ) -> None:
        weighting = execution.dimension_weighting
        _assert_equal(
            fixture,
            "dimension_weighting.weight_set_version",
            OFFICIAL_DIMENSION_WEIGHT_SET_VERSION,
            weighting.weight_set_version,
        )
        _assert_equal(
            fixture,
            "dimension_weighting.total_official_weight",
            100,
            weighting.total_official_weight,
        )
        for dimension in weighting.dimensions:
            expected_weight = APPROVED_METHODOLOGY_RUNTIME_CONFIG.dimensions[
                dimension.dimension_id
            ].weight
            _assert_equal(
                fixture,
                f"dimension_weighting.{dimension.dimension_id}.raw_score",
                expected_score,
                dimension.raw_aggregated_score,
            )
            _assert_equal(
                fixture,
                f"dimension_weighting.{dimension.dimension_id}.official_weight",
                expected_weight,
                dimension.official_weight,
            )
            _assert_equal(
                fixture,
                f"dimension_weighting.{dimension.dimension_id}.weighted_score",
                expected_score * expected_weight / 100,
                dimension.weighted_score,
            )

    def _validate_overall_assessment(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected_score: float,
    ) -> None:
        overall = execution.overall_assessment
        _assert_equal(
            fixture,
            "overall_assessment.overall_score",
            expected_score,
            overall.overall_assessment_score,
        )
        _assert_equal(
            fixture,
            "overall_assessment.total_official_weight",
            100,
            overall.total_official_weight,
        )
        _assert_equal(
            fixture,
            "decision_evaluation.overall_score",
            expected_score,
            execution.decision_evaluation.overall_score,
        )

    def _validate_readiness(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected: Mapping[str, str],
    ) -> None:
        _assert_equal(
            fixture,
            "readiness.classification",
            expected["readiness"],
            execution.readiness.readiness_classification,
        )
        _assert_equal(
            fixture,
            "readiness.threshold_version",
            READINESS_THRESHOLD_VALUES_VERSION,
            execution.readiness.readiness_threshold_version,
        )

    def _validate_severity(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected: Mapping[str, str],
    ) -> None:
        _assert_equal(
            fixture,
            "severity.classification",
            expected["severity"],
            execution.severity.severity_classification,
        )
        _assert_equal(
            fixture,
            "severity.table_version",
            SEVERITY_DECISION_TABLE_SET_VERSION,
            execution.severity.decision_table_version,
        )

    def _validate_risk(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected: Mapping[str, str],
    ) -> None:
        _assert_equal(
            fixture,
            "risk.classification",
            expected["risk"],
            execution.risk.risk_classification,
        )
        _assert_equal(
            fixture,
            "risk.table_version",
            RISK_DECISION_TABLE_SET_VERSION,
            execution.risk.risk_decision_table_version,
        )

    def _validate_confidence(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected: Mapping[str, str],
    ) -> None:
        _assert_equal(
            fixture,
            "confidence.classification",
            expected["confidence"],
            execution.confidence.confidence_classification,
        )
        _assert_equal(
            fixture,
            "confidence.table_version",
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
            execution.confidence.confidence_decision_table_version,
        )

    def _validate_recommendation(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected: Mapping[str, str],
    ) -> None:
        _assert_equal(
            fixture,
            "recommendation.classification",
            expected["recommendation"],
            execution.recommendation.recommendation_classification,
        )
        _assert_equal(
            fixture,
            "recommendation.decision_identifier",
            expected["recommendation_rule"],
            execution.recommendation.recommendation_decision_identifier,
        )
        _assert_equal(
            fixture,
            "recommendation.table_version",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
            execution.recommendation.recommendation_decision_table_version,
        )

    def _validate_executive_summary(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected: Mapping[str, str],
        expected_score: float,
    ) -> None:
        summary = execution.executive_summary
        _assert_equal(
            fixture,
            "executive_summary.template_identifier",
            EXECUTIVE_SUMMARY_TEMPLATE_ARTIFACT_VERSION,
            summary.executive_summary_template_identifier,
        )
        _assert_equal(
            fixture,
            "executive_summary.template_version",
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
            summary.executive_summary_template_version,
        )
        expected_section_ids = tuple(
            APPROVED_METHODOLOGY_RUNTIME_CONFIG.executive_summary_sections
        )
        _assert_equal(
            fixture,
            "executive_summary.section_ids",
            expected_section_ids,
            tuple(section.section_id for section in summary.sections),
        )
        section_text = {
            section.section_id: section.executive_summary_text
            for section in summary.sections
        }
        expected_section_text = _expected_executive_summary_sections(
            expected,
            expected_score,
        )
        for section_id, expected_text in expected_section_text.items():
            _assert_equal(
                fixture,
                f"executive_summary.sections.{section_id}",
                expected_text,
                section_text[section_id],
            )
        expected_summary_text = "\n\n".join(
            (
                f"{APPROVED_METHODOLOGY_RUNTIME_CONFIG.executive_summary_sections[section_id].heading}\n"
                f"{expected_text}"
            )
            for section_id, expected_text in expected_section_text.items()
        )
        _assert_equal(
            fixture,
            "executive_summary.executive_summary_text",
            expected_summary_text,
            summary.executive_summary_text,
        )

    def _validate_business_decision_package(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected_score: float,
    ) -> None:
        package = execution.business_decision_package
        validation = validate_business_decision_package(package)
        _assert_equal(fixture, "business_decision_package.is_valid", True, validation.is_valid)
        _assert_equal(
            fixture,
            "business_decision_package.contract_version",
            BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
            package.version_metadata.contract_version,
        )
        _assert_equal(
            fixture,
            "business_decision_package.component_versions",
            dict(BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS),
            dict(package.version_metadata.component_versions),
        )
        _assert_equal(
            fixture,
            "business_decision_package.limitations",
            BUSINESS_DECISION_PACKAGE_LIMITATIONS,
            package.limitations,
        )
        _assert_equal(
            fixture,
            "business_decision_package.decision_score",
            expected_score,
            package.decision_evaluation.overall_score,
        )
        _assert_equal(
            fixture,
            "business_decision_package.snapshot_score",
            expected_score,
            package.business_readiness_snapshot.overall_readiness.score,
        )

    def _validate_executive_assessment_snapshot(
        self,
        fixture: GoldenFixture,
        execution: GoldenFixtureExecution,
        expected_score: float,
    ) -> None:
        serialized_snapshot = execution.serialized_snapshot
        _assert_equal(
            fixture,
            "executive_assessment_snapshot.response_contract_version",
            EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
            serialized_snapshot["responseContractVersion"],
        )
        _assert_equal(
            fixture,
            "executive_assessment_snapshot.response_status",
            {
                "packageValidation": PACKAGE_VALIDATION_VALIDATED,
                "runtimeEligibility": RUNTIME_ELIGIBILITY_ELIGIBLE,
                "exposure": EXPOSURE_ELIGIBLE,
                "productionAuthority": NOT_PRODUCTION_AUTHORITATIVE,
            },
            serialized_snapshot["responseStatus"],
        )
        package = serialized_snapshot["businessDecisionPackage"]
        _assert_equal(
            fixture,
            "executive_assessment_snapshot.package.decision_score",
            expected_score,
            package["decisionEvaluation"]["overallScore"],
        )
        _assert_equal(
            fixture,
            "executive_assessment_snapshot.package.snapshot_score",
            expected_score,
            package["businessReadinessSnapshot"]["overallReadiness"]["score"],
        )
        _assert_equal(
            fixture,
            "executive_assessment_snapshot.package.methodology_version",
            METHODOLOGY_VERSION,
            package["versionMetadata"]["methodologyVersion"],
        )

    def _expected_failure(self, fixture: GoldenFixture, path: str):
        class ExpectedFailureContext:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback):
                if exc_type is None:
                    raise AssertionError(
                        _mismatch_message(
                            fixture,
                            path,
                            "fail closed",
                            "success",
                        )
                    )
                if not issubclass(exc_type, ValueError):
                    return False
                return True

        return ExpectedFailureContext()


class GoldenFixtureEndToEndValidationTests(unittest.TestCase):
    def test_golden_fixture_catalog_is_complete_and_ordered(self):
        self.assertEqual(
            tuple(fixture.fixture_id for fixture in GOLDEN_FIXTURES),
            tuple(APPROVED_METHODOLOGY_RUNTIME_CONFIG.golden_fixtures),
        )
        self.assertEqual(len(GOLDEN_FIXTURES), 15)

    def test_complete_valid_golden_fixtures_match_expected_outputs(self):
        runner = GoldenFixtureRegressionRunner()

        for fixture in COMPLETE_VALID_FIXTURES:
            with self.subTest(fixture_id=fixture.fixture_id):
                runner.validate_complete_fixture(fixture)

    def test_fail_closed_golden_fixtures_emit_no_partial_outputs(self):
        runner = GoldenFixtureRegressionRunner()

        for fixture in FAIL_CLOSED_FIXTURES:
            with self.subTest(fixture_id=fixture.fixture_id):
                runner.validate_fail_closed_fixture(fixture)


def _answers_for_fixture(fixture: GoldenFixture) -> dict[str, object]:
    if fixture.question_score_profile == "question-score-profile-invalid-missing-response":
        answers = _answers_from_profile("question-score-profile-all-50")
        del answers["q.ai.governance.owner"]
        return answers

    return _answers_from_profile(fixture.question_score_profile)


def _answers_from_profile(profile_id: str) -> dict[str, object]:
    scale_value, numeric_value, _ = QUESTION_SCORE_PROFILES[profile_id]
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


def _assert_equal(
    fixture: GoldenFixture,
    path: str,
    expected: object,
    observed: object,
) -> None:
    if observed != expected:
        raise AssertionError(_mismatch_message(fixture, path, expected, observed))


def _mismatch_message(
    fixture: GoldenFixture,
    path: str,
    expected: object,
    observed: object,
) -> str:
    return (
        f"Golden Fixture mismatch: fixture={fixture.fixture_id}; "
        f"path={path}; expected={expected!r}; observed={observed!r}"
    )


def _format_score(score: float) -> str:
    normalized = float(score)
    if normalized.is_integer():
        return str(int(normalized))
    return str(normalized)


def _expected_executive_summary_sections(
    expected: Mapping[str, str],
    expected_score: float,
) -> dict[str, str]:
    formatted_score = _format_score(expected_score)
    artifact_versions = (
        f"methodology_version={METHODOLOGY_VERSION}; "
        f"runtime_config_version={APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION}; "
        "recommendation_decision_table_version="
        f"{RECOMMENDATION_DECISION_TABLE_SET_VERSION}; "
        "executive_summary_template_version="
        f"{EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION}"
    )
    return {
        "overall-assessment-overview": (
            f"The overall assessment result is {formatted_score}. "
            f"The assigned readiness state is {expected['readiness']}. "
            f"This summary was produced under {METHODOLOGY_VERSION}."
        ),
        "business-capability-highlights": (
            "Business capability results are: "
            f"readiness={expected['readiness']}; "
            f"overall_assessment_score={formatted_score}. These results are "
            "summarized from approved Dimension Results and Evidence Evaluation."
        ),
        "significant-findings": (
            "The assessment produced 1 Findings. Significant Findings are "
            "summarized from Severity-Assigned Findings: "
            f"{expected['severity']}."
        ),
        "risk-overview": (
            f"The assessment-level risk is {expected['risk']}. This Risk "
            "Assessment is summarized from approved Severity-Assigned Findings."
        ),
        "confidence-statement": (
            f"The confidence assessment is {expected['confidence']}. This "
            "Confidence Assessment is summarized from approved Evidence "
            "Evaluation and required upstream context."
        ),
        "recommended-actions": (
            "The assessment produced 1 Recommendations: "
            f"{expected['recommendation']}."
        ),
        "closing-assessment-statement": (
            "This Executive Summary presents approved Assessment Service "
            f"outputs only. It is bound to {METHODOLOGY_VERSION} and source "
            f"artifact versions {artifact_versions}."
        ),
    }


if __name__ == "__main__":
    unittest.main()
