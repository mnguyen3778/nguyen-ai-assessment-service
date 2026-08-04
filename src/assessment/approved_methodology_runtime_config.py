from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from assessment.methodology_config import METHODOLOGY_VERSION


PRODUCTION_AUTHORITY_RELEASE_VERSION = "production-authority-release-v1"
APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION = (
    "approved-methodology-runtime-config-v1"
)
BUSINESS_CAPABILITY_TAXONOMY_VERSION = "business-capability-taxonomy-v1"
SCORING_SCALE_VERSION = "scoring-scale-v1"
QUESTION_MAPPING_MATRIX_VERSION = "question-mapping-matrix-v1"
QUESTION_SCORING_TABLES_VERSION = "question-scoring-tables-v1"
OFFICIAL_DIMENSION_WEIGHT_SET_VERSION = "official-dimension-weight-set-v1"
READINESS_THRESHOLD_VALUES_VERSION = "readiness-threshold-values-v1"
READINESS_THRESHOLD_SET_VERSION = "readiness-threshold-set-v1"
READINESS_BOUNDARY_CONVENTION_VERSION = "readiness-boundary-convention-v1"
SEVERITY_DECISION_TABLE_SET_VERSION = "severity-decision-table-set-v1"
RISK_DECISION_TABLE_SET_VERSION = "risk-decision-table-set-v1"
CONFIDENCE_DECISION_TABLE_SET_VERSION = "confidence-decision-table-set-v1"
RECOMMENDATION_DECISION_TABLE_SET_VERSION = (
    "recommendation-decision-table-set-v1"
)
EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION = "executive-summary-template-set-v1"
GOLDEN_FIXTURE_CATALOG_VERSION = "golden-fixture-catalog-v1"
GOLDEN_FIXTURE_PAYLOADS_VERSION = "golden-fixture-payloads-v1"
REGRESSION_VALIDATION_FRAMEWORK_VERSION = "regression-validation-framework-v1"

PROCESS_OPERATIONAL_CONTROL = "POC"
GOVERNANCE_COMPLIANCE_REGULATORY_READINESS = "GCR"
TECHNOLOGY_INTELLIGENT_SYSTEMS_MANAGEMENT = "TISM"
DATA_PRIVACY_SECURITY_CONTROLS = "DPSC"
REMEDIATION_VERIFICATION_CONTINUOUS_IMPROVEMENT = "RVCI"

APPROVED_DIMENSION_ORDER = (
    PROCESS_OPERATIONAL_CONTROL,
    GOVERNANCE_COMPLIANCE_REGULATORY_READINESS,
    TECHNOLOGY_INTELLIGENT_SYSTEMS_MANAGEMENT,
    DATA_PRIVACY_SECURITY_CONTROLS,
    REMEDIATION_VERIFICATION_CONTINUOUS_IMPROVEMENT,
)

APPROVED_READINESS_LEVEL_ORDER = (
    "not-ready",
    "developing",
    "ready",
    "advanced",
)
INCOMPLETE_OPERATIONAL_STATE = "incomplete"

APPROVED_SEVERITY_LEVEL_ORDER = (
    "critical",
    "high",
    "medium",
    "low",
    "informational",
)

APPROVED_FINDING_TYPE_ORDER = (
    "deficiency",
    "observation",
    "strength",
    "opportunity",
)

APPROVED_RISK_LEVEL_ORDER = (
    "critical-risk",
    "elevated-risk",
    "moderate-risk",
    "low-risk",
    "minimal-informational",
)

APPROVED_CONFIDENCE_LEVEL_ORDER = (
    "very-high-confidence",
    "high-confidence",
    "moderate-confidence",
    "low-confidence",
    "insufficient-confidence",
)

APPROVED_RECOMMENDATION_LABEL_ORDER = (
    "immediate-action",
    "priority-action",
    "planned-improvement",
    "best-practice",
    "monitor",
)


@dataclass(frozen=True)
class MethodologyVersionManifest:
    methodology_version: str
    production_authority_release_version: str
    runtime_config_version: str
    taxonomy_version: str
    scoring_scale_version: str
    question_mapping_matrix_version: str
    question_scoring_tables_version: str
    official_dimension_weight_set_version: str
    readiness_threshold_values_version: str
    readiness_threshold_set_version: str
    readiness_boundary_convention_version: str
    severity_decision_table_set_version: str
    risk_decision_table_set_version: str
    confidence_decision_table_set_version: str
    recommendation_decision_table_set_version: str
    executive_summary_template_set_version: str
    golden_fixture_catalog_version: str
    golden_fixture_payloads_version: str
    regression_validation_framework_version: str


@dataclass(frozen=True)
class BusinessCapabilityDimensionRuntimeConfig:
    id: str
    label: str
    weight: int
    expected_primary_question_count: int


@dataclass(frozen=True)
class ResponseModelRuntimeConfig:
    id: str
    scoring_scale_version: str
    allowed_response_scores: Mapping[object, int]
    numeric_minimum: int | None = None
    numeric_maximum: int | None = None
    identity_numeric_mapping: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.allowed_response_scores, Mapping):
            object.__setattr__(
                self,
                "allowed_response_scores",
                MappingProxyType(dict(self.allowed_response_scores)),
            )


@dataclass(frozen=True)
class QuestionRuntimeConfig:
    id: str
    text: str
    primary_dimension: str
    secondary_dimensions: tuple[str, ...]
    mapping_rationale: str
    taxonomy_version: str
    response_model_id: str
    scoring_table_version: str


@dataclass(frozen=True)
class ReadinessThresholdRuntimeConfig:
    id: str
    label: str
    lower_bound: int
    upper_bound: int
    lower_inclusive: bool
    upper_inclusive: bool


@dataclass(frozen=True)
class DecisionRuleRuntimeConfig:
    id: str
    output: str
    table_version: str


@dataclass(frozen=True)
class ExecutiveSummarySectionRuntimeConfig:
    id: str
    heading: str
    order: int
    template_id: str
    template_version: str


@dataclass(frozen=True)
class GoldenFixtureRuntimeConfig:
    id: str
    purpose: str
    catalog_version: str
    payload_version: str
    methodology_version: str


