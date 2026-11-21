"""Locally durable keeper for one explicitly governed nonproduction Attempt source."""

from contextlib import closing, contextmanager
from dataclasses import dataclass, field, replace
from hashlib import sha256
import json
import os
from pathlib import Path
import sqlite3
import stat

from ._nonproduction_attempt_authority import (
    _AttemptAuthority, _EMPTY_HISTORY, _ExpectedHistory, _LOCK_TIMEOUT_SECONDS,
    _Rejected, _Stale, _attempt_reference, _reference,
)


_SCHEMA = (
    "CREATE TABLE keeper (configuration TEXT NOT NULL)",
    """CREATE TABLE journal (
        sequence INTEGER PRIMARY KEY CHECK (sequence BETWEEN 0 AND 6),
        payload TEXT NOT NULL,
        seal TEXT NOT NULL
    )""",
)
_STEPS = (
    "bootstrap", "prepare-issue", "start-issue", "advance-issue",
    "prepare-invalidate", "start-invalidate", "advance-invalidate",
)
_STABLE = (0, 3, 6)


def _digest(value):
    return sha256(value.encode()).hexdigest()


def _is_digest(value):
    return type(value) is str and len(value) == 64 and set(value) <= set("0123456789abcdef")


def _json(value):
    return json.dumps(value, separators=(",", ":"))


@dataclass(frozen=True, slots=True)
class _KeeperGrant:
    operation: str
    namespace: str
    source_reference: str
    authority_basis_reference: str


