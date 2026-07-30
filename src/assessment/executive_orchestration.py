from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from assessment.business_decision_package import (
    BusinessDecisionPackage,
    build_business_decision_package,
)
from assessment.business_decision_package_validation import (
    BusinessDecisionPackageValidationIssue,
    validate_business_decision_package,
)
from assessment.confidence import build_confidence_evaluation
from assessment.decision_engine import evaluate_assessment
from assessment.executive_runtime import EXECUTIVE_ASSESSMENT_VERSION
from assessment.executive_summary import build_executive_summary_foundation
from assessment.methodology_config import (
    BUSINESS_DECISION_METHODOLOGY,
    METHODOLOGY_VERSION,
    BusinessDecisionMethodologyConfig,
)
from assessment.recommendation_priority import (
    build_recommendation_priority_evaluation,
)
from assessment.snapshot import build_business_readiness_snapshot


INPUT_CONTRACT_FAILURE = "INPUT_CONTRACT_FAILURE"
VERSION_COMPATIBILITY_FAILURE = "VERSION_COMPATIBILITY_FAILURE"
DETERMINISTIC_EVALUATION_FAILURE = "DETERMINISTIC_EVALUATION_FAILURE"
PACKAGE_INTEGRITY_FAILURE = "PACKAGE_INTEGRITY_FAILURE"
UNEXPECTED_INTERNAL_FAILURE = "UNEXPECTED_INTERNAL_FAILURE"


@dataclass(frozen=True)
class ValidatedCanonicalExecutiveAssessmentInput:
    assessment_version: str
    methodology_version: str
    answers: Mapping[str, object]

    def __post_init__(self) -> None:
        if isinstance(self.answers, Mapping):
            answers = {
                question_id: self.answers[question_id]
                for question_id in sorted(self.answers)
            }
            object.__setattr__(self, "answers", MappingProxyType(answers))


@dataclass(frozen=True)
class ExecutiveOrchestrationFailure:
    category: str
    code: str
    stage: str
    message: str
    assessment_version: str | None = None
    methodology_version: str | None = None
    validation_issues: tuple[BusinessDecisionPackageValidationIssue, ...] = ()
    deterministic_evaluation_started: bool = False
    package_validation_ran: bool = False


@dataclass(frozen=True)
class ExecutiveOrchestrationResult:
    business_decision_package: BusinessDecisionPackage | None = None
    failure: ExecutiveOrchestrationFailure | None = None

    def __post_init__(self) -> None:
        if (self.business_decision_package is None) == (self.failure is None):
            raise ValueError(
                "Executive orchestration result must contain exactly one outcome."
            )

    @property
    def is_success(self) -> bool:
        return self.business_decision_package is not None


