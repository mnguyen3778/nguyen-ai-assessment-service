# Readiness Methodology

## Purpose

This document defines each readiness dimension in Nguyen AI's Business Decision
Methodology. A readiness dimension converts business capabilities and evidence
categories into executive meaning.

Methodology version: `business-decision-methodology-v1`

## Readiness Dimension Standard

Every readiness dimension must define:

- Purpose.
- Inputs.
- Business interpretation.
- Executive interpretation.
- Dependencies.

The methodology defines deterministic calculation inputs, but it does not yet
define numeric formulas or final thresholds.

## AI Readiness

Purpose:

- Determine whether the organization can adopt AI in a controlled, valuable,
  measurable, and governed way.

Inputs:

- AI strategy alignment.
- Executive sponsorship.
- AI governance ownership.
- Prioritized AI use cases.
- Success metrics.
- Approved AI risk policy.

Business interpretation:

- AI Readiness indicates whether AI initiatives can progress beyond isolated
  experimentation into governed business value creation.

Executive interpretation:

- High AI Readiness means leadership has a defensible path to sponsor AI
  adoption.
- Low AI Readiness means the organization should clarify ownership, business
  outcomes, governance, or acceptable risk before scaling AI use.

Dependencies:

- Business Readiness for outcomes and sponsorship.
- Security Readiness for safe data and identity controls.
- Knowledge Readiness for reusable organizational context.
- Data evidence for trustworthy AI use.

## Security Readiness

Purpose:

- Determine whether the organization can protect identities, data, systems,
  vendors, and operations.

Inputs:

- MFA or strong authentication.
- Access review.
- Data classification.
- Incident response ownership.
- Vendor controls.
- Tested recovery or continuity procedures.

Business interpretation:

- Security Readiness indicates whether growth, AI, automation, and cloud
  initiatives can proceed without creating unacceptable exposure.

Executive interpretation:

- High Security Readiness supports investment confidence.
- Low Security Readiness may cap overall readiness and escalate priority
  recommendations.

Dependencies:

- Governance for control ownership.
- Operations for incident response and recovery.
- Cloud Readiness for cloud security baseline.
- Business Readiness for risk appetite.

## Knowledge Readiness

Purpose:

- Determine whether the organization can capture, maintain, find, and reuse
  critical knowledge.

Inputs:

- Current documentation.
- Defined knowledge owners.
- Searchable knowledge assets.
- Reduced subject matter expert dependency.
- Knowledge refresh cadence.
- Captured customer context and decision history.

Business interpretation:

- Knowledge Readiness indicates whether the organization can scale expertise,
  automate safely, onboard consistently, and preserve institutional memory.

Executive interpretation:

- High Knowledge Readiness supports automation, AI assistance, and operating
  consistency.
- Low Knowledge Readiness indicates that key work may depend on individuals and
  undocumented judgment.

Dependencies:

- Operations for process ownership.
- Automation Readiness for process documentation.
- AI Readiness for knowledge-assisted AI use cases.
- Business Readiness for customer and decision context.

## Automation Readiness

Purpose:

- Determine whether business processes can be automated safely, measurably, and
  sustainably.

Inputs:

- Documented process.
- Manual work volume.
- Exception handling.
- Integration readiness.
- Outcome measurement.
- Automation change control.

Business interpretation:

- Automation Readiness indicates whether efficiency gains are realistic without
  increasing operational risk.

Executive interpretation:

- High Automation Readiness supports targeted process improvement or workflow
  implementation.
- Low Automation Readiness means the organization should clarify process
  ownership, exceptions, and measurement before automation.

Dependencies:

- Knowledge Readiness for documented process logic.
- Engineering Readiness for controlled implementation.
- Operations for ownership and measurement.
- Security Readiness for safe integration and access.

## Engineering Readiness

Purpose:

- Determine whether the organization can build, change, release, and operate
  digital systems reliably.

Inputs:

- Source control.
- Repeatable testing.
- Controlled release process.
- Observability.
- Business-impact backlog prioritization.
- System ownership.

Business interpretation:

- Engineering Readiness indicates whether technical delivery can support business
  commitments without excessive operational fragility.

Executive interpretation:

- High Engineering Readiness supports implementation engagements and platform
  scaling.
- Low Engineering Readiness suggests that delivery foundations need improvement
  before complex transformation work.

Dependencies:

- Operations for support ownership.
- Cloud Readiness for environment governance.
- Business Readiness for backlog prioritization.
- Security Readiness for secure engineering practices.

## Cloud Readiness

Purpose:

- Determine whether cloud environments can support secure, resilient, governed,
  and cost-aware workloads.

Inputs:

- Cloud account or environment structure.
- Cost controls.
- Cloud security baseline.
- Infrastructure as code or repeatable configuration.
- Resilience expectations.
- Cloud monitoring.

Business interpretation:

- Cloud Readiness indicates whether cloud adoption can scale without uncontrolled
  cost, security exposure, or reliability gaps.

Executive interpretation:

- High Cloud Readiness supports cloud-enabled implementation and managed service
  opportunities.
- Low Cloud Readiness means the organization should establish cloud governance
  before expanding workloads.

Dependencies:

- Security Readiness for baseline controls.
- Engineering Readiness for repeatable deployment.
- Operations for monitoring and continuity.
- Business Readiness for investment and cost governance.

## Operational Readiness

Purpose:

- Determine whether the organization can operate critical processes reliably and
  respond to change or disruption.

Inputs:

- Process ownership.
- Operational KPIs.
- Escalation paths.
- Capacity planning.
- Change management.
- Continuity plans.

Business interpretation:

- Operational Readiness indicates whether the business can execute consistently
  and absorb transformation without destabilizing core operations.

Executive interpretation:

- High Operational Readiness supports implementation and scale.
- Low Operational Readiness indicates that transformation may fail because the
  operating model cannot absorb change.

Dependencies:

- Leadership for ownership and escalation.
- Governance for change control.
- Engineering and Cloud Readiness for technology operations.
- Knowledge Readiness for process documentation.

## Business Readiness

Purpose:

- Determine whether leadership, strategy, investment rationale, risk appetite,
  and decision cadence support technology-enabled transformation.

Inputs:

- Defined business outcomes.
- Customer impact.
- Financial case.
- Executive alignment.
- Risk appetite.
- Decision cadence.

Business interpretation:

- Business Readiness indicates whether the organization has the strategic and
  executive foundation needed to turn technology capability into measurable
  business value.

Executive interpretation:

- High Business Readiness means leadership can make timely, aligned decisions.
- Low Business Readiness means the organization should clarify outcomes,
  sponsorship, or investment rationale before implementation.

Dependencies:

- Leadership and Strategy evidence.
- AI Readiness for AI-specific transformation.
- Operational Readiness for delivery feasibility.
- Security Readiness for acceptable risk.

## Cross-Dimension Dependency Rules

- Security Readiness can cap AI, Automation, Cloud, and Overall Readiness when
  foundational control evidence is weak.
- Knowledge Readiness can constrain Automation Readiness when processes are not
  documented or reusable.
- Engineering Readiness can constrain Cloud and Automation implementation
  recommendations when delivery controls are weak.
- Operational Readiness can constrain Implementation Engagement and Managed AI
  Services recommendations when ownership, escalation, or continuity is weak.
- Business Readiness can constrain all strategic recommendations when outcomes,
  sponsorship, risk appetite, or decision cadence are weak.

