# Skill: Workflow Automation

## Description and Purpose

This skill describes the native capability of Ideas-brillantes to design, create, and manage automated workflows. Inspired by n8n's node-based automation architecture, the model understands triggers, nodes, connections, and execution logic. The model can translate user descriptions into executable JSON workflow definitions, explain how workflows operate in plain language, and help debug or modify existing workflows.

---

## When This Skill Applies

- User wants to automate a repetitive task ("every morning, send me a summary of my emails")
- User describes a multi-step process that should run automatically
- User asks to set up a scheduled job or cron task
- User wants to connect two systems (e.g., "when a file appears in this folder, send it to email")
- User asks to build an event-driven automation pipeline
- User wants to monitor something and take action on change

---

## Core Concepts

### Triggers
A trigger is the event that starts a workflow. There is always exactly one trigger per workflow.

| Trigger Type | Description | Example |
|---|---|---|
| `schedule` | Cron-based timer | "Every Monday at 9am" |
| `webhook` | HTTP POST to a URL | "When my app sends a webhook" |
| `file_watch` | File/directory change | "When a new CSV appears in /data" |
| `email` | Incoming email matches filter | "When I receive email from boss@company.com" |
| `manual` | User-initiated execution | "Run this when I ask" |
| `api_poll` | Periodic check of an API | "Check this endpoint every 5 minutes" |

### Nodes
A node is a single unit of work. Nodes are connected sequentially or conditionally.

| Node Type | Description | Key Parameters |
|---|---|---|
| `exec_command` | Run a shell command | `command`, `cwd`, `timeout` |
| `send_email` | Send an email | `to`, `subject`, `body`, `attachments` |
| `web_request` | HTTP request | `url`, `method`, `headers`, `body` |
| `ai_process` | LLM processing | `prompt`, `model`, `input_var` |
| `filter` | Conditional branching | `condition`, `true_path`, `false_path` |
| `split` | Iterate over a list | `input_array`, `item_var` |
| `merge` | Join parallel branches | `strategy: all | first | any` |
| `notify` | Send notification | `channel: desktop|telegram|slack`, `message` |
| `read_file` | Read file contents | `path` |
| `write_file` | Write to file | `path`, `content`, `mode: write|append` |
| `transform` | Map/format data | `expression` |
| `delay` | Wait before next step | `seconds` |
| `set_variable` | Store a value | `name`, `value` |

### Connections
Nodes connect via named outputs:
- `success` → next node on success
- `failure` → error handling node
- `true` / `false` → filter branching
- `items` → split node output per item

---

## JSON Workflow Format

```json
{
  "id": "wf_unique_id",
  "name": "Human-readable workflow name",
  "description": "What this workflow does",
  "active": true,
  "trigger": {
    "type": "schedule | webhook | file_watch | email | manual | api_poll",
    "config": { ... }
  },
  "nodes": [
    {
      "id": "node_1",
      "name": "Human name for node",
      "type": "exec_command | send_email | web_request | ...",
      "config": { ... },
      "on_success": "node_2",
      "on_failure": "node_error"
    }
  ],
  "variables": {
    "VAR_NAME": "value"
  },
  "error_handler": "node_error"
}
```

---

## Cron Expression Guide

```
┌─ minute (0–59)
│  ┌─ hour (0–23)
│  │  ┌─ day of month (1–31)
│  │  │  ┌─ month (1–12)
│  │  │  │  ┌─ day of week (0–7, 0=Sun, 7=Sun)
│  │  │  │  │
*  *  *  *  *
```

| Description | Cron Expression |
|---|---|
| Every minute | `* * * * *` |
| Every 15 minutes | `*/15 * * * *` |
| Every hour | `0 * * * *` |
| Every day at midnight | `0 0 * * *` |
| Every day at 9am | `0 9 * * *` |
| Every Monday at 9am | `0 9 * * 1` |
| Weekdays at 8:30am | `30 8 * * 1-5` |
| First day of each month | `0 0 1 * *` |
| Every 6 hours | `0 */6 * * *` |
| Twice a day (9am, 6pm) | `0 9,18 * * *` |

---

## Common Workflow Patterns

### Pattern 1: Daily Report
```json
{
  "name": "Daily Morning Briefing",
  "trigger": { "type": "schedule", "config": { "cron": "0 8 * * 1-5" } },
  "nodes": [
    {
      "id": "fetch_weather",
      "type": "web_request",
      "config": { "url": "https://wttr.in/?format=3", "method": "GET" },
      "on_success": "fetch_news"
    },
    {
      "id": "fetch_news",
      "type": "web_request",
      "config": { "url": "https://newsapi.org/v2/top-headlines?country=us&apiKey={{NEWS_API_KEY}}" },
      "on_success": "summarize"
    },
    {
      "id": "summarize",
      "type": "ai_process",
      "config": {
        "prompt": "Summarize the top 5 news headlines briefly. Weather: {{fetch_weather.body}}. Headlines: {{fetch_news.body}}",
        "model": "default"
      },
      "on_success": "notify_user"
    },
    {
      "id": "notify_user",
      "type": "notify",
      "config": { "channel": "desktop", "message": "{{summarize.output}}", "title": "Morning Briefing" }
    }
  ]
}
```

