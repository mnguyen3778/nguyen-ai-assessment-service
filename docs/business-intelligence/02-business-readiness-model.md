# Business Readiness Model

## Purpose

The Business Readiness Model defines how assessment evidence becomes an
Executive Business Readiness Snapshot. It organizes evidence into domains that
reflect executive concerns: growth readiness, risk exposure, operational
capacity, and implementation feasibility.

The model is not a technical maturity scorecard. It is a business readiness
framework that uses technical and operational evidence to support leadership
decisions.

## Readiness Domains

| Domain | Business Meaning | Evidence Examples | Executive Interpretation |
| --- | --- | --- | --- |
| AI Readiness | Ability to adopt AI in a controlled, valuable, and measurable way. | AI use cases, data access, governance, leadership sponsorship, success metrics. | Indicates whether AI initiatives can move beyond experimentation. |
| Security Readiness | Ability to protect data, systems, identities, and operations. | Access controls, incident response, data classification, vendor controls. | Indicates exposure to operational, legal, and reputational risk. |
| Automation Readiness | Ability to reduce manual work through reliable workflow automation. | Process documentation, integration patterns, error handling, ownership. | Indicates where efficiency gains are realistic and sustainable. |
| Knowledge Readiness | Ability to capture, govern, retrieve, and reuse organizational knowledge. | Documentation quality, knowledge ownership, searchability, content freshness. | Indicates whether the organization can scale expertise beyond individuals. |
| Engineering Readiness | Ability to build, maintain, and change digital systems reliably. | SDLC practices, testing, observability, release control, backlog management. | Indicates delivery reliability and change capacity. |
| Cloud Readiness | Ability to operate workloads securely and economically in cloud environments. | Account structure, cost controls, IaC, monitoring, backup, resiliency. | Indicates whether cloud adoption is governed and operationally mature. |

## Risk Dimensions

Operational Risk and Business Risk should be derived from domain evidence, not
collected as unsupported opinions.

| Risk Dimension | Meaning | Primary Drivers |
| --- | --- | --- |
| Operational Risk | Probability that current execution practices will create disruption, waste, or reliability failure. | Security gaps, manual process fragility, weak engineering controls, cloud operations gaps. |
| Business Risk | Probability that technology initiatives will fail to produce business value or create leadership exposure. | Poor strategic alignment, weak sponsorship, unclear metrics, missing knowledge governance. |

## Readiness Snapshot Structure

The target snapshot should combine:

- Domain scores.
- Domain findings.
- Risk indicators.
- Confidence score.
- Priority actions.
- Executive recommendations.
- Recommended engagement.
- Recommended service tier.
- Evidence references.
- Assessment version and timestamp.

## Architectural Recommendations

| Recommendation | Why It Exists | Business Value | Executive Value | Future Scalability | Explainability | Evidence Traceability |
| --- | --- | --- | --- | --- | --- | --- |
| Use domain-level readiness scores before calculating an overall score. | Overall scores are only meaningful when the contributing domains are visible. | Prevents a single number from hiding material risks. | Executives can see where to act rather than only seeing a composite result. | New domains can be added with explicit weighting rules. | Domain scores explain the overall score contribution. | Each domain score references question IDs, answer values, and scoring rules. |
| Include risk dimensions separate from readiness dimensions. | A company can be ready in one area while carrying severe risk in another. | Supports risk-aware service recommendations. | Leadership can distinguish growth opportunity from exposure. | Additional risk categories can be added without rewriting readiness scoring. | Risk is explained through specific evidence patterns. | Risk outputs reference the evidence that triggered risk rules. |
| Treat missing or incomplete evidence as a confidence issue, not as positive readiness. | Lack of evidence does not prove readiness. | Reduces false positives in early assessments. | Executives can identify where further discovery is needed. | Confidence can evolve with richer evidence sources. | The platform can explain which missing inputs reduced confidence. | Missing required or recommended evidence is recorded by domain. |
| Use readiness levels in addition to numeric scores. | Executives need business meaning, not just numbers. | Improves communication and advisory consistency. | Leaders can quickly understand the stage of maturity. | Level labels can be localized or tailored by industry while preserving numeric rules. | Level thresholds are explicit and versioned. | Level assignment references the score and threshold rule. |
| Preserve assessment timestamp and version in every snapshot. | Business readiness is time-bound and version-bound. | Supports repeat assessments and historical trend analysis. | Executives can track improvement over time. | Enables longitudinal analytics and benchmark comparisons. | Timestamp and version explain the context of the output. | Snapshot metadata ties results to the exact submitted assessment and rule set. |

## Domain Output Pattern

Each readiness domain should eventually produce:

- `domainId`
- `label`
- `score`
- `level`
- `summary`
- `strengths`
- `gaps`
- `riskSignals`
- `evidenceRefs`
- `confidenceContribution`

This pattern keeps every domain consistent while allowing domain-specific
questions, rules, and recommendation mappings.

## Overall Readiness Score

The Overall Readiness Score should be a weighted aggregation of domain scores,
subject to risk caps where severe risk should limit the maximum possible score.
For example, severe security readiness gaps may cap overall readiness even if
AI readiness or automation readiness appears high.

This cap-based approach is recommended because it aligns to executive reality:
a growth initiative is not ready if foundational risks make execution unsafe.

## Confidence Score

Confidence should reflect the platform's certainty in the snapshot based on:

- Required evidence completion.
- Domain coverage.
- Internal consistency of answers.
- Age of supporting evidence when available.
- Presence or absence of corroborating evidence.

Confidence should not be used to inflate readiness. It should tell executives
how much discovery should precede action.

