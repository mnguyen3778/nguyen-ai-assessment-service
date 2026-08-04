# Question Scoring Tables v1

## 1. Purpose

Status: `APPROVED`

This document defines the deterministic Question Scoring Tables for all 48
canonical executive assessment questions in `business-decision-methodology-v1`.

Each table maps allowable responses to normalized scores on the approved
0-to-100 scoring scale.

This document does not define readiness thresholds, severity rules, risk
rules, confidence rules, recommendation rules, executive summary rules,
implementation code, package contracts, or snapshot contracts.

## 2. Scope

Status: `APPROVED`

In scope:

- All 48 canonical question IDs.
- Question text.
- Primary Dimension from Question Mapping Matrix v1.
- Allowable responses.
- Deterministic response-to-score mappings.
- Validation rules.
- Fail-closed conditions.
- Version identity.

Out of scope:

- Readiness thresholds.
- Severity, Risk, Confidence, or Recommendation decision table rows.
- Executive Summary templates or narrative rules.
- Question-specific weights.
- Secondary Dimension scoring.
- Runtime behavior.
- Package or snapshot contract changes.

## 3. Version Identity

Status: `APPROVED`

Question scoring tables version:

```text
question-scoring-tables-v1
```

Scoring scale version:

```text
scoring-scale-v1
```

Methodology version:

```text
business-decision-methodology-v1
```

Taxonomy version:

```text
business-capability-taxonomy-v1
```

## 4. Shared Response Models

Status: `APPROVED`

### `scale-0-4`

The `scale-0-4` response model is the approved maturity or completion scale
used by 47 canonical questions.

Allowable responses and deterministic scores:

| Response | Normalized Score |
| ---: | ---: |
| 0 | 0 |
| 1 | 25 |
| 2 | 50 |
| 3 | 75 |
| 4 | 100 |

### `numeric-0-100`

The `numeric-0-100` response model is the approved numeric model used by
`q.automation.manual-volume`.

Allowable responses and deterministic scores:

| Response | Normalized Score |
| --- | --- |
| Any numeric value from 0 to 100 inclusive | Same numeric value |

The numeric mapping is identity normalization on the approved 0-to-100 scoring
scale.

## 5. Shared Validation Rules

Status: `APPROVED`

For every Question Scoring Table:

- The Question ID must be present in the canonical question catalog.
- The Question ID must be present in Question Mapping Matrix v1.
- The Primary Dimension must match Question Mapping Matrix v1.
- The scoring scale version must be `scoring-scale-v1`.
- The scoring table version must be `question-scoring-tables-v1`.
- The methodology version must be `business-decision-methodology-v1`.
- Each allowable response must map to exactly one normalized score.
- Every normalized score must be within 0 and 100 inclusive.
- Scoring must use Primary Dimension ownership.
- Secondary Dimensions remain traceability metadata only.

## 6. Shared Fail-Closed Conditions

Status: `APPROVED`

For every Question Scoring Table, scoring must fail closed when:

- The Question ID is missing.
- The Question ID is duplicated.
- The Question ID is unknown.
- The submitted response is missing.
- The submitted response is not one of the allowable responses.
- The response type does not match the approved response model.
- The scoring table version is unsupported.
- The scoring scale version is unsupported.
- The methodology version is unsupported.
- The normalized score would fall outside 0 to 100 inclusive.

## 7. Question Scoring Tables

Status: `APPROVED`