@dataclass(frozen=True)
class ApprovedMethodologyRuntimeConfig:
    version_manifest: MethodologyVersionManifest
    dimensions: Mapping[str, BusinessCapabilityDimensionRuntimeConfig]
    response_models: Mapping[str, ResponseModelRuntimeConfig]
    questions: Mapping[str, QuestionRuntimeConfig]
    readiness_thresholds: Mapping[str, ReadinessThresholdRuntimeConfig]
    severity_levels: tuple[str, ...]
    finding_types: tuple[str, ...]
    risk_levels: tuple[str, ...]
    confidence_levels: tuple[str, ...]
    recommendation_labels: tuple[str, ...]
    severity_decision_rules: Mapping[str, DecisionRuleRuntimeConfig]
    risk_decision_rules: Mapping[str, DecisionRuleRuntimeConfig]
    confidence_decision_rules: Mapping[str, DecisionRuleRuntimeConfig]
    recommendation_decision_rules: Mapping[str, DecisionRuleRuntimeConfig]
    executive_summary_sections: Mapping[str, ExecutiveSummarySectionRuntimeConfig]
    golden_fixtures: Mapping[str, GoldenFixtureRuntimeConfig]
    artifact_inventory: Mapping[str, str]

    def __post_init__(self) -> None:
        for field_name in (
            "dimensions",
            "response_models",
            "questions",
            "readiness_thresholds",
            "severity_decision_rules",
            "risk_decision_rules",
            "confidence_decision_rules",
            "recommendation_decision_rules",
            "executive_summary_sections",
            "golden_fixtures",
            "artifact_inventory",
        ):
            value = getattr(self, field_name)
            if isinstance(value, Mapping):
                object.__setattr__(self, field_name, MappingProxyType(dict(value)))


def validate_approved_methodology_runtime_config(
    config: object,
) -> None:
    if not isinstance(config, ApprovedMethodologyRuntimeConfig):
        raise ValueError(
            "Approved methodology runtime config must be an "
            "ApprovedMethodologyRuntimeConfig."
        )

    _validate_version_manifest(config.version_manifest)
    _validate_mapping_ids("dimension", config.dimensions)
    _validate_mapping_ids("response model", config.response_models)
    _validate_mapping_ids("question", config.questions)
    _validate_mapping_ids("readiness threshold", config.readiness_thresholds)
    _validate_mapping_ids("severity decision rule", config.severity_decision_rules)
    _validate_mapping_ids("risk decision rule", config.risk_decision_rules)
    _validate_mapping_ids("confidence decision rule", config.confidence_decision_rules)
    _validate_mapping_ids(
        "recommendation decision rule",
        config.recommendation_decision_rules,
    )
    _validate_mapping_ids(
        "executive summary section",
        config.executive_summary_sections,
    )
    _validate_mapping_ids("golden fixture", config.golden_fixtures)
    _validate_response_models(config.response_models)
    _validate_questions(config)
    _validate_dimensions(config)
    _validate_readiness_thresholds(config.readiness_thresholds)
    _validate_taxonomy_tuple(
        "severity level",
        config.severity_levels,
        APPROVED_SEVERITY_LEVEL_ORDER,
    )
    _validate_taxonomy_tuple(
        "finding type",
        config.finding_types,
        APPROVED_FINDING_TYPE_ORDER,
    )
    _validate_taxonomy_tuple("risk level", config.risk_levels, APPROVED_RISK_LEVEL_ORDER)
    _validate_taxonomy_tuple(
        "confidence level",
        config.confidence_levels,
        APPROVED_CONFIDENCE_LEVEL_ORDER,
    )
    _validate_taxonomy_tuple(
        "recommendation label",
        config.recommendation_labels,
        APPROVED_RECOMMENDATION_LABEL_ORDER,
    )
    _validate_decision_rules(
        "severity",
        config.severity_decision_rules,
        SEVERITY_DECISION_TABLE_SET_VERSION,
        config.severity_levels,
    )
    _validate_decision_rules(
        "risk",
        config.risk_decision_rules,
        RISK_DECISION_TABLE_SET_VERSION,
        config.risk_levels,
    )
    _validate_decision_rules(
        "confidence",
        config.confidence_decision_rules,
        CONFIDENCE_DECISION_TABLE_SET_VERSION,
        config.confidence_levels,
    )
    _validate_decision_rules(
        "recommendation",
        config.recommendation_decision_rules,
        RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        config.recommendation_labels,
    )
    _validate_executive_summary_sections(config.executive_summary_sections)
    _validate_golden_fixtures(config.golden_fixtures)
    _validate_artifact_inventory(config.artifact_inventory)


def _validate_version_manifest(manifest: MethodologyVersionManifest) -> None:
    expected_versions = {
        "methodology_version": METHODOLOGY_VERSION,
        "production_authority_release_version": PRODUCTION_AUTHORITY_RELEASE_VERSION,
        "runtime_config_version": APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
        "taxonomy_version": BUSINESS_CAPABILITY_TAXONOMY_VERSION,
        "scoring_scale_version": SCORING_SCALE_VERSION,
        "question_mapping_matrix_version": QUESTION_MAPPING_MATRIX_VERSION,
        "question_scoring_tables_version": QUESTION_SCORING_TABLES_VERSION,
        "official_dimension_weight_set_version": (
            OFFICIAL_DIMENSION_WEIGHT_SET_VERSION
        ),
        "readiness_threshold_values_version": READINESS_THRESHOLD_VALUES_VERSION,
        "readiness_threshold_set_version": READINESS_THRESHOLD_SET_VERSION,
        "readiness_boundary_convention_version": (
            READINESS_BOUNDARY_CONVENTION_VERSION
        ),
        "severity_decision_table_set_version": SEVERITY_DECISION_TABLE_SET_VERSION,
        "risk_decision_table_set_version": RISK_DECISION_TABLE_SET_VERSION,
        "confidence_decision_table_set_version": (
            CONFIDENCE_DECISION_TABLE_SET_VERSION
        ),
        "recommendation_decision_table_set_version": (
            RECOMMENDATION_DECISION_TABLE_SET_VERSION
        ),
        "executive_summary_template_set_version": (
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION
        ),
        "golden_fixture_catalog_version": GOLDEN_FIXTURE_CATALOG_VERSION,
        "golden_fixture_payloads_version": GOLDEN_FIXTURE_PAYLOADS_VERSION,
        "regression_validation_framework_version": (
            REGRESSION_VALIDATION_FRAMEWORK_VERSION
        ),
    }
    for field_name, expected in expected_versions.items():
        if getattr(manifest, field_name) != expected:
            raise ValueError(f"Unsupported methodology version field: {field_name}")


