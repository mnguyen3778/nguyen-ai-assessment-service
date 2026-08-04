# Assessment Methodology Specification v1

## 1. Purpose

Status: `FOUNDATION`

This specification consolidates the current repository-owned assessment
methodology evidence and approved methodology decisions into one
implementation-readiness reference for a future Executive Assessment Rubric v1.

This document does not approve implementation code, numeric question weights,
numeric readiness threshold values, deterministic decision tables, service
decisions, Executive Summary templates, narrative generation rules, or golden
fixture artifacts unless expressly stated by an approved methodology decision.
Where existing repository documentation does not define implementable
deterministic methodology, the section is explicitly marked
`METHODOLOGY_PENDING`.

Repository evidence:

- `docs/business-decision-methodology/01-decision-methodology.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `docs/architecture/executive-methodology-version-binding-v1.md`

## 2. Scope

Status: `FOUNDATION`

In scope:

- Repository-owned assessment methodology.
- Current canonical executive assessment question catalog.
- Current evidence category catalog.
- Approved business capability dimension catalog.
- Current deterministic answer normalization and weighted aggregation behavior.
- Current Business Readiness Snapshot foundation behavior.
- Current confidence, recommendation priority, and executive summary foundation
  behavior.
- Current versioning and compatibility requirements that affect methodology
  implementation readiness.
- Identification of methodology areas that remain placeholder,
  foundation-only, deferred, or pending.

Out of scope:

- Public 12-question assessment redesign.
- Public-to-executive answer translation.
- API routes, Lambda handlers, transport, persistence, dashboards, reports,
  portfolio intelligence, platform implementation, or website behavior.
- New business methodology.
- Code implementation.

Repository evidence:

- `docs/architecture/assessment-boundary-architecture-v1.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `docs/architecture/public-executive-runtime-separation-v1.md`

## 3. Non-goals

Status: `APPROVED`

This specification must not:

- Invent numeric question weights.
- Invent numeric dimension weights.
- Invent weight percentages.
- Invent numeric readiness threshold values.
- Invent readiness boundary convention.
- Invent risk caps or risk adjustment formulas.
- Invent confidence formulas or confidence-level assignment.
- Invent recommendation priority formulas.
- Invent recommendation catalog entries.
- Invent service routing decision tables.
- Invent unsupported deterministic executive summary rules or narrative
  templates.
- Introduce AI, LLM, or Bedrock reasoning as assessment truth.
- Move assessment methodology or business truth into any downstream repository.

Repository evidence:

- `docs/business-decision-methodology/02-question-catalog.md`
- `docs/business-decision-methodology/04-readiness-methodology.md`
- `docs/business-decision-methodology/05-confidence-methodology.md`
- `docs/business-decision-methodology/06-recommendation-priority.md`
- `docs/business-decision-methodology/07-service-decision-framework.md`
- `docs/architecture/assessment-boundary-architecture-v1.md`

## 4. Repository Ownership

Status: `APPROVED`

The Assessment Service repository owns the internal executive assessment
framework and deterministic business evaluation foundation.

Assessment Service responsibilities include:

- Internal executive assessment methodology.
- Deterministic Decision Engine.
- Configuration-driven answer normalization.
- Configuration-driven question mapping.
- Dimension and overall evaluation.
- Explanation metadata.
- Business Readiness Snapshot projection.
- Confidence methodology foundation.
- Recommendation priority methodology foundation.
- Service decision methodology catalog.
- Executive summary methodology foundation.
- BusinessDecisionPackage assembly and validation.
- ExecutiveAssessmentSnapshot production.

Downstream repositories and systems may consume Assessment Service outputs but
must not recompute, replace, or reinterpret deterministic business truth.

Repository evidence:

- `docs/architecture/assessment-boundary-architecture-v1.md`
- `docs/architecture/executive-assessment-snapshot-consumer-governance-v1.md`
- `docs/architecture/executive-intelligence-platform-snapshot-integration-contract-v1.md`

## 5. Methodology Version Identity

Status: `APPROVED`

Current methodology version identity:

```text
business-decision-methodology-v1
```

This version identity is approved for the current deterministic foundation. It
does not mean every methodology area is production-authoritative.

Version identity must remain distinct from production authority. Current
repository architecture states that the approved version identity can coexist
with placeholder, foundation-only, deferred, or methodology-pending areas.

Repository evidence:

- `docs/business-decision-methodology/01-decision-methodology.md`
- `docs/architecture/executive-methodology-version-binding-v1.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`

## 6. Canonical Inputs

Status: `APPROVED` for catalog identity, current normalizable question types,
Decision 2 question-to-dimension mapping principles, and the canonical Question
Mapping Matrix v1. `METHODOLOGY_PENDING` for public-to-executive translation
and any runtime behavior not already governed by current repository contracts.

The canonical internal executive assessment uses the 48-question catalog in
`docs/business-decision-methodology/02-question-catalog.md`.

Every canonical question has:

- Stable question ID.
- Business capability.
- Evidence category.
- Current configured readiness dimension metadata.
- Expected answer type.
- Weight category.

Allowed expected answer types are:

- `scale-0-4`
- `yes-no`
- `single-select`
- `multi-select`
- `numeric`
- `text-evidence`

Current deterministic evaluation supports normalizable answer types used by
current canonical questions. Numeric answers must be normalized before they
contribute to scoring. `text-evidence` may support executive context but must
not drive scoring until deterministic review criteria exist.

Approved Decision 1 replaces the previous conceptual taxonomy with five core
business capability dimensions for Executive Assessment Rubric v1. The
deterministic mapping from the current 48 canonical questions to those five
dimensions is defined in
`docs/business-decision-methodology/10-question-mapping-matrix-v1.md`.

Approved Decision 2 question-to-dimension mapping principles:

- Every canonical assessment question shall be assigned exactly one Primary
  Dimension.
- The Primary Dimension represents the principal business capability evaluated
  by the question.
- A question may optionally contain zero, one, or two Secondary Dimensions.
- Secondary mappings shall be used only when the question materially
  contributes to another approved business capability.
- Secondary mappings require explicit justification.
- Every canonical question must map to at least one approved dimension.
- Questions that cannot be mapped shall be rewritten or rejected.
- Mapping shall occur only against the approved five Business Capability
  Dimensions.
- Question mapping may not introduce new dimensions.
- Mapping decisions shall be based on the underlying business capability being
  evaluated, not on current regulations, technologies, or implementation
  details.
- Primary Dimension assignment must be deterministic.
- If reasonable reviewers would disagree, the question wording shall be revised
  until deterministic attribution is possible.

Approved Decision 2 validation requirements:

- Every canonical assessment question must have exactly one Primary Dimension.
- Every Secondary Dimension must accompany a Primary Dimension.
- Every approved Business Capability Dimension must contain at least one
  canonical assessment question.
- Questions that require more than two Secondary Dimensions should be rewritten
  or divided into smaller questions.
- Mapping decisions must remain deterministic and reproducible.

The public directional assessment and the internal executive assessment are
separate products and contracts. Public question IDs must not be silently
mapped into canonical methodology questions without a governed, versioned
translation methodology.

Repository evidence:

- `docs/business-decision-methodology/02-question-catalog.md`
- `docs/business-decision-methodology/10-question-mapping-matrix-v1.md`
- `docs/architecture/assessment-boundary-architecture-v1.md`
- `docs/architecture/public-executive-runtime-separation-v1.md`
- `src/assessment/decision_engine.py`

## 7. Assessment Traceability Requirements

Status: `APPROVED` for current question, evidence, readiness, weight-category,
finding generation, and explanation traceability. `METHODOLOGY_PENDING` for
finding severity assignment, risk, recommendation, and narrative rule
references.

Every downstream capability, score, risk, priority, and recommendation must be
traceable to one or more question IDs.

Approved Decision 1 establishes this evidence lineage:

```text
Evidence
  |
Assessment
  |
Findings
  |
Recommendations
  |
Executive Intelligence
```

Current approved traceability includes:

- Question ID.
- Business capability.
- Evidence category.
- Readiness dimension.
- Weight category.
- Applied numeric weight.
- Normalized score.
- Dimension explanation.
- Evaluation explanation.

Approved Decision 2 mapping traceability metadata includes:

- Primary Dimension.
- Secondary Dimension or Dimensions, when present.
- Mapping rationale.
- Taxonomy version.

Evidence references, question references, and rule references must remain
separate concepts:

```text
evidence.<category>.<capability>
question.<question-id>
rule.<dimension>.<capability>.<purpose>
```

Evidence Evaluation is approved as a cross-cutting methodology artifact under
Decision 11. It is not a sixth scoring dimension and must not modify question
scores, dimension results, aggregation results, overall assessment result, or
readiness assignment. It may be consumed by confidence, findings,
recommendations, executive reporting, and assessment trustworthiness after
those dependent methodologies are approved.

Repository evidence:

- `docs/business-decision-methodology/01-decision-methodology.md`
- `docs/business-decision-methodology/02-question-catalog.md`
- `docs/business-decision-methodology/03-evidence-catalog.md`
- `docs/business-decision-methodology/10-question-mapping-matrix-v1.md`
- `docs/architecture/assessment-decision-engine-v2.md`

## 8. Scoring Methodology

Status: `APPROVED` for answer normalization, question-to-methodology mapping,
weight-category catalog, Decision 4 dimension weighting governance, Decision 5
dimension weight set selection criteria, Decision 6 reference candidate weight
sets, Decision 7 official Numeric Dimension Weight Set, Decision 8 weight
normalization and aggregation methodology, Decision 9 question-to-dimension
scoring semantics, Scoring Scale Specification v1, Question Scoring Tables
Specification v1, Question Scoring Tables v1, explanation metadata, and
deterministic weighted aggregation mechanics currently implemented by the
Decision Engine.
`FOUNDATION` for current domain and overall numeric score production.
`PLACEHOLDER` for current numeric question weights and thresholds.

