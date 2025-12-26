<!--
Sync Impact Report

- Version change: 0.0.0 -> 0.1.0
- Modified principles: placeholders -> AI Notepad principles (Simplicity, Local-First Storage, Azure-Only AI, Privacy, Security, Testability, Maintainability, Packaging)
- Added sections: Project-specific Core Principles, Development Constraints, Development Workflow, Governance items for AI Notepad
- Removed sections: placeholder tokens replaced
- Templates requiring updates: .specify/templates/plan-template.md (✅ updated), .specify/templates/spec-template.md (✅ updated), .specify/templates/tasks-template.md (✅ updated)
- Follow-up TODOs: RATIFICATION_DATE (TODO if unknown)
-->

# AI Notepad Constitution

## Core Principles

### Simplicity (NON-NEGOTIABLE)
AI Notepad MUST remain extremely simple: the UI, dependencies, and codebase are intentionally minimal.
- The user interface MUST be a lightweight desktop window with basic text editing and note listing.
- Dependencies MUST be kept to a minimum; prefer the Python standard library and a very small set of vetted third-party packages.
- Code organization MUST favor small modules with clear responsibilities to keep the maintenance surface small.

### Local-First Storage (NON-NEGOTIABLE)
Notes and user data MUST be stored locally on disk using a local SQLite database by default.
- The application MUST NOT default to any cloud storage for user notes.
- Export/import features MAY be provided but MUST be explicit and opt-in.

### Azure-Only AI (NON-NEGOTIABLE)
Any AI-powered features (e.g., the rewrite assistant) MUST call an Azure OpenAI deployment.
- There MUST be no fallback or configuration option that uses the public OpenAI endpoint.
- The code MUST allow configuring the Azure OpenAI deployment endpoint via environment variables.

### Privacy By Default (NON-NEGOTIABLE)
User inputs, prompts, and AI responses MUST NOT be persisted or transmitted outside the local device unless the user explicitly saves them as notes.
- Telemetry, analytics, or prompt logging are disabled by default and require explicit opt-in with clear disclosure.
- Temporary in-memory usage for AI requests is permitted only for immediate user-visible features and must be discarded afterward.

### Security (NON-NEGOTIABLE)
Secrets MUST never be committed to source control. Configuration MUST use environment variables for secrets and API endpoints.
- Support for optional OS-provided keychain/credential storage is REQUIRED for improved user convenience.
- Configuration files containing secrets are prohibited; if used for convenience they MUST be gitignored and documented as a security risk.

### Testability (REQUIRED)
Core application logic MUST be separated from the UI to enable unit testing. Storage and AI client components MUST be unit-tested using mocks.
- Storage layer interface MUST be abstracted so tests can use an in-memory SQLite or mock implementation.
- The AI client MUST be designed to inject a transport layer or client abstraction to allow mocking Azure responses.

### Maintainability (REQUIRED)
Code MUST use clear module boundaries, include type hints, and conform to linting and formatting rules (e.g., `ruff`, `black`, or equivalent).
- Documentation for each semantic module (README.md and AGENT_INSTRUCTION.md) MUST exist and be kept in meaning parity with implementation.

### Packaging (REQUIRED)
Provide a documented, simple path to create a desktop distributable (recommended: `PyInstaller`), and include build instructions.
- Packaging scripts MUST avoid embedding secrets; builds that require secrets MUST load them from environment or secure keychain at build/runtime.

## Non-Goals
- Multi-user sync and collaboration features are out of scope.
- Mobile and web application targets are intentionally out of scope.