### Pattern 2: File Watch + Process
```json
{
  "name": "Process new CSV files",
  "trigger": {
    "type": "file_watch",
    "config": { "path": "/home/user/incoming", "pattern": "*.csv", "event": "created" }
  },
  "nodes": [
    {
      "id": "process_file",
      "type": "exec_command",
      "config": { "command": "python3 /home/user/scripts/process_csv.py '{{trigger.file_path}}'" },
      "on_success": "notify_done",
      "on_failure": "notify_error"
    },
    {
      "id": "notify_done",
      "type": "notify",
      "config": { "channel": "desktop", "message": "Processed: {{trigger.file_name}}" }
    },
    {
      "id": "notify_error",
      "type": "notify",
      "config": { "channel": "desktop", "message": "Error processing {{trigger.file_name}}: {{error.message}}" }
    }
  ]
}
```

### Pattern 3: Conditional Branching
```json
{
  "name": "Email filter and forward",
  "trigger": {
    "type": "email",
    "config": { "filter": { "from": "*@important-client.com" } }
  },
  "nodes": [
    {
      "id": "check_urgency",
      "type": "filter",
      "config": { "condition": "{{trigger.subject}} contains 'URGENT'" },
      "on_true": "notify_immediately",
      "on_false": "save_to_folder"
    },
    {
      "id": "notify_immediately",
      "type": "notify",
      "config": {
        "channel": "desktop",
        "message": "URGENT email from {{trigger.from}}: {{trigger.subject}}",
        "priority": "high"
      }
    },
    {
      "id": "save_to_folder",
      "type": "exec_command",
      "config": { "command": "echo '{{trigger.subject}}' >> /home/user/client-emails.log" }
    }
  ]
}
```

---

## Designing a Workflow from User Description

When a user describes an automation, follow this process:

1. **Identify the trigger:** What event starts this? (time, file, email, manual, API event)
2. **List the steps:** What actions happen in sequence?
3. **Find decision points:** Are there conditions? ("only if X", "for each Y")
4. **Identify data flow:** What information passes between steps? Name the variables.
5. **Define error handling:** What should happen if a step fails?
6. **Generate the JSON:** Produce the complete workflow definition.
7. **Explain it back:** Describe what the workflow does in plain language before delivering the JSON.

**Explanation template:**
> "This workflow [trigger description]. When triggered, it will [step 1], then [step 2]. If [condition], it will [branch A], otherwise [branch B]. If anything fails, it will [error behavior]."

---

## Error Handling in Workflows

Every production workflow should have error handling:

```json
{
  "error_handler": "handle_error",
  "nodes": [
    ...
    {
      "id": "handle_error",
      "type": "notify",
      "config": {
        "channel": "desktop",
        "message": "Workflow '{{workflow.name}}' failed at node '{{error.node_id}}': {{error.message}}",
        "priority": "high"
      }
    }
  ]
}
```

**Error handling best practices:**
- Always define an `error_handler` node for production workflows
- Log errors to a file in addition to notifying
- For critical workflows, send errors to multiple channels
- Use `delay` + retry for transient failures (network, API rate limits)
- Test workflows with a `manual` trigger before enabling the real trigger

---

## Variable Interpolation

Variables are referenced with double-curly-brace syntax: `{{variable_name}}`

| Context | Syntax | Example |
|---|---|---|
| Trigger data | `{{trigger.field}}` | `{{trigger.file_path}}` |
| Node output | `{{node_id.field}}` | `{{fetch_news.body}}` |
| Workflow variables | `{{variables.NAME}}` | `{{variables.API_KEY}}` |
| Error context | `{{error.message}}` | `{{error.message}}` |
| Workflow metadata | `{{workflow.name}}` | `{{workflow.name}}` |
| Current time | `{{now}}` | `{{now.format('YYYY-MM-DD')}}` |

---

## Examples

### Example 1: Simple scheduled reminder
```
User: "Remind me every weekday at 9am to review my task list"

Workflow:
- Trigger: schedule, cron "0 9 * * 1-5"
- Node 1: notify → desktop notification "Time to review your task list!"

Plain English: "Every weekday morning at 9am, you'll get a desktop 
notification reminding you to review your task list."
```

### Example 2: Multi-step automation
```
User: "Every night at 11pm, back up my ~/Projects folder to ~/Backups 
       with a date-stamped filename"

Workflow:
- Trigger: schedule, cron "0 23 * * *"
- Node 1: exec_command → "tar -czf ~/Backups/projects-$(date +%Y%m%d).tar.gz ~/Projects"
- Node 2: notify → "Backup complete: projects-{{date}}.tar.gz"
- Error handler: notify → "Backup failed: {{error.message}}"
```

### Example 3: Webhook-triggered AI processing
```
User: "When my app sends a webhook with a support ticket, have the AI 
       categorize it and save to a CSV"

Workflow:
- Trigger: webhook (POST /hooks/tickets)
- Node 1: ai_process → "Categorize this support ticket: {{trigger.body.message}}. 
                         Reply with one of: billing, technical, account, other"
- Node 2: exec_command → "echo '{{trigger.body.id}},{{ai_process.output}},{{now}}' 
                           >> /home/user/tickets.csv"
- Node 3: web_request → POST back to app API with category
```
