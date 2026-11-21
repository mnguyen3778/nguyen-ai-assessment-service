"""Local lifecycle, rollback, and handoff tests using disposable authority data."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import asdict, fields, replace
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
    _AttemptAuthority, _EMPTY_HISTORY, _Evidence, _ExpectedHistory, _Grant, _Identity,
    _OPERATION, _OWNER, _PREFIX, _ReadRequest, _Rejected, _Scope, _Stale,
)


class AttemptAuthorityTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name).resolve()
        self.scope = _Scope(
            "synthetic:entity", "synthetic:engagement", "synthetic:participation-owner",
            "synthetic:participation-provenance", "synthetic:principal", _OPERATION,
        )
        self.source_reference = "synthetic:assessment-service-test-source"
        self.issue_grant = _Grant("issue", self.scope, "synthetic:issue-approval")
        self.checkpoint = self.expected(_EMPTY_HISTORY)
        self.authority = _AttemptAuthority(
            self.directory, "nonproduction", os.getuid(), _OWNER, self.source_reference,
            self.scope, self.read_expectation, (self.issue_grant,),
        )
        self.authority.initialize()

    def expected(self, digest):
        return _ExpectedHistory(self.source_reference, self.scope, digest)

    def read_expectation(self):
        return self.checkpoint

    def issue(self):
        issued = self.authority.issue(self.scope, grant=self.issue_grant)
        self.checkpoint = self.expected(issued.history_digest)
        return issued

    def invalidation(self, issued):
        grant = _Grant("invalidate", issued.attempt_reference, "synthetic:invalidation-approval")
        return replace(self.authority, grants=(grant,)), grant

    def request(self, attempt_reference):
        return _ReadRequest(object(), self.scope, attempt_reference, "nonproduction", monotonic_ns() + 10**10)

    def test_source_issued_identity_and_exact_contract_shape(self):
        issued = self.issue()
        self.assertTrue(issued.attempt_reference.startswith(_PREFIX))
        self.assertEqual(("1", "ISSUED"), (issued.revision, issued.state))
        request = self.request(issued.attempt_reference)
        with self.authority.observe(request) as (observation, finalize):
            self.assertIs(observation.request, request)
            self.assertEqual("CURRENT", observation.status)
            self.assertEqual(
                (issued.attempt_reference, self.scope.business_entity_id, self.scope.engagement_reference,
                 self.scope.principal_id, self.scope.participation_authority_reference,
                 self.scope.participation_provenance_reference, _OPERATION),
                tuple(asdict(observation.records[0]).values()),
            )
            self.assertEqual(
                (_OWNER, self.source_reference, issued.provenance_reference, issued.revision),
                (observation.evidence.owner_reference, observation.evidence.source_reference,
                 observation.evidence.provenance_reference, observation.evidence.revision),
            )
            self.assertTrue(finalize(request.invocation, observation))
            self.assertFalse(finalize(request.invocation, observation))
        self.assertEqual(
            ("attempt_reference", "business_entity_id", "engagement_reference", "principal_id",
             "participation_authority_reference", "participation_provenance_reference", "protected_operation"),
            tuple(field.name for field in fields(_Identity)),
        )
        self.assertEqual(
            ("owner_reference", "source_reference", "source_version", "provenance_reference",
             "revision", "observed_at", "valid_until"),
            tuple(field.name for field in fields(_Evidence)),
        )
        with self.assertRaises(FileExistsError):
            self.authority.initialize()

    def test_second_source_issues_distinct_reference_and_rejects_duplicate(self):
        issued = self.issue()
        with self.assertRaises(_Rejected):
            self.authority.issue(self.scope, grant=self.issue_grant)
        second_dir = self.directory / "separate"
        second_dir.mkdir(mode=0o700)
        second_scope = replace(self.scope, business_entity_id="synthetic:other")
        second_grant = _Grant("issue", second_scope, "synthetic:second-issue")
        second = replace(
            self.authority, directory=second_dir, scope=second_scope, source_reference="synthetic:second",
            grants=(second_grant,),
            expectation=lambda: _ExpectedHistory("synthetic:second", second_scope, _EMPTY_HISTORY),
        )
        second.initialize()
        self.assertNotEqual(issued.attempt_reference, second.issue(second_scope, grant=second_grant).attempt_reference)

    def test_scope_substitution_and_nonproduction_checks(self):
        issued = self.issue()
        request = self.request(issued.attempt_reference)
        for key in asdict(self.scope):
            with self.subTest(key=key):
                switched = replace(self.scope, **{key: "wrong"})
                with self.authority.observe(replace(request, scope=switched)) as (answer, finalize):
                    self.assertEqual("MALFORMED", answer.status)
                    self.assertIsNone(answer.evidence)
                    self.assertFalse(finalize(request.invocation, answer))
                with self.assertRaises(_Rejected):
                    self.authority.issue(switched, grant=self.issue_grant)
        with self.assertRaises(_Rejected):
            replace(self.authority, environment="production")
        with self.assertRaises(_Rejected):
            replace(self.authority, owner_reference="wrong")
        with self.assertRaises(_Rejected):
            replace(self.authority, operator_uid=0)
        with self.authority.observe(replace(request, attempt_reference="request-uuid")) as (answer, _):
            self.assertEqual("MALFORMED", answer.status)

    def test_write_grants_and_access_modes(self):
        for grant in (None, replace(self.issue_grant), _Grant("invalidate", self.scope, "invalid")):
            with self.subTest(grant=grant), self.assertRaises(_Rejected):
                self.authority.issue(self.scope, grant=grant)
        with self.assertRaises(TypeError):
            self.authority.issue(self.scope, grant=self.issue_grant, attempt_reference="chosen")
        with patch("assessment._nonproduction_attempt_authority.os.geteuid", return_value=0):
            with self.assertRaises(_Rejected):
                self.authority.issue(self.scope, grant=self.issue_grant)
        self.authority._database.chmod(0o640)
        with self.assertRaises(_Rejected):
            self.authority.issue(self.scope, grant=self.issue_grant)
        self.authority._database.chmod(0o600)
        self.directory.chmod(0o750)
        with self.assertRaises(_Rejected):
            self.authority.issue(self.scope, grant=self.issue_grant)
        self.directory.chmod(0o700)
        self.issue()

    def test_invalidation_is_terminal_and_audit_is_state(self):
        issued = self.issue()
        writer, grant = self.invalidation(issued)
        with self.assertRaises(_Stale):
            writer.invalidate(issued.attempt_reference, expected_revision="2", grant=grant)
        with self.assertRaises(_Rejected):
            writer.invalidate(_PREFIX + "00000000000040008000000000000000", expected_revision="1", grant=grant)
        with self.assertRaises(_Rejected):
            writer.invalidate(issued.attempt_reference, expected_revision="1", grant=self.issue_grant)
        invalidated = writer.invalidate(issued.attempt_reference, expected_revision=issued.revision, grant=grant)
        self.assertEqual(("2", "INVALIDATED"), (invalidated.revision, invalidated.state))
        self.assertNotEqual(issued.provenance_reference, invalidated.provenance_reference)
        request = self.request(issued.attempt_reference)
        with self.authority.observe(request) as (answer, _):
            self.assertEqual("UNAVAILABLE", answer.status)
        self.checkpoint = self.expected(invalidated.history_digest)
        with self.authority.observe(request) as (answer, finalize):
            self.assertEqual("INVALIDATED", answer.status)
            self.assertEqual(invalidated.provenance_reference, answer.evidence.provenance_reference)
            self.assertEqual((), answer.records)
            self.assertFalse(finalize(request.invocation, answer))
        with self.assertRaises(_Rejected):
            writer.invalidate(issued.attempt_reference, expected_revision=invalidated.revision, grant=grant)
        with self.authority._transaction() as db:
            rows = self.authority._history(db)
        self.assertEqual(
            [(1, "ISSUED", os.getuid(), self.issue_grant.authority_basis_reference),
             (2, "INVALIDATED", os.getuid(), grant.authority_basis_reference)],
            [(rev, state, uid, basis) for rev, _, state, uid, basis, _ in rows],
        )

    def test_conflicting_writes_allow_exactly_one_commit(self):
        issued = self.issue()
        writer, grant = self.invalidation(issued)
        barrier = Barrier(2)

        def invalidate():
            barrier.wait(timeout=5)
            try:
                return writer.invalidate(issued.attempt_reference, expected_revision="1", grant=grant)
            except (_Rejected, sqlite3.OperationalError):
                return None

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(invalidate) for _ in range(2)]
            commits = [result for future in futures if (result := future.result(timeout=5)) is not None]
        self.assertEqual(1, len(commits))
        self.assertEqual("2", commits[0].revision)
        self.checkpoint = self.expected(commits[0].history_digest)
        with self.authority._transaction() as db:
            self.assertEqual(2, len(self.authority._confirmed_history(db)))

    def test_rollback_conflict_and_missing_expectation_fail_closed(self):
        issued = self.issue()
        backup = self.directory / "disposable-older.sqlite3"
        with closing(sqlite3.connect(self.authority._database)) as db, closing(sqlite3.connect(backup)) as target:
            db.backup(target)
        writer, grant = self.invalidation(issued)
        invalidated = writer.invalidate(issued.attempt_reference, expected_revision="1", grant=grant)
        self.checkpoint = self.expected(invalidated.history_digest)
        request = self.request(issued.attempt_reference)
        backup.chmod(0o600)
        backup.replace(self.authority._database)
        for source in (self.authority, replace(self.authority, expectation=None)):
            with source.observe(request) as (answer, _):
                self.assertEqual("UNAVAILABLE", answer.status)
                self.assertIsNone(answer.evidence)
        with self.assertRaises(_Stale):
            writer.invalidate(issued.attempt_reference, expected_revision="1", grant=grant)
        with self.authority._transaction() as db:
            db.execute("UPDATE audit SET state = 'INVALIDATED' WHERE revision = 1")
        with self.authority.observe(request) as (answer, _):
            self.assertEqual("MALFORMED", answer.status)

    def test_invocation_custody_expiration_and_owner_final_recheck(self):
        issued = self.issue()
        request = replace(self.request(issued.attempt_reference), completion_deadline=20)
        with patch("assessment._nonproduction_attempt_authority.monotonic_ns", return_value=10) as clock:
            with self.authority.observe(request) as (answer, finalize):
                self.assertFalse(finalize(object(), answer))
                self.assertFalse(finalize(request.invocation, replace(answer)))
                clock.return_value = 20
                self.assertFalse(finalize(request.invocation, answer))
            with self.authority.observe(request) as (expired, _):
                self.assertEqual("UNAVAILABLE", expired.status)
            clock.return_value = 10
            with self.authority.observe(request) as (current, finalize):
                self.checkpoint = None
                self.assertFalse(finalize(request.invocation, current))
                self.checkpoint = self.expected(issued.history_digest)
                self.assertFalse(finalize(request.invocation, current))
        with self.authority.observe(self.request(issued.attempt_reference)) as (detached, finalize):
            invocation = detached.request.invocation
        writer, grant = self.invalidation(issued)
        self.checkpoint = self.expected(writer.invalidate(
            issued.attempt_reference, expected_revision="1", grant=grant,
        ).history_digest)
        self.assertFalse(finalize(invocation, detached))
        with self.authority.observe(self.request(issued.attempt_reference)) as (latest, _):
            self.assertEqual("INVALIDATED", latest.status)

    def test_source_lock_prevents_invalidation_during_owner_consumption(self):
        issued = self.issue()
        request = self.request(issued.attempt_reference)
        writer, grant = self.invalidation(issued)
        with self.authority.observe(request) as (answer, finalize):
            self.assertEqual("CURRENT", answer.status)
            with self.assertRaises(sqlite3.OperationalError) as error:
                writer.invalidate(issued.attempt_reference, expected_revision=issued.revision, grant=grant)
            self.assertEqual(sqlite3.SQLITE_BUSY, error.exception.sqlite_errorcode)
            self.assertTrue(finalize(request.invocation, answer))
        self.assertFalse(finalize(request.invocation, answer))
        invalidated = writer.invalidate(issued.attempt_reference, expected_revision=issued.revision, grant=grant)
        self.checkpoint = self.expected(invalidated.history_digest)
        with self.authority.observe(self.request(issued.attempt_reference)) as (latest, _):
            self.assertEqual("INVALIDATED", latest.status)

    def test_absence_outage_schema_and_lock_timeout_are_distinct(self):
        request = self.request(_PREFIX + "00000000000040008000000000000000")
        with self.authority.observe(request) as (answer, _):
            self.assertEqual("CONFIRMED_ABSENT", answer.status)
            self.assertIsNotNone(answer.evidence)
        with self.authority._transaction():
            with self.authority.observe(request) as (answer, _):
                self.assertEqual("UNAVAILABLE", answer.status)
        with self.authority._transaction() as db:
            db.execute("PRAGMA user_version = 2")
        with self.authority.observe(request) as (answer, _):
            self.assertEqual("MALFORMED", answer.status)
        self.authority._database.unlink()
        with self.authority.observe(request) as (answer, _):
            self.assertEqual("UNAVAILABLE", answer.status)

    def test_independent_process_reads_persisted_current_and_invalidated_state(self):
        issued = self.issue()
        program = """
