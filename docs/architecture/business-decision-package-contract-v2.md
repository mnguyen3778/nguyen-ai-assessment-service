# Governed Business Decision Package Contract v2

## Scope and version binding

`business-decision-package-v2` is the required producer contract for the
governed `nguyen-ai-executive-assessment-v2` input, bound to
`business-decision-methodology-v1`. The v1 package and snapshot remain the
legacy/foundation output for executive assessment v1. Consumers must select
handling by package `versionMetadata.contractVersion`; they must not interpret
a v1 package as completed governed truth.

The v2 package preserves the eight v1 root fields, their order, and their
foundation meanings. It appends required `governedConclusions` after
`versionMetadata`. The v1 confidence, priority, and summary foundation fields
remain foundation outputs. Consumers use `governedConclusions` for final
governed decisions.

## Governed conclusions

The governed section serializes the existing `GovernedAssessmentResult` in
this order:

1. `severityAssignedFindings`: canonical finding ID order. Each item carries
   finding identity, title, primary and related dimensions, trigger source,
   type, business consequence basis, evidence source references, sequence,
   computed severity classification, severity decision identifier, and table
   version.
2. `assessmentRisk`: computed classification, decision identifier, and table
   version.
3. `confidence`: computed evidence-driven classification, decision identifier,
   and table version. The insufficient-confidence result preserves the existing
   assertability effect without publishing evidence documents.
4. `recommendations`: computed items in finding order, each with finding ID,
   classification, decision identifier, and table version. The approved
   no-findings item has `findingId: null`.
5. `executiveSummary`: finding count and the seven approved deterministic
   template section texts in governed section order. Structured findings,
   risk, confidence, and recommendations remain authoritative over text.

All five members are required. `severityAssignedFindings: []` is valid and
means a complete assessment with no findings. In that case the risk is
`minimal-informational` and the recommendation decision identifier is
`recommendation-v1-no-findings-monitor`. Missing or malformed fields fail
validation. Producer validation checks vocabulary, canonical order, version
binding, and internal result alignment; it does not execute methodology rules.

## Producer path and limitations

`evaluate_assessment_v2` computes the conclusions once. Executive orchestration
passes its result to package assembly. The snapshot contains that package and
copies its serialization without deriving conclusions. The snapshot envelope
retains `executive-runtime-response-v1`; the package v2 identity governs its
nested content. Package and snapshot validations both check this binding.

For v2, obsolete package limitations for final confidence and recommendation
assignment/generation are removed. Service decisions, executive reporting,
executive narratives, raw evidence ingestion, persistence, and snapshot
consumer API exposure remain limitations. Recommendation priority assignment
is still a foundation output and is not asserted as a governed final priority.

This candidate changes no public API, persistence, deployment, methodology,
or downstream system. Consumers migrating from v1 must recognize package v2,
read `governedConclusions`, and reject incomplete governed output.
