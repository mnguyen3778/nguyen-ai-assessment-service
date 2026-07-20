# Business Decision Roadmap

## Purpose

This document describes how Nguyen AI's Business Decision Methodology should
evolve into a proprietary executive intelligence platform.

Methodology version: `business-decision-methodology-v1`

## Evolution Path

```text
Business Rule Engine
  |
Decision Engine
  |
Executive Intelligence Engine
  |
Portfolio Intelligence
  |
Digital Twin
```

## Stage 1: Business Rule Engine

Purpose:

- Convert approved methodology into deterministic, testable rules.

Capabilities:

- Question catalog.
- Evidence catalog.
- Readiness dimensions.
- Weight categories.
- Risk adjustments.
- Confidence adjustments.
- Recommendation priority.
- Service decision rules.

Business value:

- Creates repeatable advisory logic.

Executive value:

- Produces explainable recommendations that can be defended.

Required before implementation:

- Approved numeric weights.
- Approved thresholds.
- Approved risk caps.
- Approved confidence logic.
- Golden test cases.

## Stage 2: Decision Engine

Purpose:

- Convert business rules into structured executive decisions.

Capabilities:

- Domain readiness scoring.
- Overall readiness assessment.
- Priority action generation.
- Executive recommendation selection.
- Service routing.
- Audit trace production.

Business value:

- Turns assessments into structured decision support.

Executive value:

- Gives leaders a clear action sequence tied to evidence and business impact.

## Stage 3: Executive Intelligence Engine

Purpose:

- Convert deterministic decisions into executive-ready summaries, reports, and
  briefings.

Capabilities:

- Executive summaries from approved templates.
- Board-ready snapshot generation.
- Trend comparison across assessment versions.
- Evidence-backed recommendation narratives.

Business value:

- Scales advisory communication while preserving consistency.

Executive value:

- Provides clear, reproducible decision narratives.

AI use constraint:

- Generative AI may assist with phrasing only when constrained to approved facts,
  templates, evidence references, and deterministic recommendations.

## Stage 4: Portfolio Intelligence

Purpose:

- Analyze readiness across multiple clients, business units, or assessment
  cohorts.

Capabilities:

- Portfolio-level readiness distribution.
- Common risk and capability gaps.
- Service demand forecasting.
- Benchmarking with anonymized and governed data.
- Trend analysis.

Business value:

- Supports strategic planning, service design, and market intelligence.

Executive value:

- Helps leaders compare progress, prioritize investments, and identify systemic
  risks.

Governance requirement:

- Portfolio intelligence must protect client confidentiality and use approved
  aggregation rules.

## Stage 5: Digital Twin

Purpose:

- Represent the organization's business capability, evidence, risk, and decision
  state as a living model.

Capabilities:

- Current-state business capability model.
- Evidence updates from assessments and approved integrations.
- Scenario analysis.
- Readiness trend simulation.
- Decision impact modeling.

Business value:

- Enables continuous executive intelligence rather than point-in-time reporting.

Executive value:

- Gives leaders a living view of capability, risk, investment priorities, and
  transformation readiness.

AI use constraint:

- Digital twin recommendations must remain rule-governed and evidence-traceable.
  AI may support scenario explanation but must not become an opaque decision
  authority.

## Methodology Review

The eight methodology documents were reviewed as a set against the architecture
baseline and readiness gaps.

### Document Review Matrix

| Document | Review Result | Notes |
| --- | --- | --- |
| `01-decision-methodology.md` | Complete for v1 methodology baseline. | Defines the full traceable decision flow from assessment question to executive recommendation. |
| `02-question-catalog.md` | Complete for canonical v1 question baseline. | Defines question IDs, capabilities, evidence categories, dimensions, answer types, and weight categories without numeric weights. |
| `03-evidence-catalog.md` | Complete for v1 evidence taxonomy. | Defines evidence categories, business meaning, maturity expectations, coverage rules, and reference naming. |
| `04-readiness-methodology.md` | Complete for dimension definitions. | Defines purpose, inputs, business interpretation, executive interpretation, and dependencies for all readiness dimensions. |
| `05-confidence-methodology.md` | Complete for non-formula confidence methodology. | Defines confidence factors, levels, suppression principles, traceability, and testability requirements. |
| `06-recommendation-priority.md` | Complete for priority methodology. | Defines Critical, High, Medium, and Low priority with deterministic ordering principles. |
| `07-service-decision-framework.md` | Complete for service routing methodology. | Defines deterministic mapping principles for Nguyen AI service categories and routing overrides. |
| `08-business-decision-roadmap.md` | Complete for evolution and review. | Defines the roadmap from Business Rule Engine to Digital Twin and records contradictions, missing methodology, readiness score, and first coding milestone. |

### Contradictions Identified

| Area | Finding | Resolution |
| --- | --- | --- |
| Numeric weights | The question catalog defines weight categories but not numeric weights. | This is intentional. Numeric weights require business approval before coding. |
| Text evidence | The question catalog allows `text-evidence`, while the framework requires deterministic scoring. | Text evidence may support context only until deterministic review rules exist. |
| Services vs tiers | Prior architecture discussed service tiers; this methodology defines service categories. | Service categories are the v1 deterministic routing target. Commercial tiers can be mapped later after service packaging is approved. |
| Business Readiness as a dimension | Business Readiness overlaps with executive strategy and leadership evidence. | This is intentional. Business Readiness is the executive alignment dimension that constrains technology recommendations. |

No blocking contradiction was identified. The methodology is internally
consistent if numeric scoring is deferred until weights and thresholds are
approved.

### Missing Methodology

The following items remain required before production scoring can be coded:

- Numeric domain weights.
- Numeric question weights.
- Readiness threshold boundaries.
- Risk cap rules.
- Confidence formula.
- Service routing decision table.
- Recommendation catalog entries.
- Executive summary templates.
- Audit trace schema.
- Golden test fixtures.

These are not omissions from the business methodology baseline. They are the
next methodology approval artifacts required before implementation.

## Methodology Readiness Score

Overall methodology readiness: **84%**

| Category | Score | Rationale |
| --- | --- | --- |
| Explainability | 92% | The decision flow, evidence catalog, and traceability rules make outputs explainable. |
| Determinism | 86% | Deterministic stages are defined; numeric formulas remain intentionally deferred. |
| Evidence basis | 90% | Canonical questions and evidence categories are mapped to capabilities and dimensions. |
| Auditability | 82% | Traceability standards are defined; audit trace schema remains a future artifact. |
| Testability | 78% | Testability requirements are defined; golden fixtures are still needed. |
| Versioning | 88% | Methodology versioning is declared across documents. |
| Implementation specificity | 72% | Sufficient for methodology approval and scaffolding; not yet sufficient for final scoring. |

## Recommended First Coding Milestone After Methodology Approval

Recommended milestone: **Decision Methodology Configuration Scaffold**

Scope:

1. Add configuration-only representations of question IDs, evidence categories,
   readiness dimensions, weight categories, priority levels, and service IDs.
2. Add validation tests proving every catalog entry has required metadata.
3. Add traceability tests proving every question maps to a capability, evidence
   category, readiness dimension, answer type, and weight category.
4. Add no numeric scoring behavior until weights and thresholds are approved.
5. Preserve the current placeholder response until the versioned output contract
   is approved.

Exit criteria:

- Methodology constants are represented in code without implementing final
  scoring.
- Every catalog entry is test-covered for completeness.
- No recommendation can be emitted without evidence references.
- The repository remains deterministic and backwards compatible.