def _validate_mapping_ids(name: str, values: Mapping[str, object]) -> None:
    if not values:
        raise ValueError(f"At least one {name} is required.")
    for key, value in values.items():
        if not isinstance(key, str) or not key:
            raise ValueError(f"Invalid {name} key.")
        if not hasattr(value, "id") or getattr(value, "id") != key:
            raise ValueError(f"{name.title()} key must match object id: {key}")


def _validate_dimensions(config: ApprovedMethodologyRuntimeConfig) -> None:
    if tuple(config.dimensions) != APPROVED_DIMENSION_ORDER:
        raise ValueError("Approved Business Capability Dimensions are invalid.")

    if sum(dimension.weight for dimension in config.dimensions.values()) != 100:
        raise ValueError("Approved dimension weights must sum to 100.")

    question_counts = {
        dimension_id: 0
        for dimension_id in config.dimensions
    }
    for question in config.questions.values():
        question_counts[question.primary_dimension] += 1

    for dimension_id, dimension in config.dimensions.items():
        if dimension.expected_primary_question_count <= 0:
            raise ValueError(
                f"Dimension must contain at least one question: {dimension_id}"
            )
        if question_counts[dimension_id] != dimension.expected_primary_question_count:
            raise ValueError(
                "Dimension question count mismatch: "
                f"{dimension_id}"
            )


def _validate_response_models(
    response_models: Mapping[str, ResponseModelRuntimeConfig],
) -> None:
    scale_model = response_models.get("scale-0-4")
    if scale_model is None:
        raise ValueError("Missing response model: scale-0-4")
    if dict(scale_model.allowed_response_scores) != {
        0: 0,
        1: 25,
        2: 50,
        3: 75,
        4: 100,
    }:
        raise ValueError("scale-0-4 response mapping is invalid.")
    if scale_model.scoring_scale_version != SCORING_SCALE_VERSION:
        raise ValueError("scale-0-4 scoring scale version is unsupported.")

    numeric_model = response_models.get("numeric-0-100")
    if numeric_model is None:
        raise ValueError("Missing response model: numeric-0-100")
    if (
        numeric_model.numeric_minimum != 0
        or numeric_model.numeric_maximum != 100
        or not numeric_model.identity_numeric_mapping
    ):
        raise ValueError("numeric-0-100 response mapping is invalid.")
    if numeric_model.scoring_scale_version != SCORING_SCALE_VERSION:
        raise ValueError("numeric-0-100 scoring scale version is unsupported.")


def _validate_questions(config: ApprovedMethodologyRuntimeConfig) -> None:
    if len(config.questions) != 48:
        raise ValueError("Approved methodology must contain 48 canonical questions.")

    response_model_counts = {
        response_model_id: 0
        for response_model_id in config.response_models
    }
    for question in config.questions.values():
        if question.primary_dimension not in config.dimensions:
            raise ValueError(f"Unknown Primary Dimension: {question.id}")
        if len(question.secondary_dimensions) > 2:
            raise ValueError(f"Too many Secondary Dimensions: {question.id}")
        for secondary_dimension in question.secondary_dimensions:
            if secondary_dimension not in config.dimensions:
                raise ValueError(f"Unknown Secondary Dimension: {question.id}")
            if secondary_dimension == question.primary_dimension:
                raise ValueError(
                    "Secondary Dimension must differ from Primary Dimension: "
                    f"{question.id}"
                )
        if question.taxonomy_version != BUSINESS_CAPABILITY_TAXONOMY_VERSION:
            raise ValueError(f"Unsupported taxonomy version: {question.id}")
        if question.scoring_table_version != QUESTION_SCORING_TABLES_VERSION:
            raise ValueError(f"Unsupported scoring table version: {question.id}")
        if question.response_model_id not in config.response_models:
            raise ValueError(f"Unknown response model: {question.id}")
        if not question.text.strip():
            raise ValueError(f"Question text is required: {question.id}")
        if not question.mapping_rationale.strip():
            raise ValueError(f"Mapping rationale is required: {question.id}")
        response_model_counts[question.response_model_id] += 1

    if response_model_counts["scale-0-4"] != 47:
        raise ValueError("Expected 47 scale-0-4 question scoring tables.")
    if response_model_counts["numeric-0-100"] != 1:
        raise ValueError("Expected one numeric-0-100 question scoring table.")
    if (
        config.questions["q.automation.manual-volume"].response_model_id
        != "numeric-0-100"
    ):
        raise ValueError(
            "q.automation.manual-volume must use numeric-0-100 response model."
        )


def _validate_readiness_thresholds(
    thresholds: Mapping[str, ReadinessThresholdRuntimeConfig],
) -> None:
    if tuple(thresholds) != APPROVED_READINESS_LEVEL_ORDER:
        raise ValueError("Readiness threshold order is invalid.")
    expected_lower = 0
    for threshold in thresholds.values():
        if threshold.lower_bound != expected_lower:
            raise ValueError("Readiness thresholds contain a gap.")
        if not threshold.lower_inclusive:
            raise ValueError("Readiness threshold lower bound must be inclusive.")
        if threshold.id == "advanced":
            if threshold.upper_bound != 100 or not threshold.upper_inclusive:
                raise ValueError("Advanced readiness threshold must include 100.")
            expected_lower = threshold.upper_bound
        else:
            if threshold.upper_inclusive:
                raise ValueError(
                    "Readiness threshold upper bound must be exclusive before "
                    "Advanced."
                )
            expected_lower = threshold.upper_bound
    if expected_lower != 100:
        raise ValueError("Readiness thresholds must cover 0 through 100.")


def _validate_taxonomy_tuple(
    name: str,
    observed: tuple[str, ...],
    expected: tuple[str, ...],
) -> None:
    if observed != expected:
        raise ValueError(f"Approved {name} taxonomy is invalid.")


def _validate_decision_rules(
    name: str,
    rules: Mapping[str, DecisionRuleRuntimeConfig],
    expected_version: str,
    approved_outputs: tuple[str, ...],
) -> None:
    for rule in rules.values():
        if rule.table_version != expected_version:
            raise ValueError(f"Unsupported {name} decision table version: {rule.id}")
        if rule.output and rule.output not in approved_outputs:
            raise ValueError(f"Unsupported {name} decision rule output: {rule.id}")