Current approved foundation behavior:

- The Decision Engine consumes validated canonical answers and methodology
  configuration.
- It validates methodology configuration before evaluation.
- It rejects unknown question IDs.
- It rejects missing required canonical questions.
- It validates answer type and configured answer range for normalizable
  answers.
- It normalizes configured numeric answer types to a 0-to-100 scale.
- It maps each answer to a question evaluation containing question ID,
  readiness dimension, evidence category, weight category, normalized score,
  and applied weight.
- It aggregates readiness dimension scores using deterministic weighted
  averages.
- It aggregates the overall score using a deterministic weighted average of all
  question evaluations.
- It records explanation metadata for evaluated dimensions, contributing
  questions, applied weights, question explanations, and dimension
  explanations.

Current approved scoring traceability:

- Every scored question is traceable to its canonical question ID.
- Every scored question is traceable to its configured business capability,
  evidence category, readiness dimension, answer type, and weight category.
- Every normalized score is traceable to the configured answer type range used
  for normalization.
- Every applied weight is traceable to methodology configuration.
- Every dimension score is traceable to the contributing question IDs and
  applied weights.
- The overall score is traceable to all evaluated question evaluations and
  their applied weights.

Current deterministic aggregation mechanics:

- Question evaluation order is deterministic by canonical question ID.
- Dimension output order is deterministic by readiness dimension ID.
- Dimension scores are weighted averages of question evaluations assigned to
  the dimension.
- Overall score is a weighted average of all question evaluations.
- The current aggregate is reproducible for identical canonical answers,
  methodology configuration, and component versions.

Current placeholder behavior:

- Numeric question weights come from `placeholder_question_weights`.
- Current placeholder question weights are `1.0`.
- Because all current placeholder question weights are `1.0`, current
  aggregation behaves as an equal-weight average across questions.
- This behavior is technically deterministic but is not approved as final
  equal-weight methodology.
- Placeholder thresholds exist for configuration validation but are not final
  readiness methodology.

Approved Decision 4 dimension weighting governance:

- Dimension weights represent the relative importance of approved Business
  Capability Dimensions, not the number of questions assigned to each
  dimension.
- Dimension weights apply to the approved Business Capability Dimensions and
  are independent of temporary regulatory emphasis.
- Every approved weight set must be documented, versioned, and supported by
  written rationale.
- Approved weights must be applied consistently to every assessment using that
  methodology version.
- Weighting is defined independently of aggregation, readiness, confidence,
  findings, recommendations, and executive summaries.
- Approved dimension weights are expected to remain stable across methodology
  versions.
- Weight changes may occur only when supported by documented business
  methodology evolution, material regulatory evolution affecting business
  capability priorities, and formal methodology governance approval.
- Weights must never be changed solely to influence assessment outcomes.
- Dimension weights must never be modified because of individual assessment
  results, customer outcomes, desired readiness distributions, or desired
  scoring distributions.
- Weight changes must originate only from approved methodology evolution.
- Every approved weight set must successfully complete methodology validation
  before becoming production-authoritative.

Approved Decision 4 weighting philosophy names:

- Equal Contribution.
- Business Capability Impact Weighted.
- Business Risk Weighted.
- Documented Hybrid.

Decision 4 does not approve numeric values, percentages, mathematical
formulas, aggregation equations, readiness thresholds, finding rules,
recommendation logic, confidence formulas, or executive summary rules.

Approved Decision 5 dimension weight set selection criteria:

Decision 5 establishes the mandatory evaluation criteria that every future
numeric dimension weight set must satisfy before approval. It does not approve
numeric values. It establishes only the governance standard by which future
weight sets will be evaluated.

Mandatory criteria:

- Business Importance Basis.
- Full Taxonomy Coverage.
- Explainability.
- Audit Defensibility.
- Regulatory Neutrality.
- Deterministic Compatibility.
- Version Stability.
- Outcome Independence.
- Methodology Consistency.
- Methodology Simplicity.

Methodology Consistency:

The selected weight set shall remain fully consistent with all previously
approved methodology decisions, including the Business Capability Taxonomy,
Question Mapping Methodology, Question Mapping Matrix, and Dimension Weighting
Governance. The weight set shall not contradict or undermine any approved
methodology artifact.

Methodology Simplicity:

Approved weight sets shall use simple, easily communicated values that
executives, auditors, implementation teams, and clients can readily understand.
Unnecessary mathematical precision should be avoided unless explicitly
justified.

Approved Decision 5 evaluation process:

- Candidate weight proposal or proposals.
- Evaluation against every mandatory criterion.
- Documented rationale.
- Methodology version approval.
- Frozen approved weight set.

No candidate weight set may be approved unless every mandatory criterion is
satisfied.

Approved Decision 5 terminology:

- Equal Contribution.
- Business Capability Impact Weighted.
- Business Risk Weighted.
- Documented Hybrid.

Decision 5 does not itself approve numeric dimension weights, percentages,
weight normalization mathematics, aggregation formulas, readiness thresholds,
finding rules, recommendation logic, confidence formulas, or executive summary
rules.

Approved Decision 6 reference candidate weight sets:

The Decision 6 candidate evaluation artifact is documented in
`docs/business-decision-methodology/11-dimension-weight-reference-candidates-v1.md`.
It records Reference Candidate Weight Sets for:

- Candidate A: Equal Contribution.
- Candidate B: Business Capability Impact Weighted.
- Candidate C: Business Risk Weighted.

The Decision 6 percentages are Reference Candidate Weight Sets only. They are
evaluation artifacts and are not approved production methodology,
implementation values, or an approved numeric dimension weight set. Decision 7
separately selects Candidate B, Business Capability Impact Weighted, as the
official Numeric Dimension Weight Set.

Approved Decision 7 official Numeric Dimension Weight Set:

The Decision 7 official Numeric Dimension Weight Set is documented in
`docs/business-decision-methodology/12-official-dimension-weight-set-v1.md`.
Decision 7 selects Business Capability Impact Weighted as the official
dimension weight philosophy.

| Business Capability Dimension | Official Weight (%) |
| --- | ---: |
| Process & Operational Control | 18 |
| Governance, Compliance & Regulatory Readiness | 24 |
| Technology & Intelligent Systems Management | 22 |
| Data, Privacy & Security Controls | 20 |
| Remediation, Verification & Continuous Improvement | 16 |
| Total | 100 |

Decision 7 approves only the official Numeric Dimension Weight Set. Decision 7
does not itself approve weight normalization methodology, aggregation
methodology, final scoring semantics, readiness thresholds, finding rules, risk
methodology, confidence formulas, recommendation logic, executive summary
methodology, implementation logic, package contracts, or snapshot contracts.

Approved Decision 8 aggregation and weight normalization methodology:

Decision 8 defines how approved dimension results are combined into a
deterministic overall assessment result. It also defines how approved
dimension weights are normalized without altering approved business intent.

Weight normalization principles:

- Authoritative Source: normalized weights must be derived only from the
  Decision 7 official Numeric Dimension Weight Set.
- Relative Contribution: normalization must preserve the relative contribution
  expressed by the approved dimension weights.
- Normalization Requirement: approved dimension weights must be expressed as
  normalized dimension weights before aggregation.
- No Business Distortion: normalization must not change approved business
  intent, change dimension priority, or introduce a different weighting
  philosophy.
- Version Binding: normalized weights are bound to the methodology version and
  official weight set version from which they are derived.

Aggregation principles:

- Dimension-First: aggregation combines approved dimension results, not raw
  question answers.
- Weighted Contribution: each dimension contributes according to its
  normalized dimension weight.
- Completeness: aggregation requires validated results for all five approved
  Business Capability Dimensions.
- Transparency: the overall result must be traceable to each dimension result,
  normalized dimension weight, and official methodology version.
- Separation from Readiness: aggregation does not define readiness thresholds
  or readiness-level assignment.
- Separation from Confidence: aggregation does not define confidence formulas
  or confidence-level assignment.
- Determinism: identical validated dimension results, official weights, and
  methodology versions must produce the same overall assessment result.

Approved methodology notation:

```text
Overall Assessment Result =
  sum(Normalized Dimension Weight * Dimension Result)
```

The sum is evaluated across all five approved Business Capability Dimensions.
This notation documents methodology only. It is not implementation code.

Complete Input Requirement:

Aggregation requires validated results for all five approved Business
Capability Dimensions. If one or more required dimension results are
unavailable, aggregation shall fail deterministically. No estimation,
substitution, interpolation, inference, or default values are permitted unless
explicitly approved by a future methodology decision.

Required mathematical properties:

- Proportionality: each dimension contribution must be proportional to its
  normalized dimension weight and validated dimension result.
- Boundedness: when all dimension results are bounded by the approved dimension
  result scale, the aggregated assessment result must remain within that same
  scale.
- Commutativity: changing the processing order of complete validated dimension
  inputs must not change the aggregated assessment result.
- Auditability: the aggregated assessment result must be explainable from the
  validated dimension results, normalized dimension weights, official weight
  set version, and methodology version.
- Monotonicity: increasing a single dimension result while holding all other
  dimension results constant shall never decrease the aggregated assessment
  result.

Decision 8 governance:

- Aggregation and weight normalization remain bound to methodology versioning.
- Changes to aggregation or weight normalization methodology must be
  non-retroactive unless a future governed methodology decision explicitly
  states otherwise.
- Changes require documented rationale and controlled methodology ownership.

