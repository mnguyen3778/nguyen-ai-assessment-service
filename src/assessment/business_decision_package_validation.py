from dataclasses import dataclass
from typing import Any, Mapping

from assessment.business_decision_package import (
    BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS,
    BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    BUSINESS_DECISION_PACKAGE_LIMITATIONS,
    BUSINESS_DECISION_PACKAGE_SOURCE_COMPONENTS,
    BusinessDecisionPackage,
)


ROOT_FIELD_ORDER = (
    "decisionEvaluation",
    "businessReadinessSnapshot",
    "confidenceEvaluation",
    "recommendationPriorityEvaluation",
    "executiveSummaryFoundation",
    "audit",
    "limitations",
    "versionMetadata",
)


@dataclass(frozen=True)
class BusinessDecisionPackageValidationIssue:
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
class BusinessDecisionPackageValidationResult:
    is_valid: bool
    issues: tuple[BusinessDecisionPackageValidationIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "isValid": self.is_valid,
            "issues": [issue.to_dict() for issue in self.issues],
        }


def validate_business_decision_package(
    package: object,
) -> BusinessDecisionPackageValidationResult:
    issues: list[BusinessDecisionPackageValidationIssue] = []

    if not isinstance(package, BusinessDecisionPackage):
        issues.append(
            _issue(
                "invalid-package-type",
                "$",
                "Package must be a BusinessDecisionPackage.",
            )
        )
        return _result(issues)

    _validate_required_components(package, issues)
    _validate_version_metadata(package, issues)
    _validate_audit_metadata(package, issues)
    _validate_limitations(package, issues)
    _validate_source_consistency(package, issues)

    try:
        serialized = package.to_dict()
    except (AttributeError, TypeError, ValueError) as exc:
        issues.append(
            _issue(
                "serialization-failed",
                "$",
                f"Package serialization failed: {exc}",
            )
        )
    else:
        issues.extend(
            validate_business_decision_package_serialization(
                serialized,
            ).issues
        )

    return _result(issues)


def validate_business_decision_package_serialization(
    serialized_package: object,
) -> BusinessDecisionPackageValidationResult:
    issues: list[BusinessDecisionPackageValidationIssue] = []

    if not isinstance(serialized_package, Mapping):
        issues.append(
            _issue(
                "invalid-serialization-type",
                "$",
                "Serialized package must be a mapping.",
            )
        )
        return _result(issues)

    _validate_root_field_order(serialized_package, issues)
    _validate_root_required_fields(serialized_package, issues)
    _validate_serialized_version_metadata(serialized_package, issues)
    _validate_serialized_audit(serialized_package, issues)
    _validate_serialized_limitations(serialized_package, issues)
    _validate_serialized_component_presence(serialized_package, issues)
    _validate_serialized_invariants(serialized_package, issues)

    return _result(issues)


