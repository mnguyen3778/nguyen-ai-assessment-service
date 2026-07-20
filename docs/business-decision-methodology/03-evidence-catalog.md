# Evidence Catalog

## Purpose

This document defines the evidence categories used by Nguyen AI's Business
Decision Methodology. Evidence categories classify what type of business proof
supports a readiness conclusion or recommendation.

Methodology version: `business-decision-methodology-v1`

## Evidence Category Standard

Each evidence category must support:

- Explainable business meaning.
- Deterministic mapping from question IDs.
- Evidence coverage analysis.
- Confidence adjustment.
- Recommendation traceability.

## Evidence Categories

| Evidence Category | Purpose | Business Meaning | Typical Evidence | Expected Maturity |
| --- | --- | --- | --- | --- |
| Leadership | Shows whether accountable leaders sponsor and own decisions. | Leadership evidence indicates whether readiness has executive ownership, funding attention, and decision authority. | Executive sponsor, ownership model, decision cadence, escalation owner. | Accountable leaders are named, engaged, and able to resolve tradeoffs. |
| Strategy | Shows whether work aligns to business outcomes. | Strategy evidence indicates whether initiatives are connected to measurable goals, customer impact, and investment rationale. | Business goals, use-case prioritization, KPIs, financial case, customer outcome definitions. | Goals and success metrics are documented and used to prioritize work. |
| Technology | Shows whether systems and tooling can support implementation. | Technology evidence indicates implementation feasibility, integration readiness, engineering discipline, and platform control. | Source control, tests, integrations, infrastructure practices, monitoring tooling. | Technology practices are repeatable, controlled, and aligned to business needs. |
| Security | Shows whether the organization can protect systems, identities, and data. | Security evidence indicates exposure to confidentiality, integrity, availability, compliance, and trust risks. | MFA, access review, security baseline, incident response, vendor controls. | Foundational controls are implemented, reviewed, and tested. |
| Knowledge | Shows whether critical information is captured and reusable. | Knowledge evidence indicates whether the business can scale expertise beyond individuals. | Current documentation, knowledge owners, searchable repositories, customer context, refresh cadence. | Critical knowledge is owned, current, searchable, and used in operations. |
| Operations | Shows whether work can be executed reliably. | Operations evidence indicates process ownership, continuity, escalation, capacity, and performance management. | Process owners, KPIs, escalation paths, continuity plans, capacity planning. | Key processes are measured, owned, and resilient to disruption. |
| Governance | Shows whether decisions, controls, and changes are managed intentionally. | Governance evidence indicates whether the organization can control risk and make repeatable decisions. | AI policy, change control, risk appetite, review cadence, control ownership. | Policies, owners, approvals, and review cycles are defined and followed. |
| Automation | Shows whether processes can be automated safely and effectively. | Automation evidence indicates whether manual work is understood, repeatable, measurable, and controlled. | Process documentation, exception handling, manual volume, automation change control. | Automation candidates are documented, measurable, and have clear exception ownership. |
| Data | Shows whether data can support decisions, AI, security, and reporting. | Data evidence indicates whether information is classified, accessible, governed, and suitable for business use. | Data classification, success metrics, customer context, reporting definitions. | Data is defined, protected, trusted, and connected to business outcomes. |
| Cloud | Shows whether cloud environments can support secure and economical scale. | Cloud evidence indicates readiness for resilient, governed, and cost-aware cloud operations. | Account structure, cost controls, security baseline, IaC, cloud monitoring. | Cloud workloads are governed, monitored, secure, and cost managed. |

## Evidence Coverage Rules

Evidence coverage measures whether a readiness conclusion is supported by enough
categories to be reliable.

Coverage principles:

- High readiness requires evidence beyond a single category.
- Leadership and Strategy evidence are required for executive recommendations.
- Security and Governance evidence are required before recommending advanced AI
  or automation scale.
- Operations evidence is required before recommending implementation or managed
  services.
- Knowledge evidence is required before recommending automation of complex
  business processes.
- Cloud evidence is required before recommending cloud-scale implementation.

## Evidence Quality Rules

Evidence quality is determined by:

- Specificity: the answer describes a concrete practice or control.
- Ownership: the answer identifies accountable ownership.
- Currency: the evidence appears current enough to support action.
- Repeatability: the practice can be repeated without relying on one person.
- Measurability: the practice can be evaluated through outcomes or controls.
- Consistency: the answer does not conflict with related evidence.

## Evidence Traceability Standard

Future implementations should use stable evidence references:

```text
evidence.<category>.<capability>
```

Examples:

- `evidence.leadership.executive-sponsor`
- `evidence.security.identity-control`
- `evidence.automation.exception-handling`
- `evidence.cloud.cost-control`

Question references should remain separate:

```text
question.<question-id>
```

Rule references should remain separate:

```text
rule.<dimension>.<capability>.<purpose>
```

This separation prevents raw answers, interpreted evidence, and deterministic
rules from being collapsed into the same concept.

