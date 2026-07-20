# Service Decision Framework

## Purpose

This document defines how Nguyen AI recommendations map into Nguyen AI services.
The service decision framework is deterministic and evidence-based. It must not
recommend a service because of opaque AI reasoning, sales preference, or vague
client interest.

Methodology version: `business-decision-methodology-v1`

## Service Categories

| Service | Purpose | Typical Fit |
| --- | --- | --- |
| Assessment Only | Provide a readiness snapshot and identify evidence gaps without committing to advisory or implementation work. | Low confidence, incomplete evidence, or early-stage exploration. |
| AI Strategy Workshop | Align executives on AI goals, governance, risk appetite, and prioritized use cases. | AI ambition exists but business alignment or governance is incomplete. |
| Automation Assessment | Identify safe, valuable automation opportunities and process prerequisites. | Manual work volume exists but process maturity or integration readiness needs analysis. |
| Executive AI Roadmap | Produce an executive roadmap for sequenced AI, automation, security, cloud, and operating model improvements. | Multiple dimensions show moderate or high readiness with clear business sponsorship. |
| Implementation Engagement | Deliver scoped implementation work after readiness, ownership, risk, and operating requirements are sufficient. | Evidence supports specific build, integration, automation, or cloud work. |
| Managed AI Services | Operate or support AI-enabled capabilities on an ongoing basis. | Strong operational, security, engineering, cloud, and governance evidence exists. |

## Deterministic Mapping Inputs

Service decisions must consider:

- Recommendation priority.
- Readiness dimensions.
- Risk adjustments.
- Confidence level.
- Business capability gaps.
- Evidence coverage.
- Executive urgency.
- Delivery dependencies.

## Mapping Principles

Assessment Only:

- Use when confidence is low or evidence is insufficient for stronger action.
- Use when the organization needs fact-finding before roadmap or implementation.
- Use when conflicting answers prevent reliable service selection.

AI Strategy Workshop:

- Use when AI Readiness is constrained by strategy, sponsorship, governance,
  risk appetite, or success metrics.
- Use when business leaders need alignment before implementation.
- Use when AI opportunity exists but foundational decision rights are unclear.

Automation Assessment:

- Use when automation opportunity exists but process documentation, exception
  handling, measurement, or integration readiness is incomplete.
- Use when Knowledge or Operational Readiness constrains automation.
- Use when manual work volume suggests value but implementation safety is not
  established.

Executive AI Roadmap:

- Use when the organization needs a sequenced plan across multiple dimensions.
- Use when readiness is sufficient for planning but dependencies or risk caps
  require executive sequencing.
- Use when business outcomes, sponsorship, and confidence are strong enough for
  roadmap work.

Implementation Engagement:

- Use when a specific scoped implementation can proceed with acceptable
  readiness, risk, ownership, and confidence.
- Use when Engineering, Security, Operational, and relevant domain readiness are
  sufficient for delivery.
- Do not use when foundational-control gaps remain unresolved.

Managed AI Services:

- Use when ongoing operation is appropriate and supported by strong evidence.
- Require sufficient Security, Operational, Engineering, Cloud, Governance, and
  Business Readiness.
- Do not use when confidence is low, ownership is unclear, or operating controls
  are immature.

## Service Routing Overrides

Service routing must support deterministic overrides:

- Severe security gaps route away from Implementation Engagement and Managed AI
  Services until resolved.
- Low confidence routes toward Assessment Only or workshop services.
- Weak business alignment routes toward AI Strategy Workshop or Executive AI
  Roadmap rather than implementation.
- Weak process documentation routes toward Automation Assessment rather than
  automation implementation.
- Weak operational ownership routes away from Managed AI Services.
- Weak engineering or cloud controls route toward readiness improvement before
  implementation.

## Service Decision Trace

Every service recommendation must include:

- Service ID.
- Service name.
- Rationale.
- Triggering recommendations.
- Source readiness dimensions.
- Risk adjustments.
- Confidence adjustments.
- Evidence references.
- Suppressed service options, when relevant.

## Service IDs

Canonical v1 service IDs:

- `service.assessment-only`
- `service.ai-strategy-workshop`
- `service.automation-assessment`
- `service.executive-ai-roadmap`
- `service.implementation-engagement`
- `service.managed-ai-services`

## Testability Requirements

Future tests must validate:

- Low confidence routes to Assessment Only or workshop services.
- Severe security gaps suppress implementation and managed services.
- Automation gaps route to Automation Assessment.
- Strong cross-domain readiness can route to Executive AI Roadmap or
  Implementation Engagement.
- Managed AI Services requires strong operating controls and confidence.
- Every service output has evidence references and deterministic rationale.