Decision 8 does not itself approve question scoring methodology, readiness
thresholds, finding rules, recommendation logic, confidence formulas,
executive summary methodology, implementation algorithms, package contracts,
or snapshot contracts.

Approved Decision 9 question-to-dimension scoring semantics:

Decision 9 defines deterministic methodology for transforming validated
canonical question responses into question scores and deterministic dimension
results.

Question scoring principles:

- Deterministic Conversion: each validated canonical question response must be
  converted to a question score using versioned methodology artifacts.
- Response Completeness: every required canonical question response must be
  present and valid before scoring can complete.
- Equal Contribution Default: within each Primary Dimension, scored questions
  contribute equally to the initial dimension result unless future approved
  methodology establishes question-specific weights.
- Primary Dimension Ownership: each question score contributes to the Primary
  Dimension assigned in the approved Question Mapping Matrix.
- Scale Consistency: question scores and dimension results must use the
  approved methodology-wide scoring scale.
- No Embedded Readiness: question scoring and dimension result formation do not
  assign readiness thresholds or readiness levels.

Scoring Scale:

Status: `APPROVED`

The Scoring Scale defines the approved numeric scale used throughout the
methodology. It is versioned and applies uniformly across all canonical
questions. Scoring Scale Specification v1 approves the normalized 0-to-100
inclusive scale for methodology-wide scoring. Question Scoring Tables v1
separately approves question-specific response-to-score mappings. Scoring
Scale Specification v1 does not approve readiness thresholds, deterministic
decision tables, or implementation algorithms.

Scoring Tables:

Status: `APPROVED` for Question Scoring Tables Specification v1 structure,
metadata, validation rules, computational properties, governance, versioning,
and Question Scoring Tables v1 response-to-score mappings for all 48 canonical
questions.

Scoring Tables map each allowable response value to a numeric score on the
approved Scoring Scale. They are version-controlled methodology artifacts,
question-specific, and implementation-independent. Question Scoring Tables
Specification v1 defines their deterministic structure and governance.
Question Scoring Tables v1 defines the approved deterministic
response-to-score mappings for all 48 canonical questions.

Approved deterministic scoring pipeline:

```text
Validate Question Response
  |
Convert Response to Question Score
  |
Validate Question Score
  |
Group by Primary Dimension
  |
Calculate Dimension Result
  |
Pass Dimension Result to Decision 8 Aggregation
```

This pipeline is methodology only. It is not implementation code.

Secondary Dimension contributions:

Secondary Dimensions remain traceability metadata only. Secondary contribution
to scoring remains `METHODOLOGY_PENDING`. No Secondary Dimension contribution
shall occur until explicitly approved by a future methodology decision.

Dimension result formation:

- Dimension Scope: each dimension result is formed from the question scores
  assigned to that dimension as Primary Dimension mappings.
- Equal Weight Roll-up: the initial dimension result uses equal contribution
  from each scored question in the dimension unless future approved
  methodology establishes question-specific weights.
- Arithmetic Mean: the initial dimension result is calculated as the
  arithmetic mean of complete validated question scores assigned to the
  dimension.
- Missing Response Handling: missing required responses prevent dimension
  result formation and must fail closed.
- Traceability: each dimension result must preserve references to contributing
  question IDs, Primary Dimension mapping, scoring artifact version, and
  methodology version.

Validation and fail-closed rules:

- Invalid responses must be rejected.
- Incomplete dimensions must be detected.
- Aggregation must fail closed when any required dimension result is missing
  or invalid.
- Scoring artifacts must be versioned.
- Unsupported methodology versions or scoring artifact versions must fail
  closed.

Required computational property:

- Idempotence: re-scoring the same validated responses under the same
  methodology version shall always produce identical question scores and
  identical dimension results.

Decision 9 governance:

- Question scoring semantics, Scoring Scale values, Scoring Tables, and
  dimension result semantics remain bound to methodology versioning.
- Frozen snapshots must remain reproducible from the methodology version and
  scoring artifact versions used when they were produced.
- Changes require controlled methodology ownership.

Decision 9 does not itself approve readiness methodology, readiness
thresholds, findings, risk methodology, confidence methodology, recommendation
methodology, executive summary methodology, implementation algorithms,
question-specific weights, Scoring Tables, or Scoring Scale values. Scoring
Scale Specification v1 separately approves the methodology-wide scoring scale.
Question Scoring Tables Specification v1 separately approves scoring table
structure and governance. Question Scoring Tables v1 separately approves the
actual deterministic response-to-score mappings for all 48 canonical
questions.

Methodology pending:

- Question-specific weights, if future methodology replaces Equal Contribution
  Default.
- Risk-adjusted aggregation.
- Cross-dimension dependency caps.
- Evidence quality scoring.
- Text-evidence scoring.

Scoring non-goals for this specification:

- This section does not approve numeric question weights other than
  documenting the current placeholder value.
- This section does not approve numeric dimension weights or percentages
  beyond the Decision 7 official Numeric Dimension Weight Set.
- This section does not approve implementation algorithms.
- Primary Dimension scoring contribution follows Decision 9 Primary Dimension
  Ownership.
- Secondary Dimension scoring contribution remains `METHODOLOGY_PENDING`.
- This section does not approve numeric readiness threshold values or readiness
  boundary convention.
- This section does not approve implementation algorithms.
- This section does not approve confidence formulas, recommendation logic,
  finding rules, risk output rules, executive summaries, or golden fixtures.

Repository evidence:

- `docs/business-decision-methodology/01-decision-methodology.md`
- `docs/business-decision-methodology/02-question-catalog.md`
- `docs/business-decision-methodology/11-dimension-weight-reference-candidates-v1.md`
- `docs/business-decision-methodology/12-official-dimension-weight-set-v1.md`
- `docs/business-intelligence/03-scoring-philosophy.md`
- `docs/architecture/assessment-decision-engine-v2.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `docs/architecture/executive-methodology-version-binding-v1.md`
- `src/assessment/decision_engine.py`
- `src/assessment/methodology_config.py`

## 9. Readiness Methodology

Status: `APPROVED` for the Decision 1 business capability dimension catalog
and definitions, the canonical Question Mapping Matrix v1, and Decision 10
readiness taxonomy, interpretation methodology, assignment principles, and
computational properties, Readiness Threshold Specification v1 framework, and
Readiness Threshold Values v1.
`FOUNDATION` for current numeric domain readiness projection implemented
against the existing configuration.

Approved Decision 1 business capability dimensions:

- Process & Operational Control.
- Governance, Compliance & Regulatory Readiness.
- Technology & Intelligent Systems Management.
- Data, Privacy & Security Controls.
- Remediation, Verification & Continuous Improvement.

Approved definitions:

Process & Operational Control:

The existence, clarity, ownership, consistency, and operational execution of
documented business processes and procedures that produce reliable and
repeatable business outcomes.

Governance, Compliance & Regulatory Readiness:

The structures, policies, oversight mechanisms, accountability, and practices
that enable the organization to satisfy applicable legal, regulatory, investor,
and internal governance obligations and demonstrate that readiness when
required.

Technology & Intelligent Systems Management:

The management, lifecycle control, human oversight, operational practices,
monitoring, and accountability associated with technology systems, automation,
and intelligent systems, including AI/ML, that influence business operations,
decisions, or customer outcomes.

This dimension intentionally evaluates organizational capability rather than
organizational governance. Specific AI regulatory guidance belongs within
question mappings, findings, and recommendation catalogs rather than in the
dimension definition itself.

Data, Privacy & Security Controls:

How organizational data is classified, protected, accessed, retained,
monitored, and governed, including controls supporting regulatory compliance
and the integrity of technology and intelligent systems.

Remediation, Verification & Continuous Improvement:

The capability to convert findings into owned corrective actions,
independently verify completion, appropriately close findings or document
residual risk, and continuously improve organizational processes and controls.

Current foundation behavior:

- Domain readiness scores are projected from Decision Engine dimension
  evaluations.
- Overall readiness preserves the Decision Engine overall score.
- Business Readiness Snapshot preserves evaluated dimensions, question count,
  total weight, methodology version, domain labels, domain scores, and
  contributing question references.

Approved Decision 2 dimension guidance:

- Process & Operational Control maps questions evaluating business processes,
  procedures, ownership, consistency, execution, and operational reliability.
- Governance, Compliance & Regulatory Readiness maps questions evaluating
  governance structures, oversight, accountability, regulatory obligations,
  investor expectations, and compliance readiness.
- Technology & Intelligent Systems Management maps questions evaluating
  lifecycle management, operational controls, monitoring, accountability,
  human oversight, vendor management, automation, AI/ML systems, and technology
  capabilities affecting business operations.
- Technology & Intelligent Systems Management intentionally evaluates
  organizational capability rather than organizational governance.
- AI-specific regulations remain supporting methodology rather than taxonomy.
- Data, Privacy & Security Controls maps questions evaluating classification,
  protection, monitoring, retention, access control, privacy, and security
  practices protecting organizational information and technology integrity.
- Remediation, Verification & Continuous Improvement maps questions evaluating
  corrective actions, ownership, verification, residual risk management,
  closure, and continuous improvement.

Approved Decision 2 multi-dimension mapping:

- Each canonical question has exactly one Primary Dimension.
- Each canonical question may have zero to two Secondary Dimensions.
- Secondary Dimensions require explicit justification.
- Primary Dimension scoring contribution follows Decision 9 Primary Dimension
  Ownership.
- Secondary Dimension scoring contribution remains `METHODOLOGY_PENDING`.

Approved Decision 10 readiness methodology:

Decision 10 defines deterministic methodology for interpreting approved
dimension results and the overall assessment result into readiness states.
Readiness is the first business-interpretation layer and consumes the
deterministic computation produced by Decisions 8 and 9.

Approved readiness taxonomy:

- Not Ready.
- Developing.
- Ready.
- Advanced.

Operational processing state:

- Incomplete.

Incomplete is not a readiness level. It is an operational processing state
indicating that readiness cannot be assigned because one or more required
dimension results are unavailable or invalid under the approved fail-closed
methodology.

Assignment principles:

- Score-Driven: readiness assignment is based on approved numeric dimension
  results and the approved overall assessment result.
- Dual Scope: readiness interpretation applies to individual approved Business
  Capability Dimension results and to the overall assessment result.
- No Cross-Dimension Override: readiness assignment does not override one
  dimension based on another dimension unless approved Risk Decision Tables or
  future approved methodology explicitly authorize assessment-level synthesis.
- Incomplete Results: missing or invalid required dimension results produce
  the Incomplete operational processing state instead of a readiness level.
- Deterministic Thresholds: the methodology requires explicit, versioned
  numeric thresholds. Readiness Threshold Specification v1 defines the
  deterministic threshold framework. Readiness Threshold Values v1 defines the
  approved numeric threshold values.
- Boundary Rule: boundary handling must be deterministic, versioned, and
  explicitly defined when numeric thresholds are approved. Readiness Threshold
  Specification v1 defines the boundary convention framework. Readiness
  Threshold Values v1 defines the final readiness boundary convention.

Required methodological properties:

- Idempotence: interpreting the same approved dimension results and overall
  assessment result under the same methodology version shall produce identical
  readiness states.
- Traceability: each readiness state must be traceable to the source numeric
  result, threshold artifact version, readiness boundary convention version, and
  methodology version.
- Explainability: readiness assignment must identify the numeric result,
  applicable threshold range, and assigned readiness state or Incomplete
  operational processing state.
- Version Binding: readiness taxonomy, threshold values, readiness boundary
  convention, and assignment semantics are bound to methodology versioning.
- Monotonic Readiness: increasing a numeric assessment result while holding
  the methodology version constant shall never result in assignment to a lower
  readiness level.

Decision 10 governance:

- Readiness methodology remains bound to methodology versioning.
- Frozen snapshots must remain reproducible from the methodology version and
  readiness artifact versions used when they were produced.
- Changes require controlled methodology ownership.

Decision 10 does not itself approve numeric threshold values, readiness
boundary convention, findings, risk methodology, evidence evaluation
methodology, confidence methodology, recommendation methodology, executive
summary methodology, implementation algorithms, package contracts, or snapshot
contracts. Readiness Threshold Specification v1 separately approves threshold
structure and governance. Readiness Threshold Values v1 separately approves
numeric readiness threshold values and the final boundary convention.

Methodology pending:

- Updating deterministic implementation semantics to use the approved five
  dimensions.
- Risk caps that limit readiness conclusions.
- Cross-dimension dependency rules.

Repository evidence:

- `docs/business-decision-methodology/04-readiness-methodology.md`
- `docs/business-decision-methodology/10-question-mapping-matrix-v1.md`
- `docs/business-intelligence/02-business-readiness-model.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `src/assessment/snapshot.py`

