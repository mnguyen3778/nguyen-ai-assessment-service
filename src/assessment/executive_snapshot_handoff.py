from dataclasses import dataclass
import json
from typing import Any, Mapping

from assessment.business_decision_package import (
    ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
)
from assessment.executive_assessment_snapshot import (
    ExecutiveAssessmentSnapshot,
    validate_executive_assessment_snapshot_serialization,
)
from assessment.executive_orchestration import (
    ExecutiveOrchestrationFailure,
    ValidatedCanonicalExecutiveAssessmentInput,
    orchestrate_executive_assessment,
)
from assessment.executive_runtime import (
    NOT_PRODUCTION_AUTHORITATIVE,
    ExecutiveRuntime,
    ExecutiveRuntimeMetadata,
)
from assessment.governed_assessment_input import ValidatedCanonicalExecutiveAssessmentInputV2
from assessment.producer_snapshot_attestation import (
    AttestationError,
    ProducerSnapshotIssuer,
    ProducerSnapshotVerifier,
)


INPUT_CONTRACT_FAILURE = "INPUT_CONTRACT_FAILURE"
ORCHESTRATION_FAILURE = "ORCHESTRATION_FAILURE"
RUNTIME_FAILURE = "RUNTIME_FAILURE"
SNAPSHOT_CREATION_FAILURE = "SNAPSHOT_CREATION_FAILURE"
SNAPSHOT_SERIALIZATION_FAILURE = "SNAPSHOT_SERIALIZATION_FAILURE"
SNAPSHOT_SERIALIZATION_VALIDATION_FAILURE = (
    "SNAPSHOT_SERIALIZATION_VALIDATION_FAILURE"
)
ATTESTATION_FAILURE = "ATTESTATION_FAILURE"
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
    attestation_sidecar: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        if (self.serialized_snapshot is None) == (self.failure is None):
            raise ValueError(
                "Executive snapshot production result must contain exactly one outcome."
            )
        if self.attestation_sidecar is not None and self.serialized_snapshot is None:
            raise ValueError("Attestation requires a successful snapshot.")

    @property
    def is_success(self) -> bool:
        return self.serialized_snapshot is not None


def produce_executive_assessment_snapshot(
    canonical_input: object,
    *,
    local_package_contract_version: str | None = None,
    local_v3_issuer: ProducerSnapshotIssuer | None = None,
    local_v3_verifier: ProducerSnapshotVerifier | None = None,
) -> ExecutiveSnapshotProductionResult:
    selected_v3 = (
        type(local_package_contract_version) is str
        and local_package_contract_version
            == ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION
    )
    if (
        local_package_contract_version is not None
        and (type(local_package_contract_version) is not str
             or local_package_contract_version not in (
                 GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
                 ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
             ))
    ):
        return ExecutiveSnapshotProductionResult(failure=_failure(
            INPUT_CONTRACT_FAILURE, "unsupported-package-contract-version",
            "version-binding", "Snapshot package version is not supported.",
        ))
    if (
        selected_v3
        and (not isinstance(canonical_input, ValidatedCanonicalExecutiveAssessmentInputV2)
             or type(local_v3_issuer) is not ProducerSnapshotIssuer
             or type(local_v3_verifier) is not ProducerSnapshotVerifier)
    ) or (
        not selected_v3
        and (local_v3_issuer is not None or local_v3_verifier is not None
             or (local_package_contract_version is not None
                 and not isinstance(canonical_input, ValidatedCanonicalExecutiveAssessmentInputV2)))
    ):
        return ExecutiveSnapshotProductionResult(failure=_failure(
            INPUT_CONTRACT_FAILURE, "invalid-local-v3-selection",
            "version-binding", "Local v3 handoff requires governed input and trusted attestation components.",
        ))
    if not isinstance(canonical_input, (ValidatedCanonicalExecutiveAssessmentInput,
                                        ValidatedCanonicalExecutiveAssessmentInputV2)):
        return ExecutiveSnapshotProductionResult(
            failure=_failure(
                INPUT_CONTRACT_FAILURE,
                "invalid-canonical-input",
                "input",
                "Snapshot production requires validated canonical executive input.",
            )
        )

    try:
        orchestration_result = orchestrate_executive_assessment(
            canonical_input,
            **({"governed_package_contract_version": local_package_contract_version}
               if selected_v3 else {}),
        )
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
            **({"local_package_contract_version": local_package_contract_version}
               if selected_v3 else {}),
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

    if (
        selected_v3
        and runtime_result.success.response_status.production_authority
        != NOT_PRODUCTION_AUTHORITATIVE
    ):
        return ExecutiveSnapshotProductionResult(failure=_failure(
            RUNTIME_FAILURE, "v3-production-authority-not-supported",
            "runtime", "Local v3 handoff cannot be production authoritative.",
        ))

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

    if selected_v3:
        try:
            snapshot_bytes = json.dumps(
                serialized_snapshot, ensure_ascii=False,
                separators=(",", ":"), allow_nan=False,
            ).encode("utf-8", "strict")
            sidecar = local_v3_issuer.issue(snapshot_bytes)
            local_v3_verifier.verify(snapshot_bytes, sidecar)
        except (AttestationError, TypeError, ValueError, UnicodeError):
            return ExecutiveSnapshotProductionResult(failure=_failure(
                ATTESTATION_FAILURE, "local-v3-attestation-failed",
                "attestation", "Local v3 snapshot attestation failed.",
            ))
        except Exception:
            return ExecutiveSnapshotProductionResult(failure=_failure(
                UNEXPECTED_INTERNAL_FAILURE, "unexpected-local-v3-attestation-failure",
                "attestation", "Unexpected local v3 attestation failure.",
            ))
        return ExecutiveSnapshotProductionResult(
            serialized_snapshot=serialized_snapshot,
            attestation_sidecar=sidecar,
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
