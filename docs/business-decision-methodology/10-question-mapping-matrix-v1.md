# Question Mapping Matrix v1

## Purpose

This document defines the authoritative Question Mapping Matrix for the 48
canonical executive assessment questions in
`business-decision-methodology-v1`.

The matrix applies the approved Decision 1 and Decision 2 methodology:

- Five approved Business Capability Dimensions.
- Evidence Quality, Traceability & Auditability as a cross-cutting quality
  factor, not a sixth dimension.
- Exactly one Primary Dimension per canonical question.
- Zero, one, or two Secondary Dimensions per canonical question.
- Deterministic mapping based on the underlying business capability evaluated
  by each question.
- Mapping traceability through rationale and taxonomy version.

This document does not define scoring, weights, aggregation, readiness
thresholds, findings, risks, recommendations, confidence formulas, executive
summary rules, implementation behavior, package contracts, or snapshot
contracts.

## Taxonomy Version

Taxonomy version: `business-capability-taxonomy-v1`

Methodology version: `business-decision-methodology-v1`

`business-capability-taxonomy-v1` identifies the approved Decision 1 and
Decision 2 business capability dimension taxonomy within the current
methodology version.

## Approved Dimensions

| Dimension Code | Approved Business Capability Dimension |
| --- | --- |
| `POC` | Process & Operational Control |
| `GCR` | Governance, Compliance & Regulatory Readiness |
| `TISM` | Technology & Intelligent Systems Management |
| `DPSC` | Data, Privacy & Security Controls |
| `RVCI` | Remediation, Verification & Continuous Improvement |

## Mapping Rules

Status: `APPROVED`

- Every canonical assessment question has exactly one Primary Dimension.
- A question may have zero, one, or two Secondary Dimensions.
- Secondary Dimensions are used only when the question materially contributes
  to another approved business capability.
- Secondary Dimensions require explicit justification in the mapping rationale.
- Every approved Business Capability Dimension must contain at least one
  canonical assessment question.
- Questions that require more than two Secondary Dimensions should be rewritten
  or divided into smaller questions.
- Mapping decisions must remain deterministic and reproducible.

The scoring contribution of Primary and Secondary Dimensions is
`METHODOLOGY_PENDING` until Dimension Weighting and Aggregation Methodology is
approved.

## Question Mapping Matrix

