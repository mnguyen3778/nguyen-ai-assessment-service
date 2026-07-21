from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


METHODOLOGY_VERSION = "business-decision-methodology-v1"


@dataclass(frozen=True)
class ReadinessDimensionConfig:
    id: str
    label: str


@dataclass(frozen=True)
class EvidenceCategoryConfig:
    id: str
    label: str


@dataclass(frozen=True)
class AnswerTypeConfig:
    id: str
    label: str
    minimum: float | None = None
    maximum: float | None = None

    @property
    def is_normalizable(self) -> bool:
        return self.minimum is not None and self.maximum is not None


@dataclass(frozen=True)
class QuestionConfig:
    id: str
    business_capability: str
    evidence_category: str
    readiness_dimension: str
    expected_answer_type: str
    weight_category: str


@dataclass(frozen=True)
class RecommendationPriorityConfig:
    id: str
    label: str
    rank: int


@dataclass(frozen=True)
class ServiceConfig:
    id: str
    label: str


@dataclass(frozen=True)
class PlaceholderThresholdConfig:
    id: str
    label: str
    minimum: int
    maximum: int


@dataclass(frozen=True)
class OutputSchemaConfig:
    current_response_fields: tuple[str, ...]
    snapshot_response_fields: tuple[str, ...]


@dataclass(frozen=True)
class BusinessDecisionMethodologyConfig:
    version: str
    readiness_dimensions: Mapping[str, ReadinessDimensionConfig]
    evidence_categories: Mapping[str, EvidenceCategoryConfig]
    answer_types: Mapping[str, AnswerTypeConfig]
    weight_categories: frozenset[str]
    recommendation_priorities: Mapping[str, RecommendationPriorityConfig]
    services: Mapping[str, ServiceConfig]
    questions: Mapping[str, QuestionConfig]
    placeholder_question_weights: Mapping[str, float]
    placeholder_thresholds: Mapping[str, PlaceholderThresholdConfig]
    output_schema: OutputSchemaConfig


def validate_methodology_config(
    config: BusinessDecisionMethodologyConfig,
) -> None:
    _validate_mapping_keys("readiness dimension", config.readiness_dimensions)
    _validate_mapping_keys("evidence category", config.evidence_categories)
    _validate_mapping_keys("recommendation priority", config.recommendation_priorities)
    _validate_mapping_keys("service", config.services)
    _validate_mapping_keys("question", config.questions)
    _validate_mapping_keys("placeholder threshold", config.placeholder_thresholds)

    _validate_mapping_keys("answer type", config.answer_types)

    if not config.weight_categories:
        raise ValueError("At least one weight category is required.")

    for question in config.questions.values():
        if question.evidence_category not in config.evidence_categories:
            raise ValueError(
                f"Unknown evidence category for question {question.id}: "
                f"{question.evidence_category}"
            )
        if question.readiness_dimension not in config.readiness_dimensions:
            raise ValueError(
                f"Unknown readiness dimension for question {question.id}: "
                f"{question.readiness_dimension}"
            )
        if question.expected_answer_type not in config.answer_types:
            raise ValueError(
                f"Unknown answer type for question {question.id}: "
                f"{question.expected_answer_type}"
            )
        if question.weight_category not in config.weight_categories:
            raise ValueError(
                f"Unknown weight category for question {question.id}: "
                f"{question.weight_category}"
            )

    _validate_answer_type_ranges(config.answer_types)
    _validate_placeholder_question_weights(config)
    _validate_priority_ranks(config.recommendation_priorities)
    _validate_placeholder_thresholds(config.placeholder_thresholds)


def _validate_mapping_keys(name: str, values: Mapping[str, object]) -> None:
    if not values:
        raise ValueError(f"At least one {name} is required.")

    for key, value in values.items():
        if not isinstance(key, str) or not key:
            raise ValueError(f"Invalid {name} key.")
        if not hasattr(value, "id") or getattr(value, "id") != key:
            raise ValueError(f"{name.title()} key must match object id: {key}")


def _validate_priority_ranks(
    priorities: Mapping[str, RecommendationPriorityConfig],
) -> None:
    ranks = [priority.rank for priority in priorities.values()]
    if sorted(ranks) != list(range(1, len(ranks) + 1)):
        raise ValueError("Recommendation priority ranks must be contiguous.")


