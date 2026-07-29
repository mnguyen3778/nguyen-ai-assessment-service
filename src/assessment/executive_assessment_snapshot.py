from dataclasses import dataclass
from typing import Any, Mapping

from assessment.business_decision_package import (
    BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS,
    BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BusinessDecisionPackage,
)
from assessment.business_decision_package_validation import (
    validate_business_decision_package,
    validate_business_decision_package_serialization,
)
from assessment.executive_runtime import (
    EXECUTIVE_ASSESSMENT_VERSION,
    EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION,
    EXPOSURE_ELIGIBLE,
    NOT_PRODUCTION_AUTHORITATIVE,
    PACKAGE_VALIDATION_VALIDATED,
    PRODUCTION_AUTHORITATIVE,
    RUNTIME_ELIGIBILITY_ELIGIBLE,
    ExecutiveRuntimeResponseStatus,
    ExecutiveRuntimeResult,
    ExecutiveRuntimeValidationIssue,
    ExecutiveRuntimeValidationResult,
)
from assessment.methodology_config import METHODOLOGY_VERSION


_SNAPSHOT_FIELDS = (
    "business_decision_package",
    "response_status",
    "response_contract_version",
)
_SERIALIZED_SNAPSHOT_FIELD_ORDER = (
    "responseContractVersion",
    "responseStatus",
    "businessDecisionPackage",
)
_SERIALIZED_RESPONSE_STATUS_FIELD_ORDER = (
    "packageValidation",
    "runtimeEligibility",
    "exposure",
    "productionAuthority",
)
_RUNTIME_METADATA_FIELDS = {
    "runtime_metadata",
    "request_id",
    "correlation_id",
    "trace_id",
    "invocation_id",
    "processing_timestamp",
    "api_route",
    "http_status",
    "lambda_context",
    "deployment_identifier",
}
_ERROR_RESPONSE_FIELDS = {
    "error",
    "error_response",
    "runtime_error",
}
_PUBLIC_RESPONSE_FIELDS = {
    "assessment_response",
    "public_assessment_response",
}


@dataclass(frozen=True, init=False)
class ExecutiveAssessmentSnapshot:
    business_decision_package: BusinessDecisionPackage
    response_status: ExecutiveRuntimeResponseStatus
    response_contract_version: str

    def __init__(self, executive_runtime_result: object) -> None:
        if not isinstance(executive_runtime_result, ExecutiveRuntimeResult):
            raise ValueError(
                "ExecutiveAssessmentSnapshot requires an ExecutiveRuntimeResult."
            )
        if (
            not executive_runtime_result.is_success
            or executive_runtime_result.success is None
        ):
            raise ValueError(
                "ExecutiveAssessmentSnapshot requires a successful "
                "ExecutiveRuntimeResult."
            )

        success = executive_runtime_result.success
        object.__setattr__(
            self,
            "business_decision_package",
            success.business_decision_package,
        )
        object.__setattr__(self, "response_status", success.response_status)
        object.__setattr__(
            self,
            "response_contract_version",
            success.response_contract_version,
        )
        validation_result = validate_executive_assessment_snapshot(self)
        if not validation_result.is_valid:
            issue_codes = ", ".join(
                issue.code for issue in validation_result.issues
            )
            raise ValueError(
                "ExecutiveAssessmentSnapshot validation failed: "
                f"{issue_codes}."
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "responseContractVersion": self.response_contract_version,
            "responseStatus": self.response_status.to_dict(),
            "businessDecisionPackage": self.business_decision_package.to_dict(),
        }


def create_executive_assessment_snapshot(
    executive_runtime_result: object,
) -> ExecutiveAssessmentSnapshot:
    return ExecutiveAssessmentSnapshot(executive_runtime_result)


def validate_executive_assessment_snapshot(
    snapshot: object,
) -> ExecutiveRuntimeValidationResult:
    issues: list[ExecutiveRuntimeValidationIssue] = []

    if not isinstance(snapshot, ExecutiveAssessmentSnapshot):
        issues.append(
            _issue(
                "invalid-snapshot-type",
                "$",
                "Snapshot must be an ExecutiveAssessmentSnapshot.",
            )
        )
        return _result(issues)

    _validate_snapshot_fields(snapshot, issues)
    _validate_snapshot_package(snapshot, issues)
    _validate_snapshot_response_status(snapshot, issues)
    _validate_snapshot_response_contract_version(snapshot, issues)

    return _result(issues)