## 10. Evidence Evaluation Methodology

Status: `APPROVED` for Decision 11 Evidence Availability methodology,
Evidence Quality methodology, evaluation principles, evaluation criteria,
application scope, computational properties, and governance.
`METHODOLOGY_PENDING` for remaining Evidence Quality taxonomy details and
numeric evidence scoring.

Decision 11 defines deterministic methodology for evaluating the quality,
completeness, authenticity, and traceability of supporting evidence. Evidence
Evaluation is a cross-cutting methodology that follows Readiness Methodology
and precedes Finding Methodology.

Evidence Availability:

Evidence Availability determines whether required evidence exists. If required
evidence is missing, the approved fail-closed processing model applies.
Missing required evidence is not an Evidence Quality level.

Evidence Quality:

Evidence Quality evaluates only evidence that is present.

Approved Evidence Quality levels for available evidence:

- Basic.
- Adequate.
- Strong.

Missing required evidence must not be classified as a quality level. Any
remaining quality taxonomy details, including any unlisted level detail,
remain `METHODOLOGY_PENDING`.

Core principles:

- Cross-Cutting: Evidence Evaluation may be consumed by downstream
  methodology without becoming a scoring dimension.
- Evidence-First: evaluation begins with the submitted or referenced
  supporting evidence.
- Deterministic Classification: the same evidence under the same methodology
  version must produce the same evidence evaluation result.
- Traceability Required: every evidence evaluation must preserve source
  references and methodology version.
- Independence from Score: Evidence Evaluation must not change question
  scores, dimension results, aggregation results, overall assessment result,
  or readiness assignment.
- Fail-Closed Orientation: missing required evidence or invalid evidence
  metadata must fail closed under approved methodology.

Evaluation criteria:

- Existence & Completeness.
- Source Integrity.
- Lineage & Traceability.
- Corroboration.
- Timeliness & Relevance.
- Human Review Status.
- Evidence Authenticity: determines whether evidence can be shown to be
  authentic and represents the authoritative record.

Application scope:

- Question Level.
- Dimension Level.
- Overall Assessment Level.

Higher-level evidence quality assessments shall be derived deterministically
from lower-level evidence evaluations. Higher-level evidence quality shall not
be independently assigned.

Required computational properties:

- Idempotence: evaluating the same evidence under the same methodology version
  shall produce the same evidence availability and evidence quality results.
- Version Binding: evidence evaluation criteria, taxonomy, and processing
  semantics are bound to methodology versioning.
- Auditability: evidence evaluation must preserve sufficient rationale and
  source traceability for review.
- Deterministic Independence: Evidence Evaluation shall not modify question
  scores, dimension results, aggregation results, overall assessment result, or
  readiness assignment.

Evidence Evaluation produces an independent methodology artifact consumed by
downstream methodology.

Decision 11 governance:

- Evidence Evaluation remains bound to methodology versioning.
- Frozen snapshots must remain reproducible from the methodology version and
  evidence evaluation artifact versions used when they were produced.
- Changes require controlled methodology ownership.

Decision 11 does not approve findings, finding severity, risk methodology,
confidence methodology, recommendation methodology, executive summary
methodology, implementation algorithms, package contracts, snapshot contracts,
or numeric evidence scoring.

Methodology pending:

- Remaining Evidence Quality taxonomy details.
- Numeric evidence scoring, if future methodology requires it.
- Finding consumption of Evidence Evaluation.
- Risk consumption of Evidence Evaluation.
- Confidence consumption of Evidence Evaluation.
- Recommendation consumption of Evidence Evaluation.
- Executive Summary output emission from Evidence Evaluation using Executive
  Summary Templates v1.

Repository evidence:

- `docs/business-decision-methodology/03-evidence-catalog.md`
- `docs/business-decision-methodology/05-confidence-methodology.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`

## 11. Finding Methodology

Status: `APPROVED` for Decision 12 finding generation methodology, finding
taxonomy, deterministic identity, finding structure, methodology-owned
lifecycle, computational properties, governance, and the Decision 1 severity
taxonomy definitions. `APPROVED` for Decision 13 Severity Assignment
Methodology governing principles, evaluation inputs, computational properties,
and governance, and Severity Decision Tables Specification v1 structure and
governance, and Severity Decision Tables v1.

Decision 12 defines deterministic methodology for generating Findings from
Dimension Results, Overall Assessment Result, Readiness, and Evidence
Evaluation. Findings are derived business artifacts. Findings do not create new
business truth.

Finding generation ownership:

Assessment Service owns:

- Finding generation.
- Finding identity.
- Finding structure.
- Traceability.
- Deterministic generation.

Assessment Service does not own:

- Acceptance.
- Remediation workflow.
- Verification workflow.
- Closure workflow.
- Risk acceptance workflow.

Those operational workflows belong to downstream systems such as the Client
Engagement Portal or future Case Management capabilities.

Approved Decision 1 severity model:

Critical:

A finding that creates a material breach of applicable law, regulation,
investor requirements, or organizational governance obligations such that the
organization would be considered materially non-compliant if examined today.

High:

A significant gap materially increasing the likelihood of future
non-compliance, operational failure, governance breakdown, or eligibility
concerns.

Medium:

A clear deficiency reducing effectiveness or consistency without currently
representing a material breach.

Low:

A limited weakness suitable for planned improvement.

Informational:

An observation that is not a defect and may identify strengths, context, or
improvement opportunities.

The severity model must remain business-consequence based. Vendor-specific and
regulator-specific references belong in supporting methodology rather than in
the severity definitions themselves.

Severity Assignment:

Decision 1 approved the Severity taxonomy:

- Critical.
- High.
- Medium.
- Low.
- Informational.

Decision 13 defines only the methodology for assigning those existing levels.
It does not redefine the taxonomy.

Severity Assignment consumes:

- Findings.
- Readiness.
- Evidence Evaluation.

Severity Assignment does not create new Findings and does not modify business
truth.

Evaluation inputs:

- Finding characteristics.
- Primary Dimension.
- Readiness context.
- Business consequence.
- Evidence Availability.
- Evidence Quality.

These are evaluation inputs only. No evaluation input has implicit precedence
unless explicitly defined by an approved deterministic decision table. Decision
13 does not introduce weighting or priority ordering. Severity Decision Tables
v1 defines approved deterministic Severity Assignment rules without introducing
weighting or priority ordering.

Core Severity Assignment principles:

- Consequence-Oriented: Severity expresses the business consequence
  represented by the Finding.
- Deterministic: identical Finding, Readiness, Evidence Evaluation, and
  methodology version inputs must produce the same Severity when deterministic
  decision tables are approved.
