# Project Overview

The Nguyen AI Assessment Service is the deterministic Business Decision Engine
for the Nguyen AI Executive Intelligence Platform.

It is not a scoring engine. It transforms validated business evidence into
structured, explainable, reproducible executive intelligence that downstream
platform capabilities can consume.

Long-term platform evolution:

```text
Directional Assessment
  |
Business Decision Engine
  |
Evidence Intelligence Platform
  |
Executive Dashboard
  |
Portfolio Intelligence
  |
Portfolio Digital Twin
```

Repository goals:

- Maintain the production AWS Lambda assessment service.
- Preserve deterministic business decision behavior.
- Keep methodology configuration authoritative.
- Support small, reviewable implementation increments.
- Preserve traceability from assessment answers to future executive outputs.

Primary references:

- `docs/architecture/assessment-decision-engine-v2.md`
- `docs/business-decision-methodology/01-decision-methodology.md`
- `docs/business-decision-methodology/02-question-catalog.md`
- `docs/business-decision-methodology/03-evidence-catalog.md`
- `docs/business-decision-methodology/04-readiness-methodology.md`
- `docs/business-decision-methodology/05-confidence-methodology.md`
- `docs/business-decision-methodology/06-recommendation-priority.md`
- `docs/business-decision-methodology/07-service-decision-framework.md`
- `docs/business-decision-methodology/08-business-decision-roadmap.md`

# Current Architecture

The authoritative current-state architecture baseline is
`docs/architecture/assessment-decision-engine-v2.md`. Read it before changing
Decision Engine behavior.

Current deterministic processing pipeline:

```text
Assessment Answers
  |
Validation
  |
Methodology Configuration
  |
Answer Normalization
  |
Question Mapping
  |
Decision Engine
  |
Evaluation Explanation
  |
Structured Evaluation
```

The current engine consumes validated assessment answers and methodology
configuration, normalizes configured numeric answer types, maps answers to
question evaluations, aggregates readiness dimension results, and returns
structured evaluation data with explanation metadata.

Do not rewrite the architecture in task prompts or implementation notes. Link
to the architecture baseline and document only the new delta when architecture
changes are approved.

# Engineering Principles

Maintain:

- Deterministic execution.
- Explainability.
- Configuration-driven methodology.
- Traceability.
- Enterprise quality.
- Reproducibility.
- Governance.
- Testability.

Never introduce:

- Hidden business logic.
- Hard-coded methodology.
- Probabilistic decisions.
- LLM reasoning.
- Bedrock or AI model reasoning for decisions.
- Architectural shortcuts.
- Business rules that are not traceable to approved methodology.

The engine executes methodology. Methodology belongs in configuration and
governed documentation.

# Development Workflow

Every implementation should:

1. Review repository state with `git status --short`.
2. Review the relevant architecture and methodology documents.
3. Determine the next logical increment.
4. Explain why that increment is next.
5. Implement one logical feature only.
6. Add or update unit tests for that feature.
7. Run the relevant test command.
8. Recommend a concise enterprise commit message.
9. Stop for review.

Prefer small, reversible changes. Do not skip ahead into future sprint scope.
Do not mix production code, documentation, tests, and release governance unless
the requested increment requires them.

# Coding Standards

Prefer:

- Dataclasses for typed domain models.
- Frozen or immutable models where practical.
- Deterministic pure functions.
- Small focused methods.
- Descriptive naming.
- Configuration-driven execution.
- Explicit validation.
- Clear error messages for invalid inputs or invalid configuration.

Avoid:

- Magic numbers.
- Duplicated logic.
- Hidden state.
- Unnecessary abstraction.
- Premature optimization.
- Lambda-specific logic inside domain evaluation code.
- HTTP or API concerns inside the Decision Engine.

Business vocabulary must come from methodology configuration, not scattered
constants or inferred naming conventions.

# Documentation Standards

Update documentation whenever architecture changes.

Reference architecture documents instead of duplicating them. The current
baseline is `docs/architecture/assessment-decision-engine-v2.md`.

Keep sprint documentation synchronized with implementation state. If behavior
changes, document:

- What changed.
- Why it changed.
- Which methodology source supports it.
- Which downstream components may consume it.
- What remains intentionally out of scope.

Do not document future behavior as current behavior. Future work belongs in a
dedicated roadmap or objectives section.

# Testing Standards

Every feature must include tests.

Tests should verify:

- Deterministic behavior.
- Edge cases.
- Invalid inputs.
- Invalid configuration.
- Explanation metadata.
- Methodology execution.
- Traceability from configuration to evaluation output.

Never reduce test coverage to make an implementation pass. Preserve existing
tests unless a test is explicitly obsolete and the requested task includes its
removal.

Standard full test command:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

# Git Workflow

Use small commits.

Keep increments reviewable.

Use meaningful commit messages, for example:

```text
feat: add deterministic evaluation explanation metadata
docs: baseline assessment decision engine v2 architecture
test: cover invalid methodology configuration
```

Tag architectural milestones when requested or when a governance baseline is
approved.

Never combine unrelated features in one commit. Do not commit local deployment
artifacts such as `deployment.zip`.

# Architecture Boundaries

Decision Engine responsibilities:

- Methodology execution.
- Answer normalization.
- Question evaluation mapping.
- Dimension aggregation.
- Structured evaluation.
- Explanation metadata.

Decision Engine does not perform:

- Executive reporting.
- Recommendation generation.
- Service recommendation generation.
- Persistence.
- AI reasoning.
- LLM or Bedrock decision making.
- Dashboard rendering.
- Portfolio aggregation.

These capabilities are downstream consumers. They should consume Decision Engine
outputs rather than replace or duplicate evaluation logic.

# Future Development

Future work should extend the engine without redesigning it.

Potential future capabilities include:

- Business Readiness Snapshot.
- Confidence Methodology.
- Recommendation Priority.
- Executive Reporting.
- Evidence Intelligence.
- Portfolio Intelligence.

These capabilities should consume the Decision Engine rather than replace it.
When implementing them, preserve this traceability path:

```text
Assessment Answer
  |
Normalized Evidence
  |
Methodology Rule
  |
Business Decision
  |
Executive Recommendation
```

If a future feature requires new business methodology, update the governing
methodology documents first, then translate the approved methodology into
configuration and tests.
