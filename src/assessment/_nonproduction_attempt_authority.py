"""Assessment Service-owned local Attempt authority for nonproduction only."""

from collections.abc import Callable
from contextlib import ExitStack, closing, contextmanager
from dataclasses import dataclass, field
from hashlib import sha256
import json
import os
from pathlib import Path
import sqlite3
import stat
from threading import get_ident
from time import monotonic_ns
from uuid import UUID, uuid4


_OPERATION = "PROTECTED_ASSESSMENT_SUBMISSION"
_OWNER = "assessment-service"
_VERSION = "governed-nonproduction-current-attempt-source-v1"
_PREFIX = "assessment-attempt:"
_LOCK_TIMEOUT_SECONDS = 0.25
_SCHEMA = (
    "CREATE TABLE source (configuration TEXT NOT NULL)",
    """CREATE TABLE audit (
        revision INTEGER PRIMARY KEY CHECK (revision IN (1, 2)),
        attempt TEXT NOT NULL,
        state TEXT NOT NULL CHECK (state IN ('ISSUED', 'INVALIDATED')),
        actor INTEGER NOT NULL CHECK (actor > 0),
        basis TEXT NOT NULL,
        provenance TEXT NOT NULL UNIQUE
    )""",
)
_EMPTY_HISTORY = sha256(b"[]").hexdigest()


class _Rejected(ValueError):
    """Rejected authority, scope, configuration, or transition."""


class _Stale(_Rejected):
    """Source history does not match independent expectations."""


def _reference(value):
    return type(value) is str and bool(value) and all(
        character.isprintable() and not character.isspace() for character in value
    )


def _attempt_reference(value):
    if not _reference(value) or not value.startswith(_PREFIX):
        return False
    suffix = value[len(_PREFIX):]
    try:
        parsed = UUID(suffix)
    except ValueError:
        return False
    return parsed.version == 4 and parsed.hex == suffix


def _clock_value(value):
    return type(value) is int and value >= 0


@dataclass(frozen=True, slots=True)
class _Scope:
    business_entity_id: str
    engagement_reference: str
    participation_authority_reference: str
    participation_provenance_reference: str
    principal_id: str
    protected_operation: str

    def values(self):
        return (
            self.business_entity_id, self.engagement_reference,
            self.participation_authority_reference, self.participation_provenance_reference,
            self.principal_id, self.protected_operation,
        )

    def valid(self):
        return all(map(_reference, self.values())) and self.protected_operation == _OPERATION


@dataclass(frozen=True, slots=True)
class _Grant:
    operation: str
    target: _Scope | str
    authority_basis_reference: str


@dataclass(frozen=True, slots=True)
class _ExpectedHistory:
    """A checkpoint supplied independently by trusted nonproduction bootstrap."""

    source_reference: str
    scope: _Scope
    history_digest: str


@dataclass(frozen=True, slots=True)
class _Mutation:
    attempt_reference: str
    revision: str
    state: str
    provenance_reference: str
    history_digest: str


@dataclass(frozen=True, slots=True, eq=False)
class _ReadRequest:
    invocation: object
    scope: _Scope
    attempt_reference: str
    environment: str
    # Trusted enclosing invocation deadline in the shared monotonic clock domain.
    completion_deadline: int


@dataclass(frozen=True, slots=True)
class _Identity:
    attempt_reference: str
    business_entity_id: str
    engagement_reference: str
    principal_id: str
    participation_authority_reference: str
    participation_provenance_reference: str
    protected_operation: str


@dataclass(frozen=True, slots=True)
class _Evidence:
    owner_reference: str
    source_reference: str
    source_version: str
    provenance_reference: str
    revision: str
    observed_at: int
    valid_until: int


@dataclass(frozen=True, slots=True, eq=False)
class _Observation:
    request: _ReadRequest
    status: str
    evidence: _Evidence | None = None
    records: tuple[_Identity, ...] = ()


