# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

## Semantic Architecture Plan *(Required)*

<!--
  CRITICAL: Map this feature to Semantic Modules using tool-agnostic language.
  This section defines the semantic topology BEFORE task breakdown.
  
  Reference: https://github.com/dkuwcreator/Semantic-Architecture
-->

### Semantic Map

<!--
  Define the module topology for this feature.
  This map guides all implementation and ensures bounded context discipline.
-->

**Clusters** (logical groupings of related modules):

- **[Cluster Name]**: [Purpose and scope]
  - Modules: [List module names in this cluster]
  - Cluster Responsibility: [What this cluster handles]

**Modules** (atomic bounded contexts):

- **[Module Name]** (`[path/in/build/space]`):
  - **Responsibility**: [Single clear purpose]
  - **Boundaries**: [What this module does and does NOT do]
  - **Interfaces**: [How it interacts with other modules]
  - **Agent Scope**: [Local/Cluster/System - what level of agent can modify this]
  - **Status**: [NEW/EXISTING/MODIFIED]

**Module Dependencies** (directed graph):

```
[Module A] ──→ [Module B]  (dependency relationship)
[Module C] ──→ [Module D]  (dependency relationship)
```

**Boundary Violations** (if any):

- [List any cross-cluster changes and justification]
- [Escalation required: YES/NO]

### Modules Impacted

<!--
  For each module being modified, specify planned changes.
  This section provides implementation details for the modules in the Semantic Map.
-->

- **[Module 1 Path/Name]**:
  - **Current Responsibility**: [What it does now]
  - **Planned Changes**: [Specific modifications - e.g., "Add /api/v1/users endpoint", "Extend User model with email field"]
  - **Files Affected**: [List key files - e.g., "src/api/users.py, src/models/user.py"]

- **[Module 2 Path/Name]**:
  - **Current Responsibility**: [What it does now]
  - **Planned Changes**: [Specific modifications]
  - **Files Affected**: [List key files]

### Invariants to Preserve

<!--
  Document non-negotiable behaviors that MUST remain unchanged.
  These are the "contracts" this feature must honor.
-->

- **[Module/Component]**: [Specific invariant - e.g., "User IDs must remain immutable", "API versioning maintains /v1 compatibility"]
- **[Module/Component]**: [Specific invariant]

### Interfaces & Dependencies Touched

<!--
  Map out how modules interact and what contracts are being modified.
-->

**New Interfaces**:

- [Module A] → [Module B]: [New contract/API - e.g., "UserService.validateEmail() method"]

**Modified Interfaces**:

- [Existing interface]: [How it changes - e.g., "Add optional 'include_metadata' parameter to User.toJSON()"]

**Dependencies**:

- [Module A] now depends on [Library/Module B] for [capability]
- [Existing dependency changes]

### Meaning Parity Updates Required

<!--
  CRITICAL: List all documentation that MUST be updated to maintain meaning parity.
  Stale documentation is a blocking defect.
-->

#### README.md Updates

For each impacted module:

- **[Module 1 Path]**:
  - [ ] Update responsibility description to reflect [new capability]
  - [ ] Add/modify usage examples for [new feature]
  - [ ] Update invariants section if [behavior changed]
  - [ ] Add integration patterns for [new interfaces]

- **[Module 2 Path]**:
  - [ ] Update responsibility description
  - [ ] Add/modify usage examples
  - [ ] Document new dependencies

#### AGENT_INSTRUCTION.md Updates

For each impacted module:

- **[Module 1 Path]**:
  - [ ] Update allowed edits to include [new operations]
  - [ ] Update safety constraints for [new behavior]
  - [ ] Add testing requirements for [new functionality]
  - [ ] Update boundary definitions if [scope changed]

- **[Module 2 Path]**:
  - [ ] Update allowed edits
  - [ ] Update safety constraints
  - [ ] Add testing requirements

#### Other Documentation

- [ ] **API Documentation**: Update OpenAPI/contracts for [changed endpoints]
- [ ] **Architecture Diagrams**: Reflect new [module relationships/dependencies]
- [ ] **Migration Guides**: Document [breaking changes or upgrade paths]
- [ ] **Semantic Module Index**: Update if [modules added/removed/renamed]

## Project Structure

**CRITICAL**: This section defines TWO separate folder hierarchies:

1. **Design Documents** (specs/ folder) - Where specifications live
2. **Application Code** (repository root) - Where implementation happens

### Documentation (Design Artifacts Only)

**Location**: `specs/[###-feature]/` (NOT where implementation happens)

```text
specs/[###-feature]/
├── spec.md              # Feature specification (/speckit.specify command output)
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── checklists/          # Quality checklists (/speckit.checklist command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

**Purpose**: Design documents that describe WHAT to build. These are READ by implementation agents but NOT modified during implementation (except tasks.md to mark tasks complete).

### Application Code (Implementation Target)

**Location**: Repository root (where ALL implementation tasks target)

<!--
  ACTION REQUIRED: Replace the placeholder trees below with your project's actual structure.
  Delete unused options. The delivered plan must not include Option labels.
  
  IMPORTANT: These are EXAMPLE STRUCTURES that commonly emerge when applying Semantic
  Architecture principles. They are NOT requirements - organize your project based on
  your specific needs, technology, and team preferences.
  
  All paths below are relative to REPOSITORY ROOT, NOT the specs folder.
  Implementation tasks in tasks.md will create/modify files at these paths.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project structure (example)
# Common for libraries, CLI tools, simple applications
# Organize modules directly at root or in organizational folders

<modules>/               # Your semantic modules
├── <module1>/          # Example module
│   ├── README.md      # Module documentation
│   ├── AGENT_INSTRUCTION.md
│   └── [code files]
└── <module2>/

<tests>/                # Your test organization
└── ...

# [REMOVE IF UNUSED] Option 2: Layered structure (example)
# Common for web applications with separate concerns
# Shows backend/frontend separation

backend/
├── <modules>/
│   └── [your backend modules with README.md + AGENT_INSTRUCTION.md]
└── <tests>/

frontend/
├── <modules>/
│   └── [your frontend modules with README.md + AGENT_INSTRUCTION.md]
└── <tests>/

# [REMOVE IF UNUSED] Option 3: Platform-specific structure (example)
# Common for mobile applications with API
# Shows platform separation

api/
└── <modules>/
    └── [your API modules with README.md + AGENT_INSTRUCTION.md]

ios/ or android/
└── <modules>/
    └── [your platform modules with README.md + AGENT_INSTRUCTION.md]
```

**Purpose**: Actual application code that will be created/modified by implementation tasks. This is where the application being built lives, NOT in the specs folder.

**Structure Decision**: [Document the selected structure and reference the real
directories captured above. Confirm all paths are relative to repository root.]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation                      | Why Needed         | Simpler Alternative Rejected Because |
|--------------------------------|--------------------|--------------------------------------|
| [e.g., 4th project]            | [current need]     | [why 3 projects insufficient]        |
| [e.g., Repository pattern]     | [specific problem] | [why direct DB access insufficient]  |