- Evidence-Informed: Evidence Evaluation may affect whether the Finding can be
  confidently asserted.
- Readiness-Contextual: Readiness may provide context for interpreting the
  consequence represented by a Finding.
- Single Severity per Finding: each Finding receives one approved Severity
  Level.
- No Risk Embedding: Severity Assignment does not define Risk Methodology or
  risk scoring.

Assertability versus Severity:

Evidence Quality affects the ability to confidently assert a Finding. Evidence
Quality does not reduce or increase the inherent business consequence
represented by the Finding.

Severity expresses consequence. Confidence expresses certainty. These remain
separate methodology responsibilities.

Severity Independence:

Severity Assignment shall never modify:

- Finding Identity.
- Finding Type.
- Finding Content.
- Question Scores.
- Dimension Results.
- Aggregation.
- Overall Assessment Result.
- Readiness.
- Evidence Evaluation.

Severity Assignment produces an independent attribute of an existing Finding.

Required Severity Assignment properties:

- Idempotence: assigning Severity from the same inputs under the same
  methodology version shall produce the same Severity Level.
- Traceability: Severity Assignment must preserve references to the Finding,
  Readiness context, Evidence Evaluation, decision table version, and
  methodology version.
- Explainability: Severity Assignment must explain the evaluated consequence
  basis and supporting inputs.
- Version Binding: Severity Assignment principles, decision tables, and output
  semantics are bound to methodology versioning.
- Severity Independence: Severity Assignment must not modify the Finding or
  upstream deterministic business truth.

Decision Tables:

Decision 13 approves the governing principles only. Severity Decision Tables
Specification v1 separately approves deterministic decision table structure and
governance. Severity Decision Tables v1 separately approves the deterministic
Severity Decision Table rows.

Decision 13 governance:

- Severity Assignment Methodology remains bound to methodology versioning.
- Frozen snapshots must remain reproducible from the methodology version and
  severity assignment artifact versions used when they were produced.
- Changes require controlled methodology ownership.

Decision 13 does not approve Risk Methodology, risk scoring, Confidence
Methodology, Recommendation Methodology, Executive Summary Methodology,
deterministic decision tables, implementation algorithms, package contracts, or
snapshot contracts.

Approved Finding Types:

- Deficiency.
- Observation.
- Strength.
- Opportunity.

Finding Type is independent of Severity.

Deterministic Finding Identity:

Every Finding must include deterministic identity metadata.

Minimum identity:

- Finding ID.
- Methodology Version.
- Primary Dimension.
- Trigger Source.
- Finding Type.
- Sequence Identifier.

Finding identity must be reproducible for identical assessment inputs.

Finding structure:

- Finding ID.
- Title.
- Primary Dimension.
- Related Dimensions.
- Linked Readiness.
- Evidence Quality.
- Source References.
- Methodology Version.
- Severity, assigned under Severity Decision Tables v1.

Finding lifecycle:

- Generated.
- Superseded.

This lifecycle is methodology-owned only. Remediation lifecycle, verification
lifecycle, closure workflow, and risk acceptance workflow belong to downstream
systems.

Core principles:

- Derived, Not Invented: Findings consume deterministic business truth and do
  not introduce unsupported conclusions.
- Deterministic Generation: identical assessment inputs under the same
  methodology version must produce identical Findings.
- Evidence Anchored: Findings must reference source evidence and evidence
  evaluation artifacts.
- Traceability: Findings must preserve source references, triggering
  deterministic inputs, methodology version, and identity metadata.
- Separation of Concerns: Finding generation is separate from remediation,
  verification, closure, risk acceptance, confidence, recommendation, and
  executive summary methodology.
- Fail-Closed Orientation: invalid or incomplete deterministic inputs must
  prevent Finding generation rather than produce partial or inferred Findings.

Finding Independence:

Findings shall never modify:

- Question Scores.
- Dimension Results.
- Aggregation.
- Overall Assessment Result.
- Readiness.
- Evidence Evaluation.

Findings consume deterministic business truth. They never rewrite business
truth.

Required computational properties:

- Idempotence: generating Findings from the same deterministic inputs under
  the same methodology version shall produce identical Findings.
- Auditability: each Finding must be reviewable from identity metadata,
  triggering inputs, source references, and methodology version.
- Version Binding: Finding generation rules, identity rules, structure, and
  lifecycle semantics are bound to methodology versioning.
- Finding Independence: Finding generation must not modify upstream
  deterministic business truth.

Decision 12 governance:

- Finding generation methodology remains bound to methodology versioning.
- Frozen snapshots must remain reproducible from the methodology version and
  finding artifact versions used when they were produced.
- Changes require controlled methodology ownership.

Decision 12 does not itself approve Severity Assignment Methodology, risk
methodology, confidence methodology, recommendation methodology, executive
summary methodology, remediation workflow, case management workflow,
implementation algorithms, package contracts, or snapshot contracts.

Methodology pending:

- Risk methodology consumption of Findings.
- Confidence methodology consumption of Findings.
- Recommendation output emission from Findings until actual Recommendation
  Decision Table artifacts are approved.
- Executive Summary output emission from Findings using Executive Summary
  Templates v1.

Repository evidence:

- `docs/business-intelligence/02-business-readiness-model.md`
- `docs/business-decision-methodology/03-evidence-catalog.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`

## 12. Risk Methodology

Status: `APPROVED` for Decision 14 assessment-level Risk Methodology, risk
taxonomy, assessment-level synthesis principles, evaluation conditions,
computational properties, and governance, and Risk Decision Tables
Specification v1 structure and governance, and Risk Decision Tables v1.

Decision 14 defines deterministic methodology for evaluating assessment-level
business impact from Severity-Assigned Findings. Risk Methodology consumes
Severity-Assigned Findings. Risk Methodology does not modify Findings and does
not modify business truth.

Assessment-Level Risk only:

Severity remains the business consequence classification for individual
Findings. Risk is an assessment-level synthesis derived from the complete
collection of Severity-Assigned Findings. Assessment Service methodology must
not introduce a separate Finding-Level Risk artifact.

Authoritative inputs:

Risk Methodology consumes only:

- Severity-Assigned Findings.
- Readiness.
- Evidence Evaluation as contextual input only, not confidence.

Risk Methodology shall not independently reinterpret Findings.
Severity-Assigned Findings remain the authoritative producer output.

Approved Risk taxonomy:

- Critical Risk.
- Elevated Risk.
- Moderate Risk.
- Low Risk.
- Minimal / Informational.

Risk remains a separate methodology from Severity. Decision 14 does not
redefine Severity.

Evaluation conditions:

- Presence of Critical Findings.
- High concentrations of High Severity Findings.
- Approved cross-dimension dependency conditions.

These establish evaluation conditions only. Decision 14 does not define
escalation algorithms or deterministic mapping rules.

Core principles:

- Consumes, Does Not Modify: Risk consumes Severity-Assigned Findings,
  Readiness, and Evidence Evaluation without modifying them.
- Consequence-Oriented: Risk represents assessment-level business impact.
- Deterministic: identical approved inputs under the same methodology version
  and Risk Decision Tables must produce identical Risk outputs.
- No Confidence Embedding: Risk Methodology does not define confidence
  formulas or confidence-level assignment.
- No Recommendation Embedding: Risk Methodology does not generate
  recommendations or priority assignments.
- Fail-Closed Orientation: missing, invalid, or unsupported required risk
  inputs must prevent Risk output generation.
- Assessment-Level Synthesis: Risk represents the collective business impact
  of the complete set of Severity-Assigned Findings.

Risk Independence:

Risk Methodology shall never modify:

- Question Scores.
- Dimension Results.
- Aggregation.
- Overall Assessment Result.
- Readiness.
- Evidence Evaluation.
- Findings.
- Severity Assignment.

Risk produces a downstream assessment artifact only.

Required computational properties:

- Idempotence: evaluating Risk from the same approved inputs under the same
  methodology version shall produce the same Risk output.
- Traceability: Risk output must preserve references to Severity-Assigned
  Findings, Readiness, Evidence Evaluation, Risk Decision Table version, and
  methodology version.
- Explainability: Risk output must explain the assessment-level synthesis and
  source evaluation conditions.
- Version Binding: Risk taxonomy, Risk Decision Tables, and output semantics
  are bound to methodology versioning.
- Risk Independence: Risk evaluation must not modify upstream deterministic
  business truth.

Risk Decision Tables:

Decision 14 approves governing principles only. Risk Decision Tables
Specification v1 separately approves deterministic decision table structure and
governance. Risk Decision Tables v1 separately approves the deterministic Risk
Decision Table rows.

Decision 14 governance:

- Risk Methodology remains bound to methodology versioning.
- Frozen snapshots must remain reproducible from the methodology version and
  risk artifact versions used when they were produced.
- Changes require controlled methodology ownership.

Decision 14 does not approve Confidence Methodology, Recommendation
Methodology, Executive Summary Methodology, implementation algorithms, package
contracts, or snapshot contracts.

Methodology pending:

- Confidence methodology consumption of Risk.
- Recommendation output emission from Risk until actual Recommendation
  Decision Table artifacts are approved.
- Executive Summary output emission from Risk using Executive Summary
  Templates v1.

Repository evidence:

- `docs/business-decision-methodology/01-decision-methodology.md`
- `docs/business-decision-methodology/02-question-catalog.md`
- `docs/business-intelligence/02-business-readiness-model.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`

## 13. Confidence Methodology

Status: `APPROVED` for Decision 15 Confidence Methodology governing
principles, taxonomy labels, authoritative inputs, computational properties,
repository ownership, and governance, Confidence Decision Tables Specification
v1 structure and governance, and Confidence Decision Tables v1 deterministic
assignment rules. `FOUNDATION` for current deterministic completeness and
evidence coverage evaluation. `METHODOLOGY_PENDING` for deterministic
answer-consistency, response-quality, and business-certainty rules.

