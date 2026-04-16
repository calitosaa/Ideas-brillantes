# Skill: Multi-Agent Orchestration

## Description and Purpose

This skill describes the native multi-agent orchestration capability of Ideas-brillantes. The model can decompose complex tasks into parallel or sequential sub-tasks, delegate them to specialized sub-agents, integrate their results, and verify the final output. This behavior is embedded — the model knows when to delegate, how to write effective sub-agent task descriptions, and how to handle failures.

Orchestration is not used for small tasks. It is activated for systems that are too large or complex for a single context window, tasks with naturally parallel workstreams, and multi-step workflows where each step can be independently verified.

---

## When to Delegate vs Handle Directly

### Handle directly (single-agent) when:
- The entire task fits comfortably in one context window
- The task is a single coherent concern (write one function, review one file)
- Sub-tasks would be trivially small (< 5 minutes each)
- The task requires constant back-and-forth state that would be expensive to serialize
- The user asked for quick help, not a full system build

### Delegate (orchestrate) when:
- The task involves 3+ independent workstreams that could run in parallel
- The task produces multiple large artifacts (e.g., separate service, frontend, tests)
- A sub-task requires deep specialization (security audit, database design, API design)
- The full task would exceed one context window if handled linearly
- A review phase needs an independent perspective (fresh-context sub-agent for code review)
- Speed matters and parallel execution would significantly reduce wall time

---

## Creating Focused Sub-Agent Task Descriptions

A sub-agent task description must be **self-contained**: the sub-agent has no context from the orchestrator's session and cannot ask for clarification mid-task.

### Task description template:
```markdown
## Task: [Clear, specific name]

### Context
[Everything the sub-agent needs to know about the project, codebase, and 
decisions already made. Do not assume any shared memory.]

### Objective
[Single sentence: what this task produces]

### Requirements
1. [Specific requirement]
2. [Specific requirement]
...

### Constraints
- [What NOT to do]
- [Coding standards to follow]
- [Files NOT to modify]

### Inputs
- File: [path] → [what it contains]
- Variable: [name] → [value]

### Expected Output
- [Artifact 1]: [description, format, location]
- [Artifact 2]: [description, format, location]

### Verification
The task is complete when:
- [ ] [Verifiable criterion]
- [ ] [Verifiable criterion]
```

### What makes a bad task description:
- "Build the backend" — too vague, no scope
- "Continue working on the project" — requires shared context
- "Do what makes sense" — no verifiable outcome
- Tasks that require the sub-agent to make major architecture decisions (those belong to the orchestrator)

---

## Two-Stage Review Pattern

For any significant code generation, apply a two-stage review with independent sub-agents:

### Stage 1: Spec Compliance Review
**Goal:** Verify the generated code matches the original specification.
**Reviewer context:** Given the spec document and the generated code, nothing else.

```markdown
## Task: Spec Compliance Review

### Context
A sub-agent was given a spec to implement. Verify the implementation matches the spec.

### Inputs
- Spec: [attach full spec]
- Implementation: [attach all generated files]

### Check each requirement:
For each item in the spec's "Requirements" section:
1. Does the implementation fulfill it?
2. If not, what is missing or different?

### Output
A structured report:
- PASS: requirements fulfilled
- FAIL: requirements not fulfilled (with specific gaps)
- AMBIGUOUS: unclear whether requirement is met

Overall verdict: APPROVED | NEEDS_REVISION | REJECTED
```

### Stage 2: Code Quality Review
**Goal:** Review code quality independently of spec compliance.
**Reviewer context:** Given the code and project coding standards, nothing else.
**Use:** The 9-dimension code review skill (see `/skills/engineering/code-review.md`)

```markdown
## Task: Code Quality Review

### Context
Review the following code for quality issues. Apply the 9-dimension review framework.

### Code to review: [attach files]
### Project standards: [attach relevant standards]

### Output format:
[SEVERITY] Dimension: description
Affected: file.py:line_number
Issue: ...
Fix: ...
```

---

## Parallel Agent Execution

Tasks can run in parallel when they have no data dependency between them.

### Identify parallel tasks:
```
Task A: Write frontend component
Task B: Write backend API endpoint  
Task C: Write database migration

A, B, C can run in parallel — none depends on output from another.
All three need the data model spec (which the orchestrator provides to all).
```

### Dependency graph notation:
```
[Spec] → [Task A] → [Review A] → [Integrate]
       → [Task B] → [Review B] → [Integrate]
       → [Task C]              → [Integrate]
```

Sequential when:
- Task B requires Task A's output as input
- Task A writes to a file that Task B reads
- Task B tests code that Task A writes

### Parallel execution protocol:
```
Orchestrator:
1. Prepare complete context packages for each parallel task
2. Launch all parallel sub-agents simultaneously
3. Wait for ALL to complete
4. Collect outputs
5. Detect conflicts (e.g., two agents modified the same file)
6. Integrate outputs
7. Run verification phase
```

---

## Model Selection for Sub-Agents

Choose the sub-agent model based on task complexity and cost:

| Task Type | Model Tier | Examples |
|---|---|---|
| Simple, mechanical | Fast/small | Reformatting code, writing boilerplate, renaming, simple transforms |
| Standard development | Default | Feature implementation, unit tests, documentation |
| Complex reasoning | Full/large | Architecture decisions, security review, debugging complex systems |
| Review/critique | Full/large | Code review, spec compliance check, security audit |

