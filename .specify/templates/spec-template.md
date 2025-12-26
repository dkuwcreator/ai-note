# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## Semantic Scope *(Required)*

<!--
  CRITICAL: Define the semantic boundaries for this feature to enable safe Human-AI collaboration.
  This section enforces bounded context principles and prevents unintended cross-module changes.
  
  Reference: https://github.com/dkuwcreator/Semantic-Architecture
-->

### Modules In Scope

<!--
  List all Semantic Modules that WILL be modified by this feature.
  For each module, specify:
  - Module path/name
  - Current responsibility
  - How this feature affects it
-->

- **[Module 1 Path/Name]**:
  - **Responsibility**: [What this module does]
  - **Impact**: [How this feature changes it - e.g., "Add new endpoint", "Modify validation logic", "Extend data model"]

- **[Module 2 Path/Name]**:
  - **Responsibility**: [What this module does]
  - **Impact**: [How this feature changes it]

### Constitution Alignment

- Confirm `Local-First Storage` is followed: storage changes use SQLite and include migration notes.
- Confirm `Azure-Only AI` usage: list `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, and `AZURE_OPENAI_API_KEY` usage and note that public OpenAI endpoints are disallowed.
- Confirm `Privacy By Default`: ephemeral prompt handling and no default persistence of prompts/responses.
- Confirm `Security`: secrets loaded from environment or OS keychain; do not commit secrets.

### Modules Explicitly Out Of Scope

<!--
  List modules that this feature will NOT touch, especially if there might be ambiguity.
  This prevents scope creep and unintended changes.
-->

- **[Module Name]**: [Reason why out of scope - e.g., "Auth handled separately", "Not needed for MVP", "Deferred to Phase 2"]
- **[Module Name]**: [Reason]

### Cross-Module Impacts

<!--
  Document dependencies, compatibility requirements, and migration considerations.
  Leave empty if this is a single-module change.
-->

**Module Dependencies**:

- [Module A] depends on [Module B] for [specific capability]
- [New interface/contract between modules]

**Compatibility Requirements**:

- [Backward compatibility notes]
- [Breaking changes if any, with justification]

**Migration Notes**:

- [Required updates to dependent modules]
- [Data migration requirements]
- [Deployment sequencing if modules must be updated in order]

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]  
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
