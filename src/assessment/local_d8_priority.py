"""Local synthetic D8 evaluation only. No production caller or authority."""

import hashlib
import json
from dataclasses import dataclass
from types import MappingProxyType

from assessment.approved_methodology_runtime_config import (
    APPROVED_CONFIDENCE_LEVEL_ORDER, APPROVED_RISK_LEVEL_ORDER,
    CONFIDENCE_DECISION_RULES, CONFIDENCE_DECISION_TABLE_SET_VERSION,
    RECOMMENDATION_DECISION_TABLE_SET_VERSION, RECOMMENDATION_DECISION_RULES,
    RISK_DECISION_RULES, RISK_DECISION_TABLE_SET_VERSION,
    SEVERITY_DECISION_RULES, SEVERITY_DECISION_TABLE_SET_VERSION,
)
from assessment.governed_assessment_input import FindingInput, FINDING_CONSEQUENCE_RULES
from assessment.governed_decision_runtime import (
    GovernedRecommendationResult, RECOMMENDATION_RULE_BY_FINDING,
)
from assessment.local_priority_assertions import (
    VALID_EVALUATED, RecommendationInstance, SyntheticContext,
    validate_local_assertions,
)


METHODOLOGY_VERSION = "founder-d8-methodology-approval-v1-local-synthetic"
RULE_TABLE_VERSION = "local-synthetic-d8-rule-table-v1"
PRIORITY_ASSIGNED = "PRIORITY_ASSIGNED"
PRIORITY_NOT_DETERMINED = "PRIORITY_NOT_DETERMINED"
BLOCKED_REQUIRED_EVIDENCE = "BLOCKED_REQUIRED_EVIDENCE"
REJECTED_INVALID_ASSERTION = "REJECTED_INVALID_ASSERTION"
NO_FINDINGS_MONITOR = "NO_FINDINGS_MONITOR"
INSUFFICIENT_CONFIDENCE = "INSUFFICIENT_CONFIDENCE"
TRUE, FALSE, PENDING = "TRUE", "FALSE", "PENDING_REQUIRED_EVIDENCE"

_DRIVERS = ("customer-impact", "executive-urgency", "dependency-role")
_VALUES = MappingProxyType({
    "customer-impact": MappingProxyType({
        "impact-present": "P", "impact-affirmed-absent": "A",
    }),
    "executive-urgency": MappingProxyType({
        "time-bound-executive-action": "T",
        "executive-action-required": "U",
        "executive-action-affirmed-absent": "A",
    }),
    "dependency-role": MappingProxyType({
        "blocks-related-work": "P", "unlocks-related-work": "P",
        "no-dependency-affirmed": "A",
    }),
})
_NONDEF = frozenset((
    ("Observation", "observation"), ("Strength", "strength"),
    ("Opportunity", "opportunity"),
))
_MATERIAL = ("Deficiency", "material current breach")
_SIGNIFICANT = ("Deficiency", "significant gap")
_CLEAR = ("Deficiency", "clear deficiency")
_LOW = _NONDEF | {("Deficiency", "limited weakness")}
_CANDIDATES = MappingProxyType({
    _MATERIAL: (("critical", "B-C1"), ("high", "G-H1")),
    _SIGNIFICANT: (("high", "G-H2"),),
    _CLEAR: (("high", "B-H3"), ("medium", "B-M1")),
    ("Deficiency", "limited weakness"): (("low", "G-L1"),),
    **{pair: (("high", "N-H7"), ("low", "G-L1")) for pair in _NONDEF},
})
_ORDER = ("critical", "high", "medium", "low")


@dataclass(frozen=True)
class LocalD8Input:
    findings: tuple[FindingInput, ...]
    recommendations: tuple[GovernedRecommendationResult, ...]
    recommendation_instance_identity: str
    context: SyntheticContext
    records: object
    severity_classifications: tuple[str, ...]
    risk_classification: str
    confidence_classification: str
    severity_decision_identifiers: tuple[str, ...]
    severity_decision_table_version: str
    risk_decision_identifier: str
    risk_decision_table_version: str
    confidence_decision_identifier: str
    confidence_decision_table_version: str