| Question ID | Question Text | Primary Dimension | Secondary Dimension(s) | Mapping Rationale | Taxonomy Version |
| --- | --- | --- | --- | --- | --- |
| `q.ai.strategy.business-goals` | Align AI initiatives to measurable business goals. | `GCR` | `TISM` | Primary mapping is governance and oversight because the question evaluates whether AI work is directed by business goals. Secondary mapping is technology management because the goals guide intelligent-system use. | `business-capability-taxonomy-v1` |
| `q.ai.leadership.sponsor` | Assign executive sponsorship for AI adoption. | `GCR` | None | Primary mapping is governance and accountability because the question evaluates executive sponsorship and decision ownership. | `business-capability-taxonomy-v1` |
| `q.ai.governance.owner` | Establish accountable AI governance ownership. | `GCR` | `TISM` | Primary mapping is governance because the question evaluates accountable AI oversight. Secondary mapping is technology management because AI governance ownership affects intelligent-system lifecycle accountability. | `business-capability-taxonomy-v1` |
| `q.ai.use-cases.prioritized` | Prioritize AI use cases by business value and feasibility. | `TISM` | `GCR` | Primary mapping is technology and intelligent systems management because the question evaluates AI use-case lifecycle prioritization. Secondary mapping is governance because prioritization requires accountable business oversight. | `business-capability-taxonomy-v1` |
| `q.ai.success-metrics.defined` | Define success metrics for AI initiatives. | `RVCI` | `GCR` | Primary mapping is remediation and continuous improvement because the question evaluates measurable feedback for AI initiatives. Secondary mapping is governance because success metrics support oversight and accountability. | `business-capability-taxonomy-v1` |
| `q.ai.risk-policy.approved` | Maintain approved policy for acceptable AI use. | `GCR` | `TISM` | Primary mapping is governance and compliance readiness because the question evaluates approved policy and acceptable-use oversight. Secondary mapping is technology management because the policy constrains AI system operation. | `business-capability-taxonomy-v1` |
| `q.security.identity.mfa` | Protect user access with strong authentication. | `DPSC` | `GCR` | Primary mapping is data, privacy, and security controls because the question evaluates access protection. Secondary mapping is governance because strong authentication supports control obligations. | `business-capability-taxonomy-v1` |
| `q.security.access.review` | Review access rights on a recurring basis. | `DPSC` | `GCR` | Primary mapping is data, privacy, and security controls because the question evaluates access control review. Secondary mapping is governance because recurring review supports accountability and compliance readiness. | `business-capability-taxonomy-v1` |
| `q.security.data.classification` | Classify business and customer data by sensitivity. | `DPSC` | None | Primary mapping is data, privacy, and security controls because the question evaluates data classification and sensitivity handling. | `business-capability-taxonomy-v1` |
| `q.security.incident-response.owner` | Assign incident response ownership and escalation. | `POC` | `DPSC` | Primary mapping is process and operational control because the question evaluates incident response ownership and escalation execution. Secondary mapping is data, privacy, and security controls because the process protects security outcomes. | `business-capability-taxonomy-v1` |
| `q.security.vendor.controls` | Assess vendor and third-party security controls. | `TISM` | `DPSC` | Primary mapping is technology and intelligent systems management because Decision 2 places vendor management in this dimension. Secondary mapping is data, privacy, and security controls because the vendor assessment concerns security controls. | `business-capability-taxonomy-v1` |
| `q.security.backup.recovery-tested` | Test recovery from backup or continuity procedures. | `RVCI` | `POC` | Primary mapping is remediation, verification, and continuous improvement because the question evaluates tested recovery. Secondary mapping is process and operational control because recovery testing supports operational continuity. | `business-capability-taxonomy-v1` |
| `q.knowledge.docs.current` | Maintain current documentation for key business processes. | `POC` | `RVCI` | Primary mapping is process and operational control because the question evaluates documented business processes. Secondary mapping is remediation and continuous improvement because keeping documentation current requires review and update discipline. | `business-capability-taxonomy-v1` |
| `q.knowledge.owner.defined` | Assign owners for critical knowledge assets. | `POC` | `GCR` | Primary mapping is process and operational control because the question evaluates operational ownership of knowledge assets. Secondary mapping is governance because ownership supports accountability. | `business-capability-taxonomy-v1` |
| `q.knowledge.searchable` | Make operational knowledge searchable and reusable. | `TISM` | `POC` | Primary mapping is technology and intelligent systems management because the question evaluates technology-enabled knowledge retrieval. Secondary mapping is process and operational control because reusable knowledge supports repeatable execution. | `business-capability-taxonomy-v1` |
| `q.knowledge.sme-dependency` | Reduce dependency on single subject matter experts. | `POC` | None | Primary mapping is process and operational control because the question evaluates whether operations can run consistently without single-person dependency. | `business-capability-taxonomy-v1` |
| `q.knowledge.refresh-cadence` | Review and refresh knowledge assets on a defined cadence. | `RVCI` | `POC` | Primary mapping is remediation, verification, and continuous improvement because the question evaluates recurring review and refresh. Secondary mapping is process and operational control because current knowledge supports reliable operations. | `business-capability-taxonomy-v1` |
| `q.knowledge.customer-context` | Capture customer context and decision history consistently. | `POC` | `GCR` | Primary mapping is process and operational control because the question evaluates consistent capture of business context. Secondary mapping is governance because decision history supports accountability and oversight. | `business-capability-taxonomy-v1` |
| `q.automation.process-documented` | Document processes before automation. | `POC` | `TISM` | Primary mapping is process and operational control because the question evaluates process documentation. Secondary mapping is technology and intelligent systems management because the documentation enables safe automation. | `business-capability-taxonomy-v1` |
| `q.automation.manual-volume` | Identify high-volume manual work suitable for automation. | `POC` | `TISM` | Primary mapping is process and operational control because the question evaluates process demand and execution burden. Secondary mapping is technology and intelligent systems management because manual-volume evidence informs automation suitability. | `business-capability-taxonomy-v1` |
| `q.automation.exception-handling` | Define exception handling and ownership for automated workflows. | `POC` | `TISM` | Primary mapping is process and operational control because the question evaluates exception handling and ownership. Secondary mapping is technology and intelligent systems management because the process governs automated workflows. | `business-capability-taxonomy-v1` |
| `q.automation.integration-readiness` | Confirm systems expose reliable integration paths. | `TISM` | `POC` | Primary mapping is technology and intelligent systems management because the question evaluates integration capability. Secondary mapping is process and operational control because reliable integrations support repeatable operations. | `business-capability-taxonomy-v1` |
| `q.automation.measurement` | Measure automation outcomes and process impact. | `RVCI` | `POC` | Primary mapping is remediation, verification, and continuous improvement because the question evaluates outcome measurement. Secondary mapping is process and operational control because measurement concerns process impact. | `business-capability-taxonomy-v1` |
| `q.automation.change-control` | Govern changes to automated workflows. | `GCR` | `TISM` | Primary mapping is governance and compliance readiness because the question evaluates governed change control. Secondary mapping is technology and intelligent systems management because the governed changes affect automated workflows. | `business-capability-taxonomy-v1` |
| `q.engineering.source-control` | Manage application and automation code in source control. | `TISM` | `RVCI` | Primary mapping is technology and intelligent systems management because the question evaluates lifecycle control over code. Secondary mapping is remediation and verification because source control supports review, correction, and traceability. | `business-capability-taxonomy-v1` |
| `q.engineering.testing` | Validate changes with repeatable tests. | `RVCI` | `TISM` | Primary mapping is remediation, verification, and continuous improvement because the question evaluates repeatable validation. Secondary mapping is technology and intelligent systems management because testing governs technology lifecycle quality. | `business-capability-taxonomy-v1` |
| `q.engineering.release-process` | Use a controlled release process. | `TISM` | `POC` | Primary mapping is technology and intelligent systems management because the question evaluates release lifecycle control. Secondary mapping is process and operational control because controlled releases support repeatable execution. | `business-capability-taxonomy-v1` |
| `q.engineering.observability` | Monitor systems with actionable logs, metrics, or alerts. | `TISM` | `RVCI` | Primary mapping is technology and intelligent systems management because the question evaluates monitoring of systems. Secondary mapping is remediation and continuous improvement because actionable monitoring supports correction and improvement. | `business-capability-taxonomy-v1` |
| `q.engineering.backlog-prioritization` | Prioritize technical work by business impact. | `GCR` | `TISM` | Primary mapping is governance and compliance readiness because the question evaluates business oversight of priorities. Secondary mapping is technology and intelligent systems management because the prioritized work affects technology systems. | `business-capability-taxonomy-v1` |
| `q.engineering.ownership` | Assign ownership for systems and operational support. | `TISM` | `GCR` | Primary mapping is technology and intelligent systems management because the question evaluates accountability for systems. Secondary mapping is governance because ownership supports organizational accountability. | `business-capability-taxonomy-v1` |
| `q.cloud.account-structure` | Maintain governed cloud account or environment structure. | `TISM` | `GCR` | Primary mapping is technology and intelligent systems management because the question evaluates cloud environment lifecycle structure. Secondary mapping is governance because the structure is governed. | `business-capability-taxonomy-v1` |
| `q.cloud.cost-controls` | Monitor and control cloud spend. | `TISM` | `GCR` | Primary mapping is technology and intelligent systems management because the question evaluates operational control of cloud systems. Secondary mapping is governance because cost control supports oversight and accountability. | `business-capability-taxonomy-v1` |
| `q.cloud.security-baseline` | Apply baseline cloud security controls. | `DPSC` | `TISM` | Primary mapping is data, privacy, and security controls because the question evaluates security baseline controls. Secondary mapping is technology and intelligent systems management because the controls apply to cloud technology. | `business-capability-taxonomy-v1` |
| `q.cloud.infrastructure-as-code` | Manage cloud configuration through repeatable deployment practices. | `TISM` | `RVCI` | Primary mapping is technology and intelligent systems management because the question evaluates controlled cloud configuration lifecycle. Secondary mapping is remediation and verification because repeatable deployment supports review and correction. | `business-capability-taxonomy-v1` |
| `q.cloud.resilience` | Define resilience, backup, or recovery expectations for cloud workloads. | `POC` | `TISM` | Primary mapping is process and operational control because the question evaluates operational reliability expectations. Secondary mapping is technology and intelligent systems management because the expectations apply to cloud workloads. | `business-capability-taxonomy-v1` |
| `q.cloud.monitoring` | Monitor cloud workload health and operational status. | `TISM` | `POC` | Primary mapping is technology and intelligent systems management because the question evaluates monitoring of cloud workloads. Secondary mapping is process and operational control because monitoring supports operational status management. | `business-capability-taxonomy-v1` |
| `q.operations.process-ownership` | Assign accountable owners for critical business processes. | `POC` | `GCR` | Primary mapping is process and operational control because the question evaluates business process ownership. Secondary mapping is governance because accountable ownership supports oversight. | `business-capability-taxonomy-v1` |
| `q.operations.kpi-defined` | Define operational KPIs for key processes. | `RVCI` | `POC` | Primary mapping is remediation, verification, and continuous improvement because the question evaluates measurement for improvement. Secondary mapping is process and operational control because KPIs apply to key processes. | `business-capability-taxonomy-v1` |
| `q.operations.escalation-path` | Define escalation paths for operational issues. | `POC` | `GCR` | Primary mapping is process and operational control because the question evaluates operational escalation execution. Secondary mapping is governance because escalation paths define accountability. | `business-capability-taxonomy-v1` |
| `q.operations.capacity-planning` | Plan capacity for people, systems, and process demand. | `POC` | None | Primary mapping is process and operational control because the question evaluates operational planning for reliable execution. | `business-capability-taxonomy-v1` |
| `q.operations.change-management` | Manage operational change with communication and ownership. | `POC` | `GCR` | Primary mapping is process and operational control because the question evaluates change execution. Secondary mapping is governance because change ownership and communication support oversight. | `business-capability-taxonomy-v1` |
| `q.operations.continuity` | Maintain continuity plans for critical operations. | `POC` | `RVCI` | Primary mapping is process and operational control because the question evaluates continuity of critical operations. Secondary mapping is remediation and verification because continuity plans require review and improvement. | `business-capability-taxonomy-v1` |
| `q.business.outcomes-defined` | Define target business outcomes for technology initiatives. | `GCR` | `RVCI` | Primary mapping is governance and compliance readiness because the question evaluates business oversight of initiative outcomes. Secondary mapping is remediation and continuous improvement because defined outcomes support later verification. | `business-capability-taxonomy-v1` |
| `q.business.customer-impact` | Connect initiatives to measurable customer impact. | `GCR` | `RVCI` | Primary mapping is governance and compliance readiness because the question evaluates business accountability for customer impact. Secondary mapping is remediation and continuous improvement because measurable impact supports verification. | `business-capability-taxonomy-v1` |
| `q.business.financial-case` | Define cost, benefit, or investment rationale. | `GCR` | None | Primary mapping is governance and compliance readiness because the question evaluates investment rationale and business oversight. | `business-capability-taxonomy-v1` |
| `q.business.executive-alignment` | Align executive stakeholders on priority and timing. | `GCR` | None | Primary mapping is governance and compliance readiness because the question evaluates executive alignment and oversight. | `business-capability-taxonomy-v1` |
| `q.business.risk-appetite` | Define acceptable risk for AI, automation, and cloud initiatives. | `GCR` | None | Primary mapping is governance and compliance readiness because the question evaluates organizational risk appetite and accountability. | `business-capability-taxonomy-v1` |
| `q.business.decision-cadence` | Maintain a regular decision cadence for transformation initiatives. | `GCR` | `POC` | Primary mapping is governance and compliance readiness because the question evaluates decision cadence and executive accountability. Secondary mapping is process and operational control because cadence supports repeatable execution. | `business-capability-taxonomy-v1` |

