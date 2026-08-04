# Golden Fixture Payloads v1

## 1. Purpose

Status: `APPROVED`

This document defines deterministic Golden Fixture payload definitions for
`business-decision-methodology-v1`.

Golden Fixture Payloads v1 populates the approved Golden Fixture catalog with
immutable reference cases for validating Assessment Service methodology
behavior. The payloads define canonical input profiles and expected
deterministic outputs for scoring, aggregation, readiness, findings, severity,
risk, confidence, recommendations, and Executive Summary references.

This document does not create runtime test code, implementation algorithms,
automation scripts, production logic, package contracts, or snapshot contracts.

## 2. Fixture Catalog

Status: `APPROVED`

Golden Fixture Payloads v1 populates the approved Golden Fixtures v1 catalog.

| Fixture ID | Purpose |
| --- | --- |
| `fixture-v1-complete-minimal-risk` | Validate complete processing for minimal or informational assessment-level risk. |
| `fixture-v1-complete-not-ready-readiness` | Validate Not Ready readiness assignment. |
| `fixture-v1-complete-developing-readiness` | Validate Developing readiness assignment. |
| `fixture-v1-complete-ready-readiness` | Validate Ready readiness assignment. |
| `fixture-v1-complete-advanced-readiness` | Validate Advanced readiness assignment. |
| `fixture-v1-critical-finding-risk` | Validate Critical Severity, Critical Risk, Immediate Action, and downstream propagation. |
| `fixture-v1-high-concentration-risk` | Validate High Severity concentration, Elevated Risk, Priority Action, High Confidence, and downstream propagation. |
| `fixture-v1-medium-risk` | Validate Medium Severity, Moderate Risk, Planned Improvement, and downstream propagation. |
| `fixture-v1-low-risk` | Validate Low Severity, Low Risk, Planned Improvement, and downstream propagation. |
| `fixture-v1-evidence-basic-confidence` | Validate Basic-only evidence and Low Confidence. |
| `fixture-v1-evidence-strong-confidence` | Validate Strong-only evidence and Very High Confidence. |
| `fixture-v1-evidence-assertability-limitation` | Validate present required evidence with assertability limitation and Insufficient Confidence. |
| `fixture-v1-no-findings-recommendation` | Validate no-Findings Recommendation rule and Executive Summary empty Finding statement. |
| `fixture-v1-invalid-input-fail-closed` | Validate fail-closed behavior for invalid or incomplete fixture input. |
| `fixture-v1-version-mismatch-fail-closed` | Validate fail-closed behavior for unsupported or mismatched methodology artifact versions. |

## 3. Fixture Structure

Status: `APPROVED`

Each fixture payload must include:

- Fixture ID.
- Purpose.
- Input assessment profile.
- Expected question score profile.
- Expected dimension results.
- Expected weighted assessment result.
- Expected readiness.
- Expected findings.
- Expected severity.
- Expected risk.
- Expected confidence.
- Expected recommendations.
- Expected Executive Summary references.
- Methodology version.
- Required artifact versions.

Fixture payloads are validation artifacts only. They do not define runtime
implementation behavior and do not alter approved methodology.

## 4. Required Inputs

Status: `APPROVED`

All complete-valid fixtures use the 48 canonical assessment questions approved
in Question Scoring Tables v1.

Canonical question IDs:

```text
q.ai.strategy.business-goals
q.ai.leadership.sponsor
q.ai.governance.owner
q.ai.use-cases.prioritized
q.ai.success-metrics.defined
q.ai.risk-policy.approved
q.security.identity.mfa
q.security.access.review
q.security.data.classification
q.security.incident-response.owner
q.security.vendor.controls
q.security.backup.recovery-tested
q.knowledge.docs.current
q.knowledge.owner.defined
q.knowledge.searchable
q.knowledge.sme-dependency
q.knowledge.refresh-cadence
q.knowledge.customer-context
q.automation.process-documented
q.automation.manual-volume
q.automation.exception-handling
q.automation.integration-readiness
q.automation.measurement
q.automation.change-control
q.engineering.source-control
q.engineering.testing
q.engineering.release-process
q.engineering.observability
q.engineering.backlog-prioritization
q.engineering.ownership
q.cloud.account-structure
q.cloud.cost-controls
q.cloud.security-baseline
q.cloud.infrastructure-as-code
q.cloud.resilience
q.cloud.monitoring
q.operations.process-ownership
q.operations.kpi-defined
q.operations.escalation-path
q.operations.capacity-planning
q.operations.change-management
q.operations.continuity
q.business.outcomes-defined
q.business.customer-impact
q.business.financial-case
q.business.executive-alignment
q.business.risk-appetite
q.business.decision-cadence
```