def _validate_answer_type_ranges(
    answer_types: Mapping[str, AnswerTypeConfig],
) -> None:
    for answer_type in answer_types.values():
        if answer_type.minimum is None and answer_type.maximum is None:
            continue
        if answer_type.minimum is None or answer_type.maximum is None:
            raise ValueError(
                f"Answer type range must include minimum and maximum: {answer_type.id}"
            )
        if answer_type.maximum <= answer_type.minimum:
            raise ValueError(
                f"Answer type maximum must be greater than minimum: {answer_type.id}"
            )


def _validate_placeholder_question_weights(
    config: BusinessDecisionMethodologyConfig,
) -> None:
    missing_weights = (
        config.questions.keys()
        - config.placeholder_question_weights.keys()
    )
    if missing_weights:
        raise ValueError(
            "Placeholder question weights missing question: "
            f"{sorted(missing_weights)[0]}"
        )

    unknown_weights = (
        config.placeholder_question_weights.keys()
        - config.questions.keys()
    )
    if unknown_weights:
        raise ValueError(
            "Placeholder question weights contain unknown question: "
            f"{sorted(unknown_weights)[0]}"
        )

    for question_id, weight in config.placeholder_question_weights.items():
        if not _is_positive_number(weight):
            raise ValueError(
                f"Placeholder question weight must be greater than 0: {question_id}"
            )


def _validate_placeholder_thresholds(
    thresholds: Mapping[str, PlaceholderThresholdConfig],
) -> None:
    ordered_thresholds = sorted(
        thresholds.values(),
        key=lambda threshold: threshold.minimum,
    )
    expected_minimum = 0

    for threshold in ordered_thresholds:
        if threshold.minimum != expected_minimum:
            raise ValueError("Placeholder thresholds must be contiguous.")
        if threshold.maximum < threshold.minimum:
            raise ValueError("Placeholder threshold maximum must be >= minimum.")
        expected_minimum = threshold.maximum + 1

    if expected_minimum != 101:
        raise ValueError("Placeholder thresholds must cover 0 through 100.")


def _is_positive_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and value > 0
    )


def _map_by_id(values):
    mapped_values = {}
    for value in values:
        if value.id in mapped_values:
            raise ValueError(f"Duplicate methodology id: {value.id}")
        mapped_values[value.id] = value

    return MappingProxyType(mapped_values)


READINESS_DIMENSIONS = _map_by_id(
    (
        ReadinessDimensionConfig("ai-readiness", "AI Readiness"),
        ReadinessDimensionConfig("security-readiness", "Security Readiness"),
        ReadinessDimensionConfig("knowledge-readiness", "Knowledge Readiness"),
        ReadinessDimensionConfig("automation-readiness", "Automation Readiness"),
        ReadinessDimensionConfig("engineering-readiness", "Engineering Readiness"),
        ReadinessDimensionConfig("cloud-readiness", "Cloud Readiness"),
        ReadinessDimensionConfig("operational-readiness", "Operational Readiness"),
        ReadinessDimensionConfig("business-readiness", "Business Readiness"),
    )
)


EVIDENCE_CATEGORIES = _map_by_id(
    (
        EvidenceCategoryConfig("leadership", "Leadership"),
        EvidenceCategoryConfig("strategy", "Strategy"),
        EvidenceCategoryConfig("technology", "Technology"),
        EvidenceCategoryConfig("security", "Security"),
        EvidenceCategoryConfig("knowledge", "Knowledge"),
        EvidenceCategoryConfig("operations", "Operations"),
        EvidenceCategoryConfig("governance", "Governance"),
        EvidenceCategoryConfig("automation", "Automation"),
        EvidenceCategoryConfig("data", "Data"),
        EvidenceCategoryConfig("cloud", "Cloud"),
    )
)