## Validation Results

Status: `APPROVED`

Validation performed against the approved Decision 2 requirements:

| Validation Requirement | Result |
| --- | --- |
| Every canonical assessment question has exactly one Primary Dimension. | Pass |
| No question has more than two Secondary Dimensions. | Pass |
| Every Secondary Dimension accompanies a Primary Dimension. | Pass |
| Every approved Business Capability Dimension contains at least one canonical assessment question. | Pass |
| Mapping rationale is present for every question. | Pass |
| Mapping is deterministic and reproducible. | Pass |
| No new dimensions are introduced. | Pass |
| No canonical question is orphaned. | Pass |

Primary Dimension coverage:

Counts are derived from the 48 row-level mappings in the Question Mapping Matrix.

| Dimension Code | Primary Question Count |
| --- | ---: |
| `POC` | 14 |
| `GCR` | 12 |
| `TISM` | 12 |
| `DPSC` | 4 |
| `RVCI` | 6 |

No canonical question is marked `METHODOLOGY_PENDING` for mapping.

## Remaining Out Of Scope

The following methodology remains `METHODOLOGY_PENDING`:

- Dimension Weighting Methodology.
- Aggregation Methodology.
- Readiness Methodology.
- Finding Methodology.
- Risk Methodology.
- Evidence Evaluation Methodology.
- Confidence Methodology.
- Recommendation Methodology.
- Executive Summary Methodology.
- Golden Fixtures.

## Repository Evidence

- `docs/business-decision-methodology/02-question-catalog.md`
- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