Approved primary-dimension coverage used by these payloads:

| Dimension Code | Business Capability Dimension | Question Count |
| --- | --- | ---: |
| `POC` | Process & Operational Control | 14 |
| `GCR` | Governance, Compliance & Regulatory Readiness | 12 |
| `TISM` | Technology & Intelligent Systems Management | 12 |
| `DPSC` | Data, Privacy & Security Controls | 4 |
| `RVCI` | Remediation, Verification & Continuous Improvement | 6 |
| Total |  | 48 |

Question score profiles:

| Score Profile ID | Input Response Definition | Expected Question Scores |
| --- | --- | --- |
| `question-score-profile-all-0` | Every `scale-0-4` question response is `0`; `q.automation.manual-volume` response is `0`. | Every canonical question score is `0`. |
| `question-score-profile-all-25` | Every `scale-0-4` question response is `1`; `q.automation.manual-volume` response is `25`. | Every canonical question score is `25`. |
| `question-score-profile-all-50` | Every `scale-0-4` question response is `2`; `q.automation.manual-volume` response is `50`. | Every canonical question score is `50`. |
| `question-score-profile-all-75` | Every `scale-0-4` question response is `3`; `q.automation.manual-volume` response is `75`. | Every canonical question score is `75`. |
| `question-score-profile-all-100` | Every `scale-0-4` question response is `4`; `q.automation.manual-volume` response is `100`. | Every canonical question score is `100`. |
| `question-score-profile-invalid-missing-response` | At least one required canonical question response is missing. | No question score output is valid. |

Evidence profiles:

| Evidence Profile ID | Evidence Input Definition | Expected Confidence Driver |
| --- | --- | --- |
| `evidence-profile-adequate` | Required evidence is present and all available evidence is `Adequate`. | Moderate Confidence. |
| `evidence-profile-basic` | Required evidence is present and all available evidence is `Basic`. | Low Confidence. |
| `evidence-profile-strong` | Required evidence is present and all available evidence is `Strong`. | Very High Confidence. |
| `evidence-profile-mixed-strong` | Required evidence is present, no assertability limitation is present, available evidence includes `Strong`, and at least one remaining evidence item is `Adequate` or `Basic`. | High Confidence. |
| `evidence-profile-assertability-limitation` | Required evidence is present and Evidence Evaluation identifies a valid assertability limitation under authenticity or traceability criteria. | Insufficient Confidence. |
| `evidence-profile-invalid-missing-required` | Required evidence is missing. | Fail closed. |

## 5. Expected Outputs

Status: `APPROVED`

The official dimension weights are:

| Dimension Code | Weight |
| --- | ---: |
| `POC` | 18 |
| `GCR` | 24 |
| `TISM` | 22 |
| `DPSC` | 20 |
| `RVCI` | 16 |

Because every complete-valid score profile assigns the same score to every
canonical question in that fixture, the expected result for each dimension is
the same as the expected question score for that profile. The weighted
assessment result is therefore the same value because the approved dimension
weights sum to 100.

Expected score-profile outputs:

| Score Profile ID | Expected Dimension Results (`POC`, `GCR`, `TISM`, `DPSC`, `RVCI`) | Expected Weighted Assessment Result | Expected Readiness |
| --- | --- | ---: | --- |
| `question-score-profile-all-0` | `0`, `0`, `0`, `0`, `0` | 0 | Not Ready |
| `question-score-profile-all-25` | `25`, `25`, `25`, `25`, `25` | 25 | Developing |
| `question-score-profile-all-50` | `50`, `50`, `50`, `50`, `50` | 50 | Ready |
| `question-score-profile-all-75` | `75`, `75`, `75`, `75`, `75` | 75 | Advanced |
| `question-score-profile-all-100` | `100`, `100`, `100`, `100`, `100` | 100 | Advanced |
| `question-score-profile-invalid-missing-response` | No valid dimension result. | No valid weighted assessment result. | Fail closed; no readiness assignment. |

