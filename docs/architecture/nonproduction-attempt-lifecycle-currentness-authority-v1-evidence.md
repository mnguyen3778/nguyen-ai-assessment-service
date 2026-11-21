# Nonproduction Attempt lifecycle and currentness authority v1

## Baseline and authority

Assessment Service started on `main` at `02621e2f28dae15c86e77b39b1381436c0d23489`. Local and live remote main matched. The [promoted source contract](governed-nonproduction-current-attempt-source-contract-v1.md) matched SHA-256 `4e2ed3732b78e0089596b1e133c1c73e25acce40c46099c1a49dc9e782894e44`. The read-only Trusted Authorization reference was `44700df0a56425522d967432492cf3f3e0bf4d2a`.

The private source stores one Attempt for an exact, independently verified Business Entity, Engagement, Participation authority and provenance, and principal scope. Its operation is `PROTECTED_ASSESSMENT_SUBMISSION`. The trusted local owner configures that scope and distinct issuance and invalidation grants. Grants are bound to the exact scope or issued Attempt, to the configured Assessment Service authority, and to the same non-root real and effective OS identity. These controls depend on trusted process bootstrap and filesystem custody. There is no browser input path or external grant issuer in this increment.

Issuance generates an opaque UUID-backed reference. The authorized transitions are one issuance into `ISSUED` and one terminal change to `INVALIDATED`. The source exposes neither reactivation nor reuse. Effective state is derived from the append-only audit rows. Each atomic commit records revision, state, source provenance, exact Attempt, operator and authority basis. The immutable store configuration supplies the exact scope. The source requires a canonical owner-only directory outside Git and a regular owner-only database. Initialization is exclusive and reopening never creates a missing database.

## Revision and observation boundary

Every read and lifecycle write requires an independently supplied checkpoint for the exact source and scope. It must match the audited history digest. Mutations also enforce the expected source history and, for invalidation, the expected current revision. A commit ahead of its checkpoint, an unavailable checkpoint, or an older database under a newer checkpoint fails closed. The source exposes the committed history digest for review. An independent checkpoint keeper and advance procedure are still required. Automatically deriving the expected digest from the database being read or restoring both copies together would defeat rollback detection. The Trusted Authorization positive revision pin is separate.

The private owner read returns the exact original request and distinguishes current, invalidated, confirmed absent, unavailable, and malformed evidence. The same-process observation uses an exclusive monotonic deadline from the governing invocation. There is no source TTL default. A SQLite transaction holds the writer exclusion lock through owner consumption. Final validation checks the original invocation and observation, rereads checkpoint-backed state under that lock, and is single-use. Data detached from the held context has no validity. A later invalidation is reflected when the checkpoint catches up. Reads in the intervening commit-to-checkpoint gap withhold authority.

The promoted adapter matches the owner identity and evidence fields, protected operation and applicable read statuses. Its typed observation envelope remains consumer-owned. Wiring a detached positive result into the current adapter would lose the source lock and final validation. A future approved integration must hold the owner observation through final bundle acceptance and preserve the original query, the independent positive revision pin, and the owner-backed deadline. No source callback was registered. No end-to-end post-read protection, cross-service atomicity, production readiness, or operational authorization is established.

## Verification and proposed commit

- 11 focused tests passed with disposable SQLite stores and explicit test checkpoints. They cover scope and grant rejection, exact provenance and revision, terminal invalidation, stale and conflicting writers, storage and schema failure, rollback and missing checkpoints, expired or copied evidence, owner lock exclusion, and independent-process reopen.
- 601 Assessment Service tests passed in the full suite, including the 11 focused tests. Static checks compared the owner and promoted consumer field sets, status labels, and protected operation.
- Synthetic verification issued and invalidated disposable Attempts. Independent process checks observed the issued and invalidated revisions with source provenance. There was no retained operational Attempt or operational ALLOW. Trusted Authorization and Platform were inspected read-only.

Proposed scope includes `src/assessment/_nonproduction_attempt_authority.py`, `tests/test_nonproduction_attempt_authority.py`, and this evidence document.