def _validate_executive_summary_sections(
    sections: Mapping[str, ExecutiveSummarySectionRuntimeConfig],
) -> None:
    expected_ids = (
        "overall-assessment-overview",
        "business-capability-highlights",
        "significant-findings",
        "risk-overview",
        "confidence-statement",
        "recommended-actions",
        "closing-assessment-statement",
    )
    if tuple(sections) != expected_ids:
        raise ValueError("Executive Summary section order is invalid.")
    for index, section in enumerate(sections.values(), start=1):
        if section.order != index:
            raise ValueError(f"Executive Summary section order mismatch: {section.id}")
        if section.template_version != EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION:
            raise ValueError(
                f"Unsupported Executive Summary template version: {section.id}"
            )


def _validate_golden_fixtures(
    fixtures: Mapping[str, GoldenFixtureRuntimeConfig],
) -> None:
    if len(fixtures) != 15:
        raise ValueError("Golden Fixture payload catalog must contain 15 fixtures.")
    for fixture in fixtures.values():
        if fixture.catalog_version != GOLDEN_FIXTURE_CATALOG_VERSION:
            raise ValueError(f"Unsupported Golden Fixture catalog version: {fixture.id}")
        if fixture.payload_version != GOLDEN_FIXTURE_PAYLOADS_VERSION:
            raise ValueError(f"Unsupported Golden Fixture payload version: {fixture.id}")
        if fixture.methodology_version != METHODOLOGY_VERSION:
            raise ValueError(f"Unsupported Golden Fixture methodology version: {fixture.id}")
        if not fixture.purpose.strip():
            raise ValueError(f"Golden Fixture purpose is required: {fixture.id}")


def _validate_artifact_inventory(inventory: Mapping[str, str]) -> None:
    required_artifacts = (
        "business-decision-methodology",
        "assessment-methodology-specification-v1",
        "question-mapping-matrix-v1",
        "dimension-weight-reference-candidates-v1",
        "official-dimension-weight-set-v1",
        "scoring-scale-specification-v1",
        "question-scoring-tables-specification-v1",
        "question-scoring-tables-v1",
        "readiness-threshold-specification-v1",
        "readiness-threshold-values-v1",
        "severity-decision-tables-specification-v1",
        "severity-decision-tables-v1",
        "risk-decision-tables-specification-v1",
        "risk-decision-tables-v1",
        "confidence-decision-tables-specification-v1",
        "confidence-decision-tables-v1",
        "recommendation-decision-tables-specification-v1",
        "recommendation-decision-tables-v1",
        "executive-summary-templates-v1",
        "golden-fixtures-v1",
        "golden-fixture-payloads-v1",
        "regression-validation-framework-v1",
        "production-authority-release-v1",
    )
    if tuple(inventory) != required_artifacts:
        raise ValueError("Approved artifact inventory is invalid.")
    for artifact_id, path in inventory.items():
        if not path.startswith("docs/business-decision-methodology/"):
            raise ValueError(f"Artifact path is outside methodology docs: {artifact_id}")


def _map_by_id(values):
    mapped = {}
    for value in values:
        if value.id in mapped:
            raise ValueError(f"Duplicate approved methodology id: {value.id}")
        mapped[value.id] = value
    return MappingProxyType(mapped)


VERSION_MANIFEST = MethodologyVersionManifest(
    methodology_version=METHODOLOGY_VERSION,
    production_authority_release_version=PRODUCTION_AUTHORITY_RELEASE_VERSION,
    runtime_config_version=APPROVED_METHODOLOGY_RUNTIME_CONFIG_VERSION,
    taxonomy_version=BUSINESS_CAPABILITY_TAXONOMY_VERSION,
    scoring_scale_version=SCORING_SCALE_VERSION,
    question_mapping_matrix_version=QUESTION_MAPPING_MATRIX_VERSION,
    question_scoring_tables_version=QUESTION_SCORING_TABLES_VERSION,
    official_dimension_weight_set_version=OFFICIAL_DIMENSION_WEIGHT_SET_VERSION,
    readiness_threshold_values_version=READINESS_THRESHOLD_VALUES_VERSION,
    readiness_threshold_set_version=READINESS_THRESHOLD_SET_VERSION,
    readiness_boundary_convention_version=READINESS_BOUNDARY_CONVENTION_VERSION,
    severity_decision_table_set_version=SEVERITY_DECISION_TABLE_SET_VERSION,
    risk_decision_table_set_version=RISK_DECISION_TABLE_SET_VERSION,
    confidence_decision_table_set_version=CONFIDENCE_DECISION_TABLE_SET_VERSION,
    recommendation_decision_table_set_version=(
        RECOMMENDATION_DECISION_TABLE_SET_VERSION
    ),
    executive_summary_template_set_version=EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
    golden_fixture_catalog_version=GOLDEN_FIXTURE_CATALOG_VERSION,
    golden_fixture_payloads_version=GOLDEN_FIXTURE_PAYLOADS_VERSION,
    regression_validation_framework_version=REGRESSION_VALIDATION_FRAMEWORK_VERSION,
)


APPROVED_DIMENSIONS = _map_by_id(
    (
        BusinessCapabilityDimensionRuntimeConfig(
            PROCESS_OPERATIONAL_CONTROL,
            "Process & Operational Control",
            18,
            14,
        ),
        BusinessCapabilityDimensionRuntimeConfig(
            GOVERNANCE_COMPLIANCE_REGULATORY_READINESS,
            "Governance, Compliance & Regulatory Readiness",
            24,
            12,
        ),
        BusinessCapabilityDimensionRuntimeConfig(
            TECHNOLOGY_INTELLIGENT_SYSTEMS_MANAGEMENT,
            "Technology & Intelligent Systems Management",
            22,
            12,
        ),
        BusinessCapabilityDimensionRuntimeConfig(
            DATA_PRIVACY_SECURITY_CONTROLS,
            "Data, Privacy & Security Controls",
            20,
            4,
        ),
        BusinessCapabilityDimensionRuntimeConfig(
            REMEDIATION_VERIFICATION_CONTINUOUS_IMPROVEMENT,
            "Remediation, Verification & Continuous Improvement",
            16,
            6,
        ),
    )
)