def validate_executive_assessment_snapshot_serialization(
    serialized_snapshot: object,
) -> ExecutiveRuntimeValidationResult:
    issues: list[ExecutiveRuntimeValidationIssue] = []

    if not isinstance(serialized_snapshot, Mapping):
        issues.append(
            _issue(
                "invalid-snapshot-serialization-type",
                "$",
                "Serialized snapshot must be a mapping.",
            )
        )
        return _result(issues)

    _validate_serialized_snapshot_root(serialized_snapshot, issues)
    _validate_serialized_snapshot_response_contract_version(
        serialized_snapshot,
        issues,
    )
    _validate_serialized_snapshot_response_status(serialized_snapshot, issues)
    _validate_serialized_snapshot_package(serialized_snapshot, issues)

    return _result(issues)


def _validate_snapshot_fields(
    snapshot: ExecutiveAssessmentSnapshot,
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    snapshot_fields = tuple(snapshot.__dict__)

    for field_name in _SNAPSHOT_FIELDS:
        if field_name not in snapshot.__dict__:
            issues.append(
                _issue(
                    "missing-snapshot-field",
                    f"$.{field_name}",
                    f"Required snapshot field is missing: {field_name}.",
                )
            )

    for field_name in snapshot_fields:
        if field_name in _SNAPSHOT_FIELDS:
            continue
        if field_name in _RUNTIME_METADATA_FIELDS:
            issues.append(
                _issue(
                    "runtime-metadata-in-snapshot",
                    f"$.{field_name}",
                    "Runtime metadata must not be embedded in snapshot state.",
                )
            )
        elif field_name in _ERROR_RESPONSE_FIELDS:
            issues.append(
                _issue(
                    "error-response-in-snapshot",
                    f"$.{field_name}",
                    "Runtime error response data must not be embedded in snapshot state.",
                )
            )
        elif field_name in _PUBLIC_RESPONSE_FIELDS:
            issues.append(
                _issue(
                    "public-assessment-response-in-snapshot",
                    f"$.{field_name}",
                    "Public assessment response data must not be embedded in executive snapshot state.",
                )
            )
        else:
            issues.append(
                _issue(
                    "unexpected-snapshot-field",
                    f"$.{field_name}",
                    "Snapshot contains an unapproved field.",
                )
            )


def _validate_snapshot_package(
    snapshot: ExecutiveAssessmentSnapshot,
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    package = getattr(snapshot, "business_decision_package", None)
    if package is None:
        issues.append(
            _issue(
                "missing-business-decision-package",
                "$.business_decision_package",
                "ExecutiveAssessmentSnapshot must contain a BusinessDecisionPackage.",
            )
        )
        return

    if not isinstance(package, BusinessDecisionPackage):
        issues.append(
            _issue(
                "invalid-business-decision-package",
                "$.business_decision_package",
                "Snapshot business decision package must be a BusinessDecisionPackage.",
            )
        )
        return

    package_validation = validate_business_decision_package(package)
    for package_issue in package_validation.issues:
        issues.append(
            _issue(
                f"package-{package_issue.code}",
                f"$.business_decision_package{package_issue.path[1:]}",
                "Snapshot BusinessDecisionPackage validation failed.",
            )
        )
    _validate_snapshot_package_version_compatibility(package, issues)


def _validate_snapshot_package_version_compatibility(
    package: BusinessDecisionPackage,
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    version_metadata = package.version_metadata
    if version_metadata is None:
        issues.append(
            _issue(
                "missing-package-version-metadata",
                "$.business_decision_package.version_metadata",
                "Snapshot BusinessDecisionPackage version metadata is required.",
            )
        )
        return

    if version_metadata.contract_version != BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION:
        issues.append(
            _issue(
                "invalid-package-contract-version",
                "$.business_decision_package.version_metadata.contract_version",
                "Snapshot package contract version is not supported.",
            )
        )
    if version_metadata.assessment_version != EXECUTIVE_ASSESSMENT_VERSION:
        issues.append(
            _issue(
                "invalid-executive-assessment-version",
                "$.business_decision_package.version_metadata.assessment_version",
                "Snapshot assessment version is not supported.",
            )
        )
    if version_metadata.methodology_version != METHODOLOGY_VERSION:
        issues.append(
            _issue(
                "invalid-methodology-version",
                "$.business_decision_package.version_metadata.methodology_version",
                "Snapshot methodology version is not supported.",
            )
        )
    if dict(version_metadata.component_versions) != dict(
        BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS
    ):
        issues.append(
            _issue(
                "invalid-component-versions",
                "$.business_decision_package.version_metadata.component_versions",
                "Snapshot component versions are not supported.",
            )
        )


def _validate_snapshot_response_status(
    snapshot: ExecutiveAssessmentSnapshot,
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    response_status = getattr(snapshot, "response_status", None)
    if response_status is None:
        issues.append(
            _issue(
                "missing-response-status",
                "$.response_status",
                "ExecutiveAssessmentSnapshot must preserve runtime response status.",
            )
        )
        return

    if not isinstance(response_status, ExecutiveRuntimeResponseStatus):
        issues.append(
            _issue(
                "invalid-response-status",
                "$.response_status",
                "Snapshot response status must be ExecutiveRuntimeResponseStatus.",
            )
        )
        return

    expected_status = {
        "package_validation": {PACKAGE_VALIDATION_VALIDATED},
        "runtime_eligibility": {RUNTIME_ELIGIBILITY_ELIGIBLE},
        "exposure": {EXPOSURE_ELIGIBLE},
        "production_authority": {
            PRODUCTION_AUTHORITATIVE,
            NOT_PRODUCTION_AUTHORITATIVE,
        },
    }
    for field_name, allowed_values in expected_status.items():
        if getattr(response_status, field_name, None) not in allowed_values:
            issues.append(
                _issue(
                    "invalid-response-status",
                    f"$.response_status.{field_name}",
                    "Snapshot response status contains an unsupported value.",
                )
            )


def _validate_snapshot_response_contract_version(
    snapshot: ExecutiveAssessmentSnapshot,
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    response_contract_version = getattr(
        snapshot,
        "response_contract_version",
        None,
    )
    if response_contract_version != EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION:
        issues.append(
            _issue(
                "invalid-response-contract-version",
                "$.response_contract_version",
                "Snapshot response contract version is not supported.",
            )
        )


def _validate_serialized_snapshot_root(
    serialized_snapshot: Mapping[str, Any],
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    observed_fields = tuple(serialized_snapshot)
    if observed_fields != _SERIALIZED_SNAPSHOT_FIELD_ORDER:
        issues.append(
            _issue(
                "snapshot-serialization-field-order-mismatch",
                "$",
                "Serialized snapshot root fields do not match contract order.",
            )
        )

    observed_field_set = set(serialized_snapshot)
    expected_field_set = set(_SERIALIZED_SNAPSHOT_FIELD_ORDER)
    for field_name in sorted(expected_field_set - observed_field_set):
        issues.append(
            _issue(
                "missing-serialized-snapshot-field",
                f"$.{field_name}",
                f"Serialized snapshot is missing required field: {field_name}.",
            )
        )
    for field_name in sorted(observed_field_set - expected_field_set):
        issues.append(
            _issue(
                "unexpected-serialized-snapshot-field",
                f"$.{field_name}",
                f"Serialized snapshot contains unexpected field: {field_name}.",
            )
        )


def _validate_serialized_snapshot_response_contract_version(
    serialized_snapshot: Mapping[str, Any],
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    if (
        serialized_snapshot.get("responseContractVersion")
        != EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION
    ):
        issues.append(
            _issue(
                "invalid-response-contract-version",
                "$.responseContractVersion",
                "Serialized snapshot response contract version is not supported.",
            )
        )


def _validate_serialized_snapshot_response_status(
    serialized_snapshot: Mapping[str, Any],
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    response_status = serialized_snapshot.get("responseStatus")
    if not isinstance(response_status, Mapping):
        issues.append(
            _issue(
                "invalid-response-status",
                "$.responseStatus",
                "Serialized snapshot response status must be a mapping.",
            )
        )
        return

    observed_fields = tuple(response_status)
    if observed_fields != _SERIALIZED_RESPONSE_STATUS_FIELD_ORDER:
        issues.append(
            _issue(
                "response-status-field-order-mismatch",
                "$.responseStatus",
                "Serialized response status fields do not match contract order.",
            )
        )

    observed_field_set = set(response_status)
    expected_field_set = set(_SERIALIZED_RESPONSE_STATUS_FIELD_ORDER)
    for field_name in sorted(expected_field_set - observed_field_set):
        issues.append(
            _issue(
                "missing-response-status-field",
                f"$.responseStatus.{field_name}",
                f"Serialized response status is missing required field: {field_name}.",
            )
        )
    for field_name in sorted(observed_field_set - expected_field_set):
        issues.append(
            _issue(
                "unexpected-response-status-field",
                f"$.responseStatus.{field_name}",
                f"Serialized response status contains unexpected field: {field_name}.",
            )
        )

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
                    "Serialized response status contains an unsupported value.",
                )
            )


def _validate_serialized_snapshot_package(
    serialized_snapshot: Mapping[str, Any],
    issues: list[ExecutiveRuntimeValidationIssue],
) -> None:
    package_validation = validate_business_decision_package_serialization(
        serialized_snapshot.get("businessDecisionPackage")
    )
    for package_issue in package_validation.issues:
        issues.append(
            _issue(
                f"package-{package_issue.code}",
                f"$.businessDecisionPackage{package_issue.path[1:]}",
                "Serialized snapshot BusinessDecisionPackage validation failed.",
            )
        )


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