ANSWER_TYPES = _map_by_id(
    (
        AnswerTypeConfig("scale-0-4", "Scale 0-4", 0, 4),
        AnswerTypeConfig("yes-no", "Yes/No"),
        AnswerTypeConfig("single-select", "Single Select"),
        AnswerTypeConfig("multi-select", "Multi Select"),
        AnswerTypeConfig("numeric", "Numeric", 0, 100),
        AnswerTypeConfig("text-evidence", "Text Evidence"),
    )
)


WEIGHT_CATEGORIES = frozenset(
    {
        "foundational-control",
        "strategic-alignment",
        "operational-capability",
        "value-enablement",
        "risk-control",
        "scale-readiness",
    }
)


RECOMMENDATION_PRIORITIES = _map_by_id(
    (
        RecommendationPriorityConfig("critical", "Critical", 1),
        RecommendationPriorityConfig("high", "High", 2),
        RecommendationPriorityConfig("medium", "Medium", 3),
        RecommendationPriorityConfig("low", "Low", 4),
    )
)


SERVICES = _map_by_id(
    (
        ServiceConfig("service.assessment-only", "Assessment Only"),
        ServiceConfig("service.ai-strategy-workshop", "AI Strategy Workshop"),
        ServiceConfig("service.automation-assessment", "Automation Assessment"),
        ServiceConfig("service.executive-ai-roadmap", "Executive AI Roadmap"),
        ServiceConfig("service.implementation-engagement", "Implementation Engagement"),
        ServiceConfig("service.managed-ai-services", "Managed AI Services"),
    )
)


