"""Disposable SQLite verification of separated Attempt checkpoint custody."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import asdict, replace
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Barrier
from time import monotonic_ns
import unittest
from unittest.mock import patch

from assessment._nonproduction_attempt_authority import (
    _AttemptAuthority, _Grant, _OPERATION, _OWNER, _ReadRequest, _Rejected, _Scope, _Stale,
)
from assessment._nonproduction_attempt_checkpoint import _CheckpointKeeper, _KeeperGrant


class CheckpointKeeperTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        source, checkpoint = self.root / "source", self.root / "keeper"
        source.mkdir(mode=0o700)
        checkpoint.mkdir(mode=0o700)
        self.scope = _Scope("entity:test", "engagement:test", "participation:owner",
                            "participation:provenance", "principal:test", _OPERATION)
        self.issue_grant = _Grant("issue", self.scope, "basis:issue")
        authority = _AttemptAuthority(
            source, "nonproduction", os.getuid(), _OWNER, "source:test",
            self.scope, grants=(self.issue_grant,),
        )
        authority.initialize()
        self.grants = {
            operation: _KeeperGrant(operation, "namespace:test", "source:test", "keeper:" + operation)
            for operation in ("bootstrap", "prepare-issue", "advance-issue", "prepare-invalidate", "advance-invalidate")
        }
        self.keeper = _CheckpointKeeper(
            checkpoint, "nonproduction", os.getuid(), "keeper:owner", "namespace:test",
            authority, tuple(self.grants.values()),
        )

    def boot(self):
        return self.keeper.initialize(grant=self.grants["bootstrap"])

    def prepare(self):
        return self.keeper.prepare(expected_sequence=0, grant=self.grants["prepare-issue"],
                                   lifecycle_grant=self.issue_grant)

    def issue(self):
        self.prepare()
        return self.keeper.apply(expected_sequence=1, lifecycle_grant=self.issue_grant)

    def finalize_issue(self):
        return self.keeper.advance(expected_sequence=2, grant=self.grants["advance-issue"])

    def invalidation(self, issued):
        grant = _Grant("invalidate", issued.attempt_reference, "basis:invalidate")
        return replace(self.keeper, source=replace(self.keeper.source, grants=(grant,))), grant

    def invalidate(self, issued):
        keeper, grant = self.invalidation(issued)
        keeper.prepare(expected_sequence=3, grant=self.grants["prepare-invalidate"], lifecycle_grant=grant)
        keeper.apply(expected_sequence=4, lifecycle_grant=grant)
        keeper.advance(expected_sequence=5, grant=self.grants["advance-invalidate"])

    def observe(self, attempt, *, keeper=None, expected="CURRENT"):
        authority = (keeper or self.keeper).bind()
        request = _ReadRequest(object(), self.scope, attempt, "nonproduction", monotonic_ns() + 10**10)
        with authority.observe(request) as (answer, finalize):
            self.assertIs(answer.request, request)
            self.assertEqual(expected, answer.status)
            self.assertEqual(expected == "CURRENT", finalize(request.invocation, answer))
            self.assertFalse(finalize(request.invocation, answer))
        return answer

    def backup(self, path, name):
        copy = self.root / name
        with closing(sqlite3.connect(path)) as db, closing(sqlite3.connect(copy)) as target:
            db.backup(target)
        copy.chmod(0o600)
        return copy

    def test_bootstrap_transition_audit_and_private_reads(self):
        self.assertEqual(0, self.boot().sequence)
        self.assertEqual(0o600, self.keeper._database.stat().st_mode & 0o777)
        with self.assertRaises(FileExistsError):
            self.boot()
        with self.assertRaises(_Stale):
            self.keeper.bind().issue(self.scope, grant=self.issue_grant)
        issued = self.issue()
        self.observe(issued.attempt_reference, expected="UNAVAILABLE")
        checkpoint = self.finalize_issue()
        self.assertEqual((3, "1", issued.provenance_reference),
                         (checkpoint.sequence, checkpoint.revision, checkpoint.provenance_reference))
        answer = self.observe(issued.attempt_reference)
        self.assertEqual(issued.provenance_reference, answer.evidence.provenance_reference)
        self.invalidate(issued)
        answer = self.observe(issued.attempt_reference, expected="INVALIDATED")
        self.assertEqual("2", answer.evidence.revision)
        with self.keeper._transaction() as db:
            entries = [entry for entry, _ in self.keeper._entries(db)]
        self.assertEqual(list(range(7)), [entry.sequence for entry in entries])
        self.assertEqual("basis:invalidate", entries[-1].lifecycle_basis)
        self.assertEqual("keeper:advance-invalidate", entries[-1].keeper_basis)
        with self.keeper.source._transaction() as db:
            self.assertEqual(["ISSUED", "INVALIDATED"], [row[2] for row in self.keeper.source._history(db)])
        with self.assertRaises(_Stale):
            self.prepare()

    def test_exact_grants_namespace_tenant_and_operator(self):
        with self.assertRaises(_Rejected):
            self.keeper.initialize(grant=None)
        wrong = replace(self.grants["bootstrap"], namespace="wrong")
        with self.assertRaises(_Rejected):
            replace(self.keeper, grants=(wrong,)).initialize(grant=wrong)
        wrong = replace(self.grants["bootstrap"], source_reference="wrong")
        with self.assertRaises(_Rejected):
            replace(self.keeper, grants=(wrong,)).initialize(grant=wrong)
        with self.assertRaises(_Rejected):
            self.keeper.initialize(grant=replace(self.grants["bootstrap"]))
        with self.assertRaises(_Rejected):
            replace(self.keeper, environment="production")
        with patch("assessment._nonproduction_attempt_checkpoint.os.geteuid", return_value=0):
            with self.assertRaises(_Rejected):
                self.boot()
        self.boot()
        with self.assertRaises(_Rejected):
            replace(self.keeper, namespace="wrong").expectation()
        for source in (replace(self.keeper.source, source_reference="wrong"),
                       replace(self.keeper.source, scope=replace(self.scope, business_entity_id="wrong"))):
            with self.assertRaises(_Rejected):
                replace(self.keeper, source=source).expectation()
        with self.assertRaises(_Rejected):
            self.keeper.prepare(expected_sequence=0, grant=self.grants["advance-issue"],
                                lifecycle_grant=self.issue_grant)
        with self.assertRaises(_Rejected):
            self.keeper.prepare(expected_sequence=0, grant=self.grants["prepare-issue"], lifecycle_grant=None)
        with self.assertRaises(_Stale):
            self.keeper.prepare(expected_sequence=3, grant=self.grants["prepare-issue"],
                                lifecycle_grant=self.issue_grant)

    def test_replay_conflicting_advancement_and_provenance(self):
        self.boot()
        issued = self.issue()
        with self.assertRaises(_Stale):
            self.keeper.apply(expected_sequence=1, lifecycle_grant=self.issue_grant)
        with self.assertRaises(_Rejected):
            self.keeper.advance(expected_sequence=2, grant=self.grants["prepare-issue"])
        with self.keeper.source._transaction() as db:
            db.execute("UPDATE audit SET provenance = 'wrong'")
        with self.assertRaises(_Rejected):
            self.finalize_issue()
        with self.keeper.source._transaction() as db:
            db.execute("UPDATE audit SET provenance = ?", (issued.provenance_reference,))
        barrier = Barrier(2)

        def advance():
            barrier.wait(timeout=5)
            try:
                return self.finalize_issue()
            except _Stale:
                return None

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(advance) for _ in range(2)]
            accepted = [result for future in futures if (result := future.result(timeout=5)) is not None]
        self.assertEqual(1, len(accepted))
        self.assertEqual(issued.history_digest, accepted[0].history_digest)
        with self.assertRaises(_Stale):
            self.finalize_issue()

    def test_missing_corrupt_unavailable_and_locked_checkpoint(self):
        attempt = "assessment-attempt:00000000000040008000000000000000"
        self.observe(attempt, expected="UNAVAILABLE")
        self.boot()
        self.observe(attempt, expected="CONFIRMED_ABSENT")
        with closing(sqlite3.connect(self.keeper._database, isolation_level=None)) as db:
            db.execute("BEGIN EXCLUSIVE")
            self.observe(attempt, expected="UNAVAILABLE")
            db.rollback()
        with self.keeper._transaction(write=True) as db:
            db.execute("UPDATE journal SET seal = 'broken'")
        self.observe(attempt, expected="MALFORMED")
        with self.keeper._transaction(write=True) as db:
            db.execute("DELETE FROM journal")
        self.observe(attempt, expected="MALFORMED")

    def test_one_store_rollback_never_reauthorizes_invalidated_attempt(self):
        self.boot()
        issued = self.issue()
        self.finalize_issue()
        old_source = self.backup(self.keeper.source._database, "source-1.sqlite3")
        old_checkpoint = self.backup(self.keeper._database, "keeper-1.sqlite3")
        self.invalidate(issued)
        latest_source = self.backup(self.keeper.source._database, "source-2.sqlite3")
        old_source.replace(self.keeper.source._database)
        self.observe(issued.attempt_reference, expected="UNAVAILABLE")
        latest_source.replace(self.keeper.source._database)
        old_checkpoint.replace(self.keeper._database)
        self.observe(issued.attempt_reference, expected="UNAVAILABLE")
        with self.assertRaises(_Stale):
            self.keeper.advance(expected_sequence=5, grant=self.grants["advance-invalidate"])

    def test_interrupted_lifecycle_stays_blocked_even_if_source_restored(self):
        self.boot()
        issued = self.issue()
        self.finalize_issue()
        writer, grant = self.invalidation(issued)
        writer.prepare(expected_sequence=3, grant=self.grants["prepare-invalidate"], lifecycle_grant=grant)
        self.observe(issued.attempt_reference, expected="UNAVAILABLE")
        old_source = self.backup(writer.source._database, "pre-invalidation.sqlite3")
        with patch.object(_AttemptAuthority, "_append", side_effect=RuntimeError("between start and commit")):
            with self.assertRaises(RuntimeError):
                writer.apply(expected_sequence=4, lifecycle_grant=grant)
        old_source.replace(writer.source._database)
        self.observe(issued.attempt_reference, expected="UNAVAILABLE")
        with self.assertRaises(_Stale):
            writer.apply(expected_sequence=4, lifecycle_grant=grant)
        with self.assertRaises(_Stale):
            writer.advance(expected_sequence=5, grant=self.grants["advance-invalidate"])

    def test_pre_checkpoint_source_rollback_cannot_erase_committed_invalidation(self):
        self.boot()
        issued = self.issue()
        self.finalize_issue()
        writer, grant = self.invalidation(issued)
        old_source = self.backup(writer.source._database, "before-invalidation.sqlite3")
        writer.prepare(expected_sequence=3, grant=self.grants["prepare-invalidate"], lifecycle_grant=grant)
        writer.apply(expected_sequence=4, lifecycle_grant=grant)
        self.observe(issued.attempt_reference, expected="UNAVAILABLE")
        committed = self.backup(writer.source._database, "committed-invalidation.sqlite3")
        old_source.replace(writer.source._database)
        self.observe(issued.attempt_reference, expected="UNAVAILABLE")
        with self.assertRaises(_Stale):
            writer.advance(expected_sequence=5, grant=self.grants["advance-invalidate"])
        committed.replace(writer.source._database)
        writer.advance(expected_sequence=5, grant=self.grants["advance-invalidate"])
        self.observe(issued.attempt_reference, expected="INVALIDATED")

    def test_interrupted_checkpoint_rolls_back_and_authorized_recovery_restarts(self):
        self.boot()
        issued = self.issue()
        append = _CheckpointKeeper._append

        def interrupted(keeper, db, entries, entry):
            append(keeper, db, entries, entry)
            raise RuntimeError("before checkpoint commit")

        with patch.object(_CheckpointKeeper, "_append", interrupted):
            with self.assertRaises(RuntimeError):
                self.finalize_issue()
        self.observe(issued.attempt_reference, expected="UNAVAILABLE")
        with self.assertRaises(_Rejected):
            self.keeper.advance(expected_sequence=2, grant=None)
        self.assertEqual("CURRENT", self.restart(issued, recover=True))
        self.invalidate(issued)
        self.assertEqual("INVALIDATED", self.restart(issued))

    def restart(self, issued, *, recover=False):
        program = """
