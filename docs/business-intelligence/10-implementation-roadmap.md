# Implementation Roadmap

## Purpose

This roadmap defines a maintainable path from the current operational Assessment
Service to a five-year Evidence-Based Executive Intelligence Platform. It is
intentionally sequenced to preserve the current production path while adding
business intelligence capabilities through governed increments.

Current production path:

```text
Website
  |
Amazon Cognito
  |
API Gateway
  |
Lambda
  |
Assessment Service
```

Current output:

- `overallScore = 0`
- `readinessLevel = Pending Official Rubric`

## Roadmap Principles

- Preserve the current authenticated API flow.
- Add business intelligence capability through versioned contracts.
- Introduce deterministic scoring before narrative sophistication.
- Establish evidence traceability before executive reporting.
- Treat AI-assisted language as optional and constrained.
- Build governance before scaling rules and recommendations.

## Recommended Implementation Order

| Phase | Capability | Outcome |
| --- | --- | --- |
| 1 | Business methodology governance | Approved domains, levels, ruleset ownership, and change control. |
| 2 | Canonical evidence model | Answers become traceable EvidenceItems. |
| 3 | Versioned scoring rules | Deterministic domain and overall readiness scores. |
| 4 | Risk and confidence models | Operational risk, business risk, and confidence outputs. |
| 5 | Recommendation catalog | Governed priority actions and executive recommendations. |
| 6 | Service mapping | Recommended engagement and service tier. |
| 7 | Executive summary templates | Reproducible executive narrative. |
| 8 | Snapshot persistence | Historical snapshots, audit trace, and regeneration support. |
| 9 | Analytics and BI layer | Trends, benchmarks, cohort analytics, and executive dashboards. |
| 10 | Constrained AI assistance | Optional narrative drafting using deterministic facts and templates. |

## Architectural Recommendations

| Recommendation | Why It Exists | Business Value | Executive Value | Future Scalability | Explainability | Evidence Traceability |
| --- | --- | --- | --- | --- | --- | --- |
| Start with methodology governance before implementation. | Engineering cannot safely implement rules that business has not approved. | Prevents rework and inconsistent advisory outputs. | Executives receive conclusions aligned to Nguyen AI methodology. | Governance scales across domains, industries, and service offerings. | Approved rules include rationale and ownership. | Governance artifacts define the evidence required for every output. |
| Introduce snapshot output through explicit versioning. | The current API is operational and should not be broken. | Supports product evolution with controlled client migration. | Executives receive richer outputs only when they are stable. | Multiple versions can run during transition periods. | Versioned contracts explain output semantics. | Snapshot versions link to assessment and ruleset versions. |
| Build evidence trace before persistence-heavy analytics. | Analytics without traceable evidence creates weak intelligence. | Improves quality of future reporting and benchmarking. | Executives can drill from dashboard metrics to supporting facts. | Evidence trace supports future BI, audits, and client portals. | Evidence lineage explains every aggregate and recommendation. | Evidence IDs connect raw submissions to scores, snapshots, and reports. |
| Add persistence after output semantics are clear. | Persisting unstable data models creates technical debt. | Avoids costly migrations and unclear reporting definitions. | Leaders get reports based on stable business definitions. | Storage design can support snapshots, audit traces, and analytics separately. | Persisted records include version and rule metadata. | Stored snapshots retain source submission and evidence links. |
| Add constrained AI only after deterministic facts are mature. | AI-generated text must not become the source of truth. | Reduces brand, legal, and advisory risk. | Executives get polished language without losing trust in facts. | AI assistance can scale report generation while rules remain authoritative. | AI output is constrained to approved facts and templates. | Generated text references deterministic findings and evidence IDs. |

## Target AWS Capability Evolution

The current Lambda-centered architecture is appropriate for the first service.
Future platform increments may introduce:

- Amazon DynamoDB or Amazon Aurora for submissions, snapshots, and audit traces.
- Amazon S3 for generated reports and evidence documents.
- AWS Step Functions for multi-step assessment processing.
- Amazon EventBridge for snapshot-created and recommendation-created events.
- Amazon QuickSight or another BI layer for executive dashboards.
- AWS Glue or Athena for governed analytics over historical snapshots.
- AWS KMS for encryption governance.
- AWS CloudTrail and CloudWatch for platform audit and operations.
- Amazon Bedrock only for constrained narrative assistance, not scoring.

