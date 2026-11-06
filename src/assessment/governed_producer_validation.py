"""Structural validation of published governed conclusions; no decision rules run here."""

from collections.abc import Mapping

from assessment.approved_methodology_runtime_config import (
    APPROVED_CONFIDENCE_LEVEL_ORDER,
    APPROVED_DIMENSION_ORDER,
    APPROVED_RECOMMENDATION_LABEL_ORDER,
    APPROVED_RISK_LEVEL_ORDER,
    APPROVED_SEVERITY_LEVEL_ORDER,
    CONFIDENCE_DECISION_TABLE_SET_VERSION,
    RISK_DECISION_TABLE_SET_VERSION,
    RECOMMENDATION_DECISION_TABLE_SET_VERSION,
    SEVERITY_DECISION_TABLE_SET_VERSION,
    APPROVED_METHODOLOGY_RUNTIME_CONFIG,
    NO_FINDINGS_RECOMMENDATION_RULE_ID,
    approved_recommendation_action_text,
)
from assessment.business_decision_package import (
    ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
)
from assessment.governed_decision_runtime import RECOMMENDATION_RULE_BY_FINDING
from assessment.governed_assessment_input import FINDING_CONSEQUENCE_RULES
from assessment.methodology_config import METHODOLOGY_VERSION


def validate_governed_conclusions(
    value: object,
    *,
    package_version: str = GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
) -> None:
    if package_version not in (
        GOVERNED_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
        ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION,
    ):
        raise ValueError("Unsupported governed package version.")
    v3 = package_version == ACTION_TEXT_BUSINESS_DECISION_PACKAGE_CONTRACT_VERSION
    if not isinstance(value, Mapping) or tuple(value) != (
        "severityAssignedFindings", "assessmentRisk", "confidence",
        "recommendations", "executiveSummary",
    ):
        raise ValueError("Governed conclusions are incomplete or out of order.")
    findings = value["severityAssignedFindings"]
    risk = value["assessmentRisk"]
    confidence = value["confidence"]
    recommendations = value["recommendations"]
    summary = value["executiveSummary"]
    if not isinstance(findings, list) or not isinstance(recommendations, list):
        raise ValueError("Governed findings and recommendations must be arrays.")
    if not isinstance(risk, Mapping) or not isinstance(confidence, Mapping) or not isinstance(summary, Mapping):
        raise ValueError("Governed risk, confidence and summary are required mappings.")
    ids = []
    severities = []
    for sequence, item in enumerate(findings, 1):
        if not isinstance(item, Mapping) or tuple(item) != (
            "findingId", "title", "primaryDimension", "relatedDimensions",
            "triggerSource", "findingType", "businessConsequenceBasis",
            "sourceReferences", "sequenceIdentifier", "severityClassification",
            "severityDecisionIdentifier", "severityDecisionTableVersion",
        ):
            raise ValueError("Malformed severity-assigned finding.")
        if any(not isinstance(item[key], str) or not item[key].strip() for key in (
            "findingId", "title", "triggerSource", "findingType",
            "businessConsequenceBasis", "severityDecisionIdentifier",
        )):
            raise ValueError("Finding identity and traceability fields are required.")
        if item["primaryDimension"] not in APPROVED_DIMENSION_ORDER:
            raise ValueError("Unsupported finding dimension.")
        for key in ("relatedDimensions", "sourceReferences"):
            field = item[key]
            if not isinstance(field, list) or field != sorted(set(field)):
                raise ValueError("Finding references must be canonical and unique.")
        if not item["sourceReferences"] or item["sequenceIdentifier"] != sequence:
            raise ValueError("Finding sequence or evidence references are invalid.")
        if item["severityClassification"] not in APPROVED_SEVERITY_LEVEL_ORDER or item["severityDecisionTableVersion"] != SEVERITY_DECISION_TABLE_SET_VERSION:
            raise ValueError("Unsupported severity.")
        rule = APPROVED_METHODOLOGY_RUNTIME_CONFIG.severity_decision_rules.get(item["severityDecisionIdentifier"])
        if rule is None or rule.output != item["severityClassification"]:
            raise ValueError("Severity identifier and classification disagree.")
        if v3 and item["severityDecisionIdentifier"] != FINDING_CONSEQUENCE_RULES.get((
            item["findingType"], item["businessConsequenceBasis"],
        )):
            raise ValueError("Finding severity rule does not match its type and consequence.")
        ids.append(item["findingId"])
        severities.append(item["severityClassification"])
    if ids != sorted(set(ids)):
        raise ValueError("Finding identities must be unique and canonical.")

    _validate_decision(risk, ("riskClassification", "riskDecisionIdentifier", "riskDecisionTableVersion"),
                       APPROVED_RISK_LEVEL_ORDER, RISK_DECISION_TABLE_SET_VERSION,
                       APPROVED_METHODOLOGY_RUNTIME_CONFIG.risk_decision_rules)
    _validate_decision(confidence, ("confidenceClassification", "confidenceDecisionIdentifier", "confidenceDecisionTableVersion"),
                       APPROVED_CONFIDENCE_LEVEL_ORDER, CONFIDENCE_DECISION_TABLE_SET_VERSION,
                       APPROVED_METHODOLOGY_RUNTIME_CONFIG.confidence_decision_rules)
    if len(recommendations) != max(1, len(ids)):
        raise ValueError("Recommendation collection is incomplete.")
    for sequence, item in enumerate(recommendations):
        fields = (
            "findingId", "recommendationClassification", "recommendationDecisionIdentifier",
            "recommendationDecisionTableVersion",
        ) + (("recommendationActionText",) if v3 else ())
        if not isinstance(item, Mapping) or tuple(item) != fields:
            raise ValueError("Malformed recommendation.")
        if item["findingId"] != (ids[sequence] if ids else None):
            raise ValueError("Recommendation identity or order mismatch.")
        if item["recommendationClassification"] not in APPROVED_RECOMMENDATION_LABEL_ORDER or item["recommendationDecisionTableVersion"] != RECOMMENDATION_DECISION_TABLE_SET_VERSION:
            raise ValueError("Unsupported recommendation.")
        rule = APPROVED_METHODOLOGY_RUNTIME_CONFIG.recommendation_decision_rules.get(item["recommendationDecisionIdentifier"])
        if rule is None or rule.output != item["recommendationClassification"]:
            raise ValueError("Recommendation identifier and classification disagree.")
        if v3:
            if any(type(item[key]) is not str or not item[key] for key in fields[1:]):
                raise ValueError("Recommendation fields must be nonempty strings.")
            if ids:
                finding = findings[sequence]
                expected_rule = RECOMMENDATION_RULE_BY_FINDING.get((
                    finding["findingType"], finding["severityClassification"],
                ))
                if item["recommendationDecisionIdentifier"] != expected_rule:
                    raise ValueError("Recommendation rule does not match finding severity.")
            elif item["recommendationDecisionIdentifier"] != NO_FINDINGS_RECOMMENDATION_RULE_ID:
                raise ValueError("Invalid no-findings recommendation rule.")
            expected_text = approved_recommendation_action_text(
                item["recommendationDecisionIdentifier"],
                item["recommendationDecisionTableVersion"],
                METHODOLOGY_VERSION,
            )
            if item["recommendationActionText"] != expected_text:
                raise ValueError("Recommendation action text differs from approved methodology.")
    if not ids and (risk["riskClassification"] != "minimal-informational" or
                    recommendations[0]["recommendationDecisionIdentifier"] != "recommendation-v1-no-findings-monitor"):
        raise ValueError("Malformed empty-findings conclusion.")
    if tuple(summary) != ("findingCount", "sectionText") or summary["findingCount"] != len(ids):
        raise ValueError("Executive summary finding count mismatch.")
    sections = summary["sectionText"]
    if not isinstance(sections, Mapping) or tuple(sections) != tuple(APPROVED_METHODOLOGY_RUNTIME_CONFIG.executive_summary_sections):
        raise ValueError("Executive summary sections are incomplete or out of order.")
    if any(not isinstance(text, str) or not text for text in sections.values()):
        raise ValueError("Executive summary section text is required.")


def _validate_decision(value, keys, vocabulary, version, rules):
    if tuple(value) != keys or value[keys[0]] not in vocabulary or value[keys[2]] != version:
        raise ValueError("Unsupported governed decision result.")
    rule = rules.get(value[keys[1]])
    if rule is None or rule.output != value[keys[0]]:
        raise ValueError("Governed decision identifier and classification disagree.")
