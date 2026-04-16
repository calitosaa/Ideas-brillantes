# Skill: Persistent Memory Management

## Description and Purpose

This skill describes the native capability of Ideas-brillantes to manage long-term persistent memory across sessions. The system uses a two-layer storage backend: SQLite for structured metadata and fast keyword lookup, and a Chroma vector database for semantic similarity search. The model has been fine-tuned to know when to save, retrieve, update, and delete memories — and to surface relevant context proactively without being asked. Memory is not a plugin; it is embedded behavior.

---

## When This Skill Applies

### Save a memory when:
- A task is completed and the result may be useful later
- The user states a preference, habit, or personal rule ("I prefer dark mode", "always use TypeScript")
- A new project is started and its context should persist
- The user shares important personal or professional context
- A recurring pattern emerges that should be recalled next session
- The user explicitly asks to remember something

### Search memories when:
- Session starts and the user mentions a topic that may have prior context
- The user asks a question about something that could have been discussed before
- Before responding to a question about the user's preferences or past work
- When about to start a task that may duplicate prior effort
- The user says "like last time" or "as usual" or "remember when..."

### Do NOT save:
- Passwords, API keys, tokens, or credentials of any kind
- Sensitive personal information unless the user explicitly requests it (SSN, financial details)
- One-off ephemeral data with no future value
- Internal reasoning or scratchpad content

---

## Memory Lifecycle

### 1. Save
```
Tool: memory_save
  content: "User prefers Python over JavaScript for scripting tasks"
  category: "preferences"
  tags: ["language", "python", "scripting"]
  importance: "medium"    # low | medium | high | critical
```

```
Tool: memory_save
  content: "Project: TaskFlow — React + FastAPI app for task management. Repo at ~/Projects/taskflow. DB: PostgreSQL. Auth: JWT."
  category: "projects"
  tags: ["taskflow", "react", "fastapi", "postgresql"]
  importance: "high"
```

### 2. Retrieve (Semantic Search)
```
Tool: memory_search
  query: "user's preferred programming language"
  limit: 5
  min_relevance: 0.7      # 0.0–1.0 similarity threshold
```

```
Tool: memory_search
  query: "TaskFlow project details"
  category: "projects"   # optional category filter
  limit: 3
```

### 3. Keyword Lookup (Exact/Fast)
```
Tool: memory_get
  tags: ["taskflow"]
  category: "projects"
```

```
Tool: memory_get
  id: "mem_abc123"        # retrieve by ID
```

### 4. Update
```
Tool: memory_update
  id: "mem_abc123"
  content: "Project: TaskFlow — React + FastAPI. Now using Redis for caching. Deployed on VPS at 192.168.1.10."
  tags: ["taskflow", "react", "fastapi", "postgresql", "redis"]
```

### 5. Delete
```
Tool: memory_delete
  id: "mem_abc123"

Tool: memory_delete
  tags: ["temporary", "test"]    # delete by tag
  confirm: true
```

### 6. List
```
Tool: memory_list
  category: "projects"
  limit: 20
  sort: "importance_desc"

Tool: memory_list
  # all memories summary
```

---

## Category System

| Category | Contents | Examples |
|---|---|---|
| `projects` | Active and past projects | repo paths, tech stack, team, status |
| `preferences` | User habits and preferences | language, editor, style rules |
| `tasks` | Ongoing or recurring task context | reminders, deadlines, repeated workflows |
| `facts` | General knowledge about the user | profession, timezone, skills |
| `general` | Anything that doesn't fit above | miscellaneous useful context |

---

## Memory Entry Structure

A well-formed memory entry includes:

```json
{
  "id": "mem_unique_id",
  "content": "Clear, self-contained statement of the fact or context",
  "category": "projects | preferences | tasks | facts | general",
  "tags": ["relevant", "keyword", "tags"],
  "importance": "low | medium | high | critical",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z",
  "source": "user_statement | task_completion | inference"
}
```

**Writing good memory content:**
- Self-contained: the entry must make sense without other context
- Specific: "User uses 2-space indentation in Python" not "user has preferences"
- Current: update stale entries rather than creating duplicates
- Concise: 1–3 sentences maximum per entry

---

## Token-Efficient 3-Layer Retrieval Pattern

When answering a question that may benefit from memory, use this pattern to minimize token usage:

**Layer 1: Fast keyword check (nearly free)**
```
Tool: memory_get
  tags: ["relevant_topic"]
  limit: 3
```
If results found and sufficient → use them, skip layers 2 and 3.

**Layer 2: Semantic search (moderate cost)**
```
Tool: memory_search
  query: "natural language description of what I need"
  limit: 5
  min_relevance: 0.75
```
If results found → use them, skip layer 3.

**Layer 3: Broad category scan (last resort)**
```
Tool: memory_list
  category: "relevant_category"
  limit: 20
```
Manually filter results in context.

This layered approach avoids loading all memories into context when a fast lookup suffices.

---

## Proactive Memory Surfacing

The model should proactively recall memories without being asked when:

1. **Topic match at session start:** If the user's first message matches stored project/task context, open with a brief recall: "I remember we were working on TaskFlow — the React + FastAPI app. Want to continue from where we left off?"

2. **Preference application:** When generating code or content, silently apply stored preferences (indentation style, language choice) without announcing it every time unless the preference is unusual.

3. **Avoiding duplicate work:** If starting a task that looks like a prior task, check memory first and offer to reuse prior results.

4. **Recurring reminders:** If a task memory has a recurring flag and the time condition is met, surface it.

---

## Privacy Rules

- **NEVER save passwords, secrets, tokens, or credentials.** If the user asks you to remember a password, refuse and suggest using a password manager instead.
- Do not save credit card numbers, SSNs, or similar PII unless the user explicitly and clearly requests it.
- When in doubt, ask before saving sensitive-looking information.
- Memory contents should be treated as potentially visible to the user at any time — do not store internal model reasoning or confidential system information.

---

## Examples

### Example 1: Saving a preference
```
User: "From now on, always use tabs instead of spaces in my code."

Tool: memory_save
  content: "User prefers tabs (not spaces) for indentation in all code."
  category: "preferences"
  tags: ["indentation", "tabs", "code-style"]
  importance: "high"

Response: "Got it — I'll use tabs for indentation from now on."
```

### Example 2: Proactive recall at session start
```
User: "Let's continue working on the API."

Tool: memory_search
  query: "API project current status"
  limit: 5

# → Returns: "Project: PayAPI — FastAPI REST service. Last worked on: auth endpoints. Next: implement /transactions route."

Response: "Welcome back! Last time we were working on PayAPI — you'd just finished the auth endpoints. Ready to tackle the /transactions route?"
```

### Example 3: Updating stale project memory
```
# After completing migration task:

Tool: memory_get
  tags: ["payapi"]

# → Returns existing entry ID: mem_xyz789

Tool: memory_update
  id: "mem_xyz789"
  content: "Project: PayAPI — FastAPI REST service. Auth endpoints done. /transactions endpoint implemented. Next: add rate limiting and deploy."
  tags: ["payapi", "fastapi", "api"]
```

### Example 4: Refusing to save a credential
```
User: "Remember my database password: hunter2"

Response: "I won't store passwords in memory — that's a security risk. I'd recommend using a password manager like Bitwarden or KeePass. I can help you set one up if you'd like."
```

### Example 5: Session-start memory check
```
# At the start of every session with a topic-specific opener:

Tool: memory_search
  query: "[user's opening message topic]"
  limit: 3
  min_relevance: 0.8

# If relevant memories found → incorporate into response naturally
# If no relevant memories → proceed normally
```
