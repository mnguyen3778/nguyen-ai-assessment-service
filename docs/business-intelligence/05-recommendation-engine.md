# Recommendation Engine

## Purpose

The Recommendation Engine converts scored evidence, risk signals, and confidence
into executive-friendly actions and engagement guidance. It must recommend what
leadership should do next, why that action matters, and what evidence supports
the recommendation.

The engine should not invent recommendations from free-form AI output. It should
select, rank, and explain approved recommendations from governed business rules.

## Recommendation Types

| Type | Purpose | Example |
| --- | --- | --- |
| Priority Action | Immediate leadership action to reduce risk or unlock value. | Establish AI governance owner. |
| Executive Recommendation | Strategic advisory guidance for decision makers. | Sequence AI adoption after identity-control remediation. |
| Recommended Engagement | Suggested Nguyen AI engagement path. | Executive AI Readiness Workshop. |
| Recommended Service Tier | Commercial or delivery tier aligned to need and risk. | Foundation, Growth, Enterprise, or Strategic. |

## Recommendation Object

Each recommendation should include:

- `recommendationId`
- `title`
- `summary`
- `businessRationale`
- `priority`
- `domainRefs`
- `riskRefs`
- `evidenceRefs`
- `expectedBusinessOutcome`
- `recommendedOwner`
- `timeHorizon`
- `serviceMappingRefs`
- `confidenceImpact`

## Architectural Recommendations

| Recommendation | Why It Exists | Business Value | Executive Value | Future Scalability | Explainability | Evidence Traceability |
| --- | --- | --- | --- | --- | --- | --- |
| Use a governed recommendation catalog. | Recommendations should be consistent across clients and advisors. | Improves delivery quality and commercial alignment. | Executives receive professional, repeatable guidance. | Catalog entries can be expanded by domain, industry, and company size. | Each recommendation has a documented rationale. | Catalog entries map to rule IDs, domain scores, and evidence signals. |
| Rank recommendations by risk reduction, value enablement, and dependency order. | Executives need sequencing, not a long unordered list. | Focuses client effort on the next best actions. | Leaders can sponsor a practical roadmap. | Ranking formulas can evolve without changing recommendation content. | Ranking criteria are visible and defensible. | Priority ranking references risk, score, and dependency evidence. |
| Separate recommended engagement from recommended service tier. | Delivery path and commercial tier answer different questions. | Enables clearer sales, advisory, and delivery alignment. | Executives understand both the work needed and the level of support required. | Engagement types and tiers can evolve independently. | Engagement rules explain scope; tier rules explain intensity. | Both outputs reference the same underlying readiness and risk evidence. |
| Suppress recommendations when confidence is too low. | Specific advice without enough evidence can mislead executives. | Protects Nguyen AI credibility. | Leaders are directed toward discovery when facts are insufficient. | Future evidence sources can raise confidence and unlock recommendations. | Suppression logic explains what evidence is missing. | Missing evidence is recorded with the suppressed recommendation reason. |
| Include evidence references in every executive recommendation. | Decision support must be defensible. | Enables transparent client conversations. | Executives can validate conclusions with their teams. | Evidence references can support future dashboards and reports. | Recommendations show the facts and rules behind the advice. | Recommendation objects carry evidence IDs and rule IDs. |

## Ranking Model

Recommended ranking dimensions:

- Severity of risk addressed.
- Business value unlocked.
- Dependency on foundational controls.
- Effort and time horizon.
- Confidence in evidence.
- Alignment to executive goals.

The ranking should favor foundational risk reduction when severe blockers exist.
When foundational risk is controlled, ranking can prioritize business value and
automation leverage.

## Engagement Mapping

Recommended engagement should be selected from business-defined engagement
patterns, such as:

- Executive Readiness Briefing.
- Evidence Discovery Workshop.
- AI Governance Foundation.
- Automation Opportunity Assessment.
- Security and Cloud Readiness Review.
- Enterprise AI Transformation Roadmap.

Each engagement pattern should define:

- Entry criteria.
- Outcomes.
- Required evidence.
- Typical stakeholders.
- Duration range.
- Success measures.

## Service Tier Mapping

Service tier mapping should reflect need, risk, complexity, and confidence.

Example tier semantics:

- `Foundation`: Targeted readiness clarification and foundational controls.
- `Growth`: Prioritized roadmap and implementation enablement.
- `Enterprise`: Multi-domain transformation planning and governance.
- `Strategic`: Executive program advisory for high complexity or high risk.

Tier names should be finalized by business leadership before production use.

## Recommendation Quality Controls

Before a recommendation is released, it should pass:

- Business rationale review.
- Evidence mapping review.
- Executive language review.
- Service alignment review.
- Regression test coverage.
- Version compatibility review.

