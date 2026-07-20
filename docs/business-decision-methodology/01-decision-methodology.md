# Decision Methodology

## Purpose

This document defines Nguyen AI's Business Decision Methodology. It is the
business framework that will later become deterministic rules in the Business
Decision Engine.

The methodology converts assessment answers into executive recommendations
through traceable, reproducible stages. It must never depend on opaque AI
reasoning. Every output must be explainable, deterministic, evidence-based,
auditable, testable, and versioned.

Methodology version: `business-decision-methodology-v1`

## Decision Flow

```text
Assessment Question
  |
Business Capability
  |
Evidence Category
  |
Readiness Dimension
  |
Weight
  |
Risk Adjustment
  |
Confidence Adjustment
  |
Recommendation Priority
  |
Executive Recommendation
```

## Stage 1: Assessment Question

An Assessment Question captures a discrete piece of business evidence. Each
question must have a stable identifier, expected answer type, and documented
mapping to a business capability.

Why it exists:

- Establishes the source evidence for the decision chain.
- Prevents recommendations from being based on unsupported assumptions.
- Creates a stable input contract for future tests and analytics.

Business value:

- Ensures the assessment asks about capabilities that matter to business
  readiness.
- Reduces advisory inconsistency between clients and engagements.

Executive value:

- Gives executives confidence that recommendations are grounded in submitted
  evidence, not generic opinion.

Traceability requirement:

- Every downstream capability, score, risk, priority, and recommendation must
  be traceable to one or more question IDs.

## Stage 2: Business Capability

A Business Capability describes what the organization must be able to do. It is
the business interpretation of one or more assessment questions.

Examples:

- Establish AI governance ownership.
- Protect identities and sensitive data.
- Document repeatable business processes.
- Operate cloud workloads with cost and resilience controls.

Why it exists:

- Translates technical or operational answers into business language.
- Gives the framework a stable midpoint between questions and readiness scores.

Business value:

- Allows Nguyen AI to reason about operational capability rather than isolated
  survey answers.

Executive value:

- Makes the assessment understandable to leaders who sponsor work but do not
  manage every technical control.

Traceability requirement:

- Each capability must reference one or more question IDs and one primary
  evidence category.

## Stage 3: Evidence Category

An Evidence Category classifies what kind of evidence is being observed.
Examples include Leadership, Strategy, Technology, Security, Knowledge,
Operations, Governance, Automation, Data, and Cloud.

Why it exists:

- Creates a consistent evidence vocabulary across readiness dimensions.
- Helps identify evidence gaps and confidence limitations.

Business value:

- Reveals whether readiness conclusions are supported by broad evidence or a
  narrow evidence set.

Executive value:

- Shows leaders whether findings are based on leadership alignment, operating
  practices, controls, technology, data, or governance.

Traceability requirement:

- Each evidence category must have defined maturity expectations and typical
  evidence patterns.

## Stage 4: Readiness Dimension

A Readiness Dimension groups business capabilities into executive decision
areas. The v1 methodology uses:

- AI Readiness
- Security Readiness
- Knowledge Readiness
- Automation Readiness
- Engineering Readiness
- Cloud Readiness
- Operational Readiness
- Business Readiness

Why it exists:

- Organizes assessment evidence into decision domains.
- Keeps executive output focused on business readiness rather than raw answers.

Business value:

- Supports targeted prioritization and service mapping.

Executive value:

- Helps leaders identify where the organization is ready, constrained, or
  exposed.

Traceability requirement:

- Every readiness dimension must list its inputs, dependencies, and business
  interpretation.

## Stage 5: Weight

Weight expresses the relative decision importance of a capability or evidence
area. This methodology defines weight categories but does not define numeric
weights yet.

Allowed weight categories:

- `foundational-control`: required for safe execution.
- `strategic-alignment`: required for executive sponsorship and business fit.
- `operational-capability`: required for repeatable delivery.
- `value-enablement`: increases business benefit when foundations exist.
- `risk-control`: reduces exposure to business, security, compliance, or
  operational failure.
- `scale-readiness`: supports growth, resilience, or portfolio expansion.

Why it exists:

- Prevents all evidence from being treated as equally important.
- Creates a governed path to future numeric weights.

Business value:

- Aligns scoring with business impact and risk.

Executive value:

- Explains why one gap can matter more than several lower-impact strengths.

Traceability requirement:

- Every question must declare a weight category, and every future numeric weight
  must trace back to an approved category rationale.

## Stage 6: Risk Adjustment

Risk Adjustment identifies conditions that should limit readiness conclusions or
raise executive urgency.

Risk adjustment types:

- `readiness-cap`: a severe blocker limits the maximum readiness level.
- `priority-escalation`: a risk increases recommendation urgency.
- `service-routing`: a risk changes the recommended engagement or tier.
- `confidence-reduction`: a risk pattern reduces certainty in the conclusion.

Why it exists:

- Prevents high opportunity signals from hiding foundational risks.

Business value:

- Protects client outcomes and Nguyen AI delivery quality.

Executive value:

- Makes constraints visible before investment decisions are made.

Traceability requirement:

- Every risk adjustment must identify triggering question IDs, evidence
  categories, readiness dimensions, and rule IDs.

## Stage 7: Confidence Adjustment

Confidence Adjustment determines how strongly the platform can stand behind a
readiness conclusion or recommendation.

Confidence factors:

- Assessment completeness.
- Answer consistency.
- Evidence coverage.
- Response quality.
- Business certainty.

Why it exists:

- Separates "what the evidence suggests" from "how certain we are."

Business value:

- Prevents overconfident advisory output when evidence is incomplete or weak.

Executive value:

- Helps leaders decide whether to act, request discovery, or validate evidence.

Traceability requirement:

- Every confidence adjustment must cite the evidence limitation or strength that
  caused it.

## Stage 8: Recommendation Priority

Recommendation Priority determines the order and urgency of actions. The v1
priority levels are:

- Critical
- High
- Medium
- Low

Why it exists:

- Converts findings into an executive action sequence.

Business value:

- Focuses limited resources on the actions that reduce risk or unlock value
  first.

Executive value:

- Helps leaders decide what to sponsor now, next, or later.

Traceability requirement:

- Every priority must be justified by business impact, customer impact,
  executive urgency, risk, dependencies, and confidence.

## Stage 9: Executive Recommendation

An Executive Recommendation is the final business-facing decision output. It
must state what should happen, why it matters, what evidence supports it, and
which Nguyen AI service path is appropriate.

Why it exists:

- Turns assessment evidence into business decision support.

Business value:

- Connects readiness findings to revenue protection, risk reduction, operating
  efficiency, customer impact, and delivery sequencing.

Executive value:

- Provides leadership with clear, defensible next steps.

Traceability requirement:

- Every recommendation must reference source question IDs, capabilities,
  evidence categories, readiness dimensions, risk adjustments, confidence
  adjustments, and priority rationale.

## Deterministic Decision Standard

For the same assessment answers, assessment version, methodology version,
ruleset version, and service catalog version, the same recommendation must be
produced every time.

This standard applies to:

- Readiness classifications.
- Risk adjustments.
- Confidence adjustments.
- Priority ordering.
- Recommended engagement.
- Recommended service tier.
- Executive summary inputs.

Any future AI-generated narrative must be constrained to approved deterministic
facts and may not change the recommendation, priority, score, service mapping,
or evidence trace.