APPROVED_RESPONSE_MODELS = _map_by_id(
    (
        ResponseModelRuntimeConfig(
            "scale-0-4",
            SCORING_SCALE_VERSION,
            MappingProxyType({0: 0, 1: 25, 2: 50, 3: 75, 4: 100}),
        ),
        ResponseModelRuntimeConfig(
            "numeric-0-100",
            SCORING_SCALE_VERSION,
            MappingProxyType({}),
            numeric_minimum=0,
            numeric_maximum=100,
            identity_numeric_mapping=True,
        ),
    )
)


def _scale_question(
    question_id: str,
    text: str,
    primary_dimension: str,
    secondary_dimensions: tuple[str, ...],
    rationale: str,
) -> QuestionRuntimeConfig:
    return QuestionRuntimeConfig(
        question_id,
        text,
        primary_dimension,
        secondary_dimensions,
        rationale,
        BUSINESS_CAPABILITY_TAXONOMY_VERSION,
        "scale-0-4",
        QUESTION_SCORING_TABLES_VERSION,
    )


def _numeric_question(
    question_id: str,
    text: str,
    primary_dimension: str,
    secondary_dimensions: tuple[str, ...],
    rationale: str,
) -> QuestionRuntimeConfig:
    return QuestionRuntimeConfig(
        question_id,
        text,
        primary_dimension,
        secondary_dimensions,
        rationale,
        BUSINESS_CAPABILITY_TAXONOMY_VERSION,
        "numeric-0-100",
        QUESTION_SCORING_TABLES_VERSION,
    )