Decision 15 defines Confidence Methodology. Confidence represents the degree of
certainty that the Assessment Service has in the business truth it has
produced.

Confidence is not:

- Readiness.
- Severity.
- Risk.
- Recommendation priority.

Confidence is its own methodology.

Current approved confidence factors:

- Assessment completeness.
- Answer consistency.
- Evidence coverage.
- Response quality.
- Business certainty.

Current foundation behavior:

- Assessment completeness is evaluated deterministically from observed question
  count versus configured question count.
- Evidence coverage is evaluated deterministically from observed evidence
  categories versus configured evidence categories.
- Answer consistency, response quality, and business certainty are configured
  but not evaluated.
- Not-yet-evaluated confidence factors emit explicit limitation metadata.

Approved Decision 15 core principles:

- Confidence consumes but never modifies upstream artifacts.
- Confidence is deterministic.
- Confidence is evidence-informed.
- Confidence measures certainty, not business consequence.
- Confidence is independent from Risk.
- Confidence is independent from Readiness.
- Confidence is independent from Severity.
- Confidence never recalculates scores.
- Confidence never recalculates Findings.
- Confidence never recalculates Risk.

Authoritative inputs:

Confidence consumes only approved producer outputs such as:

- Evidence Evaluation.
- Findings.
- Severity Assignment.
- Risk Assessment, once produced under approved Risk Decision Tables.
- Readiness.
- Assessment completeness.

These are authoritative inputs only. Decision 15 does not define weighting,
precedence, algorithms, or formulas for confidence assignment.

Approved Confidence taxonomy labels:

- Very High Confidence.
- High Confidence.
- Moderate Confidence.
- Low Confidence.
- Insufficient Confidence.

Confidence Decision Tables Specification v1 separately approves deterministic
decision table structure and governance. Confidence Decision Tables v1 approves
deterministic decision rows that assign one Confidence Level to each complete
valid assessment.

Confidence Independence:

Confidence shall never modify:

- Question Scores.
- Dimension Results.
- Aggregation.
- Overall Assessment Result.
- Readiness.
- Evidence Evaluation.
- Findings.
- Severity.
- Risk.

Confidence produces a downstream assessment artifact only.

Required computational properties:

- Idempotence: evaluating Confidence from the same approved inputs under the
  same methodology version shall produce the same Confidence Assessment.
- Traceability: Confidence Assessment must preserve references to consumed
  upstream artifacts and methodology version.
- Explainability: Confidence Assessment must explain the certainty basis and
  source inputs.
- Version Binding: Confidence taxonomy labels, Confidence Decision Tables, and
  output semantics are bound to methodology versioning.
- Deterministic Independence: Confidence must not modify upstream
  deterministic business truth.
- Fail-Closed behavior: missing, invalid, or unsupported required confidence
  inputs must prevent Confidence Assessment output generation.

Decision 15 governance:

- Confidence Methodology remains bound to methodology versioning.
- Frozen snapshots must remain reproducible from the methodology version and
  confidence artifact versions used when they were produced.
- Changes require controlled methodology ownership.

Decision 15 does not approve Recommendation Methodology, Executive Summary
Methodology, implementation algorithms, package contracts, or snapshot
contracts.

Methodology pending:

- Deterministic answer-consistency rules.
- Deterministic response-quality rules.
- Deterministic business-certainty rules.
- Executable suppression rules.
- Confidence rationale and evidence reference requirements as final output.

Repository evidence:

- `docs/business-decision-methodology/05-confidence-methodology.md`
- `docs/business-decision-methodology/18-confidence-decision-tables-specification-v1.md`
- `docs/business-decision-methodology/24-confidence-decision-tables-v1.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `src/assessment/confidence.py`

## 14. Recommendation Methodology

Status: `APPROVED` for Decision 16 Recommendation Methodology governing
principles, taxonomy labels, authoritative inputs, required metadata,
computational properties, repository ownership, and governance, Recommendation
Decision Tables Specification v1 structure and governance, and Recommendation
Decision Tables v1 deterministic advisory output rules.
`FOUNDATION` for current priority level catalog, priority factor catalog, and
ordering principles. `METHODOLOGY_PENDING` for recommendation prioritization
formulas or priority-level outputs if emitted beyond stable output ordering.

Decision 16 defines Recommendation Methodology. Recommendations represent
deterministic actions derived from approved business truth. Recommendations
shall never modify business truth. Recommendations are downstream advisory
artifacts only.

Current approved priority levels:

- Critical.
- High.
- Medium.
- Low.

Current approved priority drivers:

- Business Impact.
- Customer Impact.
- Executive Urgency.
- Risk Severity.
- Dependency Role.
- Confidence Level.

Current foundation behavior:

- Recommendation priority levels and factors are configured.
- Recommendation priority factors are exposed with source references and
  limitation metadata.
- No priority factors are evaluated as final deterministic recommendation
  priority outputs.
- No recommendations are generated.

Approved Decision 16 core principles:

- Recommendations consume but never modify upstream artifacts.
- Recommendations are deterministic.
- Recommendations are evidence-supported.
- Recommendations are business-action oriented.
- Recommendations are explainable.
- Recommendations are traceable.
- Recommendations never recalculate scores.
- Recommendations never modify Findings.
- Recommendations never modify Severity.
- Recommendations never modify Risk.
- Recommendations never modify Confidence.

Authoritative inputs:

Recommendations may consume only approved producer outputs, including:

- Findings.
- Severity Assignment.
- Risk Assessment.
- Confidence Assessment.
- Readiness.
- Evidence Evaluation.

Recommendations are derived from the complete assessment context, not from
isolated Findings. These are authoritative inputs only. Decision 16 does not
define weighting, precedence, or prioritization formulas.

Approved Recommendation taxonomy labels:

- Immediate Action.
- Priority Action.
- Planned Improvement.
- Best Practice.
- Monitor.

Recommendation Decision Tables Specification v1 separately approves
deterministic decision table structure and governance. Recommendation Decision
Tables v1 approves deterministic decision rows that produce one advisory
Recommendation set for each complete valid assessment.

Required Recommendation metadata:

- Recommendation ID.
- Methodology Version.
- Recommendation taxonomy label.
- Source Findings.
- Source Severity Assignment references.
- Source Risk references.
- Source Confidence references.
- Source Readiness references.
- Source Evidence Evaluation references.
- Traceability rationale.

Recommendations must reference the upstream artifacts that justify them:
Findings, Severity, Risk, Confidence, Readiness, and Evidence Evaluation.

Advisory boundary:

Recommendations are advisory only and must never imply automatic workflow
execution, remediation ownership, task management, verification workflow,
closure workflow, or risk acceptance workflow.

Recommendation Independence:

Recommendations shall never modify:

- Question Scores.
- Dimension Results.
- Aggregation.
- Overall Assessment Result.
- Readiness.
- Evidence Evaluation.
- Findings.
- Severity.
- Risk.
- Confidence.

Recommendations produce downstream advisory artifacts only.

Required computational properties:

- Idempotence: generating Recommendations from the same approved inputs under
  the same methodology version shall produce the same Recommendations.
- Traceability: Recommendations must preserve references to the upstream
  artifacts that justify them and to methodology version.
- Explainability: Recommendations must explain the business-action rationale
  and source inputs.
- Version Binding: Recommendation taxonomy labels, Recommendation Decision
  Tables, stable output ordering, and output semantics are bound to
  methodology versioning.
- Deterministic Independence: Recommendations must not modify upstream
  deterministic business truth.
- Fail-Closed behavior: missing, invalid, or unsupported required
  recommendation inputs must prevent Recommendation output generation.

Decision 16 governance:

- Recommendation Methodology remains bound to methodology versioning.
- Frozen snapshots must remain reproducible from the methodology version and
  recommendation artifact versions used when they were produced.
- Changes require controlled methodology ownership.

Decision 16 does not approve recommendation prioritization formulas or
priority-level outputs beyond stable output ordering, Executive Summary
Methodology, implementation algorithms, package contracts, or snapshot
contracts.

Methodology pending:

- Recommendation prioritization formulas or priority-level outputs if emitted
  beyond stable output ordering.
- Service decision tables, if service outputs are emitted.
- Executive Summary output emission from Recommendations using Executive
  Summary Templates v1.

Repository evidence:

- `docs/business-decision-methodology/06-recommendation-priority.md`
- `docs/business-decision-methodology/07-service-decision-framework.md`
- `docs/business-decision-methodology/19-recommendation-decision-tables-specification-v1.md`
- `docs/business-decision-methodology/25-recommendation-decision-tables-v1.md`
- `docs/business-intelligence/05-recommendation-engine.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `src/assessment/recommendation_priority.py`

## 15. Executive Summary Methodology

Status: `APPROVED` for Decision 17 Executive Summary Methodology governing
principles, required sections, authoritative inputs, required metadata,
computational properties, repository ownership, governance, deterministic
templates, and narrative composition rules. `FOUNDATION` for current
configured summary sections and source metadata. `METHODOLOGY_PENDING` for
presentation formatting rules and implementation.

Decision 17 defines Executive Summary Methodology. The Executive Summary is
the final Assessment Service producer artifact. It represents a deterministic
business narrative produced exclusively from approved Assessment Service
artifacts. It is not generative AI output. It shall never introduce new
business truth.

Current foundation behavior:

- Executive summary sections are configured.
- Executive summary foundation consumes Business Readiness Snapshot,
  ConfidenceEvaluation, RecommendationPriorityEvaluation, and methodology
  configuration.