def orchestrate_executive_assessment(
    canonical_input: object,
    methodology_config: BusinessDecisionMethodologyConfig = (
        BUSINESS_DECISION_METHODOLOGY
    ),
) -> ExecutiveOrchestrationResult:
    input_failure = _validate_orchestration_input(
        canonical_input,
        methodology_config,
    )
    if input_failure is not None:
        return ExecutiveOrchestrationResult(failure=input_failure)
    assert isinstance(canonical_input, ValidatedCanonicalExecutiveAssessmentInput)

    try:
        decision_evaluation = evaluate_assessment(
            canonical_input.answers,
            methodology_config,
        )
        business_readiness_snapshot = build_business_readiness_snapshot(
            canonical_input.assessment_version,
            decision_evaluation,
            methodology_config,
        )
        confidence_evaluation = build_confidence_evaluation(
            business_readiness_snapshot,
            methodology_config,
        )
        recommendation_priority_evaluation = (
            build_recommendation_priority_evaluation(
                business_readiness_snapshot,
                confidence_evaluation,
                methodology_config,
            )
        )
        executive_summary_foundation = build_executive_summary_foundation(
            business_readiness_snapshot,
            confidence_evaluation,
            recommendation_priority_evaluation,
            methodology_config,
        )
    except (TypeError, ValueError, AttributeError) as exc:
        return ExecutiveOrchestrationResult(
            failure=_failure(
                DETERMINISTIC_EVALUATION_FAILURE,
                "component-execution-failed",
                "deterministic-components",
                str(exc),
                canonical_input,
                deterministic_evaluation_started=True,
            )
        )
    except Exception:
        return ExecutiveOrchestrationResult(
            failure=_failure(
                UNEXPECTED_INTERNAL_FAILURE,
                "unexpected-component-failure",
                "deterministic-components",
                "Unexpected internal orchestration failure.",
                canonical_input,
                deterministic_evaluation_started=True,
            )
        )

    try:
        package = build_business_decision_package(
            decision_evaluation,
            business_readiness_snapshot,
            confidence_evaluation,
            recommendation_priority_evaluation,
            executive_summary_foundation,
        )
    except (TypeError, ValueError, AttributeError) as exc:
        return ExecutiveOrchestrationResult(
            failure=_failure(
                PACKAGE_INTEGRITY_FAILURE,
                "package-assembly-failed",
                "package-assembly",
                str(exc),
                canonical_input,
                deterministic_evaluation_started=True,
            )
        )
    except Exception:
        return ExecutiveOrchestrationResult(
            failure=_failure(
                UNEXPECTED_INTERNAL_FAILURE,
                "unexpected-package-assembly-failure",
                "package-assembly",
                "Unexpected internal package assembly failure.",
                canonical_input,
                deterministic_evaluation_started=True,
            )
        )

    try:
        package_validation = validate_business_decision_package(package)
    except Exception:
        return ExecutiveOrchestrationResult(
            failure=_failure(
                UNEXPECTED_INTERNAL_FAILURE,
                "unexpected-package-validation-failure",
                "package-validation",
                "Unexpected internal package validation failure.",
                canonical_input,
                deterministic_evaluation_started=True,
                package_validation_ran=True,
            )
        )

    if not package_validation.is_valid:
        return ExecutiveOrchestrationResult(
            failure=_failure(
                PACKAGE_INTEGRITY_FAILURE,
                "package-validation-failed",
                "package-validation",
                "BusinessDecisionPackage validation failed.",
                canonical_input,
                validation_issues=package_validation.issues,
                deterministic_evaluation_started=True,
                package_validation_ran=True,
            )
        )

    return ExecutiveOrchestrationResult(business_decision_package=package)


def _validate_orchestration_input(
    canonical_input: object,
    methodology_config: BusinessDecisionMethodologyConfig,
) -> ExecutiveOrchestrationFailure | None:
    if not isinstance(canonical_input, ValidatedCanonicalExecutiveAssessmentInput):
        return _failure(
            INPUT_CONTRACT_FAILURE,
            "invalid-canonical-input",
            "input",
            "Executive orchestration requires validated canonical executive input.",
        )

    if canonical_input.assessment_version != EXECUTIVE_ASSESSMENT_VERSION:
        return _failure(
            VERSION_COMPATIBILITY_FAILURE,
            "unsupported-assessment-version",
            "version-binding",
            "Executive assessment version is not supported.",
            canonical_input,
        )

    if canonical_input.methodology_version != METHODOLOGY_VERSION:
        return _failure(
            VERSION_COMPATIBILITY_FAILURE,
            "unsupported-methodology-version",
            "version-binding",
            "Executive methodology version is not supported.",
            canonical_input,
        )

    if methodology_config.version != canonical_input.methodology_version:
        return _failure(
            VERSION_COMPATIBILITY_FAILURE,
            "methodology-binding-mismatch",
            "version-binding",
            "Bound methodology version does not match configuration.",
            canonical_input,
        )

    if not isinstance(canonical_input.answers, Mapping):
        return _failure(
            INPUT_CONTRACT_FAILURE,
            "invalid-answer-representation",
            "input",
            "Canonical executive answers must be a mapping.",
            canonical_input,
        )

    return None


def _failure(
    category: str,
    code: str,
    stage: str,
    message: str,
    canonical_input: ValidatedCanonicalExecutiveAssessmentInput | None = None,
    *,
    validation_issues: tuple[BusinessDecisionPackageValidationIssue, ...] = (),
    deterministic_evaluation_started: bool = False,
    package_validation_ran: bool = False,
) -> ExecutiveOrchestrationFailure:
    return ExecutiveOrchestrationFailure(
        category=category,
        code=code,
        stage=stage,
        message=message,
        assessment_version=(
            canonical_input.assessment_version
            if canonical_input is not None
            else None
        ),
        methodology_version=(
            canonical_input.methodology_version
            if canonical_input is not None
            else None
        ),
        validation_issues=validation_issues,
        deterministic_evaluation_started=deterministic_evaluation_started,
        package_validation_ran=package_validation_ran,
    )
