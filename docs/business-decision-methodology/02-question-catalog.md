# Question Catalog

## Purpose

This document defines the canonical v1 assessment question catalog for Nguyen
AI's Business Decision Methodology.

The catalog does not assign numeric weights. Each question declares a weight
category so that numeric weights can be approved later through governance.

Methodology version: `business-decision-methodology-v1`

## Answer Types

Allowed expected answer types:

- `scale-0-4`: maturity or completion scale.
- `yes-no`: binary evidence.
- `single-select`: one option from an approved set.
- `multi-select`: multiple options from an approved set.
- `numeric`: quantity, count, or percentage.
- `text-evidence`: short factual description used for context, not scoring
  unless mapped by deterministic review rules.

## Weight Categories

Allowed weight categories:

- `foundational-control`
- `strategic-alignment`
- `operational-capability`
- `value-enablement`
- `risk-control`
- `scale-readiness`

## Canonical Questions

| Question ID | Business Capability | Evidence Category | Readiness Dimension | Expected Answer Type | Weight Category |
| --- | --- | --- | --- | --- | --- |
| `q.ai.strategy.business-goals` | Align AI initiatives to measurable business goals. | Strategy | AI Readiness | `scale-0-4` | `strategic-alignment` |
| `q.ai.leadership.sponsor` | Assign executive sponsorship for AI adoption. | Leadership | AI Readiness | `scale-0-4` | `strategic-alignment` |
| `q.ai.governance.owner` | Establish accountable AI governance ownership. | Governance | AI Readiness | `scale-0-4` | `foundational-control` |
| `q.ai.use-cases.prioritized` | Prioritize AI use cases by business value and feasibility. | Strategy | AI Readiness | `scale-0-4` | `value-enablement` |
| `q.ai.success-metrics.defined` | Define success metrics for AI initiatives. | Strategy | AI Readiness | `scale-0-4` | `strategic-alignment` |
| `q.ai.risk-policy.approved` | Maintain approved policy for acceptable AI use. | Governance | AI Readiness | `scale-0-4` | `risk-control` |
| `q.security.identity.mfa` | Protect user access with strong authentication. | Security | Security Readiness | `scale-0-4` | `foundational-control` |
| `q.security.access.review` | Review access rights on a recurring basis. | Security | Security Readiness | `scale-0-4` | `risk-control` |
| `q.security.data.classification` | Classify business and customer data by sensitivity. | Data | Security Readiness | `scale-0-4` | `foundational-control` |
| `q.security.incident-response.owner` | Assign incident response ownership and escalation. | Operations | Security Readiness | `scale-0-4` | `risk-control` |
| `q.security.vendor.controls` | Assess vendor and third-party security controls. | Governance | Security Readiness | `scale-0-4` | `risk-control` |
| `q.security.backup.recovery-tested` | Test recovery from backup or continuity procedures. | Operations | Security Readiness | `scale-0-4` | `foundational-control` |
| `q.knowledge.docs.current` | Maintain current documentation for key business processes. | Knowledge | Knowledge Readiness | `scale-0-4` | `operational-capability` |
| `q.knowledge.owner.defined` | Assign owners for critical knowledge assets. | Knowledge | Knowledge Readiness | `scale-0-4` | `operational-capability` |
| `q.knowledge.searchable` | Make operational knowledge searchable and reusable. | Technology | Knowledge Readiness | `scale-0-4` | `scale-readiness` |
| `q.knowledge.sme-dependency` | Reduce dependency on single subject matter experts. | Operations | Knowledge Readiness | `scale-0-4` | `risk-control` |
| `q.knowledge.refresh-cadence` | Review and refresh knowledge assets on a defined cadence. | Governance | Knowledge Readiness | `scale-0-4` | `operational-capability` |
| `q.knowledge.customer-context` | Capture customer context and decision history consistently. | Knowledge | Business Readiness | `scale-0-4` | `value-enablement` |
| `q.automation.process-documented` | Document processes before automation. | Automation | Automation Readiness | `scale-0-4` | `foundational-control` |
| `q.automation.manual-volume` | Identify high-volume manual work suitable for automation. | Operations | Automation Readiness | `numeric` | `value-enablement` |
| `q.automation.exception-handling` | Define exception handling and ownership for automated workflows. | Automation | Automation Readiness | `scale-0-4` | `risk-control` |
| `q.automation.integration-readiness` | Confirm systems expose reliable integration paths. | Technology | Automation Readiness | `scale-0-4` | `operational-capability` |
| `q.automation.measurement` | Measure automation outcomes and process impact. | Operations | Automation Readiness | `scale-0-4` | `value-enablement` |
| `q.automation.change-control` | Govern changes to automated workflows. | Governance | Automation Readiness | `scale-0-4` | `risk-control` |
| `q.engineering.source-control` | Manage application and automation code in source control. | Technology | Engineering Readiness | `scale-0-4` | `foundational-control` |
| `q.engineering.testing` | Validate changes with repeatable tests. | Technology | Engineering Readiness | `scale-0-4` | `foundational-control` |
| `q.engineering.release-process` | Use a controlled release process. | Operations | Engineering Readiness | `scale-0-4` | `operational-capability` |
| `q.engineering.observability` | Monitor systems with actionable logs, metrics, or alerts. | Operations | Engineering Readiness | `scale-0-4` | `risk-control` |
| `q.engineering.backlog-prioritization` | Prioritize technical work by business impact. | Strategy | Engineering Readiness | `scale-0-4` | `strategic-alignment` |
| `q.engineering.ownership` | Assign ownership for systems and operational support. | Leadership | Engineering Readiness | `scale-0-4` | `operational-capability` |
| `q.cloud.account-structure` | Maintain governed cloud account or environment structure. | Cloud | Cloud Readiness | `scale-0-4` | `foundational-control` |
| `q.cloud.cost-controls` | Monitor and control cloud spend. | Cloud | Cloud Readiness | `scale-0-4` | `risk-control` |
| `q.cloud.security-baseline` | Apply baseline cloud security controls. | Security | Cloud Readiness | `scale-0-4` | `foundational-control` |
| `q.cloud.infrastructure-as-code` | Manage cloud configuration through repeatable deployment practices. | Technology | Cloud Readiness | `scale-0-4` | `scale-readiness` |
| `q.cloud.resilience` | Define resilience, backup, or recovery expectations for cloud workloads. | Operations | Cloud Readiness | `scale-0-4` | `risk-control` |
| `q.cloud.monitoring` | Monitor cloud workload health and operational status. | Operations | Cloud Readiness | `scale-0-4` | `operational-capability` |
| `q.operations.process-ownership` | Assign accountable owners for critical business processes. | Operations | Operational Readiness | `scale-0-4` | `operational-capability` |
| `q.operations.kpi-defined` | Define operational KPIs for key processes. | Strategy | Operational Readiness | `scale-0-4` | `strategic-alignment` |
| `q.operations.escalation-path` | Define escalation paths for operational issues. | Operations | Operational Readiness | `scale-0-4` | `risk-control` |
| `q.operations.capacity-planning` | Plan capacity for people, systems, and process demand. | Operations | Operational Readiness | `scale-0-4` | `scale-readiness` |
| `q.operations.change-management` | Manage operational change with communication and ownership. | Governance | Operational Readiness | `scale-0-4` | `risk-control` |
| `q.operations.continuity` | Maintain continuity plans for critical operations. | Operations | Operational Readiness | `scale-0-4` | `foundational-control` |
| `q.business.outcomes-defined` | Define target business outcomes for technology initiatives. | Strategy | Business Readiness | `scale-0-4` | `strategic-alignment` |
| `q.business.customer-impact` | Connect initiatives to measurable customer impact. | Strategy | Business Readiness | `scale-0-4` | `value-enablement` |
| `q.business.financial-case` | Define cost, benefit, or investment rationale. | Strategy | Business Readiness | `scale-0-4` | `strategic-alignment` |
| `q.business.executive-alignment` | Align executive stakeholders on priority and timing. | Leadership | Business Readiness | `scale-0-4` | `strategic-alignment` |
| `q.business.risk-appetite` | Define acceptable risk for AI, automation, and cloud initiatives. | Governance | Business Readiness | `scale-0-4` | `risk-control` |
| `q.business.decision-cadence` | Maintain a regular decision cadence for transformation initiatives. | Leadership | Business Readiness | `scale-0-4` | `operational-capability` |

## Traceability Rules

- A question may support multiple future rules, but it has one primary readiness
  dimension in this catalog.
- Numeric answers must be normalized before they contribute to scoring.
- `text-evidence` answers may support executive context, but they must not drive
  scoring until deterministic review criteria exist.
- Questions with `foundational-control` or `risk-control` weight categories are
  candidates for future risk adjustments.
- Questions with `strategic-alignment` weight category are candidates for
  Business Readiness and Executive Recommendation influence.
- Questions with `value-enablement` weight category should not override severe
  foundational gaps.

## Governance Rules

- New questions require a stable question ID.
- Retired questions must remain documented for historical assessment versions.
- Question meaning must not change within the same methodology version.
- Any future numeric weight must be approved separately from this catalog.