import json, os, sys
from pathlib import Path
from time import monotonic_ns
import assessment._nonproduction_attempt_authority as source
data = json.loads(sys.argv[1])
scope = source._Scope(**data['scope'])
expected = source._ExpectedHistory(data['source'], scope, data['digest'])
authority = source._AttemptAuthority(Path(data['directory']), 'nonproduction', os.getuid(),
                                    source._OWNER, data['source'], scope, lambda: expected)
request = source._ReadRequest(object(), scope, data['attempt'], 'nonproduction', monotonic_ns()+10**10)
with authority.observe(request) as (answer, finalize):
    print(answer.status, answer.evidence.revision, answer.evidence.provenance_reference,
          finalize(request.invocation, answer))
"""

        def run(checkpoint, expected):
            result = subprocess.run(
                [sys.executable, "-B", "-c", program, json.dumps({
                    "directory": str(self.directory), "scope": asdict(self.scope),
                    "source": self.source_reference, "digest": checkpoint.history_digest,
                    "attempt": issued.attempt_reference,
                })], check=True, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(expected, result.stdout.strip())

        run(issued, f"CURRENT 1 {issued.provenance_reference} True")
        writer, grant = self.invalidation(issued)
        invalidated = writer.invalidate(issued.attempt_reference, expected_revision="1", grant=grant)
        run(invalidated, f"INVALIDATED 2 {invalidated.provenance_reference} False")


if __name__ == "__main__":
    unittest.main()