QUESTIONS = _map_by_id(
    (
        QuestionConfig(
            "q.ai.strategy.business-goals",
            "Align AI initiatives to measurable business goals.",
            "strategy",
            "ai-readiness",
            "scale-0-4",
            "strategic-alignment",
        ),
        QuestionConfig(
            "q.ai.leadership.sponsor",
            "Assign executive sponsorship for AI adoption.",
            "leadership",
            "ai-readiness",
            "scale-0-4",
            "strategic-alignment",
        ),
        QuestionConfig(
            "q.ai.governance.owner",
            "Establish accountable AI governance ownership.",
            "governance",
            "ai-readiness",
            "scale-0-4",
            "foundational-control",
        ),
        QuestionConfig(
            "q.ai.use-cases.prioritized",
            "Prioritize AI use cases by business value and feasibility.",
            "strategy",
            "ai-readiness",
            "scale-0-4",
            "value-enablement",
        ),
        QuestionConfig(
            "q.ai.success-metrics.defined",
            "Define success metrics for AI initiatives.",
            "strategy",
            "ai-readiness",
            "scale-0-4",
            "strategic-alignment",
        ),
        QuestionConfig(
            "q.ai.risk-policy.approved",
            "Maintain approved policy for acceptable AI use.",
            "governance",
            "ai-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.security.identity.mfa",
            "Protect user access with strong authentication.",
            "security",
            "security-readiness",
            "scale-0-4",
            "foundational-control",
        ),
        QuestionConfig(
            "q.security.access.review",
            "Review access rights on a recurring basis.",
            "security",
            "security-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.security.data.classification",
            "Classify business and customer data by sensitivity.",
            "data",
            "security-readiness",
            "scale-0-4",
            "foundational-control",
        ),
        QuestionConfig(
            "q.security.incident-response.owner",
            "Assign incident response ownership and escalation.",
            "operations",
            "security-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.security.vendor.controls",
            "Assess vendor and third-party security controls.",
            "governance",
            "security-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.security.backup.recovery-tested",
            "Test recovery from backup or continuity procedures.",
            "operations",
            "security-readiness",
            "scale-0-4",
            "foundational-control",
        ),
        QuestionConfig(
            "q.knowledge.docs.current",
            "Maintain current documentation for key business processes.",
            "knowledge",
            "knowledge-readiness",
            "scale-0-4",
            "operational-capability",
        ),
        QuestionConfig(
            "q.knowledge.owner.defined",
            "Assign owners for critical knowledge assets.",
            "knowledge",
            "knowledge-readiness",
            "scale-0-4",
            "operational-capability",
        ),
        QuestionConfig(
            "q.knowledge.searchable",
            "Make operational knowledge searchable and reusable.",
            "technology",
            "knowledge-readiness",
            "scale-0-4",
            "scale-readiness",
        ),
        QuestionConfig(
            "q.knowledge.sme-dependency",
            "Reduce dependency on single subject matter experts.",
            "operations",
            "knowledge-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.knowledge.refresh-cadence",
            "Review and refresh knowledge assets on a defined cadence.",
            "governance",
            "knowledge-readiness",
            "scale-0-4",
            "operational-capability",
        ),
        QuestionConfig(
            "q.knowledge.customer-context",
            "Capture customer context and decision history consistently.",
            "knowledge",
            "business-readiness",
            "scale-0-4",
            "value-enablement",
        ),
        QuestionConfig(
            "q.automation.process-documented",
            "Document processes before automation.",
            "automation",
            "automation-readiness",
            "scale-0-4",
            "foundational-control",
        ),
        QuestionConfig(
            "q.automation.manual-volume",
            "Identify high-volume manual work suitable for automation.",
            "operations",
            "automation-readiness",
            "numeric",
            "value-enablement",
        ),
        QuestionConfig(
            "q.automation.exception-handling",
            "Define exception handling and ownership for automated workflows.",
            "automation",
            "automation-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.automation.integration-readiness",
            "Confirm systems expose reliable integration paths.",
            "technology",
            "automation-readiness",
            "scale-0-4",
            "operational-capability",
        ),
        QuestionConfig(
            "q.automation.measurement",
            "Measure automation outcomes and process impact.",
            "operations",
            "automation-readiness",
            "scale-0-4",
            "value-enablement",
        ),
        QuestionConfig(
            "q.automation.change-control",
            "Govern changes to automated workflows.",
            "governance",
            "automation-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.engineering.source-control",
            "Manage application and automation code in source control.",
            "technology",
            "engineering-readiness",
            "scale-0-4",
            "foundational-control",
        ),
        QuestionConfig(
            "q.engineering.testing",
            "Validate changes with repeatable tests.",
            "technology",
            "engineering-readiness",
            "scale-0-4",
            "foundational-control",
        ),
        QuestionConfig(
            "q.engineering.release-process",
            "Use a controlled release process.",
            "operations",
            "engineering-readiness",
            "scale-0-4",
            "operational-capability",
        ),
        QuestionConfig(
            "q.engineering.observability",
            "Monitor systems with actionable logs, metrics, or alerts.",
            "operations",
            "engineering-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.engineering.backlog-prioritization",
            "Prioritize technical work by business impact.",
            "strategy",
            "engineering-readiness",
            "scale-0-4",
            "strategic-alignment",
        ),
        QuestionConfig(
            "q.engineering.ownership",
            "Assign ownership for systems and operational support.",
            "leadership",
            "engineering-readiness",
            "scale-0-4",
            "operational-capability",
        ),
        QuestionConfig(
            "q.cloud.account-structure",
            "Maintain governed cloud account or environment structure.",
            "cloud",
            "cloud-readiness",
            "scale-0-4",
            "foundational-control",
        ),
        QuestionConfig(
            "q.cloud.cost-controls",
            "Monitor and control cloud spend.",
            "cloud",
            "cloud-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.cloud.security-baseline",
            "Apply baseline cloud security controls.",
            "security",
            "cloud-readiness",
            "scale-0-4",
            "foundational-control",
        ),
        QuestionConfig(
            "q.cloud.infrastructure-as-code",
            "Manage cloud configuration through repeatable deployment practices.",
            "technology",
            "cloud-readiness",
            "scale-0-4",
            "scale-readiness",
        ),
        QuestionConfig(
            "q.cloud.resilience",
            "Define resilience, backup, or recovery expectations for cloud workloads.",
            "operations",
            "cloud-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.cloud.monitoring",
            "Monitor cloud workload health and operational status.",
            "operations",
            "cloud-readiness",
            "scale-0-4",
            "operational-capability",
        ),
        QuestionConfig(
            "q.operations.process-ownership",
            "Assign accountable owners for critical business processes.",
            "operations",
            "operational-readiness",
            "scale-0-4",
            "operational-capability",
        ),
        QuestionConfig(
            "q.operations.kpi-defined",
            "Define operational KPIs for key processes.",
            "strategy",
            "operational-readiness",
            "scale-0-4",
            "strategic-alignment",
        ),
        QuestionConfig(
            "q.operations.escalation-path",
            "Define escalation paths for operational issues.",
            "operations",
            "operational-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.operations.capacity-planning",
            "Plan capacity for people, systems, and process demand.",
            "operations",
            "operational-readiness",
            "scale-0-4",
            "scale-readiness",
        ),
        QuestionConfig(
            "q.operations.change-management",
            "Manage operational change with communication and ownership.",
            "governance",
            "operational-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.operations.continuity",
            "Maintain continuity plans for critical operations.",
            "operations",
            "operational-readiness",
            "scale-0-4",
            "foundational-control",
        ),
        QuestionConfig(
            "q.business.outcomes-defined",
            "Define target business outcomes for technology initiatives.",
            "strategy",
            "business-readiness",
            "scale-0-4",
            "strategic-alignment",
        ),
        QuestionConfig(
            "q.business.customer-impact",
            "Connect initiatives to measurable customer impact.",
            "strategy",
            "business-readiness",
            "scale-0-4",
            "value-enablement",
        ),
        QuestionConfig(
            "q.business.financial-case",
            "Define cost, benefit, or investment rationale.",
            "strategy",
            "business-readiness",
            "scale-0-4",
            "strategic-alignment",
        ),
        QuestionConfig(
            "q.business.executive-alignment",
            "Align executive stakeholders on priority and timing.",
            "leadership",
            "business-readiness",
            "scale-0-4",
            "strategic-alignment",
        ),
        QuestionConfig(
            "q.business.risk-appetite",
            "Define acceptable risk for AI, automation, and cloud initiatives.",
            "governance",
            "business-readiness",
            "scale-0-4",
            "risk-control",
        ),
        QuestionConfig(
            "q.business.decision-cadence",
            "Maintain a regular decision cadence for transformation initiatives.",
            "leadership",
            "business-readiness",
            "scale-0-4",
            "operational-capability",
        ),
    )
)


