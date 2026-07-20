# Executive Summary Rules

## Purpose

Executive summaries translate scored evidence into concise business meaning.
They should help leaders understand readiness, risk, confidence, and next
actions without requiring them to inspect the full scoring model.

Executive summaries must be reproducible. The same inputs, assessment version,
ruleset version, and narrative rules should produce the same summary.

## Summary Structure

The Executive Summary should include:

1. Overall readiness statement.
2. Primary strength or opportunity.
3. Primary risk or blocker.
4. Confidence statement.
5. Recommended executive action.
6. Recommended engagement path.

## Narrative Principles

- Use business language, not internal system language.
- Explain the conclusion before naming technology.
- Avoid exaggerated claims.
- Avoid unsupported certainty.
- State when evidence is incomplete.
- Reference priority actions and readiness domains.
- Keep the summary suitable for an executive or board audience.

## Architectural Recommendations

| Recommendation | Why It Exists | Business Value | Executive Value | Future Scalability | Explainability | Evidence Traceability |
| --- | --- | --- | --- | --- | --- | --- |
| Generate summaries from approved narrative templates and facts. | Free-form generation can create inconsistent or unsupported statements. | Protects brand quality and advisory integrity. | Executives receive concise, stable, defensible summaries. | Templates can expand by version, industry, and readiness level. | Template selection is governed by explicit rules. | Summary sections reference facts, findings, and evidence IDs. |
| Include confidence language in every summary. | Executives need to know whether recommendations are strongly supported. | Reduces risk of acting on incomplete evidence. | Leaders understand whether to proceed or gather more facts. | Confidence language can adapt as evidence depth improves. | Confidence rules explain the wording. | Missing or weak evidence references support the confidence statement. |
| Make severe risk visible in the first paragraph. | Major blockers should not be buried in a detailed report. | Improves risk communication and prioritization. | Executives can quickly understand decision constraints. | Risk narrative rules can scale with new risk categories. | Risk statements map to severity rules. | Risk statements cite triggering evidence and affected domains. |
| Keep recommendations action-oriented and owner-aware. | Executive summaries should drive decisions and sponsorship. | Converts assessment output into follow-through. | Leaders see who should act and what outcome to pursue. | Owner categories can support workflow routing later. | Recommendation text is selected from approved catalog entries. | Action statements reference recommendation IDs and evidence. |
| Preserve narrative audit metadata. | Summary language may be reviewed by clients, legal, or leadership. | Supports quality control and client trust. | Executives can validate report consistency. | Audit metadata supports report regeneration and comparison. | The platform can explain why each sentence appeared. | Template ID, rule ID, and evidence references are stored. |

## Summary Inputs

The summary generator should consume:

- Overall readiness score and level.
- Domain scores and levels.
- Operational risk and business risk.
- Priority actions.
- Executive recommendations.
- Recommended engagement.
- Recommended service tier.
- Confidence score.
- Evidence trace.
- Assessment version and timestamp.

## Summary Rules

Recommended rules:

- If confidence is low, the summary must lead with evidence limitations before
  prescribing specific transformation actions.
- If Security Readiness is low and AI Readiness is high, the summary should
  acknowledge opportunity while recommending governance and control remediation.
- If Automation Readiness is high but Knowledge Readiness is low, the summary
  should warn against automating undocumented processes.
- If Engineering or Cloud Readiness is low, the summary should avoid promising
  rapid platform scale.
- If multiple domains are low, the summary should recommend foundational
  discovery rather than a narrow implementation project.

## Executive Language Standards

Preferred language:

- "The organization shows emerging readiness..."
- "The strongest evidence supports..."
- "The primary constraint is..."
- "Leadership should prioritize..."
- "Confidence is limited by..."

Avoid:

- "AI determined..."
- "The model believes..."
- "Guaranteed improvement..."
- "Best-in-class..."
- "Fully ready..." unless thresholds and evidence support that conclusion.

## Reproducibility Standard

Executive summaries should be reproducible through:

- Stable input facts.
- Versioned templates.
- Deterministic template selection rules.
- Approved phrase libraries.
- Stored template IDs.
- Stored evidence references.

If future generative AI is used, it should operate only within approved facts,
phrases, and structure, with deterministic facts remaining the source of truth.