| Question ID | Question Text | Primary Dimension | Allowable Responses | Deterministic Response-to-Score Mapping | Validation Rules | Fail-Closed Conditions | Version |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `q.ai.strategy.business-goals` | Align AI initiatives to measurable business goals. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.ai.leadership.sponsor` | Assign executive sponsorship for AI adoption. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.ai.governance.owner` | Establish accountable AI governance ownership. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.ai.use-cases.prioritized` | Prioritize AI use cases by business value and feasibility. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.ai.success-metrics.defined` | Define success metrics for AI initiatives. | `RVCI` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.ai.risk-policy.approved` | Maintain approved policy for acceptable AI use. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.security.identity.mfa` | Protect user access with strong authentication. | `DPSC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.security.access.review` | Review access rights on a recurring basis. | `DPSC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.security.data.classification` | Classify business and customer data by sensitivity. | `DPSC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.security.incident-response.owner` | Assign incident response ownership and escalation. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.security.vendor.controls` | Assess vendor and third-party security controls. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.security.backup.recovery-tested` | Test recovery from backup or continuity procedures. | `RVCI` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.knowledge.docs.current` | Maintain current documentation for key business processes. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.knowledge.owner.defined` | Assign owners for critical knowledge assets. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.knowledge.searchable` | Make operational knowledge searchable and reusable. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.knowledge.sme-dependency` | Reduce dependency on single subject matter experts. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.knowledge.refresh-cadence` | Review and refresh knowledge assets on a defined cadence. | `RVCI` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.knowledge.customer-context` | Capture customer context and decision history consistently. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.automation.process-documented` | Document processes before automation. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.automation.manual-volume` | Identify high-volume manual work suitable for automation. | `POC` | `numeric-0-100`: any numeric value from `0` to `100` inclusive | `n -> n` for every valid numeric response `n` where `0 <= n <= 100` | Apply shared validation rules for `numeric-0-100`; response must be numeric and within 0 to 100 inclusive. | Apply shared fail-closed conditions; non-numeric, below-0, and above-100 responses fail closed. | `question-scoring-tables-v1` |
| `q.automation.exception-handling` | Define exception handling and ownership for automated workflows. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.automation.integration-readiness` | Confirm systems expose reliable integration paths. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.automation.measurement` | Measure automation outcomes and process impact. | `RVCI` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.automation.change-control` | Govern changes to automated workflows. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.engineering.source-control` | Manage application and automation code in source control. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.engineering.testing` | Validate changes with repeatable tests. | `RVCI` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.engineering.release-process` | Use a controlled release process. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.engineering.observability` | Monitor systems with actionable logs, metrics, or alerts. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.engineering.backlog-prioritization` | Prioritize technical work by business impact. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.engineering.ownership` | Assign ownership for systems and operational support. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.cloud.account-structure` | Maintain governed cloud account or environment structure. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.cloud.cost-controls` | Monitor and control cloud spend. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.cloud.security-baseline` | Apply baseline cloud security controls. | `DPSC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.cloud.infrastructure-as-code` | Manage cloud configuration through repeatable deployment practices. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.cloud.resilience` | Define resilience, backup, or recovery expectations for cloud workloads. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.cloud.monitoring` | Monitor cloud workload health and operational status. | `TISM` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.operations.process-ownership` | Assign accountable owners for critical business processes. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.operations.kpi-defined` | Define operational KPIs for key processes. | `RVCI` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.operations.escalation-path` | Define escalation paths for operational issues. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.operations.capacity-planning` | Plan capacity for people, systems, and process demand. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.operations.change-management` | Manage operational change with communication and ownership. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.operations.continuity` | Maintain continuity plans for critical operations. | `POC` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.business.outcomes-defined` | Define target business outcomes for technology initiatives. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.business.customer-impact` | Connect initiatives to measurable customer impact. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.business.financial-case` | Define cost, benefit, or investment rationale. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.business.executive-alignment` | Align executive stakeholders on priority and timing. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.business.risk-appetite` | Define acceptable risk for AI, automation, and cloud initiatives. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |
| `q.business.decision-cadence` | Maintain a regular decision cadence for transformation initiatives. | `GCR` | `scale-0-4`: `0`, `1`, `2`, `3`, `4` | `0 -> 0`; `1 -> 25`; `2 -> 50`; `3 -> 75`; `4 -> 100` | Apply shared validation rules for `scale-0-4`. | Apply shared fail-closed conditions. | `question-scoring-tables-v1` |

## 8. Validation Summary

Status: `APPROVED`

| Validation Requirement | Result |
| --- | --- |
| Every canonical question has exactly one scoring table. | Pass |
| Every allowable response maps to exactly one score. | Pass |
| No undefined responses exist for approved response models. | Pass |
| No duplicate question IDs are present. | Pass |
| All mappings are deterministic. | Pass |
| All mappings conform to the approved 0-to-100 scoring scale. | Pass |
| Invalid responses fail closed. | Pass |
| All 48 canonical questions are covered. | Pass |
| 47 questions use `scale-0-4`. | Pass |
| 1 question uses `numeric-0-100`. | Pass |

## 9. Remaining Out Of Scope

Status: `METHODOLOGY_PENDING`

- Regression validation implementation.

## 10. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE QUESTION SCORING TABLES V1
```

The 48 canonical Question Scoring Tables are approved for
`business-decision-methodology-v1` using `scoring-scale-v1`. They provide one
deterministic normalized score for every allowable response under the approved
response models.

No implementation code is authorized by this artifact.

Repository evidence:

- `docs/business-decision-methodology/02-question-catalog.md`
- `docs/business-decision-methodology/10-question-mapping-matrix-v1.md`
- `docs/business-decision-methodology/13-scoring-scale-specification-v1.md`
- `docs/business-decision-methodology/14-question-scoring-tables-specification-v1.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
