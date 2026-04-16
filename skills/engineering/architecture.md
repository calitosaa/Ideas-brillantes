# Skill: Software Architecture and Planning

## Description and Purpose

This skill describes the native software architecture and planning capability of Ideas-brillantes. The model has been fine-tuned to always design before coding, to decompose systems into well-defined components, and to produce precise implementation plans before a single line of production code is written. Architecture is not an optional step — it is the foundation that determines whether a system is buildable, maintainable, and correct.

---

## Core Principle: Design Before Code

> **Always design before coding. A system built without a plan is a system that will be rebuilt.**

The cost of changing an architecture after implementation is 10-100x the cost of changing it on paper. The model always produces at minimum:
1. A component diagram (described in text or ASCII)
2. A data model
3. An API contract (if applicable)
4. A sequenced implementation plan

This applies to tasks of any size, including "small" features that touch multiple files.

---

## When This Skill Applies

- User asks to build a new system, app, service, or feature
- User asks "how should I structure this?"
- User asks to plan an implementation before coding
- User asks to review an existing architecture
- User is starting a project and hasn't defined structure yet
- A task requires creating more than 2 new files

---

## System Decomposition

### Step 1: Identify Responsibilities

Start by listing everything the system must do, then group related responsibilities into components:

```
System: URL shortener service

Responsibilities:
- Accept a long URL and return a short code
- Redirect short code to the original URL
- Track click counts
- Expire links after N days
- Admin API to manage links

Components:
- API Layer (HTTP handlers)
- URL Service (business logic: generate codes, validate URLs)
- Storage Layer (read/write links)
- Redirect Handler (lookup and redirect)
- Expiry Job (background cleanup)
```

### Step 2: Define Component Interfaces

For each component, define its public interface before implementation:

```python
# URL Service interface
class URLService:
    def shorten(self, long_url: str, ttl_days: int = 30) -> ShortLink: ...
    def resolve(self, code: str) -> str: ...          # returns long_url or raises NotFound
    def get_stats(self, code: str) -> LinkStats: ...
    def delete(self, code: str) -> None: ...
```

### Step 3: Define Data Models

```python
@dataclass
class ShortLink:
    code: str               # 6-char alphanumeric
    long_url: str
    created_at: datetime
    expires_at: datetime
    click_count: int = 0

@dataclass
class LinkStats:
    code: str
    click_count: int
    last_accessed: datetime | None
    created_at: datetime
    expires_at: datetime
```

### Step 4: Define Dependencies

Draw the dependency graph — which component depends on which:

```
API Layer → URL Service → Storage Layer
              ↑
Redirect Handler
Expiry Job → Storage Layer
```

Rule: **Dependencies flow inward.** Outer layers depend on inner layers. Business logic (URL Service) does NOT depend on HTTP or database details — those are injected.

---

## Directory Structure Decisions

Structure follows responsibility. Common patterns:

### Feature-Based (recommended for larger apps)
```
src/
  features/
    auth/
      auth_router.py
      auth_service.py
      auth_models.py
      test_auth.py
    links/
      links_router.py
      links_service.py
      links_models.py
      test_links.py
  shared/
    database.py
    config.py
    exceptions.py
  main.py
```
**Use when:** Multiple features with clear boundaries, team separation possible.

### Layer-Based (simpler apps)
```
src/
  api/           # HTTP handlers/routes
  services/      # Business logic
  models/        # Data models
  repositories/  # Database access
  utils/         # Shared utilities
tests/
  unit/
  integration/
```
**Use when:** Small-to-medium app, single team, features are tightly integrated.

### Domain-Driven (complex domains)
```
src/
  domain/        # Core business entities and rules (no external deps)
  application/   # Use cases / commands / queries
  infrastructure/  # DB, email, external APIs
  interfaces/    # HTTP, CLI, GraphQL
```
**Use when:** Complex business rules, long-lived enterprise software.

### Rules for structure decisions:
- If a file would be needed in 3+ features → move to `shared/` or `utils/`
- Test files live next to the code they test, OR in a parallel `tests/` tree (be consistent)
- `__init__.py` files should be empty or contain only re-exports
- Configuration at the top level, not buried inside features

---

## API Design Principles

### REST API conventions:
```
Resource: /links

GET    /links          → list all links (paginated)
POST   /links          → create new link
GET    /links/{code}   → get link details
PUT    /links/{code}   → update link
DELETE /links/{code}   → delete link
GET    /links/{code}/stats → get click stats (sub-resource)
```

**URL rules:**
- Nouns, not verbs (`/links` not `/createLink`)
- Lowercase with hyphens (`/short-links` not `/shortLinks`)
- Plural for collections
- IDs in path, filters in query string

**Response conventions:**
```json
// Success (201 Created):
{
  "data": { "code": "abc123", "long_url": "...", "expires_at": "..." },
  "meta": { "created_at": "2025-01-15T10:30:00Z" }
}

// Error (400/404/500):
{
  "error": {
    "code": "INVALID_URL",
    "message": "The provided URL is not valid",
    "details": { "field": "long_url", "value": "not-a-url" }
  }
}
```

**Versioning:** Prefix with `/api/v1/` from the start. Adding versioning later is painful.

---

## Database Schema Design

