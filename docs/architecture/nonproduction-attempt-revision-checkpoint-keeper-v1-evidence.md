# Nonproduction Attempt revision checkpoint keeper v1

Assessment Service started on `main` at `64fecbb1f19700e8760af13aff582ac779831c73`, matching local and live remote main. The [promoted current-Attempt contract](governed-nonproduction-current-attempt-source-contract-v1.md) retained SHA-256 `4e2ed3732b78e0089596b1e133c1c73e25acce40c46099c1a49dc9e782894e44`. Trusted Authorization remained at `44700df0a56425522d967432492cf3f3e0bf4d2a`.

## Custody and protocol

The private keeper uses a separate SQLite database in a distinct owner-only directory outside Git. Its configuration pins the nonproduction namespace, explicit keeper owner, non-root operator, and exact Assessment Service source, directory and scope. Its append-only journal binds monotonic sequence, source history digest, Attempt and provenance, lifecycle grant basis, and keeper grant basis. SHA-256 seals link entries to the configured source and previous entry. The trusted bootstrap supplies separate exact-scope grants for bootstrap, preparation, and advancement. Bootstrap is exclusive and requires a verified empty source. The bootstrap grant belongs only in initial enrollment configuration.

1. Prepare under an exact expected checkpoint sequence and separate keeper and lifecycle grants. Validate the prior source history and commit the intent to the journal. The source withholds authority from this point.
2. Apply through the existing Assessment Service issuance or invalidation operation. Before source commit, durably mark the intent started while holding the source lock. The started intent cannot be reapplied.
3. Advance under a separate authorized keeper grant. Read the exact next committed source event under lock and compare its predecessor digest, Attempt scope, lifecycle basis, revision and provenance with the prepared intent. Commit the keeper event and expose the stable digest through the existing private read expectation.
4. After interruption, repeat authorized advancement only when the matching source commit survives. If a started intent has no verifiable successor, preserve the blocked state. The current evidence cannot distinguish non-commit from a source rollback in that case. The keeper neither cancels a started intent nor synthesizes the successor.

The source and keeper each commit locally. There is no cross-store atomic transaction. Pending or missing checkpoints, source-ahead and checkpoint-ahead histories, wrong configuration, malformed journals and lock timeouts withhold authority. A one-store restore that creates a disagreement cannot reactivate an invalidated Attempt. The source can hold the Attempt lock through its existing owner-side final validation. No Trusted Authorization integration or positive revision-pin maintenance is added.

## Verification and limits

- 19 focused tests passed, including 8 new keeper tests and 11 existing authority tests. The suite covered authorization and replay rejection, cross-tenant configuration, grants, provenance conflicts, concurrent advancement, missing and corrupt checkpoint records, SQLite lock timeout, both one-store rollback directions, and interruption before both source and checkpoint commits. An independent process recovered a matching committed issuance and independently observed terminal invalidation. A checkpoint-gap rollback after committed invalidation stayed blocked until the matching committed source image was available and advancement was authorized.
- All 609 Assessment Service tests passed. Disposable tests used real SQLite files and synthetic scope and verified revision 2 invalidation. No retained operational store was provisioned and no operational ALLOW was issued.
- This implementation separates logical ownership, write interfaces and durability domains. The local files share an OS operator. A compromised operator can rewrite both stores and their custody configuration, and coordinated rollback to a matching older pair is undetectable without an independently protected anchor. There is no automatic recovery for a started mutation with missing source evidence. Stronger keeper custody and owner-backed final bundle integration remain separate work.

## Proposed commit scope

- `src/assessment/_nonproduction_attempt_checkpoint.py`
- `src/assessment/_nonproduction_attempt_authority.py`
- `tests/test_nonproduction_attempt_checkpoint.py`
- `docs/architecture/nonproduction-attempt-revision-checkpoint-keeper-v1-evidence.md`
