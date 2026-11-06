# Local Synthetic Priority Assertion Validation Evidence v1

**LOCAL SYNTHETIC NONPRODUCTION ONLY.** Founder-authorized bounded local
implementation of assertion validation for D2, D3, and D5. The governing
[input extension design](../business-decision-methodology/33-recommendation-priority-governed-input-extension-draft-v1.md)
and [final-priority methodology draft](../business-decision-methodology/32-final-recommendation-priority-addendum-draft-v1.md)
remain proposed and nonauthoritative. This evidence does not approve their
business rules or any final priority assignment.

## Scope and files

The isolated [validator](../../src/assessment/local_priority_assertions.py)
accepts explicitly supplied synthetic context and assertion mappings. Focused
[unit tests](../../tests/test_local_priority_assertions.py) exercise the local
boundary. These are the only source/test additions. This evidence document is
the only implementation record added. No existing tracked source, runtime,
contract, decision table, methodology, fixture, or EIP file was modified.
The two untracked design drafts were left unchanged.

## Local contract and authority

The supported contract version is `local-synthetic-priority-assertion-v1`.
The fixed synthetic authority profile is
`local-synthetic-priority-authority-v1`: `synthetic-issuer-customer` may issue
`customer-impact`, `synthetic-issuer-executive` may issue
`executive-urgency`, and `synthetic-issuer-dependency` may issue
`dependency-role`. The issuer catalog and driver-value catalog are immutable.
These are test-only identifiers, not production business approvers or
authorization decisions. Only exact `local-{driver}-{evaluated|not-applicable}-v1`
rule IDs with `local-synthetic-applicability-v1` are accepted.

The validator requires the exact record schema: assertion ID, contract version,
snapshot and assessment identities, recommendation instance and finding IDs,
recommendation rule and table version, driver, value, applicability state and
rule/version, evidence references, business authority reference, source
revision, currentness reference, and nullable D5 target and D3 timing-basis
references. It rejects extra/missing fields, wrong types, strings over 128
characters, more than eight evidence references, noncanonical/duplicate
references, more than 32 assertions, and unsupported versions or values.
It accepts mappings, not raw JSON; duplicate raw JSON keys are outside this
API because raw JSON is not parsed.

Synthetic values are bounded to `impact-present`,
`impact-affirmed-absent`, the three documented executive-action values,
`blocks-related-work`, `unlocks-related-work`,
`no-dependency-affirmed`, and evidence-backed `not-applicable`. They are local
test labels, **not approved production classifications**. Affirmative absence
and exclusion require a synthetic evidence fact with reviewed-scope support.
Time-bound action requires a matching explicit timing-basis reference.

## Binding, currentness, and conflicts

The caller supplies a synthetic context with exact snapshot and assessment
identities, recommendation instances, evidence facts, and current revision
state. A record must match its instance ID, finding ID, recommendation rule ID,
and table version; a matching finding ID alone is insufficient. Evidence must
exist in that context and match the driver, value, and instance. Positive D5
relations require a different, existing same-snapshot target with matching
evidence. Unknown/cross-snapshot targets, self-links, and directed cycles
reject. No edge is inferred from recommendation order or shared references.
No driver assertion is issued for the null-linked no-findings monitor.

Currentness uses only caller-supplied synthetic revision state. A record's
currentness reference must resolve to its exact source revision. Unknown,
superseded, or conflicting revisions reject; timestamps are not consulted.
Duplicate assertion IDs and multiple active records for the same
recommendation/driver reject atomically. No array-order winner is selected.

The result reports `VALID_EVALUATED`, `VALID_NOT_APPLICABLE`,
`BLOCKED_PENDING_DATA`, or `INVALID`. Missing required records block; malformed
submitted records reject. Valid records return assertion validation evidence
only. The result has no priority field, and the module has no priority formula
or production call path.

## Verification

All commands used the existing Python 3.14 environment without AWS access:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests /opt/homebrew/bin/python3.14 -m unittest test_local_priority_assertions -v
12 tests passed.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests /opt/homebrew/bin/python3.14 -m unittest test_recommendation_priority test_approved_recommendation_runtime test_governed_decision_v2 test_approved_confidence_runtime test_business_decision_package test_business_decision_package_validation test_governed_producer_contract test_golden_fixture_regression
120 tests passed.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /opt/homebrew/bin/python3.14 -m unittest discover -s tests
535 tests passed.
```

Focused tests cover D2/D3/D5 evaluated values, exclusions, missing records,
unsupported schemas/values/versions, evidence and timing support, snapshot and
instance links, wrong assessment, authority profile and issuer scope,
currentness, duplicates, D5 target and cycle failures, deterministic replay,
no-findings behavior, and absence of priority output. The full suite includes
historical v2/v3 contract and golden-fixture regressions. Existing baseline
was 523 tests; the 12 new tests bring the suite to 535.

## Integrity limits and next gate

Structural validation, fixed local issuer checks, synthetic snapshot binding,
and synthetic revision checks are implemented and tested. The following
controls are **NOT IMPLEMENTED** for the assertion records:

- Cryptographic integrity or signature verification.
- Real business approval.
- Live authority verification.
- Live revocation.
- Real evidence-content verification.
- Production currentness.
- Production authorization.
- Final priority assignment.

Existing signed producer snapshots do not authenticate these assertion
records. The validator does not use production keys, IAM, Cognito, a network
lookup, AWS resources, or deployment. Synthetic evidence facts and revision
state are explicit caller-supplied test inputs; they are not proof of real
business facts.

Future production work would first require founder-approved source authority,
applicability rules, value semantics, currentness ownership, and a separate
versioned integrity profile. Final priority additionally needs an approved
D1–D8 decision table and separate implementation authorization. No existing
v2/v3 package, signed handoff, EIP admission, or downstream production path
was changed or activated here.

**Result: LOCAL SYNTHETIC NONPRODUCTION ONLY.**
