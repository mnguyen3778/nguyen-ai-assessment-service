# Output Schema

## Purpose

The output schema defines the target Executive Business Readiness Snapshot
contract. It describes the business information the platform should eventually
return after a successful assessment submission.

This document is architectural. It does not require immediate implementation
and does not replace the current operational placeholder response until the
engineering team is ready to introduce a versioned contract.

## Schema Principles

- The output must be stable, versioned, and backward compatible where possible.
- Every recommendation and score must have evidence references.
- Executive-facing fields must be understandable without internal context.
- Audit fields must support reproducibility.
- Missing or low-confidence evidence must be visible.

## Target Snapshot Shape

```json
{
  "requestId": "uuid",
  "assessmentVersion": "nguyen-ai-readiness-v1",
  "assessmentTimestamp": "2026-07-20T18:30:00Z",
  "executiveSummary": {
    "headline": "Emerging readiness with foundational security constraints",
    "summary": "Executive-ready narrative generated from deterministic facts.",
    "confidenceStatement": "Confidence is moderate based on domain coverage.",
    "templateId": "exec-summary-emerging-risk-v1",
    "evidenceRefs": ["evidence.security.mfa", "evidence.ai.sponsorship"]
  },
  "overallReadiness": {
    "score": 64,
    "level": "Emerging Readiness",
    "rationale": "Weighted domain scores indicate progress with unresolved blockers.",
    "evidenceRefs": ["domain.ai", "domain.security", "risk.operational"]
  },
  "domains": [
    {
      "domainId": "ai-readiness",
      "label": "AI Readiness",
      "score": 72,
      "level": "Operationally Ready",
      "summary": "Leadership sponsorship exists, but governance is incomplete.",
      "strengths": ["Identified AI use cases"],
      "gaps": ["No approved AI governance owner"],
      "evidenceRefs": ["answer.ai.useCases", "answer.ai.governanceOwner"]
    }
  ],
  "risks": {
    "operationalRisk": {
      "level": "Elevated",
      "summary": "Manual controls and weak ownership may limit execution reliability.",
      "evidenceRefs": ["answer.automation.errorHandling"]
    },
    "businessRisk": {
      "level": "Moderate",
      "summary": "Business outcomes are defined but measurement ownership is unclear.",
      "evidenceRefs": ["answer.ai.successMetrics"]
    }
  },
  "priorityActions": [
    {
      "actionId": "action.establish-ai-governance",
      "title": "Establish AI governance ownership",
      "priority": 1,
      "businessRationale": "Governance is required before expanding AI use cases.",
      "expectedBusinessOutcome": "Reduced implementation and compliance risk.",
      "recommendedOwner": "Executive sponsor",
      "timeHorizon": "30-60 days",
      "evidenceRefs": ["answer.ai.governanceOwner"],
      "ruleRefs": ["rule.ai.governance.required"]
    }
  ],
  "executiveRecommendations": [
    {
      "recommendationId": "rec.sequence-foundation-before-scale",
      "summary": "Prioritize governance and security foundations before scaling AI automation.",
      "businessValue": "Improves the probability that AI investments produce measurable value.",
      "evidenceRefs": ["domain.security", "domain.ai"],
      "ruleRefs": ["rule.risk.security-cap"]
    }
  ],
  "recommendedEngagement": {
    "engagementId": "engagement.ai-readiness-workshop",
    "name": "Executive AI Readiness Workshop",
    "rationale": "The organization needs executive alignment and governance design.",
    "evidenceRefs": ["rec.sequence-foundation-before-scale"]
  },
  "recommendedServiceTier": {
    "tierId": "foundation",
    "label": "Foundation",
    "rationale": "Foundational controls and governance are the primary next steps.",
    "evidenceRefs": ["risk.operational", "domain.security"]
  },
  "confidence": {
    "score": 74,
    "level": "Moderate",
    "rationale": "Most domains are covered, but supporting evidence is incomplete.",
    "contributors": [
      {
        "type": "missing-evidence",
        "summary": "Cloud operations evidence was not provided.",
        "evidenceRefs": ["missing.cloud.operations"]
      }
    ]
  },
  "audit": {
    "rulesetVersion": "business-readiness-rules-v1",
    "scoringModelVersion": "scoring-v1",
    "narrativeRulesVersion": "narrative-v1",
    "generatedAt": "2026-07-20T18:30:01Z"
  }
}
```

## Architectural Recommendations

| Recommendation | Why It Exists | Business Value | Executive Value | Future Scalability | Explainability | Evidence Traceability |
| --- | --- | --- | --- | --- | --- | --- |
| Introduce the Executive Business Readiness Snapshot as a versioned output contract. | The current placeholder must evolve without breaking clients. | Enables product growth while protecting integration stability. | Executives receive richer insight when the model is ready. | New fields can be added through versioning and compatibility policies. | Version metadata explains which contract produced the response. | Every snapshot includes assessment, ruleset, and timestamp metadata. |
| Require evidence references on all material conclusions. | Scores and recommendations must be defensible. | Builds client trust and supports advisory review. | Evidence references can power future dashboards and reports. | Users can inspect why an output exists. | Fields link to answer IDs, evidence IDs, rule IDs, and domain IDs. |
| Separate executive summary, domain findings, risks, and recommendations. | Different audiences need different levels of detail. | Improves usability across sales, advisory, and delivery teams. | Executives can start with summary and drill into support. | Each section can evolve independently. | Section boundaries clarify whether content is fact, score, risk, or advice. | Each section retains its own evidence references. |
| Include audit metadata in the response or persisted snapshot. | Reproducibility requires more than the visible business output. | Supports quality assurance and compliance review. | Executives can compare snapshots with confidence. | Audit metadata supports historical analytics and rule migration. | Audit fields identify models and rules used. | Audit records connect output to exact rule versions and generation time. |
| Model confidence as a first-class object. | Confidence affects how strongly recommendations should be interpreted. | Reduces risk of overcommitting based on thin evidence. | Leaders understand whether additional discovery is needed. | Confidence can incorporate future evidence channels. | Confidence rationale explains uncertainty. | Contributors identify missing or weak evidence. |

## Compatibility Guidance

The current placeholder response should remain valid until a new assessment
version or explicit response version is introduced. Recommended migration path:

1. Add non-breaking metadata fields where safe.
2. Introduce snapshot fields behind a new response version.
3. Support clients during transition with explicit version negotiation.
4. Retire older response contracts only after client migration.