APPROVED_QUESTIONS = _map_by_id(
    (
        _scale_question(
            "q.ai.strategy.business-goals",
            "Align AI initiatives to measurable business goals.",
            "GCR",
            ("TISM",),
            "Primary mapping is governance and oversight because the question "
            "evaluates whether AI work is directed by business goals.",
        ),
        _scale_question(
            "q.ai.leadership.sponsor",
            "Assign executive sponsorship for AI adoption.",
            "GCR",
            (),
            "Primary mapping is governance and accountability because the question "
            "evaluates executive sponsorship and decision ownership.",
        ),
        _scale_question(
            "q.ai.governance.owner",
            "Establish accountable AI governance ownership.",
            "GCR",
            ("TISM",),
            "Primary mapping is governance because the question evaluates "
            "accountable AI oversight.",
        ),
        _scale_question(
            "q.ai.use-cases.prioritized",
            "Prioritize AI use cases by business value and feasibility.",
            "TISM",
            ("GCR",),
            "Primary mapping is technology and intelligent systems management "
            "because the question evaluates AI use-case lifecycle prioritization.",
        ),
        _scale_question(
            "q.ai.success-metrics.defined",
            "Define success metrics for AI initiatives.",
            "RVCI",
            ("GCR",),
            "Primary mapping is remediation and continuous improvement because "
            "the question evaluates measurable feedback for AI initiatives.",
        ),
        _scale_question(
            "q.ai.risk-policy.approved",
            "Maintain approved policy for acceptable AI use.",
            "GCR",
            ("TISM",),
            "Primary mapping is governance and compliance readiness because the "
            "question evaluates approved policy and acceptable-use oversight.",
        ),
        _scale_question(
            "q.security.identity.mfa",
            "Protect user access with strong authentication.",
            "DPSC",
            ("GCR",),
            "Primary mapping is data, privacy, and security controls because the "
            "question evaluates access protection.",
        ),
        _scale_question(
            "q.security.access.review",
            "Review access rights on a recurring basis.",
            "DPSC",
            ("GCR",),
            "Primary mapping is data, privacy, and security controls because the "
            "question evaluates access control review.",
        ),
        _scale_question(
            "q.security.data.classification",
            "Classify business and customer data by sensitivity.",
            "DPSC",
            (),
            "Primary mapping is data, privacy, and security controls because the "
            "question evaluates data classification and sensitivity handling.",
        ),
        _scale_question(
            "q.security.incident-response.owner",
            "Assign incident response ownership and escalation.",
            "POC",
            ("DPSC",),
            "Primary mapping is process and operational control because the "
            "question evaluates incident response ownership and escalation execution.",
        ),
        _scale_question(
            "q.security.vendor.controls",
            "Assess vendor and third-party security controls.",
            "TISM",
            ("DPSC",),
            "Primary mapping is technology and intelligent systems management "
            "because Decision 2 places vendor management in this dimension.",
        ),
        _scale_question(
            "q.security.backup.recovery-tested",
            "Test recovery from backup or continuity procedures.",
            "RVCI",
            ("POC",),
            "Primary mapping is remediation, verification, and continuous "
            "improvement because the question evaluates tested recovery.",
        ),
        _scale_question(
            "q.knowledge.docs.current",
            "Maintain current documentation for key business processes.",
            "POC",
            ("RVCI",),
            "Primary mapping is process and operational control because the "
            "question evaluates documented business processes.",
        ),
        _scale_question(
            "q.knowledge.owner.defined",
            "Assign owners for critical knowledge assets.",
            "POC",
            ("GCR",),
            "Primary mapping is process and operational control because the "
            "question evaluates operational ownership of knowledge assets.",
        ),
        _scale_question(
            "q.knowledge.searchable",
            "Make operational knowledge searchable and reusable.",
            "TISM",
            ("POC",),
            "Primary mapping is technology and intelligent systems management "
            "because the question evaluates technology-enabled knowledge retrieval.",
        ),
        _scale_question(
            "q.knowledge.sme-dependency",
            "Reduce dependency on single subject matter experts.",
            "POC",
            (),
            "Primary mapping is process and operational control because the "
            "question evaluates whether operations can run consistently without "
            "single-person dependency.",
        ),
        _scale_question(
            "q.knowledge.refresh-cadence",
            "Review and refresh knowledge assets on a defined cadence.",
            "RVCI",
            ("POC",),
            "Primary mapping is remediation, verification, and continuous "
            "improvement because the question evaluates recurring review and refresh.",
        ),
        _scale_question(
            "q.knowledge.customer-context",
            "Capture customer context and decision history consistently.",
            "POC",
            ("GCR",),
            "Primary mapping is process and operational control because the "
            "question evaluates consistent capture of business context.",
        ),
        _scale_question(
            "q.automation.process-documented",
            "Document processes before automation.",
            "POC",
            ("TISM",),
            "Primary mapping is process and operational control because the "
            "question evaluates process documentation.",
        ),
        _numeric_question(
            "q.automation.manual-volume",
            "Identify high-volume manual work suitable for automation.",
            "POC",
            ("TISM",),
            "Primary mapping is process and operational control because the "
            "question evaluates process demand and execution burden.",
        ),
        _scale_question(
            "q.automation.exception-handling",
            "Define exception handling and ownership for automated workflows.",
            "POC",
            ("TISM",),
            "Primary mapping is process and operational control because the "
            "question evaluates exception handling and ownership.",
        ),
        _scale_question(
            "q.automation.integration-readiness",
            "Confirm systems expose reliable integration paths.",
            "TISM",
            ("POC",),
            "Primary mapping is technology and intelligent systems management "
            "because the question evaluates integration capability.",
        ),
        _scale_question(
            "q.automation.measurement",
            "Measure automation outcomes and process impact.",
            "RVCI",
            ("POC",),
            "Primary mapping is remediation, verification, and continuous "
            "improvement because the question evaluates outcome measurement.",
        ),
        _scale_question(
            "q.automation.change-control",
            "Govern changes to automated workflows.",
            "GCR",
            ("TISM",),
            "Primary mapping is governance and compliance readiness because the "
            "question evaluates governed change control.",
        ),
        _scale_question(
            "q.engineering.source-control",
            "Manage application and automation code in source control.",
            "TISM",
            ("RVCI",),
            "Primary mapping is technology and intelligent systems management "
            "because the question evaluates lifecycle control over code.",
        ),
        _scale_question(
            "q.engineering.testing",
            "Validate changes with repeatable tests.",
            "RVCI",
            ("TISM",),
            "Primary mapping is remediation, verification, and continuous "
            "improvement because the question evaluates repeatable validation.",
        ),
        _scale_question(
            "q.engineering.release-process",
            "Use a controlled release process.",
            "TISM",
            ("POC",),
            "Primary mapping is technology and intelligent systems management "
            "because the question evaluates release lifecycle control.",
        ),
        _scale_question(
            "q.engineering.observability",
            "Monitor systems with actionable logs, metrics, or alerts.",
            "TISM",
            ("RVCI",),
            "Primary mapping is technology and intelligent systems management "
            "because the question evaluates monitoring of systems.",
        ),
        _scale_question(
            "q.engineering.backlog-prioritization",
            "Prioritize technical work by business impact.",
            "GCR",
            ("TISM",),
            "Primary mapping is governance and compliance readiness because the "
            "question evaluates business oversight of priorities.",
        ),
        _scale_question(
            "q.engineering.ownership",
            "Assign ownership for systems and operational support.",
            "TISM",
            ("GCR",),
            "Primary mapping is technology and intelligent systems management "
            "because the question evaluates accountability for systems.",
        ),
        _scale_question(
            "q.cloud.account-structure",
            "Maintain governed cloud account or environment structure.",
            "TISM",
            ("GCR",),
            "Primary mapping is technology and intelligent systems management "
            "because the question evaluates cloud environment lifecycle structure.",
        ),
        _scale_question(
            "q.cloud.cost-controls",
            "Monitor and control cloud spend.",
            "TISM",
            ("GCR",),
            "Primary mapping is technology and intelligent systems management "
            "because the question evaluates operational control of cloud systems.",
        ),
        _scale_question(
            "q.cloud.security-baseline",
            "Apply baseline cloud security controls.",
            "DPSC",
            ("TISM",),
            "Primary mapping is data, privacy, and security controls because the "
            "question evaluates security baseline controls.",
        ),
        _scale_question(
            "q.cloud.infrastructure-as-code",
            "Manage cloud configuration through repeatable deployment practices.",
            "TISM",
            ("RVCI",),
            "Primary mapping is technology and intelligent systems management "
            "because the question evaluates controlled cloud configuration lifecycle.",
        ),
        _scale_question(
            "q.cloud.resilience",
            "Define resilience, backup, or recovery expectations for cloud workloads.",
            "POC",
            ("TISM",),
            "Primary mapping is process and operational control because the "
            "question evaluates operational reliability expectations.",
        ),
        _scale_question(
            "q.cloud.monitoring",
            "Monitor cloud workload health and operational status.",
            "TISM",
            ("POC",),
            "Primary mapping is technology and intelligent systems management "
            "because the question evaluates monitoring of cloud workloads.",
        ),
        _scale_question(
            "q.operations.process-ownership",
            "Assign accountable owners for critical business processes.",
            "POC",
            ("GCR",),
            "Primary mapping is process and operational control because the "
            "question evaluates business process ownership.",
        ),
        _scale_question(
            "q.operations.kpi-defined",
            "Define operational KPIs for key processes.",
            "RVCI",
            ("POC",),
            "Primary mapping is remediation, verification, and continuous "
            "improvement because the question evaluates measurement for improvement.",
        ),
        _scale_question(
            "q.operations.escalation-path",
            "Define escalation paths for operational issues.",
            "POC",
            ("GCR",),
            "Primary mapping is process and operational control because the "
            "question evaluates operational escalation execution.",
        ),
        _scale_question(
            "q.operations.capacity-planning",
            "Plan capacity for people, systems, and process demand.",
            "POC",
            (),
            "Primary mapping is process and operational control because the "
            "question evaluates operational planning for reliable execution.",
        ),
        _scale_question(
            "q.operations.change-management",
            "Manage operational change with communication and ownership.",
            "POC",
            ("GCR",),
            "Primary mapping is process and operational control because the "
            "question evaluates change execution.",
        ),
        _scale_question(
            "q.operations.continuity",
            "Maintain continuity plans for critical operations.",
            "POC",
            ("RVCI",),
            "Primary mapping is process and operational control because the "
            "question evaluates continuity of critical operations.",
        ),
        _scale_question(
            "q.business.outcomes-defined",
            "Define target business outcomes for technology initiatives.",
            "GCR",
            ("RVCI",),
            "Primary mapping is governance and compliance readiness because the "
            "question evaluates business oversight of initiative outcomes.",
        ),
        _scale_question(
            "q.business.customer-impact",
            "Connect initiatives to measurable customer impact.",
            "GCR",
            ("RVCI",),
            "Primary mapping is governance and compliance readiness because the "
            "question evaluates business accountability for customer impact.",
        ),
        _scale_question(
            "q.business.financial-case",
            "Define cost, benefit, or investment rationale.",
            "GCR",
            (),
            "Primary mapping is governance and compliance readiness because the "
            "question evaluates investment rationale and business oversight.",
        ),
        _scale_question(
            "q.business.executive-alignment",
            "Align executive stakeholders on priority and timing.",
            "GCR",
            (),
            "Primary mapping is governance and compliance readiness because the "
            "question evaluates executive alignment and oversight.",
        ),
        _scale_question(
            "q.business.risk-appetite",
            "Define acceptable risk for AI, automation, and cloud initiatives.",
            "GCR",
            (),
            "Primary mapping is governance and compliance readiness because the "
            "question evaluates organizational risk appetite and accountability.",
        ),
        _scale_question(
            "q.business.decision-cadence",
            "Maintain a regular decision cadence for transformation initiatives.",
            "GCR",
            ("POC",),
            "Primary mapping is governance and compliance readiness because the "
            "question evaluates decision cadence and executive accountability.",
        ),
    )
)