@dataclass(frozen=True)
class LocalD8Result:
    outcome: str
    priority: str | None
    matched_rule_ids: tuple[str, ...]
    excluded_rule_ids: tuple[str, ...]
    pending_rule_ids: tuple[str, ...]
    recommendation_instance_identity: str
    snapshot_identity: str
    assessment_identity: str
    finding_id: str | None
    reason: str
    validated_assertion_ids: tuple[str, ...]
    review_required: bool = False
    methodology_version: str = METHODOLOGY_VERSION
    rule_table_version: str = RULE_TABLE_VERSION
    governed_finding_type: str | None = None
    governed_consequence_basis: str | None = None
    evaluated_driver_values: tuple[tuple[str, str | None], ...] = ()
    review_reference: str | None = None


def _result(data: LocalD8Input, status: str, reason: str, *,
            priority: str | None = None, matched: tuple[str, ...] = (),
            excluded: tuple[str, ...] = (), pending: tuple[str, ...] = (),
            trace: tuple[str, ...] = (), review: bool = False,
            finding_id: str | None = None,
            governed_pair: tuple[str, str] | None = None,
            evaluated_values: tuple[tuple[str, str | None], ...] = (),
            review_reference: str | None = None) -> LocalD8Result:
    return LocalD8Result(status, priority, matched, excluded, pending,
                         data.recommendation_instance_identity,
                         data.context.snapshot_identity if isinstance(data.context, SyntheticContext) else "",
                         data.context.assessment_identity if isinstance(data.context, SyntheticContext) else "",
                         finding_id,
                         reason, trace, review, METHODOLOGY_VERSION, RULE_TABLE_VERSION,
                         governed_pair[0] if governed_pair else None,
                         governed_pair[1] if governed_pair else None,
                         evaluated_values, review_reference)