**Principles:**
1. **Normalize first:** Eliminate redundancy before adding denormalization for performance
2. **Name things clearly:** `user_id` not `uid`, `created_at` not `ts`
3. **Every table gets:** `id` (PK), `created_at`, `updated_at`
4. **Soft deletes:** Use `deleted_at` column rather than `DELETE` when history matters
5. **Index thoughtfully:** Index columns used in WHERE, JOIN, and ORDER BY

**Example schema:**
```sql
CREATE TABLE short_links (
    id          SERIAL PRIMARY KEY,
    code        VARCHAR(10) NOT NULL UNIQUE,
    long_url    TEXT NOT NULL,
    created_by  INTEGER REFERENCES users(id),
    click_count INTEGER NOT NULL DEFAULT 0,
    expires_at  TIMESTAMPTZ,
    deleted_at  TIMESTAMPTZ,          -- soft delete
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_short_links_code ON short_links(code);
CREATE INDEX idx_short_links_expires ON short_links(expires_at) 
    WHERE deleted_at IS NULL;
```

---

## Implementation Plan Format

An implementation plan breaks a feature into a sequenced list of tasks, each small enough to complete in 2–5 minutes. Each task produces a verifiable deliverable.

### Task Granularity Rules:
- **2–5 minutes per task** at the code level
- Each task should be independently committable
- Tasks should have a clear definition of done
- Dependencies between tasks are explicitly stated
- Tests are tasks too — they appear BEFORE the code they test (TDD)

### Plan Format:
```markdown
# Implementation Plan: [Feature Name]

## Overview
[1-2 sentences describing what will be built]

## Components
- [Component 1]: [what it does]
- [Component 2]: [what it does]

## Tasks

### Phase 1: Data Layer
- [ ] Task 1.1: Create `ShortLink` dataclass with fields: code, long_url, created_at, expires_at, click_count
- [ ] Task 1.2: Write unit tests for ShortLink validation (valid URL, invalid URL, expired link)
- [ ] Task 1.3: Implement ShortLink.is_expired() method
- [ ] Task 1.4: Create `LinkRepository` interface (abstract class) with methods: save(), get_by_code(), delete()

### Phase 2: Service Layer
- [ ] Task 2.1: Write tests for URLService.shorten() — valid URL, invalid URL, duplicate code collision
- [ ] Task 2.2: Implement URLService.shorten() with random code generation
- [ ] Task 2.3: Write tests for URLService.resolve() — found, not found, expired
- [ ] Task 2.4: Implement URLService.resolve()

### Phase 3: API Layer
- [ ] Task 3.1: Define request/response schemas (Pydantic models)
- [ ] Task 3.2: Write integration tests for POST /links
- [ ] Task 3.3: Implement POST /links handler
- [ ] Task 3.4: Write integration tests for GET /{code} (redirect)
- [ ] Task 3.5: Implement redirect handler

### Phase 4: Infrastructure
- [ ] Task 4.1: Write SQLite-backed LinkRepository implementation
- [ ] Task 4.2: Wire up dependency injection in main.py
- [ ] Task 4.3: Add database migration script

## Verification
- All unit tests pass
- Integration tests pass against local server
- Manual test: shorten a URL, follow redirect, verify click count increments
```

---

## Spec Document Format

For larger features or new systems, produce a spec document before the implementation plan:

```markdown
# Spec: [System/Feature Name]

## Problem Statement
[What problem does this solve? Why does it need to be built?]

## Goals
- [Measurable goal 1]
- [Measurable goal 2]

## Non-Goals
- [Explicitly out of scope — prevents scope creep]

## Users / Actors
- [Who uses this system and how]

## Functional Requirements
1. The system SHALL [requirement]
2. The system SHALL [requirement]

## Non-Functional Requirements
- Performance: [e.g., "< 100ms p99 for redirect"]
- Scale: [e.g., "1000 requests/sec"]
- Availability: [e.g., "99.9% uptime"]

## Architecture
[Component diagram, data flow description]

## Data Model
[Schema or dataclass definitions]

## API Contract
[Endpoints, request/response shapes]

## Open Questions
- [Unresolved decision that needs input]

## Risks
- [What could go wrong, and mitigation]
```

---

## Examples

### Example 1: Designing a CLI tool
```
User: "I want to build a CLI tool that converts Markdown files to HTML"

Architecture response:

Components:
- CLI Parser: reads args (input file, output file, options)
- Markdown Parser: converts .md text to HTML
- File Handler: reads input file, writes output file
- Template Engine: wraps HTML in configurable template

Directory structure:
md2html/
  __init__.py
  cli.py          # argparse setup
  converter.py    # core markdown-to-HTML logic
  file_handler.py # read/write with error handling
  templates/
    default.html
tests/
  test_converter.py
  test_cli.py

Implementation plan: [10 tasks, 2-5 min each, tests first]
```

### Example 2: Reviewing a poorly-structured proposal
```
User: "I'll put all the database logic in the API handler"

Architecture response:
"That approach will cause problems as the codebase grows:
- Impossible to unit test business logic without a database
- If you add a second interface (CLI, websocket), you'll duplicate DB logic
- Schema changes require hunting through handler code

Better: 3-layer separation:
- Handler: validates input, calls service, formats response
- Service: business logic, orchestrates operations
- Repository: all database access

This adds ~5 minutes of setup but saves hours of refactoring later."
```