import json, os, sys
from pathlib import Path
from time import monotonic_ns
import assessment._nonproduction_attempt_authority as source
import assessment._nonproduction_attempt_checkpoint as checkpoint
config = json.loads(sys.argv[1])
scope = source._Scope(**config['scope'])
authority = source._AttemptAuthority(Path(config['source']), 'nonproduction', os.getuid(),
                                     source._OWNER, 'source:test', scope)
grant = checkpoint._KeeperGrant('advance-issue', 'namespace:test', 'source:test', 'keeper:recovery')
keeper = checkpoint._CheckpointKeeper(Path(config['directory']), 'nonproduction', os.getuid(),
                                       'keeper:owner', 'namespace:test', authority, (grant,))
if config['recover']:
    keeper.advance(expected_sequence=2, grant=grant)
request = source._ReadRequest(object(), scope, config['attempt'], 'nonproduction', monotonic_ns()+10**10)
with keeper.bind().observe(request) as (answer, finalize):
    assert finalize(request.invocation, answer) == (answer.status == 'CURRENT')
    print(answer.status)
"""
        result = subprocess.run(
            [sys.executable, "-B", "-c", program, json.dumps({
                "scope": asdict(self.scope), "source": str(self.keeper.source.directory),
                "directory": str(self.keeper.directory), "attempt": issued.attempt_reference, "recover": recover,
            })], check=True, capture_output=True, text=True, timeout=10,
        )
        return result.stdout.strip()


if __name__ == "__main__":
    unittest.main()
