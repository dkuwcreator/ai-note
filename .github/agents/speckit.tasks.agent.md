---
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
handoffs: 
  - label: Analyze For Consistency
    agent: speckit.analyze
    prompt: Run a project analysis for consistency
    send: true
  - label: Implement Project
    agent: speckit.implement
    prompt: Start the implementation in phases
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Artifact Spaces (Semantic Architecture)

**IMPORTANT**: Understand the three artifact spaces before generating tasks:

1. **Design Space (Read-Only)**:
   - Contains: spec.md, plan.md, tasks.md, contracts/, data-model.md, research.md
   - Location: `FEATURE_DIR` from script output
   - **Purpose**: Describes WHAT to build (read to understand requirements)
   - **Rule**: Tasks do NOT modify files here (except tasks.md to mark complete)

2. **Build Space (Implementation Target)**:
   - Contains: Application code, tests, configuration
   - Location: Repository/application root
   - **Purpose**: The actual product being built
   - **Rule**: ALL implementation tasks create/modify files here
   - Structure: Defined in plan.md based on project type and organization

3. **Module Space (Co-located Meaning)**:
   - Contains: Module code + README.md + AGENT_INSTRUCTION.md together
   - Location: Within Build Space (organized per plan.md)
   - **Purpose**: Prevents semantic drift through proximity
   - **Rule**: Module documentation MUST be updated when module behavior changes

**Key Principle**: Design Space describes requirements. Build Space contains implementation. Module Space co-locates code with meaning.

**Note**: Semantic Architecture doesn't prescribe folder names like `src/` or `tests/`. These are examples of how projects commonly organize code when applying the principles. Your project structure is defined in plan.md based on your specific needs.

## Outline

1. **Setup**: Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract:
     - Tech stack, libraries, project structure
     - **Semantic Map**: clusters, modules, boundaries, dependencies
     - Agent scope requirements (Local/Cluster/System)
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - **Map user stories to semantic modules**: Which modules implement each story
   - If data-model.md exists: Extract entities and map to modules and stories
   - If contracts/ exists: Map endpoints to modules and stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story AND tagged by module (see Task Generation Rules below)
   - **For each module modified**: Generate module documentation update tasks
   - **Check for boundary violations**: Flag tasks that cross module boundaries
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization in Build Space)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - **CRITICAL**: Every task MUST include:
     - Task ID (T001, T002, etc.)
     - Module tag ([ModuleName]) - which semantic module this modifies
     - Story tag ([US1], [US2], etc.) - which user story this belongs to
     - File paths in Build Space (repository root), NOT Design Space
     - Module documentation update requirement (if behavior changes)
   - **Boundary Violation Checks**: Flag tasks that modify multiple modules (escalation needed)
   - **Phase N: Semantic Architecture Compliance** (REQUIRED - module doc updates)
   - Phase N+1: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - **CRITICAL**: File paths in tasks MUST target repository root (src/, tests/, etc.), NOT the specs folder
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: $ARGUMENTS

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Module] [Story?] Description with file path in Build Space
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Module] label**: REQUIRED for all implementation tasks
   - Format: [Auth], [Models], [API], [Services], etc.
   - Identifies which semantic module this task modifies
   - Enables module-scoped work and boundary violation detection
   - Setup phase: Use [Setup] or [Infrastructure]
5. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label  
   - User Story phases: MUST have story label
   - Polish phase: NO story label
6. **Description**: Clear action with exact file path in Build Space (NOT Design Space)
7. **Module Doc Flag**: Add "(update docs)" if task changes module behavior

**Examples**:

- ✅ CORRECT: `- [ ] T001 [Setup] Create project structure in Build Space per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] [Auth] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [Models] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [Services] [US1] Implement UserService in src/services/user_service.py (update docs)`
- ✅ CORRECT: `- [ ] T020 [P] [Models] [US1] Update src/models/README.md with User entity documentation`
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing Module label and file path)
- ❌ WRONG: `- [ ] T012 Create User model in src/models/user.py` (missing Task ID and Module label)
- ❌ WRONG: `- [ ] T012 [US1] Create model in specs/001-feature/models/user.py` (wrong space - Design Space not Build Space)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns
