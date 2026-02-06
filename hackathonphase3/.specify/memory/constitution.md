<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: All principles and sections
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->

# AI-Powered Todo Chatbot Constitution

## Core Principles

### MCP Architecture Compliance
All components must follow Model Context Protocol (MCP) architecture standards; MCP tools must be stateless and persist data in database; Strict adherence to MCP specifications for interoperability.

### AI Logic Implementation
Use OpenAI Agents SDK for all AI logic; Implement clean, well-documented AI interaction patterns; Ensure AI responses are reliable and contextually appropriate.

### Statelessness Requirement (NON-NEGOTIABLE)
Server must be stateless; all conversation state must be stored in the database; No hardcoded secrets or environment variables; Clean separation of concerns between application logic and state management.

### Production-Ready Code Quality
Code must be clean, readable, and production-ready; Follow established coding standards; Include appropriate error handling and validation; Maintain high code coverage.

### Specification Adherence
Do not include unnecessary features outside the specification; Follow the given technology stack exactly; Implement only required functionality as specified.

### Database-First Design

All data persistence must utilize the database layer; Conversation state, user data, and todos stored in database; Proper data modeling and relationships maintained.

## Additional Technical Constraints
Technology stack requirements: MCP architecture, OpenAI Agents SDK, Database integration; Security standards: No hardcoded secrets, proper data validation; Performance standards: Efficient database queries, minimal memory footprint.

## Development Workflow
Code review requirements: All changes must pass peer review; Testing gates: Unit tests and integration tests required; Deployment approval process: Automated testing and manual verification required.

## Governance
Constitution supersedes all other practices; All development must comply with these principles; Changes require proper documentation and approval.

All PRs/reviews must verify compliance; Code complexity must be justified; Use project documentation for development guidance.

**Version**: 1.0.0 | **Ratified**: 2026-01-21 | **Last Amended**: 2026-01-21