def _validate_required_components(
    package: BusinessDecisionPackage,
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    required_components = {
        "decision_evaluation": package.decision_evaluation,
        "business_readiness_snapshot": package.business_readiness_snapshot,
        "confidence_evaluation": package.confidence_evaluation,
        "recommendation_priority_evaluation": (
            package.recommendation_priority_evaluation
        ),
        "executive_summary_foundation": package.executive_summary_foundation,
        "audit": package.audit,
        "limitations": package.limitations,
        "version_metadata": package.version_metadata,
    }

    for field_name, value in required_components.items():
        if value is None:
            issues.append(
                _issue(
                    "missing-component",
                    f"$.{field_name}",
                    f"Required package component is missing: {field_name}.",
                )
            )


def _validate_version_metadata(
    package: BusinessDecisionPackage,
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    if package.version_metadata is None:
        return

    version_metadata = package.version_metadata
    if version_metadata.contract_version != BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION:
        issues.append(
            _issue(
                "contract-version-mismatch",
                "$.version_metadata.contract_version",
                "Package contract version does not match the approved contract.",
            )
        )

    _validate_non_empty_string(
        version_metadata.assessment_version,
        "$.version_metadata.assessment_version",
        "missing-assessment-version",
        issues,
    )
    _validate_non_empty_string(
        version_metadata.methodology_version,
        "$.version_metadata.methodology_version",
        "missing-methodology-version",
        issues,
    )

    if dict(version_metadata.component_versions) != dict(
        BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS
    ):
        issues.append(
            _issue(
                "component-version-mismatch",
                "$.version_metadata.component_versions",
                "Component versions do not match the approved contract.",
            )
        )


def _validate_audit_metadata(
    package: BusinessDecisionPackage,
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    if package.audit is None:
        return

    audit = package.audit
    if audit.source_component_ids != BUSINESS_DECISION_PACKAGE_SOURCE_COMPONENTS:
        issues.append(
            _issue(
                "source-components-mismatch",
                "$.audit.source_component_ids",
                "Audit source components do not match approved package components.",
            )
        )

    if package.version_metadata is not None:
        if audit.assessment_version != package.version_metadata.assessment_version:
            issues.append(
                _issue(
                    "audit-assessment-version-mismatch",
                    "$.audit.assessment_version",
                    "Audit assessment version does not match version metadata.",
                )
            )
        if audit.methodology_version != package.version_metadata.methodology_version:
            issues.append(
                _issue(
                    "audit-methodology-version-mismatch",
                    "$.audit.methodology_version",
                    "Audit methodology version does not match version metadata.",
                )
            )


def _validate_limitations(
    package: BusinessDecisionPackage,
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    if package.limitations is None:
        return

    if package.limitations != BUSINESS_DECISION_PACKAGE_LIMITATIONS:
        issues.append(
            _issue(
                "limitations-mismatch",
                "$.limitations",
                "Package limitations do not match the approved contract.",
            )
        )

    if len(package.limitations) != len(set(package.limitations)):
        issues.append(
            _issue(
                "duplicate-limitations",
                "$.limitations",
                "Package limitations contain duplicate values.",
            )
        )


def _validate_source_consistency(
    package: BusinessDecisionPackage,
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    if (
        package.business_readiness_snapshot is None
        or package.confidence_evaluation is None
        or package.recommendation_priority_evaluation is None
        or package.executive_summary_foundation is None
    ):
        return

    assessment_versions = {
        package.business_readiness_snapshot.assessment_version,
        package.confidence_evaluation.assessment_version,
        package.recommendation_priority_evaluation.assessment_version,
        package.executive_summary_foundation.assessment_version,
    }
    if len(assessment_versions) != 1:
        issues.append(
            _issue(
                "source-assessment-version-mismatch",
                "$",
                "Source assessment versions do not match.",
            )
        )

    methodology_versions = {
        package.business_readiness_snapshot.audit.methodology_version,
        package.confidence_evaluation.methodology_version,
        package.recommendation_priority_evaluation.methodology_version,
        package.executive_summary_foundation.methodology_version,
    }
    if len(methodology_versions) != 1:
        issues.append(
            _issue(
                "source-methodology-version-mismatch",
                "$",
                "Source methodology versions do not match.",
            )
        )

    if package.decision_evaluation is None:
        return

    snapshot = package.business_readiness_snapshot
    if package.decision_evaluation.overall_score != snapshot.overall_readiness.score:
        issues.append(
            _issue(
                "decision-snapshot-score-mismatch",
                "$.business_readiness_snapshot.overall_readiness.score",
                "Snapshot readiness score does not match decision evaluation.",
            )
        )
    if package.decision_evaluation.question_count != snapshot.audit.question_count:
        issues.append(
            _issue(
                "decision-snapshot-question-count-mismatch",
                "$.business_readiness_snapshot.audit.question_count",
                "Snapshot question count does not match decision evaluation.",
            )
        )
    if package.decision_evaluation.total_weight != snapshot.audit.total_weight:
        issues.append(
            _issue(
                "decision-snapshot-total-weight-mismatch",
                "$.business_readiness_snapshot.audit.total_weight",
                "Snapshot total weight does not match decision evaluation.",
            )
        )

    evaluated_dimensions = tuple(sorted(package.decision_evaluation.dimensions))
    if evaluated_dimensions != snapshot.audit.evaluated_dimensions:
        issues.append(
            _issue(
                "decision-snapshot-dimension-mismatch",
                "$.business_readiness_snapshot.audit.evaluated_dimensions",
                "Snapshot evaluated dimensions do not match decision evaluation.",
            )
        )


def _validate_root_field_order(
    serialized_package: Mapping[str, Any],
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    observed_fields = tuple(serialized_package)
    if observed_fields != ROOT_FIELD_ORDER:
        issues.append(
            _issue(
                "root-field-order-mismatch",
                "$",
                "Serialized root fields do not match contract order.",
            )
        )


def _validate_root_required_fields(
    serialized_package: Mapping[str, Any],
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    observed_fields = set(serialized_package)
    expected_fields = set(ROOT_FIELD_ORDER)

    for missing_field in sorted(expected_fields - observed_fields):
        issues.append(
            _issue(
                "missing-serialized-field",
                f"$.{missing_field}",
                f"Serialized package is missing required field: {missing_field}.",
            )
        )

    for unexpected_field in sorted(observed_fields - expected_fields):
        issues.append(
            _issue(
                "unexpected-serialized-field",
                f"$.{unexpected_field}",
                f"Serialized package contains unexpected field: {unexpected_field}.",
            )
        )


def _validate_serialized_version_metadata(
    serialized_package: Mapping[str, Any],
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    metadata = serialized_package.get("versionMetadata")
    if not isinstance(metadata, Mapping):
        issues.append(
            _issue(
                "invalid-version-metadata",
                "$.versionMetadata",
                "Version metadata must be a mapping.",
            )
        )
        return

    _validate_required_serialized_keys(
        metadata,
        (
            "contractVersion",
            "assessmentVersion",
            "methodologyVersion",
            "componentVersions",
        ),
        "$.versionMetadata",
        issues,
    )

    if metadata.get("contractVersion") != BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION:
        issues.append(
            _issue(
                "serialized-contract-version-mismatch",
                "$.versionMetadata.contractVersion",
                "Serialized contract version does not match approved contract.",
            )
        )

    component_versions = metadata.get("componentVersions")
    if not isinstance(component_versions, Mapping):
        issues.append(
            _issue(
                "invalid-component-versions",
                "$.versionMetadata.componentVersions",
                "Serialized component versions must be a mapping.",
            )
        )
        return

    if dict(component_versions) != dict(BUSINESS_DECISION_PACKAGE_COMPONENT_VERSIONS):
        issues.append(
            _issue(
                "serialized-component-version-mismatch",
                "$.versionMetadata.componentVersions",
                "Serialized component versions do not match approved contract.",
            )
        )


def _validate_serialized_audit(
    serialized_package: Mapping[str, Any],
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    audit = serialized_package.get("audit")
    if not isinstance(audit, Mapping):
        issues.append(
            _issue(
                "invalid-audit",
                "$.audit",
                "Package audit must be a mapping.",
            )
        )
        return

    _validate_required_serialized_keys(
        audit,
        (
            "assessmentVersion",
            "methodologyVersion",
            "sourceComponentIds",
            "evaluatedDimensions",
            "questionCount",
            "totalWeight",
        ),
        "$.audit",
        issues,
    )

    if tuple(audit.get("sourceComponentIds", ())) != (
        BUSINESS_DECISION_PACKAGE_SOURCE_COMPONENTS
    ):
        issues.append(
            _issue(
                "serialized-source-components-mismatch",
                "$.audit.sourceComponentIds",
                "Serialized audit source components do not match approved contract.",
            )
        )


def _validate_serialized_limitations(
    serialized_package: Mapping[str, Any],
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    limitations = serialized_package.get("limitations")
    if not isinstance(limitations, list):
        issues.append(
            _issue(
                "invalid-limitations",
                "$.limitations",
                "Serialized limitations must be an array.",
            )
        )
        return

    if tuple(limitations) != BUSINESS_DECISION_PACKAGE_LIMITATIONS:
        issues.append(
            _issue(
                "serialized-limitations-mismatch",
                "$.limitations",
                "Serialized limitations do not match approved contract.",
            )
        )

    if len(limitations) != len(set(limitations)):
        issues.append(
            _issue(
                "serialized-duplicate-limitations",
                "$.limitations",
                "Serialized limitations contain duplicate values.",
            )
        )


def _validate_serialized_component_presence(
    serialized_package: Mapping[str, Any],
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    component_fields = (
        "decisionEvaluation",
        "businessReadinessSnapshot",
        "confidenceEvaluation",
        "recommendationPriorityEvaluation",
        "executiveSummaryFoundation",
    )
    for field_name in component_fields:
        if serialized_package.get(field_name) is None:
            issues.append(
                _issue(
                    "missing-serialized-component",
                    f"$.{field_name}",
                    f"Serialized component is missing: {field_name}.",
                )
            )


def _validate_serialized_invariants(
    serialized_package: Mapping[str, Any],
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    version_metadata = serialized_package.get("versionMetadata")
    audit = serialized_package.get("audit")
    decision_evaluation = serialized_package.get("decisionEvaluation")
    snapshot = serialized_package.get("businessReadinessSnapshot")

    if isinstance(version_metadata, Mapping) and isinstance(audit, Mapping):
        if audit.get("assessmentVersion") != version_metadata.get(
            "assessmentVersion"
        ):
            issues.append(
                _issue(
                    "serialized-audit-assessment-version-mismatch",
                    "$.audit.assessmentVersion",
                    "Serialized audit assessment version does not match metadata.",
                )
            )
        if audit.get("methodologyVersion") != version_metadata.get(
            "methodologyVersion"
        ):
            issues.append(
                _issue(
                    "serialized-audit-methodology-version-mismatch",
                    "$.audit.methodologyVersion",
                    "Serialized audit methodology version does not match metadata.",
                )
            )

    if isinstance(decision_evaluation, Mapping) and isinstance(snapshot, Mapping):
        overall_readiness = snapshot.get("overallReadiness")
        snapshot_audit = snapshot.get("audit")
        if isinstance(overall_readiness, Mapping):
            if overall_readiness.get("score") != decision_evaluation.get(
                "overallScore"
            ):
                issues.append(
                    _issue(
                        "serialized-decision-snapshot-score-mismatch",
                        "$.businessReadinessSnapshot.overallReadiness.score",
                        "Serialized snapshot score does not match decision score.",
                    )
                )
        if isinstance(snapshot_audit, Mapping):
            if snapshot_audit.get("questionCount") != decision_evaluation.get(
                "questionCount"
            ):
                issues.append(
                    _issue(
                        "serialized-decision-snapshot-question-count-mismatch",
                        "$.businessReadinessSnapshot.audit.questionCount",
                        "Serialized snapshot question count does not match decision.",
                    )
                )
            if snapshot_audit.get("totalWeight") != decision_evaluation.get(
                "totalWeight"
            ):
                issues.append(
                    _issue(
                        "serialized-decision-snapshot-total-weight-mismatch",
                        "$.businessReadinessSnapshot.audit.totalWeight",
                        "Serialized snapshot total weight does not match decision.",
                    )
                )


def _validate_required_serialized_keys(
    serialized_value: Mapping[str, Any],
    required_keys: tuple[str, ...],
    path: str,
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    for key in required_keys:
        if key not in serialized_value:
            issues.append(
                _issue(
                    "missing-serialized-field",
                    f"{path}.{key}",
                    f"Serialized object is missing required field: {key}.",
                )
            )


def _validate_non_empty_string(
    value: object,
    path: str,
    code: str,
    issues: list[BusinessDecisionPackageValidationIssue],
) -> None:
    if not isinstance(value, str) or not value.strip():
        issues.append(
            _issue(
                code,
                path,
                "Version value must be a non-empty string.",
            )
        )


def _issue(
    code: str,
    path: str,
    message: str,
) -> BusinessDecisionPackageValidationIssue:
    return BusinessDecisionPackageValidationIssue(
        code=code,
        path=path,
        message=message,
    )


def _result(
    issues: list[BusinessDecisionPackageValidationIssue],
) -> BusinessDecisionPackageValidationResult:
    return BusinessDecisionPackageValidationResult(
        is_valid=not issues,
        issues=tuple(issues),
    )