## Development Constraints
- Language: Python 3.11+ (PREFERRED) or the project's supported Python runtime.
- Primary storage: SQLite (local file). Migrations and schema MUST be versioned.
- AI integration: Azure OpenAI only; endpoint and deployment name configured via `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, `AZURE_OPENAI_API_KEY` environment variables.
- Secrets: Prefer OS keychain integration (e.g., `keyring` on desktop platforms) for optional credential storage.
- Testing: `pytest` for unit tests; storage and AI client tests MUST use mocks or in-memory databases.
- Packaging: Provide `pyproject.toml` or `requirements.txt` and a `build/` script showing `pyinstaller` usage.

## Development Workflow
- Pull requests MUST include unit tests for modified core logic and update semantic module README/AGENT_INSTRUCTION files when behavior changes.
- Code reviews MUST verify no secrets are present and that Azure-only AI usage is enforced.
- Linting and formatting MUST pass before merge; CI SHOULD run `ruff`/`black` and `pytest`.

## Semantic Architecture (Meaning-First Development)

### Definition: Semantic Modules**Reference**: [Semantic Architecture](https://github.com/dkuwcreator/Semantic-Architecture)

### Core Principle: Operate Where You Have Full Context

Work is organized into **Semantic Modules** – bounded cognitive units that carry both code and meaning. Agents operate within a single module unless explicitly escalating to broader scope.

### Artifact Spaces (Tool-Agnostic)

Development artifacts live in three distinct spaces:

1. **Design Space (Read-Only)**:
   - Contains specifications, plans, contracts, research
   - Describes WHAT to build and WHY
   - **Immutable during implementation** (except progress tracking)
   - In Spec Kit: maps to `FEATURE_DIR` (typically `specs/<feature>/`)

2. **Build Space (Mutable)**:
   - Contains application code, tests, runtime configuration
   - The actual product being built
   - Where ALL implementation happens
   - In Spec Kit: maps to repository/application root

3. **Module Space (Co-located Meaning)**:
   - Module code + documentation live together
   - Each module includes README.md + AGENT_INSTRUCTION.md alongside its code
   - Prevents semantic drift through proximity
   - In Spec Kit: modules live in Build Space
   - **Note**: Semantic Architecture doesn't prescribe folder names like `src/` or `tests/` - these are outcomes of applying the principles to organize code

**Rule**: Design Space is read-only. Implementation happens in Build Space. Module documentation is co-located in Build Space.

**Important**: Semantic Architecture defines the **principles** (bounded contexts, co-located meaning, agent scope), not the **folder structure**. Folder organization (like `src/`, `tests/`, `backend/`) emerges from applying these principles to your specific project.

### Semantic Modules: The Atomic Bounded Context

**Semantic Modules** are the fundamental unit for safe Human–AI collaboration. Each module:

- **Has clear responsibilities**: Explicit purpose and scope
- **Declares invariants**: Non-negotiable behavioral guarantees
- **Defines boundaries**: What is inside vs. outside the module
- **Specifies interfaces**: How the module interacts with others

**Required artifacts per module** (co-located with code):

- **README.md**: Human intent documentation
  - What the module does and why it exists
  - Key responsibilities and invariants
  - Usage examples and integration patterns
  
- **AGENT_INSTRUCTION.md**: AI guidance documentation
  - Allowed edits and safety constraints
  - Module boundaries and forbidden changes
  - Testing requirements and verification steps

### Agent Scope Discipline

Agents must operate within their authorized scope:

1. **Local Module Agent** (Default):
   - Can only modify one semantic module
   - Must update module's README.md and AGENT_INSTRUCTION.md when changing behavior
   - Operates where full context is available

2. **Cluster Agent**:
   - May coordinate changes across modules in the same cluster
   - Requires explicit justification for multi-module scope
   - Must document inter-module dependencies

3. **System Agent**:
   - Allowed to refactor cross-cutting architecture
   - Requires escalation and additional review
   - Must provide migration paths for affected modules

**Escalation Rule**: When a change requires broader scope than authorized, agent MUST:
- Document why single-module approach is insufficient
- Map all affected modules and dependencies
- Request explicit approval before proceeding

### Bounded Context Rules

1. **Scope Declaration (REQUIRED)**:
  - Feature specifications MUST explicitly declare:
    - Modules in scope (with responsibilities)
    - Modules out of scope (with rationale)
    - Cross-module impacts and dependencies

2. **Module Isolation**:
  - Changes SHOULD remain within declared module boundaries
  - Single-module changes are preferred over cross-module changes
  - Module dependencies MUST be explicitly documented

3. **Interface Stability**:
  - Module interfaces MUST maintain backward compatibility
  - Breaking changes MUST be documented with migration notes
  - Interface changes MUST update all dependent modules

### Cross-Module Escalation

When changes affect multiple modules:

1. **Justification Required**: Document why cross-module scope is necessary
2. **Dependency Mapping**: List all affected modules and their relationships
3. **Compatibility Analysis**: Assess impact on module interfaces
4. **Migration Planning**: Provide upgrade path for dependent modules
5. **Review Escalation**: Cross-module changes require additional review

### Meaning Parity (NON-NEGOTIABLE)

**Principle**: Documentation MUST match implemented behavior. No semantic drift allowed.

**Required actions when changing module behavior**:

1. **Update README.md**:
  - Reflect changed responsibilities or invariants
  - Update examples if behavior changes
  - Document new integration patterns

2. **Update AGENT_INSTRUCTION.md**:
  - Adjust allowed edits if boundaries change
  - Update safety constraints for new behavior
  - Revise testing requirements

3. **Verification**:
  - Documentation review MUST accompany code review
  - Both artifacts MUST be updated in the same commit/PR
  - Stale documentation is a blocking defect

### Semantic Drift Prevention

**Drift Definition**: When documentation describes behavior that differs from actual implementation.

**Prevention measures**:

- Specification phase: Declare semantic scope upfront
- Planning phase: Map modules to implementation changes
- Task phase: Include documentation update tasks for each affected module
- Implementation phase: Update docs alongside code
- Review phase: Verify meaning parity (use checklist)

**Detection**:

- Regular semantic drift audits via `/speckit.checklist`
- Automated checks for documentation staleness
- Human review of README.md ↔ code alignment
- Agent instruction validation against actual constraints

**Resolution**:

- Semantic drift is a **HIGH severity** issue
- MUST be fixed before feature merge
- Both code and docs may need updates to restore parity
- Document resolution in commit messages

## Governance

All changes to this constitution or to project-level governance MUST follow the amendment process below.

**Amendment Procedure**:
- Proposer files a draft amendment as a PR that updates `.specify/memory/constitution.md` and includes a migration plan for affected modules.
- A minimum of two maintainers MUST approve the PR. If maintainers disagree, a 3rd-party reviewer is invited to adjudicate.
- The PR MUST include a Semantic Impact Assessment describing affected modules, required documentation updates, and test changes.
- Once merged, the amendment's `Last Amended` date on the Constitution MUST be updated in this file.

**Versioning Policy**:
- Follow semantic versioning for the constitution: MAJOR.MINOR.PATCH.
  - MAJOR: Backward incompatible governance or principle removals/redefinitions.
  - MINOR: New principle/section added or material expansion of guidance.
  - PATCH: Clarifications, wording fixes, or non-semantic refinements.

**Compliance Reviews**:
- Every release MUST include an internal compliance check that verifies:
  - Azure-only AI integration is enforced (no OpenAI public endpoints present).
  - Secrets are not committed in the repository.
  - Core unit tests for storage and AI client exist and pass.

**Version**: 0.1.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2025-12-24

- Both code and docs may need updates to restore parity
- Document resolution in commit messages

## Governance

All changes to this constitution or to project-level governance MUST follow the amendment process below.

**Amendment Procedure**:
- Proposer files a draft amendment as a PR that updates `.specify/memory/constitution.md` and includes a migration plan for affected modules.
- A minimum of two maintainers MUST approve the PR. If maintainers disagree, a 3rd-party reviewer is invited to adjudicate.
- The PR MUST include a Semantic Impact Assessment describing affected modules, required documentation updates, and test changes.
- Once merged, the amendment's `Last Amended` date on the Constitution MUST be updated in this file.

**Versioning Policy**:
- Follow semantic versioning for the constitution: MAJOR.MINOR.PATCH.
  - MAJOR: Backward incompatible governance or principle removals/redefinitions.
  - MINOR: New principle/section added or material expansion of guidance.
  - PATCH: Clarifications, wording fixes, or non-semantic refinements.

**Compliance Reviews**:
- Every release MUST include an internal compliance check that verifies:
  - Azure-only AI integration is enforced (no OpenAI public endpoints present).
  - Secrets are not committed in the repository.
  - Core unit tests for storage and AI client exist and pass.

**Version**: 0.1.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2025-12-24

```