def _review_reference(data: LocalD8Input, finding_id: str) -> str:
    """Local correlation only; does not attest approval or review completion."""
    identity = (
        data.context.assessment_identity, data.context.snapshot_identity,
        finding_id, data.recommendation_instance_identity,
        METHODOLOGY_VERSION, RULE_TABLE_VERSION,
    )
    encoded = json.dumps(identity, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    return "local-synthetic-d8-review-v1:" + hashlib.sha256(encoded).hexdigest()


def _and(*values: str) -> str:
    if FALSE in values:
        return FALSE
    return TRUE if all(value == TRUE for value in values) else PENDING


def _or(*values: str) -> str:
    if TRUE in values:
        return TRUE
    return FALSE if all(value == FALSE for value in values) else PENDING


def _atom(values: dict[str, str], driver: str, expected: str) -> str:
    actual = values.get(driver)
    if actual is None:
        return PENDING
    return TRUE if actual == expected else FALSE


def _rule(rule_id: str, values: dict[str, str]) -> str:
    d2 = lambda v: _atom(values, _DRIVERS[0], v)
    d3 = lambda v: _atom(values, _DRIVERS[1], v)
    d5 = lambda v: _atom(values, _DRIVERS[2], v)
    if rule_id == "B-C1":
        return _and(d3("T"), d5("P"))
    if rule_id == "G-H1":
        return _and(d2("P"), _or(d3("T"), d3("U")))
    if rule_id == "G-H2":
        return _or(_and(d2("P"), _or(d3("T"), d3("U"))),
                   _and(d2("P"), d5("P")),
                   _and(d3("T"), d5("P")))
    if rule_id == "B-H3":
        return _and(d2("P"), d3("T"))
    if rule_id == "N-H7":
        return _and(d2("P"), d3("T"), d5("P"))
    if rule_id == "B-M1" or rule_id == "G-L1":
        return _and(d2("A"), d3("A"), d5("A"))
    raise ValueError("Unsupported local D8 rule.")


def _binding(data: LocalD8Input) -> tuple[str | None, RecommendationInstance | None,
                                           GovernedRecommendationResult | None,
                                           FindingInput | None]:
    if (not isinstance(data.findings, tuple) or
            not isinstance(data.recommendations, tuple) or
            not isinstance(data.context, SyntheticContext) or
            not isinstance(data.recommendation_instance_identity, str)):
        return "invalid-local-input", None, None, None
    instances = data.context.recommendations
    if (not isinstance(instances, tuple) or
            any(not isinstance(item, RecommendationInstance) for item in instances) or
            any(not isinstance(item, FindingInput) for item in data.findings) or
            any(not isinstance(item, GovernedRecommendationResult)
                for item in data.recommendations) or
            len(instances) != len(data.recommendations) or
            len({item.instance_identity for item in instances}) != len(instances) or
            len({item.finding_id for item in data.findings}) != len(data.findings)):
        return "invalid-instance-collection", None, None, None
    if (len(data.findings) == 0 and len(data.recommendations) != 1 or
            len(data.findings) != 0 and len(data.findings) != len(data.recommendations)):
        return "incomplete-governed-collection", None, None, None
    if (not isinstance(data.severity_classifications, tuple) or
            len(data.severity_classifications) != len(data.findings) or
            not isinstance(data.severity_decision_identifiers, tuple) or
            len(data.severity_decision_identifiers) != len(data.findings) or
            data.severity_decision_table_version != SEVERITY_DECISION_TABLE_SET_VERSION or
            data.risk_classification not in APPROVED_RISK_LEVEL_ORDER or
            data.confidence_classification not in APPROVED_CONFIDENCE_LEVEL_ORDER or
            data.risk_decision_table_version != RISK_DECISION_TABLE_SET_VERSION or
            data.confidence_decision_table_version != CONFIDENCE_DECISION_TABLE_SET_VERSION or
            data.risk_decision_identifier not in RISK_DECISION_RULES or
            RISK_DECISION_RULES[data.risk_decision_identifier].output !=
            data.risk_classification or
            data.confidence_decision_identifier not in CONFIDENCE_DECISION_RULES or
            CONFIDENCE_DECISION_RULES[data.confidence_decision_identifier].output !=
            data.confidence_classification):
        return "invalid-governed-context", None, None, None
    for finding, severity, severity_id, recommendation, instance in zip(
            data.findings, data.severity_classifications,
            data.severity_decision_identifiers, data.recommendations, instances):
        if (not isinstance(finding, FindingInput) or
                not isinstance(recommendation, GovernedRecommendationResult) or
                not isinstance(instance, RecommendationInstance) or
                severity != SEVERITY_DECISION_RULES[
                    FINDING_CONSEQUENCE_RULES[
                        (finding.finding_type, finding.business_consequence_basis)
                    ]].output or
                severity_id != FINDING_CONSEQUENCE_RULES[
                    (finding.finding_type, finding.business_consequence_basis)] or
                recommendation.finding_id != finding.finding_id or
                instance.finding_id != finding.finding_id or
                instance.decision_identifier != recommendation.recommendation_decision_identifier or
                instance.decision_table_version != recommendation.recommendation_decision_table_version or
                recommendation.recommendation_decision_table_version !=
                RECOMMENDATION_DECISION_TABLE_SET_VERSION or
                recommendation.recommendation_decision_identifier !=
                RECOMMENDATION_RULE_BY_FINDING[(finding.finding_type, severity)] or
                recommendation.recommendation_classification !=
                RECOMMENDATION_DECISION_RULES[
                    recommendation.recommendation_decision_identifier].output):
            return "invalid-recommendation-binding", None, None, None
    selected = [(instance, recommendation) for instance, recommendation in
                zip(instances, data.recommendations)
                if instance.instance_identity == data.recommendation_instance_identity]
    if len(selected) != 1:
        return "unknown-recommendation-instance", None, None, None
    instance, recommendation = selected[0]
    if not data.findings:
        if (instance.finding_id is not None or recommendation.finding_id is not None or
                recommendation.recommendation_decision_identifier !=
                "recommendation-v1-no-findings-monitor" or
                recommendation.recommendation_classification != "monitor" or
                recommendation.recommendation_decision_table_version !=
                RECOMMENDATION_DECISION_TABLE_SET_VERSION):
            return "invalid-no-findings-monitor", None, None, None
        return None, instance, recommendation, None
    finding = next((item for item in data.findings if item.finding_id == instance.finding_id), None)
    return None, instance, recommendation, finding


def _resolve_level(states: tuple[tuple[str, str], ...]) -> tuple[tuple[str, ...],
                                                                 tuple[str, ...]]:
    """Return all true and pending peer IDs in stable order; usable by synthetic tests."""
    return (tuple(sorted(rule for rule, state in states if state == TRUE)),
            tuple(sorted(rule for rule, state in states if state == PENDING)))


def evaluate_local_d8_priority(data: LocalD8Input) -> LocalD8Result:
    """Evaluate one explicitly bound synthetic recommendation; never publish priority."""
    if not isinstance(data, LocalD8Input):
        raise ValueError("LocalD8Input is required.")
    try:
        error, instance, _, finding = _binding(data)
    except (TypeError, AttributeError, KeyError, ValueError):
        return _result(data, REJECTED_INVALID_ASSERTION, "invalid-local-input")
    if error:
        return _result(data, REJECTED_INVALID_ASSERTION, error)
    checked = validate_local_assertions(data.records, data.context,
                                        required_driver_ids=frozenset())
    if any(item.status != VALID_EVALUATED for item in checked.outcomes):
        return _result(data, REJECTED_INVALID_ASSERTION, "invalid-or-not-applicable-assertion",
                       finding_id=instance.finding_id)
    if not data.findings:
        if data.risk_classification != "minimal-informational":
            return _result(data, REJECTED_INVALID_ASSERTION, "invalid-no-findings-risk")
        return _result(data, NO_FINDINGS_MONITOR, "approved-no-findings-monitor")
    if data.confidence_classification == "insufficient-confidence":
        return _result(data, INSUFFICIENT_CONFIDENCE, "insufficient-confidence",
                       finding_id=finding.finding_id)
    values = {}
    asserted_values = {}
    trace = []
    for record in data.records:
        if record["recommendationInstanceIdentity"] == instance.instance_identity:
            driver = record["driverId"]
            values[driver] = _VALUES[driver][record["assertedValue"]]
            asserted_values[driver] = record["assertedValue"]
            trace.append(record["assertionId"])
    states = tuple((level, rule_id, _rule(rule_id, values))
                   for level, rule_id in _CANDIDATES[
                       (finding.finding_type, finding.business_consequence_basis)])
    excluded = tuple(sorted(rule for _, rule, state in states if state == FALSE))
    for level in _ORDER:
        peers = tuple((rule, state) for candidate_level, rule, state in states
                      if candidate_level == level)
        matched, pending = _resolve_level(peers)
        if pending:
            return _result(data, BLOCKED_REQUIRED_EVIDENCE, "pending-eligible-rule",
                           excluded=excluded, pending=pending, trace=tuple(sorted(trace)),
                           finding_id=finding.finding_id)
        if matched:
            return _result(data, PRIORITY_ASSIGNED, "matched-approved-local-rule",
                           priority=level, matched=matched, excluded=excluded,
                           trace=tuple(sorted(trace)), finding_id=finding.finding_id)
    return _result(data, PRIORITY_NOT_DETERMINED, "all-eligible-rules-excluded-review-required",
                   excluded=excluded, trace=tuple(sorted(trace)), review=True,
                   finding_id=finding.finding_id,
                   governed_pair=(finding.finding_type, finding.business_consequence_basis),
                   evaluated_values=tuple((driver, asserted_values.get(driver))
                                          for driver in _DRIVERS),
                   review_reference=_review_reference(data, finding.finding_id))
