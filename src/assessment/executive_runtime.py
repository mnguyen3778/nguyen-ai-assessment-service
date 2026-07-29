from dataclasses import dataclass
from typing import Any, Mapping

from assessment.business_decision_package import (
    BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BusinessDecisionPackage,
)
from assessment.business_decision_package_validation import (
    validate_business_decision_package,
    validate_business_decision_package_serialization,
)
from assessment.methodology_config import METHODOLOGY_VERSION


EXECUTIVE_ASSESSMENT_VERSION = "nguyen-ai-executive-assessment-v1"
EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION = "executive-runtime-response-v1"

PACKAGE_VALIDATION_VALIDATED = "VALIDATED"
RUNTIME_ELIGIBILITY_ELIGIBLE = "RUNTIME_ELIGIBLE"
EXPOSURE_ELIGIBLE = "EXPOSURE_ELIGIBLE"
PRODUCTION_AUTHORITATIVE = "PRODUCTION_AUTHORITATIVE"
NOT_PRODUCTION_AUTHORITATIVE = "NOT_PRODUCTION_AUTHORITATIVE"

EXECUTIVE_REQUEST_INVALID = "EXECUTIVE_REQUEST_INVALID"
EXECUTIVE_VERSION_INCOMPATIBLE = "EXECUTIVE_VERSION_INCOMPATIBLE"
EXECUTIVE_VERSION_CONFIGURATION_ERROR = "EXECUTIVE_VERSION_CONFIGURATION_ERROR"
EXECUTIVE_PROCESSING_FAILED = "EXECUTIVE_PROCESSING_FAILED"
EXECUTIVE_PACKAGE_INTEGRITY_FAILED = "EXECUTIVE_PACKAGE_INTEGRITY_FAILED"
EXECUTIVE_RESULT_UNAVAILABLE = "EXECUTIVE_RESULT_UNAVAILABLE"
EXECUTIVE_INTERNAL_ERROR = "EXECUTIVE_INTERNAL_ERROR"


_ERROR_CONTRACT = {
    EXECUTIVE_REQUEST_INVALID: (
        "request-error",
        "The submitted executive request is invalid.",
        400,
    ),
    EXECUTIVE_VERSION_INCOMPATIBLE: (
        "version-error",
        "The submitted executive version is not supported.",
        409,
    ),
    EXECUTIVE_VERSION_CONFIGURATION_ERROR: (
        "service-configuration-error",
        "The executive version configuration is unavailable.",
        500,
    ),
    EXECUTIVE_PROCESSING_FAILED: (
        "processing-error",
        "The executive result could not be processed.",
        500,
    ),
    EXECUTIVE_PACKAGE_INTEGRITY_FAILED: (
        "integrity-error",
        "The executive package failed integrity validation.",
        500,
    ),
    EXECUTIVE_RESULT_UNAVAILABLE: (
        "governance-error",
        "The executive result is not available under the current governance state.",
        409,
    ),
    EXECUTIVE_INTERNAL_ERROR: (
        "internal-error",
        "The executive runtime failed closed.",
        500,
    ),
}


@dataclass(frozen=True)
class ExecutiveRuntimeMetadata:
    request_id: str
    correlation_id: str
    trace_id: str | None = None


@dataclass(frozen=True)
class ExecutiveRuntimeValidationIssue:
    code: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "path": self.path,
            "message": self.message,
        }


@dataclass(frozen=True)
class ExecutiveRuntimeValidationResult:
    is_valid: bool
    issues: tuple[ExecutiveRuntimeValidationIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "isValid": self.is_valid,
            "issues": [issue.to_dict() for issue in self.issues],
        }


@dataclass(frozen=True)
class ExecutiveRuntimeResponseStatus:
    package_validation: str
    runtime_eligibility: str
    exposure: str
    production_authority: str

    def to_dict(self) -> dict[str, str]:
        return {
            "packageValidation": self.package_validation,
            "runtimeEligibility": self.runtime_eligibility,
            "exposure": self.exposure,
            "productionAuthority": self.production_authority,
        }


@dataclass(frozen=True)
class ExecutiveRuntimeSuccessResponse:
    business_decision_package: BusinessDecisionPackage
    response_status: ExecutiveRuntimeResponseStatus
    response_contract_version: str = EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "responseContractVersion": self.response_contract_version,
            "responseStatus": self.response_status.to_dict(),
            "businessDecisionPackage": self.business_decision_package.to_dict(),
        }


