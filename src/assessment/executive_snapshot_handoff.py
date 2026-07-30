from dataclasses import dataclass
from typing import Any, Mapping

from assessment.executive_assessment_snapshot import (
    ExecutiveAssessmentSnapshot,
    validate_executive_assessment_snapshot_serialization,
)
from assessment.executive_orchestration import (
    ExecutiveOrchestrationFailure,
    ValidatedCanonicalExecutiveAssessmentInput,
    orchestrate_executive_assessment,
)
from assessment.executive_runtime import ExecutiveRuntime, ExecutiveRuntimeMetadata


INPUT_CONTRACT_FAILURE = "INPUT_CONTRACT_FAILURE"
ORCHESTRATION_FAILURE = "ORCHESTRATION_FAILURE"
RUNTIME_FAILURE = "RUNTIME_FAILURE"
SNAPSHOT_CREATION_FAILURE = "SNAPSHOT_CREATION_FAILURE"
SNAPSHOT_SERIALIZATION_FAILURE = "SNAPSHOT_SERIALIZATION_FAILURE"
SNAPSHOT_SERIALIZATION_VALIDATION_FAILURE = (
    "SNAPSHOT_SERIALIZATION_VALIDATION_FAILURE"
)
UNEXPECTED_INTERNAL_FAILURE = "UNEXPECTED_INTERNAL_FAILURE"

_HANDOFF_RUNTIME_METADATA = ExecutiveRuntimeMetadata(
    request_id="internal-snapshot-production-handoff",
    correlation_id="internal-snapshot-production-handoff",
)


@dataclass(frozen=True)
class ExecutiveSnapshotProductionFailure:
    category: str
    code: str
    stage: str
    message: str
    orchestration_failure: ExecutiveOrchestrationFailure | None = None


@dataclass(frozen=True)
class ExecutiveSnapshotProductionResult:
    serialized_snapshot: Mapping[str, Any] | None = None
    failure: ExecutiveSnapshotProductionFailure | None = None

    def __post_init__(self) -> None:
        if (self.serialized_snapshot is None) == (self.failure is None):
            raise ValueError(
                "Executive snapshot production result must contain exactly one outcome."
            )

    @property
    def is_success(self) -> bool:
        return self.serialized_snapshot is not None


def produce_executive_assessment_snapshot(
    canonical_input: object,
) -> ExecutiveSnapshotProductionResult:
    if not isinstance(canonical_input, ValidatedCanonicalExecutiveAssessmentInput):
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                INPUT_CONTRACT_FAILURE,
                "invalid-canonical-input",
                "input",
                "Snapshot production requires validated canonical executive input.",
            )
        )

    try:
        orchestration_result = orchestrate_executive_assessment(canonical_input)
    except Exception:
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                UNEXPECTED_INTERNAL_FAILURE,
                "unexpected-orchestration-failure",
                "orchestration",
                "Unexpected internal orchestration failure.",
            )
        )

    if not orchestration_result.is_success:
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                ORCHESTRATION_FAILURE,
                "orchestration-failed",
                "orchestration",
                "Executive orchestration failed.",
                orchestration_failure=orchestration_result.failure,
            )
        )

    try:
        runtime_result = ExecutiveRuntime().execute(
            orchestration_result.business_decision_package,
            _HANDOFF_RUNTIME_METADATA,
        )
    except Exception:
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                UNEXPECTED_INTERNAL_FAILURE,
                "unexpected-runtime-failure",
                "runtime",
                "Unexpected executive runtime failure.",
            )
        )

    if not runtime_result.is_success:
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                RUNTIME_FAILURE,
                "runtime-failed",
                "runtime",
                "Executive runtime failed.",
            )
        )

    try:
        snapshot = ExecutiveAssessmentSnapshot(runtime_result)
    except (TypeError, ValueError, AttributeError) as exc:
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                SNAPSHOT_CREATION_FAILURE,
                "snapshot-creation-failed",
                "snapshot-creation",
                str(exc),
            )
        )
    except Exception:
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                UNEXPECTED_INTERNAL_FAILURE,
                "unexpected-snapshot-creation-failure",
                "snapshot-creation",
                "Unexpected executive snapshot creation failure.",
            )
        )

    try:
        serialized_snapshot = snapshot.to_dict()
    except (TypeError, ValueError, AttributeError) as exc:
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                SNAPSHOT_SERIALIZATION_FAILURE,
                "snapshot-serialization-failed",
                "snapshot-serialization",
                str(exc),
            )
        )
    except Exception:
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                UNEXPECTED_INTERNAL_FAILURE,
                "unexpected-snapshot-serialization-failure",
                "snapshot-serialization",
                "Unexpected executive snapshot serialization failure.",
            )
        )

    try:
        validation_result = validate_executive_assessment_snapshot_serialization(
            serialized_snapshot
        )
    except Exception:
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                UNEXPECTED_INTERNAL_FAILURE,
                "unexpected-snapshot-serialization-validation-failure",
                "snapshot-serialization-validation",
                "Unexpected serialized snapshot validation failure.",
            )
        )

    if not validation_result.is_valid:
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                SNAPSHOT_SERIALIZATION_VALIDATION_FAILURE,
                "snapshot-serialization-validation-failed",
                "snapshot-serialization-validation",
                "Serialized ExecutiveAssessmentSnapshot validation failed.",
            )
        )

    return ExecutiveSnapshotProductionResult(
        serialized_snapshot=serialized_snapshot,
    )


def _failure(
    category: str,
    code: str,
    stage: str,
    message: str,
    *,
    orchestration_failure: ExecutiveOrchestrationFailure | None = None,
) -> ExecutiveSnapshotProductionFailure:
    return ExecutiveSnapshotProductionFailure(
        category=category,
        code=code,
        stage=stage,
        message=message,
        orchestration_failure=orchestration_failure,
    )