- All configured sections are marked not evaluated.
- Source snapshot, confidence, and priority metadata is preserved.
- Explicit limitation metadata states that narrative generation, executive
  reporting rules, recommendation generation, and service decisions are not yet
  approved.

Approved Decision 17 core principles:

- Executive Summary consumes but never modifies upstream artifacts.
- Executive Summary is deterministic.
- Executive Summary is evidence-supported.
- Executive Summary summarizes rather than evaluates.
- Executive Summary is explainable.
- Executive Summary is traceable.
- Executive Summary never recalculates scores.
- Executive Summary never modifies Findings.
- Executive Summary never modifies Severity.
- Executive Summary never modifies Risk.
- Executive Summary never modifies Confidence.
- Executive Summary never modifies Recommendations.
- Executive Summary shall summarize only approved producer artifacts.
- Executive Summary shall not interpret beyond approved business truth.

Authoritative inputs:

Executive Summary may consume only approved Assessment Service artifacts,
including:

- Overall Assessment Result.
- Dimension Results.
- Readiness.
- Evidence Evaluation.
- Findings.
- Severity Assignment.
- Risk Assessment.
- Confidence Assessment.
- Recommendations.

No other inputs are permitted.

Required Executive Summary sections:

- Overall Assessment Overview.
- Business Capability Highlights.
- Significant Findings.
- Risk Overview.
- Confidence Statement.
- Recommended Actions.
- Closing Assessment Statement.

Executive Summary Templates v1 defines deterministic section templates and
narrative composition rules for these required sections.

Required Executive Summary metadata:

- Summary ID.
- Methodology Version.
- Source Overall Assessment Result references.
- Source Dimension Result references.
- Source Readiness references.
- Source Evidence Evaluation references.
- Source Finding references.
- Source Severity Assignment references.
- Source Risk references.
- Source Confidence references.
- Source Recommendation references.
- Section-level traceability rationale.

Every section must trace back to one or more approved producer artifacts.

Executive Summary Independence:

Executive Summary shall never modify:

- Scores.
- Aggregation.
- Readiness.
- Evidence.
- Findings.
- Severity.
- Risk.
- Confidence.
- Recommendations.

Executive Summary is presentation of approved business truth only.

Required computational properties:

- Idempotence: generating Executive Summary output from the same approved
  inputs under the same methodology version shall produce the same Executive
  Summary.
- Traceability: each Executive Summary section must preserve references to
  the approved producer artifacts that justify it and to methodology version.
- Explainability: each Executive Summary section must explain the approved
  business truth it summarizes.
- Version Binding: required sections, templates, narrative composition rules,
  and output semantics are bound to methodology versioning.
- Deterministic Independence: Executive Summary must not modify upstream
  deterministic business truth.
- Fail-Closed behavior: missing, invalid, or unsupported required Executive
  Summary inputs must prevent Executive Summary output generation.

Decision 17 governance:

- Executive Summary Methodology remains bound to methodology versioning.
- Frozen snapshots must remain reproducible from the methodology version and
  Executive Summary artifact versions used when they were produced.
- Changes require controlled methodology ownership.

Decision 17 does not approve AI-generated narrative, presentation styling,
Website formatting, Client Portal formatting, implementation algorithms,
package contracts, or snapshot contracts.

Methodology pending:

- Presentation formatting rules, if future Assessment Service output requires
  them.
- Website or Client Portal formatting remains out of Assessment Service scope.

Repository evidence:

- `docs/business-intelligence/06-executive-summary-rules.md`
- `docs/business-decision-methodology/08-business-decision-roadmap.md`
- `docs/business-decision-methodology/26-executive-summary-templates-v1.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `src/assessment/executive_summary.py`

## 16. Executive Assessment Snapshot Relationship

Status: `APPROVED` for current immutable snapshot boundary and serialized
snapshot validation. `METHODOLOGY_PENDING` for any future snapshot contract
change that would add final rubric outputs as new fields.

Current approved relationship:

- BusinessDecisionPackage remains the canonical immutable deterministic
  business truth.
- ExecutiveAssessmentSnapshot is created only from a successful
  ExecutiveRuntimeResult.
- ExecutiveAssessmentSnapshot preserves the BusinessDecisionPackage, response
  status, and response contract version.
- Snapshot creation must not recompute assessment values, generate
  recommendations, create narratives, add runtime metadata, or introduce
  downstream enrichment.
- Serialized snapshot validation must fail closed and delegate package
  validation to the existing package validator.

Current BusinessDecisionPackage limitations must remain visible until approved
methodology replaces them through governed versioning.

Repository evidence:

- `docs/architecture/executive-assessment-snapshot-architecture-v1.md`
- `docs/architecture/executive-assessment-snapshot-integrity-compatibility-validation-v1.md`
- `docs/architecture/executive-intelligence-platform-snapshot-integration-contract-v1.md`
- `src/assessment/executive_assessment_snapshot.py`
- `src/assessment/business_decision_package.py`

## 17. Versioning Requirements

Status: `APPROVED`

A new methodology version is required when methodology meaning,
deterministic evaluation behavior, or methodology-owned output semantics
change.

Examples requiring methodology version review include:

- Changing canonical question IDs.
- Changing canonical question meaning.
- Changing question-to-readiness-dimension mapping.
- Mapping canonical questions to the approved five business capability
  dimensions.
- Changing a Primary Dimension for an approved production question.
- Changing Secondary Dimension mapping rules in a way that changes
  methodology-owned output semantics.
- Changing question-to-evidence-category mapping.
- Changing expected answer type or normalization range.
- Replacing placeholder question weights with approved numeric weights.
- Approving a numeric dimension weight set.
- Changing an approved numeric dimension weight set.
- Changing weighting philosophy in a way that changes methodology-owned output
  semantics.
- Changing mandatory dimension weight set selection criteria.
- Changing weight normalization methodology.
- Changing aggregation methodology.
- Changing Equal Contribution Default or replacing it with question-specific
  weights.
- Approving methodology-wide Scoring Scale values.
- Changing methodology-wide Scoring Scale values.
- Approving question-specific Scoring Tables.
- Changing question-specific Scoring Tables.
- Approving numeric readiness threshold values.
- Approving readiness boundary convention.
- Changing Evidence Availability methodology.
- Changing Evidence Quality methodology.
- Changing Evidence Evaluation criteria or application scope.
- Changing Finding generation methodology.
- Changing Finding identity, structure, type taxonomy, or methodology-owned
  lifecycle.
- Changing Severity Assignment Methodology.
- Approving or changing Severity Decision Table artifacts.
- Changing Risk Methodology.
- Approving or changing Risk Decision Table artifacts.
- Changing Confidence Methodology.
- Approving or changing Confidence Decision Table artifacts.
- Changing Recommendation Methodology.
- Approving or changing Recommendation Decision Table artifacts.
- Adding recommendation prioritization formulas or priority-level outputs
  beyond stable output ordering.
- Adding service decision rules.
- Changing Executive Summary Methodology.
- Approving or changing Executive Summary templates or narrative composition
  rules.
- Adding Assessment Service presentation formatting rules, if future
  methodology requires them.
- Changing Golden Fixture governance.
- Approving or changing Golden Fixture artifacts.
- Changing Production Authority governance or implementation readiness gates.

Approved Decision 2 change-control rule:

Changing a Primary Dimension for an approved production question requires a
methodology version increment, documented rationale, and preserved
traceability.

Approved Decision 4 change-control rule:

Changing approved dimension weights requires previous and new weight
documentation, written rationale, effective version, non-retroactive
application, and controlled methodology ownership. Weight changes may occur
only through approved methodology evolution and must not be made to influence
individual assessment results, customer outcomes, desired readiness
distributions, or desired scoring distributions.

Approved Decision 5 acceptance rule:

Every future numeric dimension weight set must be evaluated against every
mandatory Decision 5 criterion before approval. No candidate weight set may be
approved unless every mandatory criterion is satisfied, documented rationale is
preserved, methodology version approval is completed, and the approved weight
set is frozen.

Approved Decision 8 change-control rule:

Changing aggregation or weight normalization methodology requires methodology
versioning, documented rationale, non-retroactive behavior unless explicitly
approved by future methodology governance, and controlled methodology
ownership.

Approved Decision 9 change-control rule:

Changing question-to-dimension scoring semantics, Scoring Scale values,
Scoring Tables, or dimension result formation requires methodology versioning,
documented rationale, frozen snapshot reproducibility, and controlled
methodology ownership.

Approved Decision 10 change-control rule:

Changing readiness taxonomy, numeric threshold values, readiness boundary
convention, or readiness assignment semantics requires methodology versioning,
documented rationale, frozen snapshot reproducibility, and controlled
methodology ownership.

Approved Decision 11 change-control rule:

Changing Evidence Availability methodology, Evidence Quality methodology,
Evidence Evaluation criteria, application scope, computational properties, or
downstream consumption rules requires methodology versioning, documented
rationale, frozen snapshot reproducibility, and controlled methodology
ownership.

Approved Decision 12 change-control rule:

Changing Finding generation methodology, Finding identity, Finding structure,
Finding Type taxonomy, methodology-owned lifecycle, or downstream consumption
rules requires methodology versioning, documented rationale, frozen snapshot
reproducibility, and controlled methodology ownership. Remediation workflow,
verification workflow, closure workflow, and risk acceptance workflow remain
outside Assessment Service ownership.

Approved Decision 13 change-control rule:

Changing Severity Assignment Methodology, Severity Assignment evaluation
inputs, Severity Decision Tables, Severity Decision Table artifacts,
computational properties, or downstream consumption rules requires methodology
versioning, documented rationale, frozen snapshot reproducibility, and
controlled methodology ownership.

Approved Decision 14 change-control rule:

Changing Risk Methodology, Risk taxonomy, assessment-level synthesis
principles, evaluation conditions, Risk Decision Tables, actual Risk Decision
Table artifacts, computational properties, or downstream consumption rules
requires methodology versioning, documented rationale, frozen snapshot
reproducibility, and controlled methodology ownership.

Approved Decision 15 change-control rule:

Changing Confidence Methodology, taxonomy labels, authoritative inputs,
Confidence Decision Tables, Confidence Decision Table artifacts, computational
properties, or downstream consumption rules requires methodology versioning,
documented rationale, frozen snapshot reproducibility, and controlled
methodology ownership.

Approved Decision 16 change-control rule:

Changing Recommendation Methodology, taxonomy labels, authoritative inputs,
required metadata, Recommendation Decision Tables, Recommendation Decision
Table artifacts, computational properties, stable output ordering,
duplicate-prevention semantics, or downstream consumption rules requires
methodology versioning, documented rationale, frozen snapshot reproducibility,
and controlled methodology ownership.

Approved Decision 17 change-control rule:

Changing Executive Summary Methodology, required sections, authoritative
inputs, required metadata, Executive Summary templates, narrative composition
rules, computational properties, or downstream consumption rules requires
methodology versioning, documented rationale, frozen snapshot reproducibility,
and controlled methodology ownership.

Approved Decision 18 change-control rule:

Changing Golden Fixture governance, approved Golden Fixtures, Production
Authority governance, implementation readiness gates, validation ownership,
required computational properties, or production-authority criteria requires
methodology versioning, documented rationale, frozen snapshot reproducibility,
and controlled Assessment Service methodology ownership.

Repository evidence:

- `docs/architecture/executive-methodology-version-binding-v1.md`
- `docs/architecture/executive-input-contract-versioning-v1.md`
- `docs/architecture/business-decision-package-versioning-v1.md`

## 18. Backward Compatibility

Status: `APPROVED`

Backward compatibility requires existing immutable contracts to remain
recognizable unless a governed version change explicitly replaces them.

Current compatibility requirements:

- Public directional and executive assessment identities remain distinct.
- Current placeholder public/runtime behavior must not be silently promoted to
  executive methodology.
- BusinessDecisionPackage contract identity must remain explicit.
- BusinessDecisionPackage limitations must remain visible.
- ExecutiveRuntime response contract version must remain explicit.
- ExecutiveAssessmentSnapshot must preserve package truth without mutation.
- Unknown or unsupported versions must fail closed.

Any future Executive Assessment Rubric v1 implementation must preserve
compatibility by using governed version changes for methodology or contract
semantics that alter deterministic output meaning.

Repository evidence:

- `docs/architecture/assessment-boundary-architecture-v1.md`
- `docs/architecture/public-executive-runtime-separation-v1.md`
- `docs/architecture/business-decision-package-versioning-v1.md`
- `docs/architecture/executive-assessment-snapshot-integrity-compatibility-validation-v1.md`

## 19. Golden Fixtures & Production Authority

Status: `APPROVED` for Decision 18 Golden Fixture governance, Production
Authority governance, implementation readiness criteria, validation ownership,
repository ownership, required computational properties, Golden Fixtures v1
framework, official fixture catalog, required fixture metadata, expected-output
structure, validation framework, Golden Fixture Payloads v1 deterministic
payload definitions, Regression Validation Framework v1 governance, and
Production Authority Release v1. Implementation code remains outside this
documentation artifact.

Decision 18 defines the validation framework that every future implementation
of Executive Assessment Rubric v1 must satisfy. Golden Fixtures establish the
authoritative expected outputs for deterministic regression testing.
Production Authority defines when methodology is sufficiently complete to
authorize implementation.

Golden Fixture principles:

- Golden Fixtures are repository-owned validation artifacts.
- Golden Fixtures represent canonical assessment scenarios.
- Golden Fixtures contain approved inputs and expected outputs.
- Golden Fixtures are deterministic.
- Golden Fixtures are immutable once approved.
- Any Golden Fixture change requires a new methodology version.

Fixture coverage:

Golden Fixtures v1 validates the framework required to cover:

- Question scoring.
- Dimension results.
- Aggregation.
- Overall Assessment Result.
- Readiness.
- Evidence Evaluation.
- Findings.
- Severity.
- Risk.
- Confidence.
- Recommendations.
- Executive Summary.

Golden Fixtures v1 defines the fixture framework and official fixture catalog.
Golden Fixture Payloads v1 defines the deterministic fixture payloads and
expected outputs. Regression Validation Framework v1 defines deterministic
validation governance for comparing future implementation outputs to immutable
expected outputs. These documentation artifacts do not implement runtime
validation execution.

Production Authority:

Executive Assessment Rubric v1 implementation is authorized only when:

- Methodology decisions are approved.
- Deterministic decision tables are approved.
- Scoring tables are approved.
- Readiness thresholds are approved.
- Golden Fixtures are approved.
- Regression Validation Framework v1 is approved.
- Production Authority Release v1 is approved.
- Cross-repository contracts remain unchanged.
- Assessment Service architecture remains conformant.

Implementation readiness gates:

- Methodology completeness.
- Decision table completeness.
- Validation completeness.
- Regression fixture completeness.
- Architecture conformance.
- Repository ownership confirmation.

Required computational properties:

- Deterministic reproducibility: the same approved inputs under the same
  methodology version must produce the same expected outputs.
- Regression stability: approved Golden Fixtures must detect unintended
  changes to deterministic output behavior.
- Version Binding: Golden Fixtures, expected outputs, and Production Authority
  decisions are bound to methodology versioning.
- Traceability: Golden Fixtures must preserve references between approved
  inputs, methodology artifacts, expected outputs, and repository-owned
  validation authority.
- Auditability: Golden Fixtures and Production Authority decisions must be
  reviewable from documented methodology, expected outputs, rationale, and
  version identity.
- Fail-Closed validation: missing, malformed, unsupported, or version-mismatched
  fixture inputs or expected outputs must prevent production authority.

Decision 18 governance:

- Golden Fixture governance remains bound to methodology versioning.
- Production Authority governance remains bound to methodology versioning.
- Approved Golden Fixtures are immutable.
- Changing an approved Golden Fixture requires a new methodology version.
- Production Authority cannot be granted by implementation code, runtime
  behavior, or downstream consumer acceptance.
- Changes require controlled Assessment Service methodology ownership.

Decision 18 establishes:

- Golden Fixture governance.
- Production Authority governance.
- Implementation readiness criteria.
- Validation ownership.
- Repository ownership.

Decision 18, Regression Validation Framework v1, and Production Authority
Release v1 do not establish implementation code or runtime validation
execution.

Methodology governance status:

- No remaining methodology governance artifacts are pending.
- Future implementation remains a separate bounded implementation activity.

Repository evidence:

- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `docs/business-decision-methodology/08-business-decision-roadmap.md`
- `docs/business-decision-methodology/27-golden-fixtures-v1.md`
- `docs/business-decision-methodology/28-golden-fixture-payloads-v1.md`
- `docs/business-decision-methodology/29-regression-validation-framework-v1.md`
- `docs/business-decision-methodology/30-production-authority-release-v1.md`
- `docs/architecture/executive-runtime-contract-test-strategy-v1.md`

## 20. Production Approval Requirements

Status: `APPROVED` for Decision 18 Production Authority governance and
implementation readiness gates, Golden Fixtures v1 framework, and Golden
Fixture Payloads v1 deterministic payload definitions, and Regression
Validation Framework v1 governance, and Production Authority Release v1.
Implementation remains a separate bounded activity.

Production-authoritative executive output requires approved final methodology
for all emitted final business conclusions and approved Golden Fixtures for
deterministic regression validation.

Required before production-authoritative rubric output:

- Approved methodology completeness for all emitted outputs.
- Approved Scoring Scale Specification v1.
- Approved question-specific Scoring Tables.
- Approved Readiness Threshold Values v1.
- Approved Severity Decision Tables v1, if Severity is emitted as final finding
  output.
- Approved Risk Decision Tables v1, if Risk is emitted as final assessment-level
  output.
- Approved Confidence Decision Tables v1, if Confidence Assessment is emitted
  as final output.
- Approved Recommendation Decision Tables v1 before Recommendations are
  emitted.
- Approved Executive Summary Templates v1 before Executive Summary output is
  represented as evaluated.
- Approved Golden Fixtures v1 framework and official fixture catalog.
- Approved Golden Fixture Payloads v1 covering representative executive
  assessment cases.
- Approved Regression Validation Framework v1.
- Approved Production Authority Release v1.
- Approved validation completeness and regression fixture completeness.
- Confirmed Assessment Service architecture conformance.
- Confirmed Assessment Service repository ownership.
- Confirmed unchanged cross-repository contracts.
- Release documentation stating which outputs are production-authoritative and
  which remain foundation-only.

Repository evidence:

- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `docs/releases/sprint5-executive-runtime-readiness-foundation-complete-v1.md`
- `docs/business-decision-methodology/08-business-decision-roadmap.md`

## 21. Outstanding Methodology Gaps

Status: `APPROVED`

No remaining methodology governance gaps block future bounded implementation
of production-authoritative Executive Assessment Rubric v1.

Future implementation must execute the approved methodology baseline and
remain subject to Assessment Service repository ownership, architecture
conformance, version binding, immutable expected outputs, and fail-closed
validation.

Repository evidence:

- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `docs/architecture/executive-methodology-version-binding-v1.md`
- `docs/business-decision-methodology/08-business-decision-roadmap.md`
- `docs/business-decision-methodology/30-production-authority-release-v1.md`