APPROVED_READINESS_THRESHOLDS = _map_by_id(
    (
        ReadinessThresholdRuntimeConfig("not-ready", "Not Ready", 0, 25, True, False),
        ReadinessThresholdRuntimeConfig("developing", "Developing", 25, 50, True, False),
        ReadinessThresholdRuntimeConfig("ready", "Ready", 50, 75, True, False),
        ReadinessThresholdRuntimeConfig("advanced", "Advanced", 75, 100, True, True),
    )
)


SEVERITY_DECISION_RULES = _map_by_id(
    (
        DecisionRuleRuntimeConfig(
            "severity-v1-deficiency-critical",
            "critical",
            SEVERITY_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "severity-v1-deficiency-high",
            "high",
            SEVERITY_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "severity-v1-deficiency-medium",
            "medium",
            SEVERITY_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "severity-v1-deficiency-low",
            "low",
            SEVERITY_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "severity-v1-observation-informational",
            "informational",
            SEVERITY_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "severity-v1-strength-informational",
            "informational",
            SEVERITY_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "severity-v1-opportunity-informational",
            "informational",
            SEVERITY_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "severity-v1-reject-nondefect-defect-consequence",
            "",
            SEVERITY_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "severity-v1-reject-deficiency-informational-consequence",
            "",
            SEVERITY_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "severity-v1-reject-unsupported-finding-type",
            "",
            SEVERITY_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "severity-v1-reject-unsupported-consequence",
            "",
            SEVERITY_DECISION_TABLE_SET_VERSION,
        ),
    )
)


RISK_DECISION_RULES = _map_by_id(
    (
        DecisionRuleRuntimeConfig(
            "risk-v1-critical-any-critical",
            "critical-risk",
            RISK_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "risk-v1-elevated-high-concentration",
            "elevated-risk",
            RISK_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "risk-v1-moderate-single-high",
            "moderate-risk",
            RISK_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "risk-v1-moderate-any-medium",
            "moderate-risk",
            RISK_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "risk-v1-low-low-only-defects",
            "low-risk",
            RISK_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "risk-v1-minimal-informational-only",
            "minimal-informational",
            RISK_DECISION_TABLE_SET_VERSION,
        ),
    )
)


CONFIDENCE_DECISION_RULES = _map_by_id(
    (
        DecisionRuleRuntimeConfig(
            "confidence-v1-insufficient-unassertable",
            "insufficient-confidence",
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "confidence-v1-low-basic-only",
            "low-confidence",
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "confidence-v1-moderate-mixed-basic-adequate",
            "moderate-confidence",
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "confidence-v1-high-strong-present",
            "high-confidence",
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "confidence-v1-very-high-strong-only",
            "very-high-confidence",
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "confidence-v1-reject-missing-required-evidence",
            "",
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "confidence-v1-reject-incomplete-assessment",
            "",
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "confidence-v1-reject-missing-upstream-artifact",
            "",
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "confidence-v1-reject-unsupported-confidence-level",
            "",
            CONFIDENCE_DECISION_TABLE_SET_VERSION,
        ),
    )
)


