<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0
- Modified principles: All principles updated to reflect Phase II technology requirements
- Added sections: Technology Stack Constraints section detailing Phase I, II, and III boundaries
- Removed sections: None
- Templates requiring updates: N/A
- Follow-up TODOs: None
-->
# Todo Application Constitution

## Core Principles

### Phase-Appropriate Technology Stack
Use only approved technologies per phase: Phase I (in-memory console), Phase II (Python REST API, Neon PostgreSQL, Next.js, Better Auth), Phase III+ (AI/agents infrastructure)

### Backend Technology Standard
Phase II backend MUST use Python REST API with Neon Serverless PostgreSQL database and SQLModel or equivalent ORM for data layer

### Frontend Technology Standard
Phase II frontend MUST use Next.js (React, TypeScript) with Better Auth for authentication (signup/signin)

### Architecture Standards
Phase II applications MUST be full-stack web applications with clear separation between frontend and backend services

### Phase Isolation
Technologies and features are restricted by phase: Authentication allowed Phase II+, Web frontend allowed Phase II+, Neon PostgreSQL allowed Phase II+, AI/agent frameworks only Phase III+

### Dependency Management
All dependencies must align with approved technology stack per phase and be documented in project configuration files

## Technology Stack Constraints
Phase I: In-memory console application only. Phase II: Python REST API, Neon Serverless PostgreSQL, SQLModel ORM, Next.js frontend, Better Auth. Phase III+: Advanced cloud infrastructure, agents, AI, orchestration

## Development Workflow
Adhere to phase-appropriate technology constraints. No forward-phase technologies allowed until respective phase. Follow standard development practices with appropriate testing and documentation

## Governance
Constitution serves as authoritative technology policy. Amendments require explicit approval. Phase boundaries must be preserved. All PRs must verify compliance with current phase requirements

**Version**: 2.0.0 | **Ratified**: 2026-01-07 | **Last Amended**: 2026-01-07