@dataclass(frozen=True, slots=True)
class _AttemptAuthority:
    """One exact owner-approved synthetic context in one governed source.

    Configuration and grants come from trusted local bootstrap. The OS account
    and bootstrap are trusted. Python object identity is a local custody check.
    """

    directory: Path
    environment: str
    operator_uid: int
    owner_reference: str
    source_reference: str
    scope: _Scope
    expectation: Callable[[], _ExpectedHistory | None] | None = field(default=None, repr=False)
    grants: tuple[_Grant, ...] = field(default=(), repr=False)
    mutation_expectation: Callable[[str], _ExpectedHistory | None] | None = field(default=None, repr=False)

    def __post_init__(self):
        if (
            type(self.environment) is not str or self.environment != "nonproduction"
            or type(self.operator_uid) is not int or self.operator_uid <= 0
            or type(self.owner_reference) is not str or self.owner_reference != _OWNER
            or not _reference(self.source_reference)
            or type(self.scope) is not _Scope or not self.scope.valid()
            or not isinstance(self.directory, Path) or not self.directory.is_absolute()
            or not self.directory.name or self.directory.resolve() != self.directory
            or (self.expectation is not None and not callable(self.expectation))
            or (self.mutation_expectation is not None and not callable(self.mutation_expectation))
            or type(self.grants) is not tuple or any(type(grant) is not _Grant for grant in self.grants)
        ):
            raise _Rejected("invalid nonproduction authority configuration")
        self._check_operator()

    @property
    def _database(self):
        return self.directory / "attempt-v1.sqlite3"

    def _check_operator(self):
        if os.getuid() != self.operator_uid or os.geteuid() != self.operator_uid:
            raise _Rejected("wrong local operator")

    def _check_access(self, *, database=True):
        self._check_operator()
        if self.directory.resolve() != self.directory or any(
            (parent / ".git").exists() for parent in (self.directory, *self.directory.parents)
        ):
            raise _Rejected("source requires a canonical directory outside Git")
        folder = self.directory.lstat()
        if (
            not stat.S_ISDIR(folder.st_mode) or folder.st_uid != self.operator_uid
            or stat.S_IMODE(folder.st_mode) != 0o700
        ):
            raise _Rejected("source directory requires owner-only access")
        if database:
            file = self._database.lstat()
            if (
                not stat.S_ISREG(file.st_mode) or file.st_uid != self.operator_uid
                or stat.S_IMODE(file.st_mode) != 0o600 or file.st_nlink != 1
            ):
                raise _Rejected("database requires a private owner-controlled file")

    def _configuration(self):
        return json.dumps(
            (self.environment, self.operator_uid, self.owner_reference, self.source_reference,
             _VERSION, self.scope.values()), separators=(",", ":"),
        )

    def initialize(self):
        """Initialize a new source only. An existing file is never reused or replaced."""
        self._check_operator()
        self._check_access(database=False)
        fd = os.open(self._database, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        os.close(fd)
        with self._transaction() as db:
            for statement in _SCHEMA:
                db.execute(statement)
            db.execute("INSERT INTO source VALUES (?)", (self._configuration(),))
            db.execute("PRAGMA user_version = 1")

    @contextmanager
    def _transaction(self):
        self._check_access()
        with closing(sqlite3.connect(
            self._database.as_uri() + "?mode=rw", uri=True, timeout=_LOCK_TIMEOUT_SECONDS,
            isolation_level=None,
        )) as db:
            db.execute("PRAGMA trusted_schema = OFF")
            db.execute("PRAGMA synchronous = FULL")
            db.execute("BEGIN IMMEDIATE")
            try:
                yield db
                db.commit()
            except BaseException:
                db.rollback()
                raise

    def _history(self, db):
        objects = db.execute(
            "SELECT sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        if (
            db.execute("PRAGMA user_version").fetchone() != (1,)
            or db.execute("PRAGMA journal_mode").fetchone() != ("delete",)
            or objects != [(_SCHEMA[1],), (_SCHEMA[0],)]
            or db.execute("SELECT configuration FROM source LIMIT 2").fetchall() != [(self._configuration(),)]
            or db.execute("PRAGMA quick_check(1)").fetchone() != ("ok",)
        ):
            raise _Rejected("unsupported or invalid source storage")
        history = db.execute("SELECT * FROM audit ORDER BY revision LIMIT 3").fetchall()
        if len(history) > 2:
            raise _Rejected("ambiguous audit history")
        for index, (revision, attempt, state, actor, basis, provenance) in enumerate(history):
            if (
                revision != index + 1 or state != ("ISSUED", "INVALIDATED")[index]
                or not _attempt_reference(attempt) or attempt != history[0][1]
                or actor != self.operator_uid or not _reference(basis)
                or provenance != self._provenance(attempt, revision)
            ):
                raise _Rejected("invalid audit history")
        return history

    def _digest(self, history):
        return sha256(json.dumps(history, separators=(",", ":")).encode()).hexdigest()

    def _confirmed_history(self, db, *, mutation=False):
        history = self._history(db)
        actual = self._digest(history)
        if mutation and self.mutation_expectation is not None:
            expected = self.mutation_expectation(actual)
        else:
            expected = self.expectation() if self.expectation is not None else None
        if (
            type(expected) is not _ExpectedHistory or expected.scope != self.scope
            or expected.source_reference != self.source_reference
            or expected.history_digest != actual
        ):
            raise _Stale("independent history expectation mismatch")
        return history

    def _provenance(self, attempt, revision):
        return f"{self.source_reference}/{attempt}/rev-{revision}"

    def _require_grant(self, grant, operation, target):
        self._check_operator()
        if (
            type(grant) is not _Grant or not any(grant is configured for configured in self.grants)
            or grant.operation != operation or grant.target != target
            or not _reference(grant.authority_basis_reference)
        ):
            raise _Rejected("operation-specific authority grant required")

    def issue(self, scope, *, grant):
        if type(scope) is not _Scope or scope != self.scope:
            raise _Rejected("issuance scope mismatch")
        self._require_grant(grant, "issue", scope)
        with self._transaction() as db:
            history = self._confirmed_history(db, mutation=True)
            if history:
                raise _Rejected("scope already has an issued Attempt")
            attempt = _PREFIX + uuid4().hex
            return self._append(db, history, attempt, "ISSUED", grant)

    def invalidate(self, attempt_reference, *, expected_revision, grant):
        if not _attempt_reference(attempt_reference) or not _reference(expected_revision):
            raise _Rejected("exact Attempt and expected revision required")
        self._require_grant(grant, "invalidate", attempt_reference)
        with self._transaction() as db:
            history = self._confirmed_history(db, mutation=True)
            if not history or history[-1][1] != attempt_reference:
                raise _Rejected("wrong Attempt")
            if str(history[-1][0]) != expected_revision:
                raise _Stale("wrong expected revision")
            if history[-1][2] != "ISSUED":
                raise _Rejected("Attempt is already invalidated")
            return self._append(db, history, attempt_reference, "INVALIDATED", grant)

    def _append(self, db, history, attempt, state, grant):
        revision = len(history) + 1
        provenance = self._provenance(attempt, revision)
        event = (revision, attempt, state, self.operator_uid, grant.authority_basis_reference, provenance)
        db.execute("INSERT INTO audit VALUES (?, ?, ?, ?, ?, ?)", event)
        return _Mutation(attempt, str(revision), state, provenance, self._digest([*history, event]))

    def _read(self, request, db):
        observed_at = monotonic_ns()
        if observed_at >= request.completion_deadline:
            return _Observation(request, "UNAVAILABLE")
        history = self._confirmed_history(db)
        if monotonic_ns() >= request.completion_deadline:
            return _Observation(request, "UNAVAILABLE")
        if not history or history[-1][1] != request.attempt_reference:
            scope = self.scope
            lookup = sha256(json.dumps(
                (scope.values(), request.attempt_reference), separators=(",", ":"),
            ).encode()).hexdigest()
            provenance = f"{self.source_reference}/absence/{lookup}/{self._digest(history)}"
            revision, status = str(len(history)), "CONFIRMED_ABSENT"
        else:
            revision, _, state, _, _, provenance = history[-1]
            status = "CURRENT" if state == "ISSUED" else "INVALIDATED"
        evidence = _Evidence(
            self.owner_reference, self.source_reference, _VERSION, provenance,
            str(revision), observed_at, request.completion_deadline,
        )
        records = ()
        if status == "CURRENT":
            scope = self.scope
            records = (_Identity(
                request.attempt_reference, scope.business_entity_id, scope.engagement_reference,
                scope.principal_id, scope.participation_authority_reference,
                scope.participation_provenance_reference, scope.protected_operation,
            ),)
        return _Observation(request, status, evidence, records)

    @contextmanager
    def observe(self, request):
        """Hold a source lock through private consumption and final verification.

        Detaching a result voids its validity. The published Trusted Authorization
        consumer has no finalization hook and must not receive CURRENT from here.
        """
        with ExitStack() as stack:
            db = None
            if (
                type(request) is not _ReadRequest or request.invocation is None
                or type(request.environment) is not str or request.environment != "nonproduction"
                or type(request.scope) is not _Scope or request.scope != self.scope
                or not _attempt_reference(request.attempt_reference)
                or not _clock_value(request.completion_deadline)
            ):
                observation = _Observation(request, "MALFORMED")
            else:
                try:
                    db = stack.enter_context(self._transaction())
                    observation = self._read(request, db)
                except _Stale:
                    observation = _Observation(request, "UNAVAILABLE")
                except _Rejected:
                    observation = _Observation(request, "MALFORMED")
                except sqlite3.DatabaseError as exc:
                    corrupt = getattr(exc, "sqlite_errorcode", None) in (sqlite3.SQLITE_CORRUPT, sqlite3.SQLITE_NOTADB)
                    observation = _Observation(request, "MALFORMED" if corrupt else "UNAVAILABLE")
                except Exception:
                    observation = _Observation(request, "UNAVAILABLE")
            if observation.status not in ("CURRENT", "INVALIDATED", "CONFIRMED_ABSENT"):
                stack.close()
                db = None
            active, consumed, owner_thread = db is not None, False, get_ident()

            def finalize(invocation, evidence):
                nonlocal consumed
                if (
                    not active or consumed or get_ident() != owner_thread
                    or invocation is not request.invocation or evidence is not observation
                    or observation.status != "CURRENT"
                    or monotonic_ns() >= observation.evidence.valid_until
                ):
                    return False
                consumed = True
                try:
                    latest = self._read(request, db)
                    return (
                        latest.status == "CURRENT"
                        and latest.records == observation.records
                        and latest.evidence.revision == observation.evidence.revision
                        and latest.evidence.provenance_reference == observation.evidence.provenance_reference
                        and monotonic_ns() < observation.evidence.valid_until
                    )
                except Exception:
                    return False

            try:
                yield observation, finalize
            finally:
                active = False