RECOMMENDATION_DECISION_RULES = _map_by_id(
    (
        DecisionRuleRuntimeConfig(
            "recommendation-v1-deficiency-critical-immediate",
            "immediate-action",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-deficiency-high-priority",
            "priority-action",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-deficiency-medium-planned",
            "planned-improvement",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-deficiency-low-planned",
            "planned-improvement",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-observation-monitor",
            "monitor",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-strength-best-practice",
            "best-practice",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-opportunity-best-practice",
            "best-practice",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-no-findings-monitor",
            "monitor",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-reject-missing-finding-collection",
            "",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-reject-missing-severity",
            "",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-reject-unsupported-finding-severity-combination",
            "",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-reject-missing-risk",
            "",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-reject-missing-confidence",
            "",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-reject-missing-context",
            "",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-reject-unsupported-recommendation-label",
            "",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
        DecisionRuleRuntimeConfig(
            "recommendation-v1-reject-duplicate-output",
            "",
            RECOMMENDATION_DECISION_TABLE_SET_VERSION,
        ),
    )
)


EXECUTIVE_SUMMARY_SECTIONS = _map_by_id(
    (
        ExecutiveSummarySectionRuntimeConfig(
            "overall-assessment-overview",
            "Overall Assessment Overview",
            1,
            "executive-summary-v1-overall-assessment-overview",
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
        ),
        ExecutiveSummarySectionRuntimeConfig(
            "business-capability-highlights",
            "Business Capability Highlights",
            2,
            "executive-summary-v1-business-capability-highlights",
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
        ),
        ExecutiveSummarySectionRuntimeConfig(
            "significant-findings",
            "Significant Findings",
            3,
            "executive-summary-v1-significant-findings",
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
        ),
        ExecutiveSummarySectionRuntimeConfig(
            "risk-overview",
            "Risk Overview",
            4,
            "executive-summary-v1-risk-overview",
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
        ),
        ExecutiveSummarySectionRuntimeConfig(
            "confidence-statement",
            "Confidence Statement",
            5,
            "executive-summary-v1-confidence-statement",
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
        ),
        ExecutiveSummarySectionRuntimeConfig(
            "recommended-actions",
            "Recommended Actions",
            6,
            "executive-summary-v1-recommended-actions",
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
        ),
        ExecutiveSummarySectionRuntimeConfig(
            "closing-assessment-statement",
            "Closing Assessment Statement",
            7,
            "executive-summary-v1-closing-assessment-statement",
            EXECUTIVE_SUMMARY_TEMPLATE_SET_VERSION,
        ),
    )
)


GOLDEN_FIXTURES = _map_by_id(
    (
        GoldenFixtureRuntimeConfig(
            "fixture-v1-complete-minimal-risk",
            "Validate complete processing for minimal or informational risk.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-complete-not-ready-readiness",
            "Validate Not Ready readiness assignment.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-complete-developing-readiness",
            "Validate Developing readiness assignment.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-complete-ready-readiness",
            "Validate Ready readiness assignment.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-complete-advanced-readiness",
            "Validate Advanced readiness assignment.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-critical-finding-risk",
            "Validate Critical Severity and Critical Risk propagation.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-high-concentration-risk",
            "Validate High Severity concentration and Elevated Risk propagation.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-medium-risk",
            "Validate Medium Severity and Moderate Risk propagation.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-low-risk",
            "Validate Low Severity and Low Risk propagation.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-evidence-basic-confidence",
            "Validate Basic-only evidence and Low Confidence.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-evidence-strong-confidence",
            "Validate Strong-only evidence and Very High Confidence.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-evidence-assertability-limitation",
            "Validate assertability limitation and Insufficient Confidence.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-no-findings-recommendation",
            "Validate no-Findings Recommendation rule.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-invalid-input-fail-closed",
            "Validate fail-closed behavior for invalid fixture input.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
        GoldenFixtureRuntimeConfig(
            "fixture-v1-version-mismatch-fail-closed",
            "Validate fail-closed behavior for mismatched versions.",
            GOLDEN_FIXTURE_CATALOG_VERSION,
            GOLDEN_FIXTURE_PAYLOADS_VERSION,
            METHODOLOGY_VERSION,
        ),
    )
)


APPROVED_ARTIFACT_INVENTORY = MappingProxyType(
    {
        "business-decision-methodology": (
            "docs/business-decision-methodology/01-decision-methodology.md"
        ),
        "assessment-methodology-specification-v1": (
            "docs/business-decision-methodology/"
            "09-assessment-methodology-specification-v1.md"
        ),
        "question-mapping-matrix-v1": (
            "docs/business-decision-methodology/10-question-mapping-matrix-v1.md"
        ),
        "dimension-weight-reference-candidates-v1": (
            "docs/business-decision-methodology/"
            "11-dimension-weight-reference-candidates-v1.md"
        ),
        "official-dimension-weight-set-v1": (
            "docs/business-decision-methodology/12-official-dimension-weight-set-v1.md"
        ),
        "scoring-scale-specification-v1": (
            "docs/business-decision-methodology/13-scoring-scale-specification-v1.md"
        ),
        "question-scoring-tables-specification-v1": (
            "docs/business-decision-methodology/"
            "14-question-scoring-tables-specification-v1.md"
        ),
        "question-scoring-tables-v1": (
            "docs/business-decision-methodology/20-question-scoring-tables-v1.md"
        ),
        "readiness-threshold-specification-v1": (
            "docs/business-decision-methodology/"
            "15-readiness-threshold-specification-v1.md"
        ),
        "readiness-threshold-values-v1": (
            "docs/business-decision-methodology/21-readiness-threshold-values-v1.md"
        ),
        "severity-decision-tables-specification-v1": (
            "docs/business-decision-methodology/"
            "16-severity-decision-tables-specification-v1.md"
        ),
        "severity-decision-tables-v1": (
            "docs/business-decision-methodology/22-severity-decision-tables-v1.md"
        ),
        "risk-decision-tables-specification-v1": (
            "docs/business-decision-methodology/"
            "17-risk-decision-tables-specification-v1.md"
        ),
        "risk-decision-tables-v1": (
            "docs/business-decision-methodology/23-risk-decision-tables-v1.md"
        ),
        "confidence-decision-tables-specification-v1": (
            "docs/business-decision-methodology/"
            "18-confidence-decision-tables-specification-v1.md"
        ),
        "confidence-decision-tables-v1": (
            "docs/business-decision-methodology/24-confidence-decision-tables-v1.md"
        ),
        "recommendation-decision-tables-specification-v1": (
            "docs/business-decision-methodology/"
            "19-recommendation-decision-tables-specification-v1.md"
        ),
        "recommendation-decision-tables-v1": (
            "docs/business-decision-methodology/"
            "25-recommendation-decision-tables-v1.md"
        ),
        "executive-summary-templates-v1": (
            "docs/business-decision-methodology/"
            "26-executive-summary-templates-v1.md"
        ),
        "golden-fixtures-v1": (
            "docs/business-decision-methodology/27-golden-fixtures-v1.md"
        ),
        "golden-fixture-payloads-v1": (
            "docs/business-decision-methodology/28-golden-fixture-payloads-v1.md"
        ),
        "regression-validation-framework-v1": (
            "docs/business-decision-methodology/"
            "29-regression-validation-framework-v1.md"
        ),
        "production-authority-release-v1": (
            "docs/business-decision-methodology/"
            "30-production-authority-release-v1.md"
        ),
    }
)


APPROVED_METHODOLOGY_RUNTIME_CONFIG = ApprovedMethodologyRuntimeConfig(
    version_manifest=VERSION_MANIFEST,
    dimensions=APPROVED_DIMENSIONS,
    response_models=APPROVED_RESPONSE_MODELS,
    questions=APPROVED_QUESTIONS,
    readiness_thresholds=APPROVED_READINESS_THRESHOLDS,
    severity_levels=APPROVED_SEVERITY_LEVEL_ORDER,
    finding_types=APPROVED_FINDING_TYPE_ORDER,
    risk_levels=APPROVED_RISK_LEVEL_ORDER,
    confidence_levels=APPROVED_CONFIDENCE_LEVEL_ORDER,
    recommendation_labels=APPROVED_RECOMMENDATION_LABEL_ORDER,
    severity_decision_rules=SEVERITY_DECISION_RULES,
    risk_decision_rules=RISK_DECISION_RULES,
    confidence_decision_rules=CONFIDENCE_DECISION_RULES,
    recommendation_decision_rules=RECOMMENDATION_DECISION_RULES,
    executive_summary_sections=EXECUTIVE_SUMMARY_SECTIONS,
    golden_fixtures=GOLDEN_FIXTURES,
    artifact_inventory=APPROVED_ARTIFACT_INVENTORY,
)


validate_approved_methodology_runtime_config(APPROVED_METHODOLOGY_RUNTIME_CONFIG)
