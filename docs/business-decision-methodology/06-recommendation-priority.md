# Recommendation Priority

## Purpose

This document defines deterministic recommendation priority methodology for
Nguyen AI's Business Decision Framework.

Recommendation priority determines executive urgency. It must be based on
business impact, customer impact, risk, dependencies, and confidence. It must not
be based on opaque AI reasoning or sales preference.

Methodology version: `business-decision-methodology-v1`

## Priority Levels

| Priority | Meaning | Executive Action |
| --- | --- | --- |
| Critical | Immediate executive attention is required because a blocker, risk, or foundational gap materially constrains safe progress. | Sponsor action now; resolve before scaling related initiatives. |
| High | Action is important for near-term readiness, risk reduction, or value enablement. | Assign owner and plan near-term remediation or engagement. |
| Medium | Action improves readiness or efficiency but is not the primary blocker. | Sequence after critical and high items. |
| Low | Action is beneficial, informational, or optimization-oriented. | Track for later improvement or roadmap refinement. |

## Priority Drivers

| Driver | Business Meaning | Priority Influence |
| --- | --- | --- |
| Business Impact | Effect on revenue, cost, strategic goals, operational capacity, or transformation success. | Higher impact increases priority. |
| Customer Impact | Effect on customer trust, service quality, response time, reliability, or experience. | Customer-facing risk or value increases priority. |
| Executive Urgency | Need for leadership decision, sponsorship, risk acceptance, or funding. | Unresolved executive decisions increase priority. |
| Risk Severity | Exposure to security, compliance, operational, financial, or reputational harm. | Severe risk increases priority. |
| Dependency Role | Whether the action unlocks or blocks later work. | Foundational dependencies increase priority. |
| Confidence Level | Strength of evidence supporting the recommendation. | Low confidence may route to discovery instead of implementation. |

## Critical Priority

Critical recommendations apply when:

- A foundational-control gap blocks safe AI, automation, cloud, or implementation
  work.
- A risk-control gap creates material operational, security, customer, or
  business exposure.
- Multiple readiness dimensions depend on the same unresolved blocker.
- Low confidence affects a high-stakes decision and requires discovery before
  action.

Business impact:

- Prevents avoidable harm, failed implementation, or misdirected investment.

Customer impact:

- Protects trust, reliability, data handling, and service continuity.

Executive urgency:

- Requires executive sponsorship, risk decision, or immediate prioritization.

## High Priority

High recommendations apply when:

- The action materially improves readiness or reduces risk.
- The evidence is strong enough for near-term planning.
- The action is a dependency for a major use case or service engagement.
- The issue affects one or more important readiness dimensions but does not
  create an immediate blocker.

Business impact:

- Improves probability of successful transformation and measurable value.

Customer impact:

- May improve customer outcomes or reduce customer-facing risk.

Executive urgency:

- Requires owner assignment and near-term planning.

## Medium Priority

Medium recommendations apply when:

- The action improves readiness but does not block the primary path.
- The recommendation supports optimization or secondary capability building.
- The evidence is directional but not urgent.

Business impact:

- Supports sustained improvement and roadmap maturity.

Customer impact:

- May indirectly improve quality, consistency, or responsiveness.

Executive urgency:

- Can be sequenced after critical and high recommendations.

## Low Priority

Low recommendations apply when:

- The action is beneficial but not required for current readiness decisions.
- The action is informational, refinement-oriented, or future-facing.
- Evidence is insufficient for a stronger recommendation and discovery is not
  urgent.

Business impact:

- Supports long-term maturity and continuous improvement.

Customer impact:

- Usually indirect or future-oriented.

Executive urgency:

- Track as backlog or future roadmap input.

## Deterministic Ordering Principles

When multiple recommendations have the same priority:

1. Foundational-control recommendations come before value-enablement
   recommendations.
2. Risk-control recommendations come before scale-readiness recommendations.
3. Recommendations affecting multiple dimensions come before single-dimension
   recommendations.
4. Recommendations with higher confidence come before recommendations with
   weak evidence unless the weak evidence creates a discovery need.
5. Customer-impacting recommendations come before internal optimization
   recommendations.

## Traceability Requirements

Every priority assignment must reference:

- Recommendation ID.
- Source question IDs.
- Evidence categories.
- Readiness dimensions.
- Risk adjustment.
- Confidence adjustment.
- Business impact rationale.
- Customer impact rationale.
- Executive urgency rationale.

## Testability Requirements

Future tests must validate:

- Critical recommendations precede high, medium, and low recommendations.
- Risk-control and foundational-control findings can escalate priority.
- Low confidence can suppress implementation recommendations.
- Priority ties are resolved deterministically.
- Priority outputs include evidence and rule references.

