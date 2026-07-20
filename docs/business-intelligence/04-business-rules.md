# Business Rules

## Purpose

Business rules define the approved logic that transforms evidence into
readiness, risk, confidence, recommendations, engagement guidance, and service
tier assignments. They are the primary mechanism that prevents the platform from
becoming a black-box scoring engine.

## Rule Categories

| Category | Purpose | Example |
| --- | --- | --- |
| Validation Rules | Determine whether submitted evidence is acceptable. | `answers` must contain numeric values. |
| Domain Scoring Rules | Convert evidence into domain score contributions. | MFA coverage contributes to Security Readiness. |
| Risk Rules | Identify operational or business risk patterns. | No incident response owner increases Operational Risk. |
| Confidence Rules | Assess evidence completeness and reliability. | Missing security evidence lowers confidence. |
| Recommendation Rules | Select priority actions and advisory recommendations. | Low security plus AI ambition triggers governance action. |
| Service Mapping Rules | Assign recommended engagement and service tier. | Multiple high-risk domains suggest assessment workshop. |
| Narrative Rules | Select executive-friendly summary language. | Use approved text for elevated operational risk. |

## Rule Design Standard

Every business rule should include:

- `ruleId`
- `name`
- `description`
- `businessRationale`
- `inputs`
- `conditions`
- `outputs`
- `severity`
- `evidenceRefs`
- `assessmentVersion`
- `rulesetVersion`
- `owner`
- `approvalStatus`

## Architectural Recommendations

| Recommendation | Why It Exists | Business Value | Executive Value | Future Scalability | Explainability | Evidence Traceability |
| --- | --- | --- | --- | --- | --- | --- |
| Manage rules as business assets with owners and approvals. | Rules encode Nguyen AI advisory judgment. | Prevents uncontrolled scoring drift. | Executives can trust that outputs reflect approved methodology. | Enables governance boards and domain owners as the platform grows. | Rule metadata explains the business rationale. | Each output references the rule ID and version that produced it. |
| Keep validation rules separate from scoring rules. | Valid data and meaningful business scoring are different concerns. | Reduces accidental coupling between API acceptance and advisory methodology. | Executives receive consistent error handling and stable scoring behavior. | New scoring models can reuse existing validation where appropriate. | Validation errors explain request quality; scoring explains readiness. | Invalid fields and scoring evidence are tracked separately. |
| Define negative evidence and missing evidence explicitly. | Absence of a capability is different from absence of information. | Improves accuracy and reduces false conclusions. | Leaders can distinguish known gaps from unknowns. | Supports future evidence ingestion from documents, systems, and interviews. | Rules can explain whether an issue is confirmed or unknown. | Evidence records identify observed gaps, missing answers, and assumptions. |
| Use rule conflict resolution policies. | Multiple rules may produce competing recommendations or severity levels. | Prevents inconsistent executive outputs. | Executives receive a prioritized and coherent action plan. | More rules can be added without creating contradictory reports. | Conflict resolution rules explain why one outcome won. | The selected and suppressed rule outcomes can be logged. |
| Create a rule test catalog before production scoring launch. | Business rules need regression protection like software logic. | Reduces risk of broken scoring after methodology updates. | Executives receive stable outputs across releases. | Test catalogs scale across assessment versions and industries. | Expected outputs demonstrate intended rule behavior. | Test cases include input evidence and expected rule traces. |

## Rule Execution Principles

Rules should execute in a predictable sequence:

1. Validate payload.
2. Normalize answers.
3. Classify evidence signals.
4. Apply domain scoring rules.
5. Apply risk rules.
6. Apply confidence rules.
7. Apply recommendation rules.
8. Apply service mapping rules.
9. Apply narrative rules.
10. Produce audit trace.

## Rule Conflict Handling

Recommended conflict policies:

- Higher severity risk rules override lower severity readiness optimism.
- Required foundational actions precede optimization recommendations.
- Security and compliance blockers precede automation scale recommendations.
- Low confidence suppresses overly specific engagement promises.
- Service tier mapping should choose the minimum tier that addresses the top
  risks and priority actions.

## Rule Governance Lifecycle

1. Draft rule from business methodology.
2. Review with domain owner.
3. Validate against example assessments.
4. Approve for a specific assessment version.
5. Release with ruleset version.
6. Monitor output quality.
7. Revise or retire through change control.

## Enterprise Controls

The business rules layer should support:

- Human-readable rule definitions.
- Machine-executable rule representation.
- Approval workflow.
- Regression tests.
- Audit trace generation.
- Change history.
- Version compatibility rules.
- Environment promotion from development to production.

