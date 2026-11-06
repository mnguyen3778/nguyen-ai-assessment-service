"""Isolated synthetic assertion validation; no runtime or priority integration."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


ASSERTION_CONTRACT_VERSION = "local-synthetic-priority-assertion-v1"
AUTHORITY_PROFILE_VERSION = "local-synthetic-priority-authority-v1"
APPLICABILITY_RULE_VERSION = "local-synthetic-applicability-v1"
RECOMMENDATION_TABLE_VERSION = "recommendation-decision-table-set-v1"
VALID_EVALUATED = "VALID_EVALUATED"
VALID_NOT_APPLICABLE = "VALID_NOT_APPLICABLE"
BLOCKED_PENDING_DATA = "BLOCKED_PENDING_DATA"
INVALID = "INVALID"

DRIVER_VALUES = MappingProxyType({
    "customer-impact": frozenset(("impact-present", "impact-affirmed-absent")),
    "executive-urgency": frozenset((
        "time-bound-executive-action", "executive-action-required",
        "executive-action-affirmed-absent",
    )),
    "dependency-role": frozenset((
        "blocks-related-work", "unlocks-related-work", "no-dependency-affirmed",
    )),
})
RELATION_VALUES = frozenset(("blocks-related-work", "unlocks-related-work"))
ABSENCE_VALUES = frozenset((
    "impact-affirmed-absent", "executive-action-affirmed-absent",
    "no-dependency-affirmed",
))
AUTHORITY_BY_DRIVER = MappingProxyType({
    "customer-impact": "synthetic-issuer-customer",
    "executive-urgency": "synthetic-issuer-executive",
    "dependency-role": "synthetic-issuer-dependency",
})
FIELDS = frozenset((
    "assertionId", "assessmentSnapshotIdentity", "assessmentIdentity",
    "recommendationInstanceIdentity", "findingId",
    "recommendationDecisionIdentifier", "recommendationDecisionTableVersion",
    "driverId", "assertedValue", "applicabilityStatus",
    "applicabilityRuleId", "applicabilityRuleVersion",
    "evidenceReferences", "businessAuthorityReference", "sourceRevision",
    "currentnessReference", "assertionContractVersion", "targetReference",
    "timingBasisReference",
))
MAX_TEXT = 128
MAX_ASSERTIONS = 32
MAX_EVIDENCE_REFERENCES = 8


@dataclass(frozen=True)
class RecommendationInstance:
    instance_identity: str
    finding_id: str | None
    decision_identifier: str
    decision_table_version: str = RECOMMENDATION_TABLE_VERSION


@dataclass(frozen=True)
class SyntheticEvidence:
    reference: str
    driver_id: str
    supported_value: str
    instance_identity: str
    scope_confirmed: bool = False
    timing_basis_reference: str | None = None
    target_reference: str | None = None


@dataclass(frozen=True)
class SyntheticContext:
    snapshot_identity: str
    assessment_identity: str
    recommendations: tuple[RecommendationInstance, ...]
    evidence: Mapping[str, SyntheticEvidence]
    current_revisions: Mapping[str, str]


@dataclass(frozen=True)
class SyntheticAuthorityProfile:
    version: str
    issuer_by_driver: Mapping[str, str]


LOCAL_AUTHORITY_PROFILE = SyntheticAuthorityProfile(
    AUTHORITY_PROFILE_VERSION, AUTHORITY_BY_DRIVER,
)


@dataclass(frozen=True)
class AssertionOutcome:
    status: str
    reason: str
    assertion_id: str | None = None
    driver_id: str | None = None
    recommendation_instance_identity: str | None = None


@dataclass(frozen=True)
class AssertionSetResult:
    outcomes: tuple[AssertionOutcome, ...]

    @property
    def is_valid(self) -> bool:
        return all(item.status in (VALID_EVALUATED, VALID_NOT_APPLICABLE)
                   for item in self.outcomes)


def _text(value: object) -> bool:
    return type(value) is str and 0 < len(value) <= MAX_TEXT and value.strip() == value


def _invalid(reason: str) -> AssertionOutcome:
    return AssertionOutcome(INVALID, reason)


def _validate_context(context: SyntheticContext,
                      profile: SyntheticAuthorityProfile) -> str | None:
    if not isinstance(context, SyntheticContext) or not _text(context.snapshot_identity):
        return "Invalid synthetic snapshot context."
    if not _text(context.assessment_identity) or not isinstance(context.recommendations, tuple):
        return "Invalid synthetic assessment context."
    if not isinstance(context.evidence, Mapping) or not isinstance(context.current_revisions, Mapping):
        return "Invalid synthetic source context."
    if (not isinstance(profile, SyntheticAuthorityProfile) or
            profile.version != AUTHORITY_PROFILE_VERSION or
            not isinstance(profile.issuer_by_driver, Mapping) or
            dict(profile.issuer_by_driver) != AUTHORITY_BY_DRIVER):
        return "Unsupported synthetic authority profile."
    if not context.recommendations or len(context.recommendations) > MAX_ASSERTIONS:
        return "Invalid synthetic recommendation collection."
    identities = []
    finding_ids = []
    for item in context.recommendations:
        if (not isinstance(item, RecommendationInstance) or
                not _text(item.instance_identity) or
                not _text(item.decision_identifier) or
                item.decision_table_version != RECOMMENDATION_TABLE_VERSION or
                (item.finding_id is not None and not _text(item.finding_id))):
            return "Invalid synthetic recommendation context."
        identities.append(item.instance_identity)
        if item.finding_id is not None:
            finding_ids.append(item.finding_id)
    if len(identities) != len(set(identities)) or len(finding_ids) != len(set(finding_ids)):
        return "Duplicate synthetic recommendation identity."
    if any(item.finding_id is None for item in context.recommendations) and not (
        len(context.recommendations) == 1 and
        context.recommendations[0].decision_identifier == "recommendation-v1-no-findings-monitor"
    ):
        return "Invalid synthetic no-findings context."
    return None


def _validate_one(record: Mapping[str, object], context: SyntheticContext,
                  profile: SyntheticAuthorityProfile) -> AssertionOutcome:
    if not isinstance(record, Mapping) or set(record) != FIELDS:
        return _invalid("Assertion fields are incomplete or unsupported.")
    text_fields = FIELDS - frozenset(("findingId", "evidenceReferences",
                                     "targetReference", "timingBasisReference"))
    if any(not _text(record[key]) for key in text_fields):
        return _invalid("Assertion field type or length is invalid.")
    for key in ("findingId", "targetReference", "timingBasisReference"):
        if record[key] is not None and not _text(record[key]):
            return _invalid(f"{key} type or length is invalid.")
    refs = record["evidenceReferences"]
    if (type(refs) is not list or not 1 <= len(refs) <= MAX_EVIDENCE_REFERENCES or
            any(not _text(ref) for ref in refs) or refs != sorted(set(refs))):
        return _invalid("Evidence references must be bounded, unique, and canonical.")
    if record["assertionContractVersion"] != ASSERTION_CONTRACT_VERSION:
        return _invalid("Unsupported assertion contract version.")
    driver = record["driverId"]
    if driver not in DRIVER_VALUES:
        return _invalid("Unsupported driver identifier.")
    status = record["applicabilityStatus"]
    if status not in ("evaluated", "not-applicable"):
        return _invalid("Unsupported applicability status.")
    if (record["applicabilityRuleVersion"] != APPLICABILITY_RULE_VERSION or
            record["applicabilityRuleId"] != f"local-{driver}-{status}-v1"):
        return _invalid("Unsupported synthetic applicability rule.")
    value = record["assertedValue"]
    if status == "not-applicable" and value != "not-applicable":
        return _invalid("Invalid exclusion value.")
    if status == "evaluated" and value not in DRIVER_VALUES[driver]:
        return _invalid("Unsupported synthetic driver value.")
    if (record["assessmentSnapshotIdentity"] != context.snapshot_identity or
            record["assessmentIdentity"] != context.assessment_identity):
        return _invalid("Assertion snapshot or assessment binding mismatch.")
    matches = [item for item in context.recommendations
               if item.instance_identity == record["recommendationInstanceIdentity"]]
    if len(matches) != 1 or matches[0].finding_id is None:
        return _invalid("Unknown or no-findings recommendation instance.")
    recommendation = matches[0]
    if (record["findingId"] != recommendation.finding_id or
            record["recommendationDecisionIdentifier"] != recommendation.decision_identifier or
            record["recommendationDecisionTableVersion"] != recommendation.decision_table_version):
        return _invalid("Recommendation and finding linkage mismatch.")
    if record["businessAuthorityReference"] != profile.issuer_by_driver[driver]:
        return _invalid("Unsupported or wrong-driver synthetic authority.")
    current = context.current_revisions.get(record["currentnessReference"])
    if current is None or current != record["sourceRevision"] or not _text(current):
        return _invalid("Unknown or stale synthetic source revision.")
    for ref in refs:
        evidence = context.evidence.get(ref)
        if (not isinstance(evidence, SyntheticEvidence) or
                evidence.reference != ref or evidence.driver_id != driver or
                evidence.supported_value != value or
                evidence.instance_identity != recommendation.instance_identity):
            return _invalid("Evidence does not support this linked assertion.")
        if (status == "not-applicable" or value in ABSENCE_VALUES) and not evidence.scope_confirmed:
            return _invalid("Exclusion or affirmative absence lacks reviewed scope.")
        if driver == "executive-urgency" and value == "time-bound-executive-action":
            if (record["timingBasisReference"] is None or
                    evidence.timing_basis_reference != record["timingBasisReference"]):
                return _invalid("Time-bound action lacks supported timing basis.")
        elif record["timingBasisReference"] is not None:
            return _invalid("Unexpected timing basis.")
        if driver == "dependency-role" and value in RELATION_VALUES:
            target = record["targetReference"]
            if (target is None or target == recommendation.instance_identity or
                    target not in {item.instance_identity for item in context.recommendations} or
                    evidence.target_reference != target):
                return _invalid("Invalid synthetic dependency target.")
        elif record["targetReference"] is not None:
            return _invalid("Unexpected dependency target.")
    return AssertionOutcome(
        VALID_NOT_APPLICABLE if status == "not-applicable" else VALID_EVALUATED,
        "Validated synthetic assertion; no priority assigned.",
        record["assertionId"], driver, recommendation.instance_identity,
    )


def validate_local_assertions(
    records: object,
    context: SyntheticContext,
    profile: SyntheticAuthorityProfile = LOCAL_AUTHORITY_PROFILE,
    required_driver_ids: frozenset[str] = frozenset(),
) -> AssertionSetResult:
    """Validate only caller-supplied synthetic context; never assign priority."""
    context_error = _validate_context(context, profile)
    if context_error:
        return AssertionSetResult((_invalid(context_error),))
    if (type(records) is not list or len(records) > MAX_ASSERTIONS or
            type(required_driver_ids) is not frozenset or
            not required_driver_ids <= DRIVER_VALUES.keys()):
        return AssertionSetResult((_invalid("Invalid assertion collection or required drivers."),))
    outcomes = []
    assertion_ids = set()
    active_keys = set()
    dependency_edges = []
    for record in records:
        outcome = _validate_one(record, context, profile)
        if outcome.status == INVALID:
            return AssertionSetResult((outcome,))
        assertion_id = record["assertionId"]
        key = (record["recommendationInstanceIdentity"], record["driverId"])
        if assertion_id in assertion_ids or key in active_keys:
            return AssertionSetResult((_invalid("Duplicate or conflicting active assertion."),))
        assertion_ids.add(assertion_id)
        active_keys.add(key)
        outcomes.append(outcome)
        if record["driverId"] == "dependency-role" and record["assertedValue"] in RELATION_VALUES:
            dependency_edges.append((record["recommendationInstanceIdentity"],
                                     record["targetReference"]))
    edges_by_source = {source: target for source, target in dependency_edges}
    for source in edges_by_source:
        seen = set()
        current = source
        while current in edges_by_source:
            if current in seen:
                return AssertionSetResult((_invalid("Synthetic dependency cycle is unsupported."),))
            seen.add(current)
            current = edges_by_source[current]
    missing = [
        (item.instance_identity, driver)
        for item in context.recommendations if item.finding_id is not None
        for driver in sorted(required_driver_ids)
        if (item.instance_identity, driver) not in active_keys
    ]
    if missing:
        return AssertionSetResult((AssertionOutcome(
            BLOCKED_PENDING_DATA, "Required synthetic assertion is missing.",
            driver_id=missing[0][1], recommendation_instance_identity=missing[0][0],
        ),))
    return AssertionSetResult(tuple(sorted(
        outcomes, key=lambda item: (item.recommendation_instance_identity,
                                    item.driver_id),
    )))
