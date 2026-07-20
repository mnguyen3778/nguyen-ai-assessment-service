# Domain Model

## Purpose

The domain model identifies the major business entities required for the
Evidence-Based Executive Intelligence Platform. It provides a shared language
for product, architecture, engineering, analytics, and advisory teams.

This model is conceptual. It should guide future implementation without
requiring immediate database or code changes.

## Core Entities

| Entity | Description | Business Role |
| --- | --- | --- |
| Organization | Company or business unit being assessed. | Assessment subject and future reporting boundary. |
| User | Authenticated person submitting or viewing assessment data. | Identity, authorization, and ownership context. |
| AssessmentSubmission | Raw submitted assessment payload. | Evidence source for validation and scoring. |
| AssessmentVersion | Versioned assessment questionnaire and accepted contract. | Controls compatibility and methodology. |
| EvidenceItem | Canonical evidence derived from submitted answers or future sources. | Traceable fact used in scoring and recommendations. |
| ReadinessDomain | Business readiness area such as AI, Security, or Cloud. | Organizes scoring and findings. |
| ScoringRule | Approved deterministic rule for score contribution. | Converts evidence into readiness meaning. |
| RiskSignal | Business or operational risk detected from evidence. | Flags constraints and blockers. |
| Recommendation | Governed action or advisory guidance. | Converts findings into executive next steps. |
| EngagementMapping | Mapping from evidence and recommendations to Nguyen AI engagement path. | Aligns advisory output to service delivery. |
| ServiceTier | Recommended commercial or delivery support level. | Supports sales and delivery alignment. |
| Snapshot | Generated Executive Business Readiness Snapshot. | Client-facing decision-support artifact. |
| AuditTrace | Machine-readable explanation of how the snapshot was produced. | Reproducibility and governance record. |

## Conceptual Relationships

```text
Organization
  has many AssessmentSubmissions

AssessmentSubmission
  uses AssessmentVersion
  produces EvidenceItems
  produces Snapshot

EvidenceItem
  supports ReadinessDomain scores
  triggers RiskSignals
  supports Recommendations

ScoringRule
  evaluates EvidenceItems
  contributes to DomainScore
  records AuditTrace

Recommendation
  maps to EngagementMapping
  maps to ServiceTier
  references EvidenceItems and RiskSignals

Snapshot
  contains DomainScores, Risks, Recommendations, Confidence, and AuditTrace
```

## Architectural Recommendations

| Recommendation | Why It Exists | Business Value | Executive Value | Future Scalability | Explainability | Evidence Traceability |
| --- | --- | --- | --- | --- | --- | --- |
| Introduce EvidenceItem as a first-class domain concept. | Answers are input format; evidence is business meaning. | Enables richer scoring and future evidence sources. | Executives see facts, not raw form mechanics. | Evidence can later come from documents, integrations, interviews, or systems. | Evidence items state what was observed and how it was derived. | Every item references source answer, source document, or integration record. |
| Separate AssessmentSubmission from Snapshot. | Submitted evidence and generated conclusions have different lifecycles. | Preserves raw evidence while allowing regenerated outputs. | Executives can understand when a snapshot was generated from a specific submission. | Supports re-scoring when rules evolve. | Snapshot audit explains which submission and rules were used. | Submission IDs connect raw input to generated output. |
| Model RiskSignal independently from Recommendation. | A risk may inform multiple actions or tiers. | Improves consistency and avoids duplicate logic. | Leaders can see risk before advice. | Risk signals can be reused in dashboards, alerts, and reporting. | Risk rules explain severity and rationale. | Risk signals reference triggering evidence and rule IDs. |
| Make EngagementMapping and ServiceTier explicit entities. | Advisory recommendations and commercial packaging should be governed. | Aligns product, sales, and delivery. | Executives receive recommendations that match practical support options. | New service offerings can be added without rewriting scoring. | Mapping rules explain why a service is recommended. | Service recommendations reference readiness, risk, confidence, and recommendation evidence. |
| Retain AuditTrace as a platform entity. | Reproducibility requires durable explanation data. | Supports enterprise governance and client trust. | Executives can defend or revisit decisions later. | Audit traces can feed analytics and compliance review. | Audit trace exposes rule execution and selected outcomes. | Each trace links evidence, rules, scores, recommendations, and versions. |

## Entity Lifecycle

1. User submits assessment.
2. AssessmentSubmission is validated.
3. EvidenceItems are derived.
4. ScoringRules calculate domain scores.
5. RiskSignals and confidence contributors are identified.
6. Recommendations, engagement, and service tier are mapped.
7. Snapshot is generated.
8. AuditTrace is stored or returned.
9. Snapshot may later be compared, regenerated, or superseded.

## Future Data Architecture Implications

When persistence is introduced, the domain model suggests separate stores or
logical collections for:

- Submissions and raw payloads.
- Canonical evidence.
- Rule definitions and versions.
- Generated snapshots.
- Audit traces.
- Analytics aggregates.

This separation supports governance, reprocessing, analytics, and client
reporting without forcing every capability into a single record shape.