These services should be introduced only when the business capability requires
them. Technology selection should follow operating model clarity.

## Complete Architecture Review

### Missing Capabilities

| Capability | Why It Matters | Recommended Direction |
| --- | --- | --- |
| Approved scoring rubric | Placeholder output cannot produce business readiness decisions. | Establish domain weights, thresholds, risk caps, and test cases. |
| Canonical evidence model | Raw answers are not enough for traceable intelligence. | Define EvidenceItem and evidence reference standards. |
| Rule governance | Deterministic scoring requires controlled business logic. | Create owner, approval, versioning, and change history processes. |
| Recommendation catalog | Executive advice must be consistent and evidence-backed. | Build governed catalog with rationale and evidence mappings. |
| Confidence model | Recommendations need uncertainty context. | Define confidence contributors and suppression rules. |
| Snapshot persistence | Historical tracking and audit require durable records. | Store submissions, snapshots, and audit traces separately. |
| Executive reporting | The platform vision requires decision-ready output. | Create templates and dashboard-ready snapshot structures. |
| Observability and audit | Enterprise services require operational visibility. | Add trace IDs, structured logs, metrics, and audit records. |

### Future Extension Points

- Industry-specific assessment versions.
- Company-size or maturity-segment weighting.
- Client portal for historical snapshots.
- BI dashboards for trend and portfolio analysis.
- CRM integration for engagement follow-up.
- Document-based evidence ingestion.
- Advisor review workflow before client delivery.
- Benchmarking against anonymized peer cohorts.
- Multi-language executive summaries.
- Constrained AI drafting from deterministic facts.

### Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Scoring becomes opaque | Loss of trust and weak executive adoption. | Keep scoring deterministic, versioned, and evidence-linked. |
| Recommendations appear sales-driven | Client confidence may decline. | Use evidence-based service mapping with minimum sufficient tier logic. |
| Weak evidence produces strong advice | Poor client outcomes and reputational risk. | Use confidence thresholds and discovery routing. |
| Rules change without governance | Historical comparisons become unreliable. | Implement ruleset versioning and approval workflow. |
| Persistence starts before model stability | Data migrations and reporting confusion. | Finalize snapshot and evidence semantics before storage expansion. |
| AI narrative overreaches | Unsupported claims or inconsistent executive language. | Use templates first; constrain any AI to approved facts. |
| Overloaded Lambda responsibility | Service becomes difficult to maintain. | Separate rule evaluation, persistence, reporting, and events as scale requires. |

### Technical Debt To Avoid

- Hard-coded business rules without version metadata.
- Recommendations without evidence references.
- Scores without domain-level explanations.
- Persisted snapshots without source submission IDs.
- Narrative text that cannot be regenerated.
- Service-tier mapping mixed directly into scoring logic.
- Analytics built from raw answers instead of canonical evidence.
- AI-generated summaries without deterministic source facts.

### Recommended Near-Term Sequence

1. Approve readiness domains, level names, and business definitions.
2. Define the canonical question bank and evidence identifiers.
3. Design the first scoring ruleset and domain thresholds.
4. Define confidence rules and missing-evidence behavior.
5. Define recommendation catalog and service-tier mapping criteria.
6. Finalize the versioned Executive Business Readiness Snapshot contract.
7. Implement scoring and rule traceability in the service.
8. Add unit and regression tests for business rules.
9. Introduce persistence for submissions, snapshots, and audit traces.
10. Add executive report generation and BI analytics.

## Architecture Review Conclusion

The current Assessment Service is a sound starting point because it already has
authentication, API mediation, validation, and deterministic placeholder output.
The most important next architectural move is not adding infrastructure. It is
formalizing the business methodology that will make future outputs explainable,
evidence-based, deterministic, business focused, and executive friendly.

Long-term maintainability depends on keeping evidence, rules, recommendations,
service mapping, and narrative generation as separate governed concerns. This
separation gives Nguyen AI a platform that can mature over five years without
turning the assessment into a black-box AI scoring engine.

