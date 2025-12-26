---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Module] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Module]**: Which semantic module this task modifies (e.g., Auth, API, Users)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in Build Space (application root)
- Mark if task requires module documentation updates

## Artifact Spaces (Semantic Architecture)

**CRITICAL**: Understand the three artifact spaces before implementing:

1. **Design Space (Read-Only)**:
   - Contains: spec.md, plan.md, tasks.md, contracts/, data-model.md
   - Location in Spec Kit: `FEATURE_DIR` (typically `specs/[###-feature-name]/`)
   - **Tasks do NOT create/modify files here** (except marking tasks complete)

2. **Build Space (Implementation Target)**:
   - Contains: Application code, tests, runtime configuration
   - Location in Spec Kit: Repository/application root
   - **This is where ALL implementation tasks target their file paths**
   - Structure: Defined in plan.md based on project needs
   - **Note**: Semantic Architecture doesn't prescribe `src/`, `tests/`, etc. - these emerge from your project organization

3. **Module Space (Co-located Meaning)**:
   - Module code + documentation together in Build Space
   - Each module has: code files + README.md + AGENT_INSTRUCTION.md
   - Location: Within Build Space (structure determined by plan.md)
   - **Tasks MUST update module docs when changing module behavior**

**Folder Organization** (examples - not prescribed by Semantic Architecture):

The plan.md will define your project's structure based on type and needs. Common patterns that emerge from applying Semantic Architecture:
- **Single project**: Code and tests at repository root
- **Web app**: Separate backend and frontend areas
- **Mobile**: API and platform-specific areas

**Important**: These folder patterns are **outcomes** of applying Semantic Architecture principles, not requirements. Your project may organize differently based on its specific needs.

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  
  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Setup database schema and migrations framework
- [ ] T005 [P] Implement authentication/authorization framework
- [ ] T006 [P] Setup API routing and middleware structure
- [ ] T007 Create base models/entities that all stories depend on
- [ ] T008 Configure error handling and logging infrastructure
- [ ] T009 Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T011 [P] [US1] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 1

- [ ] T012 [P] [Models] [US1] Create [Entity1] model in src/models/[entity1].py
- [ ] T013 [P] [Models] [US1] Create [Entity2] model in src/models/[entity2].py
- [ ] T014 [Services] [US1] Implement [Service] in src/services/[service].py (depends on T012, T013)
- [ ] T015 [API] [US1] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T016 [Services] [US1] Add validation and error handling
- [ ] T017 [Logging] [US1] Add logging for user story 1 operations

### Module Documentation Updates for User Story 1

- [ ] T018 [P] [Models] [US1] Update src/models/README.md with new entities and usage examples
- [ ] T019 [P] [Models] [US1] Update src/models/AGENT_INSTRUCTION.md with validation rules
- [ ] T020 [P] [Services] [US1] Update src/services/README.md with new service responsibilities
- [ ] T021 [P] [Services] [US1] Update src/services/AGENT_INSTRUCTION.md with testing requirements

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T019 [P] [US2] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 2

- [ ] T020 [P] [US2] Create [Entity] model in src/models/[entity].py
- [ ] T021 [US2] Implement [Service] in src/services/[service].py
- [ ] T022 [US2] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T023 [US2] Integrate with User Story 1 components (if needed)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US3] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T025 [P] [US3] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 3

- [ ] T026 [P] [US3] Create [Entity] model in src/models/[entity].py
- [ ] T027 [US3] Implement [Service] in src/services/[service].py
- [ ] T028 [US3] Implement [endpoint/feature] in src/[location]/[file].py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Semantic Architecture Compliance *(Required)*

**Purpose**: Maintain meaning parity between code and documentation to prevent semantic drift

<!--
  CRITICAL: These tasks ensure documentation stays synchronized with implementation.
  Stale documentation is a HIGH severity defect that must be fixed before merge.
  
  Reference: https://github.com/dkuwcreator/Semantic-Architecture
-->

### Module Documentation Updates

For each impacted module from the Semantic Architecture Plan:

- [ ] TXXX [P] Update [Module 1 Path]/README.md:
  - Update responsibility description to reflect [new capabilities]
  - Add/modify usage examples for [new features]
  - Update invariants section if [behaviors changed]
  - Document new integration patterns

- [ ] TXXX [P] Update [Module 1 Path]/AGENT_INSTRUCTION.md:
  - Update allowed edits to include [new operations]
  - Update safety constraints for [new behaviors]
  - Add testing requirements for [new functionality]
  - Update boundary definitions if [scope changed]

- [ ] TXXX [P] Update [Module 2 Path]/README.md:
  - Update responsibility description
  - Add/modify usage examples
  - Document new dependencies

- [ ] TXXX [P] Update [Module 2 Path]/AGENT_INSTRUCTION.md:
  - Update allowed edits
  - Update safety constraints
  - Add testing requirements

### Cross-Module Documentation

- [ ] TXXX [P] Update API documentation in contracts/:
  - Sync OpenAPI/GraphQL schemas with implemented endpoints
  - Document new error responses
  - Update authentication/authorization requirements

- [ ] TXXX Update architecture diagrams (if module relationships changed):
  - Reflect new dependencies
  - Show updated data flows
  - Document interface contracts

- [ ] TXXX [P] Update semantic module index (if exists):
  - Add new modules if created
  - Update module responsibilities if changed
  - Document deprecated modules if removed

### Semantic Drift Verification

- [ ] TXXX Verify spec ↔ plan ↔ tasks ↔ code alignment:
  - Confirm all functional requirements implemented
  - Verify planned modules match actual changes
  - Ensure no undocumented cross-module dependencies
  - Check that declared semantic scope matches actual changes

- [ ] TXXX Meaning parity check:
  - Verify README.md describes actual behavior (not old/planned)
  - Verify AGENT_INSTRUCTION.md reflects actual boundaries
  - Confirm examples in docs work with current code
  - Check that invariants are still enforced

---

## Phase N+1: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] TXXX [P] Documentation updates in docs/
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Performance optimization across all stories
- [ ] TXXX [P] Additional unit tests (if requested) in tests/unit/
- [ ] TXXX Security hardening
- [ ] TXXX Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# Launch all models for User Story 1 together:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