**Rule:** Do not use expensive models for tasks that are purely mechanical. Do not use cheap models for tasks that require nuanced judgment.

---

## Handling Sub-Agent Failures

Sub-agents can fail in several ways:

### Failure Type 1: Task not completed
The sub-agent ran out of context, got stuck, or produced empty output.

**Response:**
1. Check if the task description was ambiguous — refine it
2. Decompose the task further (it may have been too large)
3. Retry with a clearer, more scoped task description
4. Handle the task directly if retry also fails

### Failure Type 2: Output doesn't meet requirements
The sub-agent produced output but it misses requirements or has critical bugs.

**Response:**
1. Run Stage 1 review to identify specific gaps
2. Create a targeted revision task: "Fix these specific issues: [list from review]"
3. Send revision task to a new sub-agent with the original output + issue list
4. Maximum 2 revision cycles before handling directly

### Failure Type 3: Output conflicts with other sub-agents
Two sub-agents modified the same file or made incompatible design decisions.

**Response:**
1. Do not merge conflicting outputs automatically
2. Analyze both outputs and identify the conflict
3. Make the integration decision as the orchestrator (authoritative)
4. If the conflict reveals an architecture issue, address it before integration

### Escalation threshold:
> **After 2 failed retries, handle the task directly rather than continuing to loop.**

---

## Integration and Verification of Sub-Agent Results

After collecting all sub-agent outputs:

### Integration checklist:
- [ ] All required files are present
- [ ] No duplicate/conflicting implementations of the same function
- [ ] Import paths are consistent between files from different agents
- [ ] Naming conventions are consistent (one agent may use camelCase, another snake_case)
- [ ] Tests reference the correct module paths
- [ ] No hardcoded paths or configuration that differs between agents

### Verification protocol:
```bash
# 1. Syntax check all new files
python -m py_compile src/**/*.py   # Python
npx tsc --noEmit                   # TypeScript

# 2. Run unit tests
pytest tests/unit/                 # Python
npm test                           # JS

# 3. Run integration tests
pytest tests/integration/

# 4. Check for obvious integration failures
python -c "from src.main import app"   # does it import?
```

### Verification sub-agent:
For large integrations, use a dedicated verification sub-agent:

```markdown
## Task: Integration Verification

### Context
Multiple sub-agents have produced code that has been assembled into a project.
Verify the integrated codebase is correct and functional.

### Files to verify: [list all new/modified files]

### Checks to perform:
1. Run: [test command] — should pass with 0 failures
2. Verify: all functions referenced in tests exist in source
3. Verify: no import errors (run: python -c "import src")
4. Check: no TODO or FIXME left by sub-agents in production code

### Output:
PASS: project integrates correctly
FAIL: [specific issues found with file:line references]
```

---

## Complete Orchestration Example

**Task:** Build a REST API for a bookmark manager

```
Orchestrator plan:

Phase 1 (parallel — all have full spec):
  Agent A: Implement data layer (BookmarkRepository + SQLite)
  Agent B: Implement service layer (BookmarkService business logic)
  Agent C: Write all unit tests (data layer + service layer)

Phase 2 (sequential — depends on Phase 1):
  Agent D: Implement API layer (FastAPI routes) using Phase 1 interfaces
  Agent E (parallel with D): Write integration tests for API

Phase 3: Integration
  Orchestrator: merge outputs, resolve conflicts, run tests

Phase 4 (parallel):
  Agent F: Stage 1 review (spec compliance)
  Agent G: Stage 2 review (code quality — 9 dimensions)

Phase 5: Fixes
  Orchestrator: apply critical and high findings
  Re-run tests to verify
```

**Task description to Agent A:**
```markdown
## Task: Implement SQLite Bookmark Repository

### Context
Building a bookmark manager REST API. You are implementing the data access layer only.
Do NOT implement business logic or HTTP handlers — those are handled by other agents.

### Data Model (already decided):
```python
@dataclass
class Bookmark:
    id: int
    url: str
    title: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
```

### Interface to implement:
```python
class BookmarkRepository(ABC):
    def save(self, bookmark: Bookmark) -> Bookmark: ...
    def get_by_id(self, id: int) -> Bookmark | None: ...
    def list_all(self, limit: int = 50, offset: int = 0) -> list[Bookmark]: ...
    def list_by_tag(self, tag: str) -> list[Bookmark]: ...
    def delete(self, id: int) -> bool: ...
```

### Requirements:
1. Implement SQLiteBookmarkRepository(BookmarkRepository)
2. Database file path passed via constructor
3. Auto-create table on first instantiation
4. Tags stored as comma-separated string in a TEXT column
5. All methods raise RepositoryError (custom exception) on DB errors

### File locations:
- src/repositories/base.py — write abstract base class here
- src/repositories/sqlite_repository.py — write implementation here
- src/repositories/exceptions.py — write RepositoryError here

### Do NOT:
- Import or reference Flask, FastAPI, or any HTTP framework
- Write tests (separate agent handles tests)
- Implement any business logic

### Verification:
Task complete when the files exist, import without error, and 
SQLiteBookmarkRepository passes a manual smoke test.
```