@dataclass(frozen=True, slots=True)
class _Entry:
    sequence: int
    history_digest: str
    attempt_reference: str
    provenance_reference: str
    lifecycle_basis: str
    keeper_basis: str

    @property
    def revision(self):
        return str(self.sequence // 3)


@dataclass(frozen=True, slots=True)
class _CheckpointKeeper:
    directory: Path
    environment: str
    operator_uid: int
    owner_reference: str
    namespace: str
    source: _AttemptAuthority = field(repr=False)
    grants: tuple[_KeeperGrant, ...] = field(default=(), repr=False)

    def __post_init__(self):
        if (
            self.environment != "nonproduction" or type(self.environment) is not str
            or type(self.operator_uid) is not int or self.operator_uid <= 0
            or type(self.source) is not _AttemptAuthority
            or self.operator_uid != self.source.operator_uid
            or not _reference(self.owner_reference) or self.owner_reference == self.source.owner_reference
            or not _reference(self.namespace)
            or not isinstance(self.directory, Path) or not self.directory.is_absolute()
            or self.directory.resolve() != self.directory
            or self.directory == self.source.directory
            or self.directory in self.source.directory.parents or self.source.directory in self.directory.parents
            or type(self.grants) is not tuple or any(type(grant) is not _KeeperGrant for grant in self.grants)
        ):
            raise _Rejected("invalid independent checkpoint configuration")
        self._check_operator()

    @property
    def _database(self):
        return self.directory / "attempt-checkpoint-v1.sqlite3"

    def _check_operator(self):
        if os.getuid() != self.operator_uid or os.geteuid() != self.operator_uid:
            raise _Rejected("wrong checkpoint operator")

    def _check_access(self, *, database=True):
        self._check_operator()
        if self.directory.resolve() != self.directory or any(
            (parent / ".git").exists() for parent in (self.directory, *self.directory.parents)
        ):
            raise _Rejected("checkpoint requires a canonical directory outside Git")
        folder = self.directory.lstat()
        if (
            not stat.S_ISDIR(folder.st_mode) or folder.st_uid != self.operator_uid
            or stat.S_IMODE(folder.st_mode) != 0o700
        ):
            raise _Rejected("checkpoint directory requires owner-only access")
        if database:
            file = self._database.lstat()
            if (
                not stat.S_ISREG(file.st_mode) or file.st_uid != self.operator_uid
                or stat.S_IMODE(file.st_mode) != 0o600 or file.st_nlink != 1
            ):
                raise _Rejected("checkpoint requires a private owner-controlled database")

    def _configuration(self):
        return _json((
            "attempt-checkpoint-v1", self.environment, self.operator_uid, self.owner_reference,
            self.namespace, str(self.source.directory), self.source._configuration(),
        ))

    @contextmanager
    def _transaction(self, *, write=False):
        self._check_access()
        mode = "rw" if write else "ro"
        with closing(sqlite3.connect(
            f"{self._database.as_uri()}?mode={mode}", uri=True, timeout=_LOCK_TIMEOUT_SECONDS,
            isolation_level=None,
        )) as db:
            db.execute("PRAGMA trusted_schema = OFF")
            if write:
                db.execute("PRAGMA synchronous = FULL")
            db.execute("BEGIN IMMEDIATE" if write else "BEGIN")
            try:
                yield db
                db.commit()
            except BaseException:
                db.rollback()
                raise

    def _require_grant(self, grant, operation):
        self._check_operator()
        if (
            type(grant) is not _KeeperGrant or not any(grant is candidate for candidate in self.grants)
            or grant.operation != operation or grant.namespace != self.namespace
            or grant.source_reference != self.source.source_reference
            or not _reference(grant.authority_basis_reference)
        ):
            raise _Rejected("exact checkpoint grant required")

    def _seal(self, sequence, previous, payload):
        return _digest(_json((self._configuration(), sequence, previous, payload)))

    def _append(self, db, entries, entry):
        payload = _json((
            entry.history_digest, entry.attempt_reference, entry.provenance_reference,
            entry.lifecycle_basis, entry.keeper_basis,
        ))
        previous = entries[-1][1] if entries else ""
        db.execute("INSERT INTO journal VALUES (?, ?, ?)", (
            entry.sequence, payload, self._seal(entry.sequence, previous, payload),
        ))
        return entry

    def _entries(self, db):
        if (
            db.execute("PRAGMA user_version").fetchone() != (1,)
            or db.execute("PRAGMA journal_mode").fetchone() != ("delete",)
            or db.execute(
                "SELECT sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%' ORDER BY name"
            ).fetchall() != [(_SCHEMA[1],), (_SCHEMA[0],)]
            or db.execute("SELECT configuration FROM keeper LIMIT 2").fetchall() != [(self._configuration(),)]
            or db.execute("PRAGMA quick_check(1)").fetchone() != ("ok",)
        ):
            raise _Rejected("invalid checkpoint storage or namespace")
        rows = db.execute("SELECT * FROM journal ORDER BY sequence LIMIT 8").fetchall()
        if not 1 <= len(rows) <= len(_STEPS):
            raise _Rejected("missing or ambiguous checkpoint history")
        entries = []
        previous = ""
        for index, (sequence, payload, seal) in enumerate(rows):
            if sequence != index or type(payload) is not str or seal != self._seal(sequence, previous, payload):
                raise _Rejected("conflicting checkpoint history")
            try:
                values = json.loads(payload)
                if type(values) is not list or len(values) != 5:
                    raise ValueError("wrong journal shape")
                entry = _Entry(sequence, *values)
            except ValueError as exc:
                raise _Rejected("malformed checkpoint payload") from exc
            self._verify_entry(entry, entries)
            entries.append((entry, seal))
            previous = seal
        return entries

    def _verify_entry(self, entry, entries):
        if not _is_digest(entry.history_digest) or not _reference(entry.keeper_basis):
            raise _Rejected("malformed checkpoint evidence")
        if not entries:
            if (entry.history_digest, entry.attempt_reference, entry.provenance_reference,
                entry.lifecycle_basis) != (_EMPTY_HISTORY, "", "", ""):
                raise _Rejected("invalid checkpoint bootstrap")
            return
        prior = entries[-1][0]
        if not _reference(entry.lifecycle_basis):
            raise _Rejected("missing lifecycle authority basis")
        if entry.sequence in (3, 6):
            if (
                entry.history_digest == prior.history_digest
                or not _attempt_reference(entry.attempt_reference)
                or (entry.sequence == 6 and entry.attempt_reference != prior.attempt_reference)
                or entry.provenance_reference != self.source._provenance(entry.attempt_reference, int(entry.revision))
                or entry.lifecycle_basis != prior.lifecycle_basis
            ):
                raise _Rejected("wrong checkpoint revision or provenance")
        elif (
            (entry.history_digest, entry.attempt_reference, entry.provenance_reference)
            != (prior.history_digest, prior.attempt_reference, prior.provenance_reference)
            or (entry.sequence in (2, 5)
                and (entry.lifecycle_basis, entry.keeper_basis) != (prior.lifecycle_basis, prior.keeper_basis))
        ):
            raise _Rejected("conflicting prepared checkpoint history")

    def _head(self, entries, expected_sequence, permitted):
        entry = entries[-1][0]
        if type(expected_sequence) is not int or entry.sequence != expected_sequence or entry.sequence not in permitted:
            raise _Stale("unexpected checkpoint sequence")
        return entry

    def initialize(self, *, grant):
        """Explicitly enroll an already initialized and empty source once."""
        self._require_grant(grant, "bootstrap")
        with self.source._transaction() as source_db:
            if self.source._history(source_db):
                raise _Rejected("bootstrap requires a verified empty Attempt source")
            self._check_access(database=False)
            fd = os.open(self._database, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            os.close(fd)
            with self._transaction(write=True) as db:
                for statement in _SCHEMA:
                    db.execute(statement)
                db.execute("INSERT INTO keeper VALUES (?)", (self._configuration(),))
                db.execute("PRAGMA user_version = 1")
                return self._append(db, [], _Entry(0, _EMPTY_HISTORY, "", "", "", grant.authority_basis_reference))

    def expectation(self):
        """Read-only checkpoint dependency for the existing source reader."""
        with self._transaction() as db:
            head = self._entries(db)[-1][0]
            return self._expectation(head) if head.sequence in _STABLE else None

    def _expectation(self, entry):
        return _ExpectedHistory(self.source.source_reference, self.source.scope, entry.history_digest)

    def bind(self):
        """The bound lifecycle cannot bypass the keeper's preparation path."""
        return replace(self.source, expectation=self.expectation, mutation_expectation=lambda _: None)

    def prepare(self, *, expected_sequence, grant, lifecycle_grant):
        """Record the separately authorized intent before any source mutation."""
        with self.source._transaction() as source_db, self._transaction(write=True) as db:
            entries = self._entries(db)
            head = self._head(entries, expected_sequence, (0, 3))
            operation = "issue" if head.sequence == 0 else "invalidate"
            self._require_grant(grant, "prepare-" + operation)
            target = self.source.scope if operation == "issue" else head.attempt_reference
            self.source._require_grant(lifecycle_grant, operation, target)
            if self.source._digest(self.source._history(source_db)) != head.history_digest:
                raise _Stale("source and checkpoint disagree before preparation")
            return self._append(db, entries, replace(
                head, sequence=head.sequence + 1, lifecycle_basis=lifecycle_grant.authority_basis_reference,
                keeper_basis=grant.authority_basis_reference,
            ))

    def apply(self, *, expected_sequence, lifecycle_grant):
        """Start the prepared write once, using existing lifecycle authorization."""
        with self._transaction() as db:
            intent = self._head(self._entries(db), expected_sequence, (1, 4))
        operation = "issue" if intent.sequence == 1 else "invalidate"
        target = self.source.scope if operation == "issue" else intent.attempt_reference
        self.source._require_grant(lifecycle_grant, operation, target)
        if lifecycle_grant.authority_basis_reference != intent.lifecycle_basis:
            raise _Rejected("lifecycle grant differs from the recorded intent")

        def start(actual_digest):
            # The source mutation holds its write lock during this callback.
            with self._transaction(write=True) as db:
                entries = self._entries(db)
                head = self._head(entries, expected_sequence, (1, 4))
                if head != intent or actual_digest != intent.history_digest:
                    raise _Stale("prepared checkpoint no longer matches source")
                self._append(db, entries, replace(intent, sequence=intent.sequence + 1))
            return self._expectation(intent)

        source = replace(self.bind(), mutation_expectation=start)
        if operation == "issue":
            return source.issue(self.source.scope, grant=lifecycle_grant)
        return source.invalidate(intent.attempt_reference, expected_revision=intent.revision, grant=lifecycle_grant)

    def advance(self, *, expected_sequence, grant):
        """Checkpoint only an exact, durably recorded successor of the started intent."""
        with self.source._transaction() as source_db, self._transaction(write=True) as db:
            entries = self._entries(db)
            started = self._head(entries, expected_sequence, (2, 5))
            sequence = started.sequence + 1
            self._require_grant(grant, _STEPS[sequence])
            history = self.source._history(source_db)
            if len(history) != int(started.revision) + 1 or self.source._digest(history[:-1]) != started.history_digest:
                raise _Stale("missing or conflicting committed source successor")
            _, attempt, _, _, basis, provenance = history[-1]
            if basis != started.lifecycle_basis or (sequence == 6 and attempt != started.attempt_reference):
                raise _Rejected("committed source does not match prepared lifecycle intent")
            entry = _Entry(sequence, self.source._digest(history), attempt, provenance, basis, grant.authority_basis_reference)
            self._verify_entry(entry, entries)
            return self._append(db, entries, entry)