@dataclass(frozen=True)
class ExecutiveRuntimeError:
    code: str
    category: str
    message: str
    details: tuple[ExecutiveRuntimeValidationIssue, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "category": self.category,
            "message": self.message,
            "details": [detail.to_dict() for detail in self.details],
        }


@dataclass(frozen=True)
class ExecutiveRuntimeErrorResponse:
    error: ExecutiveRuntimeError
    http_status: int
    response_contract_version: str = EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "responseContractVersion": self.response_contract_version,
            "error": self.error.to_dict(),
        }


@dataclass(frozen=True)
class ExecutiveRuntimeResult:
    success: ExecutiveRuntimeSuccessResponse | None = None
    error: ExecutiveRuntimeErrorResponse | None = None

    def __post_init__(self) -> None:
        if (self.success is None) == (self.error is None):
            raise ValueError(
                "Executive runtime result must contain exactly one terminal response."
            )

    @property
    def is_success(self) -> bool:
        return self.success is not None

    def to_dict(self) -> dict[str, Any]:
        if self.success is not None:
            return self.success.to_dict()
        if self.error is None:
            raise ValueError("Executive runtime result has no terminal response.")
        return self.error.to_dict()


def create_executive_runtime_success_response(
    business_decision_package: object,
    runtime_metadata: object,
    *,
    production_authoritative: bool = False,
) -> ExecutiveRuntimeResult:
    validation_result = validate_executive_runtime_input(
        business_decision_package,
        runtime_metadata,
    )
    if not validation_result.is_valid:
        return create_executive_runtime_error_response(
            _error_code_for_validation_issues(validation_result.issues),
            validation_result.issues,
        )

    if not isinstance(business_decision_package, BusinessDecisionPackage):
        return create_executive_runtime_error_response(
            EXECUTIVE_PACKAGE_INTEGRITY_FAILED,
        )

    response_status = ExecutiveRuntimeResponseStatus(
        package_validation=PACKAGE_VALIDATION_VALIDATED,
        runtime_eligibility=RUNTIME_ELIGIBILITY_ELIGIBLE,
        exposure=EXPOSURE_ELIGIBLE,
        production_authority=(
            PRODUCTION_AUTHORITATIVE
            if production_authoritative
            else NOT_PRODUCTION_AUTHORITATIVE
        ),
    )
    return ExecutiveRuntimeResult(
        success=ExecutiveRuntimeSuccessResponse(
            business_decision_package=business_decision_package,
            response_status=response_status,
        )
    )


def create_executive_runtime_error_response(
    error_code: str,
    validation_issues: tuple[ExecutiveRuntimeValidationIssue, ...] = (),
) -> ExecutiveRuntimeResult:
    contract = _ERROR_CONTRACT.get(error_code, _ERROR_CONTRACT[EXECUTIVE_INTERNAL_ERROR])
    resolved_code = (
        error_code
        if error_code in _ERROR_CONTRACT
        else EXECUTIVE_INTERNAL_ERROR
    )
    category, message, http_status = contract
    details = validation_issues if resolved_code == EXECUTIVE_REQUEST_INVALID else ()

    return ExecutiveRuntimeResult(
        error=ExecutiveRuntimeErrorResponse(
            error=ExecutiveRuntimeError(
                code=resolved_code,
                category=category,
                message=message,
                details=details,
            ),
            http_status=http_status,
        )
    )


def validate_executive_runtime_input(
    business_decision_package: object,
    runtime_metadata: object,
) -> ExecutiveRuntimeValidationResult:
    issues: list[ExecutiveRuntimeValidationIssue] = []

    _validate_runtime_metadata(runtime_metadata, issues)
    _validate_business_decision_package_input(business_decision_package, issues)

    return _result(issues)


def validate_executive_runtime_response_payload(
    response_payload: object,
) -> ExecutiveRuntimeValidationResult:
    issues: list[ExecutiveRuntimeValidationIssue] = []

    if not isinstance(response_payload, Mapping):
        issues.append(
            _issue(
                "invalid-response-type",
                "$",
                "Executive runtime response must be a mapping.",
            )
        )
        return _result(issues)

    if (
        response_payload.get("responseContractVersion")
        != EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION
    ):
        issues.append(
            _issue(
                "invalid-response-contract-version",
                "$.responseContractVersion",
                "Executive runtime response contract version is not supported.",
            )
        )

    has_success = "businessDecisionPackage" in response_payload
    has_error = "error" in response_payload

    if has_success and has_error:
        issues.append(
            _issue(
                "success-error-conflict",
                "$",
                "Executive runtime response cannot contain both package and error.",
            )
        )
    if not has_success and not has_error:
        issues.append(
            _issue(
                "missing-terminal-response",
                "$",
                "Executive runtime response must contain package or error.",
            )
        )

    if has_success:
        _validate_success_payload(response_payload, issues)
    if has_error:
        _validate_error_payload(response_payload, issues)

    return _result(issues)