PLACEHOLDER_QUESTION_WEIGHTS = MappingProxyType(
    {
        question_id: 1.0
        for question_id in QUESTIONS
    }
)


PLACEHOLDER_THRESHOLDS = _map_by_id(
    (
        PlaceholderThresholdConfig("not-ready", "Not Ready", 0, 24),
        PlaceholderThresholdConfig("foundational-gaps", "Foundational Gaps", 25, 49),
        PlaceholderThresholdConfig("emerging-readiness", "Emerging Readiness", 50, 69),
        PlaceholderThresholdConfig("operationally-ready", "Operationally Ready", 70, 84),
        PlaceholderThresholdConfig("strategically-ready", "Strategically Ready", 85, 100),
    )
)


OUTPUT_SCHEMA = OutputSchemaConfig(
    current_response_fields=(
        "requestId",
        "assessmentVersion",
        "overallScore",
        "readinessLevel",
        "categoryScores",
        "recommendations",
        "modelInvoked",
        "persisted",
    ),
    snapshot_response_fields=(
        "requestId",
        "assessmentVersion",
        "assessmentTimestamp",
        "executiveSummary",
        "overallReadiness",
        "domains",
        "risks",
        "priorityActions",
        "executiveRecommendations",
        "recommendedEngagement",
        "recommendedServiceTier",
        "confidence",
        "audit",
    ),
)


BUSINESS_DECISION_METHODOLOGY = BusinessDecisionMethodologyConfig(
    version=METHODOLOGY_VERSION,
    readiness_dimensions=READINESS_DIMENSIONS,
    evidence_categories=EVIDENCE_CATEGORIES,
    answer_types=ANSWER_TYPES,
    weight_categories=WEIGHT_CATEGORIES,
    recommendation_priorities=RECOMMENDATION_PRIORITIES,
    services=SERVICES,
    questions=QUESTIONS,
    placeholder_question_weights=PLACEHOLDER_QUESTION_WEIGHTS,
    placeholder_thresholds=PLACEHOLDER_THRESHOLDS,
    output_schema=OUTPUT_SCHEMA,
)


validate_methodology_config(BUSINESS_DECISION_METHODOLOGY)
