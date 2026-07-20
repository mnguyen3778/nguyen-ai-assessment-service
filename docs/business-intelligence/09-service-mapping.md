# Service Mapping

## Purpose

Service mapping connects assessment outcomes to Nguyen AI engagement offerings
and service tiers. It ensures that recommendations are not only analytically
correct but commercially and operationally actionable.

Service mapping must remain evidence-based. A service tier should never be
recommended because of vague interest, sales preference, or opaque AI output.

## Mapping Inputs

Service mapping should consider:

- Overall readiness score and level.
- Domain scores and levels.
- Operational risk.
- Business risk.
- Priority actions.
- Executive recommendations.
- Confidence score.
- Organization context when approved for use.
- Assessment version and ruleset version.

## Engagement Categories

| Engagement | Best Fit | Business Outcome |
| --- | --- | --- |
| Executive Readiness Briefing | Leaders need interpretation of current readiness. | Shared understanding and decision alignment. |
| Evidence Discovery Workshop | Confidence is low or evidence is incomplete. | Better evidence and clearer action path. |
| AI Governance Foundation | AI ambition exists but governance is weak. | Safer AI adoption and accountability. |
| Security and Cloud Readiness Review | Foundational control or cloud risks constrain execution. | Reduced operational and compliance exposure. |
| Automation Opportunity Assessment | Manual process pain exists with moderate operational control. | Prioritized automation backlog. |
| Enterprise AI Transformation Roadmap | Multi-domain readiness is sufficient for program planning. | Sequenced transformation roadmap. |

## Service Tier Semantics

| Tier | Meaning | Typical Evidence Pattern |
| --- | --- | --- |
| Foundation | The organization needs baseline clarity, governance, or controls. | Low confidence, low readiness, or severe foundational gaps. |
| Growth | The organization has enough foundation to prioritize targeted initiatives. | Moderate readiness with clear business opportunities. |
| Enterprise | The organization needs coordinated multi-domain transformation. | Multiple domains ready enough for program-level planning. |
| Strategic | The organization has high complexity, high stakes, or executive transformation needs. | Broad scope, high risk, high opportunity, or major change portfolio. |

Tier names should be confirmed by business leadership before production launch.

## Architectural Recommendations

| Recommendation | Why It Exists | Business Value | Executive Value | Future Scalability | Explainability | Evidence Traceability |
| --- | --- | --- | --- | --- | --- | --- |
| Make service mapping rule-based and versioned. | Commercial recommendations affect trust and revenue. | Creates consistent alignment between assessment findings and offerings. | Executives understand why a specific engagement is recommended. | New offerings can be introduced through mapping versions. | Mapping rules state entry criteria and rationale. | Service outputs reference scores, risks, confidence, and recommendation IDs. |
| Use minimum sufficient tier selection. | Over-scoping damages trust; under-scoping fails to address need. | Aligns service tier to actual evidence. | Executives see practical, proportionate guidance. | Tier logic can expand as offerings mature. | Rules explain why higher or lower tiers were not selected. | Selected and non-selected tier criteria can be audited. |
| Route low-confidence assessments to discovery-oriented engagements. | Thin evidence should not produce aggressive transformation recommendations. | Protects delivery quality and client outcomes. | Leaders understand the need for fact-finding before major spend. | Discovery paths can feed richer future snapshots. | Low-confidence mapping explains missing evidence. | Missing evidence and confidence contributors support the route. |
| Let severe risk override opportunity-led service mapping. | High opportunity does not justify unsafe execution. | Reduces client and Nguyen AI delivery risk. | Executives receive sequencing guidance before investment. | Risk override rules can support new domains and industries. | Override explanations show the blocker. | Risk signals reference triggering evidence and affected recommendations. |
| Keep service mapping separate from scoring. | Readiness and service packaging are different business decisions. | Enables independent governance by methodology and commercial owners. | Executives receive objective readiness plus clear next-step options. | Offerings can change without changing historical scores. | Score explains state; service mapping explains engagement fit. | Service mapping references score outputs instead of recalculating them. |

## Mapping Decision Pattern

Recommended sequence:

1. Check confidence.
2. Identify severe blockers.
3. Identify dominant domain gaps.
4. Identify value opportunities.
5. Select priority actions.
6. Select engagement category.
7. Select minimum sufficient tier.
8. Generate rationale and evidence references.

## Service Mapping Governance

Service mapping should be jointly governed by:

- Executive advisory leadership.
- Delivery leadership.
- Product leadership.
- Sales or client success leadership.
- Architecture owner.

This joint governance prevents the mapping from becoming either purely technical
or purely commercial. The platform recommendation should represent the best
next step for the client based on evidence.