def _validate_runtime_metadata(
    runtime_metadata: object,
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    if runtime_metadata is None:
        issues.append(
            _issue(
                "missing-runtime-metadata",
                "$.runtimeMetadata",
                "Runtime metadata is required at the executive runtime boundary.",
            )
        )
        return

    if not isinstance(runtime_metadata, ExecutiveRuntimeMetadata):
        issues.append(
            _issue(
                "invalid-runtime-metadata",
                "$.runtimeMetadata",
                "Runtime metadata must be ExecutiveRuntimeMetadata.",
            )
        )
        return

    _validate_non_empty_string(
        runtime_metadata.request_id,
        "$.runtimeMetadata.requestId",
        "missing-runtime-request-id",
        "Runtime request identifier is required.",
        issues,
    )
    _validate_non_empty_string(
        runtime_metadata.correlation_id,
        "$.runtimeMetadata.correlationId",
        "missing-runtime-correlation-id",
        "Runtime correlation identifier is required.",
        issues,
    )
    if runtime_metadata.trace_id is not None:
        _validate_non_empty_string(
            runtime_metadata.trace_id,
            "$.runtimeMetadata.traceId",
            "invalid-runtime-trace-id",
            "Runtime trace identifier must be non-empty when supplied.",
            issues,
        )


def _validate_business_decision_package_input(
    business_decision_package: object,
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    if business_decision_package is None:
        issues.append(
            _issue(
                "missing-business-decision-package",
                "$.businessDecisionPackage",
                "BusinessDecisionPackage is required.",
            )
        )
        return

    if not isinstance(business_decision_package, BusinessDecisionPackage):
        issues.append(
            _issue(
                "invalid-business-decision-package",
                "$.businessDecisionPackage",
                "Runtime input must be a BusinessDecisionPackage.",
            )
        )
        return

    version_metadata = business_decision_package.version_metadata
    if version_metadata is None:
        issues.append(
            _issue(
                "missing-package-version-metadata",
                "$.businessDecisionPackage.versionMetadata",
                "BusinessDecisionPackage version metadata is required.",
            )
        )
    else:
        if (
            version_metadata.contract_version
            != BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION
        ):
            issues.append(
                _issue(
                    "invalid-package-contract-version",
                    "$.businessDecisionPackage.versionMetadata.contractVersion",
                    "BusinessDecisionPackage contract version is not supported.",
                )
            )
        if version_metadata.assessment_version != EXECUTIVE_ASSESSMENT_VERSION:
            issues.append(
                _issue(
                    "invalid-executive-assessment-version",
                    "$.businessDecisionPackage.versionMetadata.assessmentVersion",
                    "BusinessDecisionPackage assessment version is not supported.",
                )
            )
        if version_metadata.methodology_version != METHODOLOGY_VERSION:
            issues.append(
                _issue(
                    "invalid-methodology-version",
                    "$.businessDecisionPackage.versionMetadata.methodologyVersion",
                    "BusinessDecisionPackage methodology version is not supported.",
                )
            )

    package_validation = validate_business_decision_package(business_decision_package)
    for package_issue in package_validation.issues:
        issues.append(
            _issue(
                f"package-{package_issue.code}",
                f"$.businessDecisionPackage{package_issue.path[1:]}",
                "BusinessDecisionPackage validation failed.",
            )
        )


def _validate_success_payload(
    response_payload: Mapping[str, Any],
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    expected_fields = (
        "responseContractVersion",
        "responseStatus",
        "businessDecisionPackage",
    )
    observed_fields = tuple(response_payload)
    if observed_fields != expected_fields:
        issues.append(
            _issue(
                "success-root-field-order-mismatch",
                "$",
                "Successful response root fields do not match contract order.",
            )
        )

    response_status = response_payload.get("responseStatus")
    if not isinstance(response_status, Mapping):
        issues.append(
            _issue(
                "invalid-response-status",
                "$.responseStatus",
                "Successful response status must be a mapping.",
            )
        )
    else:
        _validate_response_status(response_status, issues)

    package_validation = validate_business_decision_package_serialization(
        response_payload.get("businessDecisionPackage")
    )
    for package_issue in package_validation.issues:
        issues.append(
            _issue(
                f"response-package-{package_issue.code}",
                f"$.businessDecisionPackage{package_issue.path[1:]}",
                "Successful response package serialization failed validation.",
            )
        )


def _validate_response_status(
    response_status: Mapping[str, Any],
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    expected_status = {
        "packageValidation": {PACKAGE_VALIDATION_VALIDATED},
        "runtimeEligibility": {RUNTIME_ELIGIBILITY_ELIGIBLE},
        "exposure": {EXPOSURE_ELIGIBLE},
        "productionAuthority": {
            PRODUCTION_AUTHORITATIVE,
            NOT_PRODUCTION_AUTHORITATIVE,
        },
    }
    for field_name, allowed_values in expected_status.items():
        if response_status.get(field_name) not in allowed_values:
            issues.append(
                _issue(
                    "invalid-response-status",
                    f"$.responseStatus.{field_name}",
                    "Successful response status contains an unsupported value.",
                )
            )

    unexpected_fields = set(response_status) - set(expected_status)
    for field_name in sorted(unexpected_fields):
        issues.append(
            _issue(
                "unexpected-response-status-field",
                f"$.responseStatus.{field_name}",
                "Successful response status contains an unexpected field.",
            )
        )


def _validate_error_payload(
    response_payload: Mapping[str, Any],
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    expected_fields = (
        "responseContractVersion",
        "error",
    )
    if (
        tuple(response_payload) != expected_fields
        and "businessDecisionPackage" not in response_payload
    ):
        issues.append(
            _issue(
                "error-root-field-order-mismatch",
                "$",
                "Error response root fields do not match contract order.",
            )
        )

    error = response_payload.get("error")
    if not isinstance(error, Mapping):
        issues.append(
            _issue(
                "invalid-error",
                "$.error",
                "Error response error field must be a mapping.",
            )
        )
        return

    error_code = error.get("code")
    if error_code not in _ERROR_CONTRACT:
        issues.append(
            _issue(
                "invalid-error-code",
                "$.error.code",
                "Error response contains an unsupported error code.",
            )
        )
        return

    expected_category, expected_message, _ = _ERROR_CONTRACT[error_code]
    if error.get("category") != expected_category:
        issues.append(
            _issue(
                "invalid-error-category",
                "$.error.category",
                "Error response category does not match the error code.",
            )
        )
    if error.get("message") != expected_message:
        issues.append(
            _issue(
                "invalid-error-message",
                "$.error.message",
                "Error response message does not match the client-safe message.",
            )
        )

    details = error.get("details")
    if not isinstance(details, list):
        issues.append(
            _issue(
                "invalid-error-details",
                "$.error.details",
                "Error details must be an array.",
            )
        )


def _error_code_for_validation_issues(
    issues: tuple[ExecutiveRuntimeValidationIssue, ...],
) -> str:
    issue_codes = {issue.code for issue in issues}
    if any(code.startswith("missing-runtime") for code in issue_codes):
        return EXECUTIVE_REQUEST_INVALID
    if "invalid-runtime-metadata" in issue_codes:
        return EXECUTIVE_REQUEST_INVALID
    if {
        "invalid-package-contract-version",
        "invalid-executive-assessment-version",
        "invalid-methodology-version",
    } & issue_codes:
        return EXECUTIVE_VERSION_INCOMPATIBLE
    if any("business-decision-package" in code for code in issue_codes):
        return EXECUTIVE_PACKAGE_INTEGRITY_FAILED
    if any(code.startswith("package-") for code in issue_codes):
        return EXECUTIVE_PACKAGE_INTEGRITY_FAILED
    return EXECUTIVE_INTERNAL_ERROR


def _validate_non_empty_string(
    value: object,
    path: str,
    code: str,
    message: str,
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    if not isinstance(value, str) or not value.strip():
        issues.append(_issue(code, path, message))


def _result(
    issues: list[ExecutiveRuntimeValidationIssue],
) -> ExecutiveRuntimeValidationResult:
    return ExecutiveRuntimeValidationResult(
        is_valid=not issues,
        issues=tuple(issues),
    )


def _issue(
    code: str,
    path: str,
    message: str,
) -> ExecutiveRuntimeValidationIssue:
    return ExecutiveRuntimeValidationIssue(
        code=code,
        path=path,
        message=message,
    )
