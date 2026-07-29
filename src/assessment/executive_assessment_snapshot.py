from dataclasses import dataclass

from assessment.business_decision_package import BusinessDecisionPackage
from assessment.executive_runtime import (
    ExecutiveRuntimeResponseStatus,
    ExecutiveRuntimeResult,
)


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


def create_executive_assessment_snapshot(
    executive_runtime_result: object,
) -> ExecutiveAssessmentSnapshot:
    return ExecutiveAssessmentSnapshot(executive_runtime_result)