Expected Finding payload definitions:

| Finding Payload ID | Expected Findings | Expected Severity |
| --- | --- | --- |
| `finding-payload-none` | Empty Finding collection. | No Severity Assignment. |
| `finding-payload-strength-informational` | `finding-v1-strength-operating-practice`: Finding Type `Strength`, Primary Dimension `POC`, source `fixture-input`, business consequence basis `strength`. | `Informational` via `severity-v1-strength-informational`. |
| `finding-payload-critical-deficiency` | `finding-v1-critical-governance-breach`: Finding Type `Deficiency`, Primary Dimension `GCR`, source `fixture-input`, business consequence basis `material current breach`. | `Critical` via `severity-v1-deficiency-critical`. |
| `finding-payload-two-high-deficiencies` | `finding-v1-high-governance-gap`: Finding Type `Deficiency`, Primary Dimension `GCR`, source `fixture-input`, business consequence basis `significant gap`; `finding-v1-high-technology-gap`: Finding Type `Deficiency`, Primary Dimension `TISM`, source `fixture-input`, business consequence basis `significant gap`. | Each Finding receives `High` via `severity-v1-deficiency-high`. |
| `finding-payload-medium-deficiency` | `finding-v1-medium-process-deficiency`: Finding Type `Deficiency`, Primary Dimension `POC`, source `fixture-input`, business consequence basis `clear deficiency`. | `Medium` via `severity-v1-deficiency-medium`. |
| `finding-payload-low-deficiency` | `finding-v1-low-control-weakness`: Finding Type `Deficiency`, Primary Dimension `RVCI`, source `fixture-input`, business consequence basis `limited weakness`. | `Low` via `severity-v1-deficiency-low`. |

Expected Executive Summary references:

```text
overall-assessment-overview
business-capability-highlights
significant-findings
risk-overview
confidence-statement
recommended-actions
closing-assessment-statement
```

Complete-valid fixture payloads:

| Fixture ID | Input Assessment Profile | Expected Question Scores | Expected Dimension Results | Expected Weighted Assessment Result | Expected Readiness | Expected Findings | Expected Severity | Expected Risk | Expected Confidence | Expected Recommendations | Expected Executive Summary References | Methodology Version |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| `fixture-v1-complete-minimal-risk` | Complete 48-question assessment; `question-score-profile-all-100`; `evidence-profile-strong`; `finding-payload-strength-informational`. | `question-score-profile-all-100` | `POC=100`, `GCR=100`, `TISM=100`, `DPSC=100`, `RVCI=100` | 100 | Advanced | `finding-v1-strength-operating-practice` | Informational | Minimal / Informational | Very High Confidence | `recommendation-v1-strength-best-practice` -> Best Practice | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-complete-not-ready-readiness` | Complete 48-question assessment; `question-score-profile-all-0`; `evidence-profile-adequate`; `finding-payload-none`. | `question-score-profile-all-0` | `POC=0`, `GCR=0`, `TISM=0`, `DPSC=0`, `RVCI=0` | 0 | Not Ready | Empty Finding collection. | No Severity Assignment. | Minimal / Informational | Moderate Confidence | `recommendation-v1-no-findings-monitor` -> Monitor | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-complete-developing-readiness` | Complete 48-question assessment; `question-score-profile-all-25`; `evidence-profile-adequate`; `finding-payload-none`. | `question-score-profile-all-25` | `POC=25`, `GCR=25`, `TISM=25`, `DPSC=25`, `RVCI=25` | 25 | Developing | Empty Finding collection. | No Severity Assignment. | Minimal / Informational | Moderate Confidence | `recommendation-v1-no-findings-monitor` -> Monitor | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-complete-ready-readiness` | Complete 48-question assessment; `question-score-profile-all-50`; `evidence-profile-adequate`; `finding-payload-none`. | `question-score-profile-all-50` | `POC=50`, `GCR=50`, `TISM=50`, `DPSC=50`, `RVCI=50` | 50 | Ready | Empty Finding collection. | No Severity Assignment. | Minimal / Informational | Moderate Confidence | `recommendation-v1-no-findings-monitor` -> Monitor | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-complete-advanced-readiness` | Complete 48-question assessment; `question-score-profile-all-75`; `evidence-profile-adequate`; `finding-payload-none`. | `question-score-profile-all-75` | `POC=75`, `GCR=75`, `TISM=75`, `DPSC=75`, `RVCI=75` | 75 | Advanced | Empty Finding collection. | No Severity Assignment. | Minimal / Informational | Moderate Confidence | `recommendation-v1-no-findings-monitor` -> Monitor | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-critical-finding-risk` | Complete 48-question assessment; `question-score-profile-all-75`; `evidence-profile-adequate`; `finding-payload-critical-deficiency`. | `question-score-profile-all-75` | `POC=75`, `GCR=75`, `TISM=75`, `DPSC=75`, `RVCI=75` | 75 | Advanced | `finding-v1-critical-governance-breach` | Critical | Critical Risk | Moderate Confidence | `recommendation-v1-deficiency-critical-immediate` -> Immediate Action | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-high-concentration-risk` | Complete 48-question assessment; `question-score-profile-all-75`; `evidence-profile-mixed-strong`; `finding-payload-two-high-deficiencies`. | `question-score-profile-all-75` | `POC=75`, `GCR=75`, `TISM=75`, `DPSC=75`, `RVCI=75` | 75 | Advanced | `finding-v1-high-governance-gap`, `finding-v1-high-technology-gap` | High, High | Elevated Risk | High Confidence | Two `recommendation-v1-deficiency-high-priority` outputs -> Priority Action, stable ordered by source Finding ID. | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-medium-risk` | Complete 48-question assessment; `question-score-profile-all-50`; `evidence-profile-adequate`; `finding-payload-medium-deficiency`. | `question-score-profile-all-50` | `POC=50`, `GCR=50`, `TISM=50`, `DPSC=50`, `RVCI=50` | 50 | Ready | `finding-v1-medium-process-deficiency` | Medium | Moderate Risk | Moderate Confidence | `recommendation-v1-deficiency-medium-planned` -> Planned Improvement | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-low-risk` | Complete 48-question assessment; `question-score-profile-all-50`; `evidence-profile-adequate`; `finding-payload-low-deficiency`. | `question-score-profile-all-50` | `POC=50`, `GCR=50`, `TISM=50`, `DPSC=50`, `RVCI=50` | 50 | Ready | `finding-v1-low-control-weakness` | Low | Low Risk | Moderate Confidence | `recommendation-v1-deficiency-low-planned` -> Planned Improvement | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-evidence-basic-confidence` | Complete 48-question assessment; `question-score-profile-all-50`; `evidence-profile-basic`; `finding-payload-none`. | `question-score-profile-all-50` | `POC=50`, `GCR=50`, `TISM=50`, `DPSC=50`, `RVCI=50` | 50 | Ready | Empty Finding collection. | No Severity Assignment. | Minimal / Informational | Low Confidence | `recommendation-v1-no-findings-monitor` -> Monitor | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-evidence-strong-confidence` | Complete 48-question assessment; `question-score-profile-all-75`; `evidence-profile-strong`; `finding-payload-none`. | `question-score-profile-all-75` | `POC=75`, `GCR=75`, `TISM=75`, `DPSC=75`, `RVCI=75` | 75 | Advanced | Empty Finding collection. | No Severity Assignment. | Minimal / Informational | Very High Confidence | `recommendation-v1-no-findings-monitor` -> Monitor | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-evidence-assertability-limitation` | Complete 48-question assessment; `question-score-profile-all-50`; `evidence-profile-assertability-limitation`; `finding-payload-none`. | `question-score-profile-all-50` | `POC=50`, `GCR=50`, `TISM=50`, `DPSC=50`, `RVCI=50` | 50 | Ready | Empty Finding collection. | No Severity Assignment. | Minimal / Informational | Insufficient Confidence | `recommendation-v1-no-findings-monitor` -> Monitor | All seven Executive Summary section IDs. | `business-decision-methodology-v1` |
| `fixture-v1-no-findings-recommendation` | Complete 48-question assessment; `question-score-profile-all-100`; `evidence-profile-adequate`; `finding-payload-none`. | `question-score-profile-all-100` | `POC=100`, `GCR=100`, `TISM=100`, `DPSC=100`, `RVCI=100` | 100 | Advanced | Empty Finding collection. | No Severity Assignment. | Minimal / Informational | Moderate Confidence | `recommendation-v1-no-findings-monitor` -> Monitor | All seven Executive Summary section IDs, including Significant Findings empty statement. | `business-decision-methodology-v1` |

Fail-closed fixture payloads:

| Fixture ID | Input Assessment Profile | Expected Question Scores | Expected Dimension Results | Expected Weighted Assessment Result | Expected Readiness | Expected Findings | Expected Severity | Expected Risk | Expected Confidence | Expected Recommendations | Expected Executive Summary References | Methodology Version |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `fixture-v1-invalid-input-fail-closed` | Missing required canonical question response; `question-score-profile-invalid-missing-response`; `evidence-profile-adequate`. | No valid question scores. | No valid dimension results. | No valid weighted assessment result. | No readiness assignment; fail closed. | No Findings emitted. | No Severity Assignment. | No Risk Assessment. | No Confidence Assessment. | No Recommendations. | No Executive Summary. | `business-decision-methodology-v1` |
| `fixture-v1-version-mismatch-fail-closed` | Complete input shape with unsupported methodology artifact version `unsupported-methodology-version`. | No valid question scores. | No valid dimension results. | No valid weighted assessment result. | No readiness assignment; fail closed. | No Findings emitted. | No Severity Assignment. | No Risk Assessment. | No Confidence Assessment. | No Recommendations. | No Executive Summary. | Unsupported version; fail closed before production authority. |

## 6. Validation Requirements

Status: `APPROVED`

Golden Fixture payload validation must fail closed.

Required validation rules:

- Every fixture must have a unique Fixture ID.
- Every fixture must reference an approved fixture catalog entry from Golden
  Fixtures v1.
- Every complete-valid fixture must define deterministic expected outputs.
- Every fail-closed fixture must define deterministic expected absence of
  partial downstream output.
- Expected outputs must be immutable once approved.
- Expected outputs must be version-bound.
- Expected question scores must conform to Question Scoring Tables v1.
- Expected dimension results must conform to equal contribution within each
  Primary Dimension.
- Expected weighted assessment results must conform to the official dimension
  weight set.
- Expected readiness must conform to Readiness Threshold Values v1.
- Expected severity must conform to Severity Decision Tables v1.
- Expected risk must conform to Risk Decision Tables v1.
- Expected confidence must conform to Confidence Decision Tables v1.
- Expected recommendations must conform to Recommendation Decision Tables v1.
- Expected Executive Summary references must conform to Executive Summary
  Templates v1.
- Invalid or incomplete fixtures must fail closed.

## 7. Immutability Rules

Status: `APPROVED`

Golden Fixture payload expected outputs are immutable once approved.

Immutability requirements:

- Expected question scores shall not change without methodology version review.
- Expected dimension results shall not change without methodology version
  review.
- Expected weighted assessment results shall not change without methodology
  version review.
- Expected readiness, findings, severity, risk, confidence, recommendations,
  and Executive Summary references shall not change without methodology version
  review.
- Fixture IDs shall not be reused for materially different payloads.
- Superseded fixtures must remain traceable to the prior version.

## 8. Version Binding

Status: `APPROVED`

Golden Fixture payload artifact version:

```text
golden-fixture-payloads-v1
```

Golden Fixture catalog version:

```text
golden-fixture-catalog-v1
```

Methodology version:

```text
business-decision-methodology-v1
```

Required artifact versions:

- `scoring-scale-v1`
- `question-scoring-tables-v1`
- `official-dimension-weight-set-v1`
- `readiness-threshold-values-v1`
- `severity-decision-table-set-v1`
- `risk-decision-table-set-v1`
- `confidence-decision-table-set-v1`
- `recommendation-decision-table-set-v1`
- `executive-summary-template-set-v1`

## 9. Computational Properties

Status: `APPROVED`

Golden Fixture Payloads v1 satisfies:

- Determinism: each fixture has one deterministic set of expected outputs.
- Reproducibility: identical fixture inputs under the same methodology and
  artifact versions must reproduce the same expected outputs.
- Immutability: approved expected outputs are immutable.
- Version binding: every fixture payload is bound to methodology and artifact
  versions.
- Traceability: every expected output traces to fixture inputs and approved
  methodology artifacts.
- Explainability: expected outputs preserve the method, rule, and source
  references needed to explain the result.
- Fail-closed behavior: invalid, incomplete, unsupported, or version-mismatched
  fixtures produce no partial downstream business output.
- Independence: fixture execution never modifies business truth.

## 10. Fixture Coverage Matrix

Status: `APPROVED`

| Coverage Area | Fixture Coverage |
| --- | --- |
| Question scoring | All complete-valid fixtures define one of the approved question score profiles. |
| Dimension scoring | All complete-valid fixtures define expected results for all five approved Business Capability Dimensions. |
| Weighted aggregation | All complete-valid fixtures define expected weighted assessment result. |
| Readiness | Not Ready, Developing, Ready, and Advanced are each covered. |
| Findings | Empty Finding collection, Strength, Critical Deficiency, High Deficiency, Medium Deficiency, and Low Deficiency are covered. |
| Severity | Critical, High, Medium, Low, Informational, and no-Severity empty collection are covered. |
| Risk | Critical Risk, Elevated Risk, Moderate Risk, Low Risk, and Minimal / Informational are covered. |
| Confidence | Very High Confidence, High Confidence, Moderate Confidence, Low Confidence, and Insufficient Confidence are covered. |
| Recommendations | Immediate Action, Priority Action, Planned Improvement, Best Practice, and Monitor are covered. |
| Executive Summary | All seven Executive Summary template section IDs are referenced by complete-valid fixtures. |
| Fail-closed validation | Invalid input and version mismatch fixtures are covered. |

## 11. Validation Summary

Status: `APPROVED`

| Validation Requirement | Result |
| --- | --- |
| Every fixture has a unique ID. | Pass |
| Every fixture has deterministic expected outputs. | Pass |
| Expected outputs are immutable. | Pass |
| Fixture coverage spans the complete assessment pipeline. | Pass |
| No duplicate fixtures exist. | Pass |
| Fixtures are version-bound. | Pass |
| Invalid or incomplete fixtures fail closed. | Pass |
| Runtime implementation is not introduced. | Pass |
| Automated test code is not introduced. | Pass |
| Consumer-specific behavior is not introduced. | Pass |

## 12. Remaining Implementation Artifacts

Status: `APPROVED`

- No remaining methodology governance artifacts are pending.
- Future implementation remains a separate bounded implementation activity.

## 13. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE GOLDEN FIXTURE PAYLOADS V1
```

Golden Fixture Payloads v1 is approved as the repository-owned deterministic
payload definition artifact for `business-decision-methodology-v1`. It
populates the approved fixture catalog with deterministic input profiles,
expected outputs, version binding, validation requirements, immutability
rules, and coverage confirmation.

No implementation code is authorized by this artifact.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/12-official-dimension-weight-set-v1.md`
- `docs/business-decision-methodology/20-question-scoring-tables-v1.md`
- `docs/business-decision-methodology/21-readiness-threshold-values-v1.md`
- `docs/business-decision-methodology/22-severity-decision-tables-v1.md`
- `docs/business-decision-methodology/23-risk-decision-tables-v1.md`
- `docs/business-decision-methodology/24-confidence-decision-tables-v1.md`
- `docs/business-decision-methodology/25-recommendation-decision-tables-v1.md`
- `docs/business-decision-methodology/26-executive-summary-templates-v1.md`
- `docs/business-decision-methodology/27-golden-fixtures-v1.md`
- `docs/business-decision-methodology/29-regression-validation-framework-v1.md`
- `docs/business-decision-methodology/30-production-authority-release-v1.md`
