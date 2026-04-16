---
name: automation-patterns
description: n8n-style workflow automation patterns, triggers, nodes and JSON format reference
---

# Automation Workflow Patterns (n8n-inspired)

## Workflow JSON Format
```json
{
  "name": "workflow-name",
  "description": "What this workflow does",
  "active": true,
  "trigger": {
    "type": "schedule|webhook|file_watch|email|manual",
    "config": {}
  },
  "nodes": [
    {
      "id": "node_1",
      "name": "Human readable name",
      "type": "node_type",
      "config": {},
      "next": "node_2",
      "on_error": "node_error_handler"
    }
  ],
  "created_at": "2025-04-16T00:00:00Z",
  "updated_at": "2025-04-16T00:00:00Z"
}
```

## Trigger Types

### Schedule (Cron)
```json
{
  "type": "schedule",
  "config": {
    "cron": "0 9 * * 1",
    "timezone": "Europe/Madrid"
  }
}
```

**Cron Expression Guide:**
```
┌─── minute (0-59)
│ ┌─── hour (0-23)
│ │ ┌─── day of month (1-31)
│ │ │ ┌─── month (1-12)
│ │ │ │ ┌─── day of week (0=Sun, 1=Mon, ... 6=Sat)
│ │ │ │ │
* * * * *

Ejemplos comunes:
  "0 9 * * 1"       = Lunes a las 9:00
  "0 8 * * 1-5"     = Lunes a viernes a las 8:00
  "*/15 * * * *"    = Cada 15 minutos
  "0 * * * *"       = Cada hora (en punto)
  "0 0 * * *"       = Cada día a medianoche
  "0 3 * * 0"       = Domingos a las 3:00
  "0 23 * * *"      = Cada noche a las 23:00
  "0 0 1 * *"       = Primer día de cada mes
```

### Webhook
```json
{
  "type": "webhook",
  "config": {
    "path": "/trigger/my-workflow",
    "method": "POST",
    "auth": "header",
    "auth_header": "X-Workflow-Token"
  }
}
```

### File Watch (inotify)
```json
{
  "type": "file_watch",
  "config": {
    "path": "~/Downloads",
    "events": ["create", "modify"],
    "pattern": "*",
    "recursive": false
  }
}
```

### Email Trigger
```json
{
  "type": "email",
  "config": {
    "folder": "INBOX",
    "filter": {
      "from": "boss@company.com",
      "subject_contains": "URGENT",
      "unread_only": true
    },
    "poll_interval": 60
  }
}
```

## Node Types

### exec_command
```json
{
  "type": "exec_command",
  "config": {
    "command": "du -sh ~/Downloads",
    "cwd": "~",
    "timeout": 30
  }
}
```

### read_email
```json
{
  "type": "read_email",
  "config": {
    "folder": "INBOX",
    "filter": "unread",
    "limit": 10,
    "mark_as_read": false
  }
}
```

### send_email
```json
{
  "type": "send_email",
  "config": {
    "to": ["{{trigger.from}}"],
    "subject": "Re: {{trigger.subject}}",
    "body": "{{ai_summary}}",
    "confirm_before_send": true
  }
}
```

### web_request (HTTP)
```json
{
  "type": "web_request",
  "config": {
    "url": "https://api.example.com/data",
    "method": "GET",
    "headers": {"Authorization": "Bearer {{env.API_KEY}}"},
    "output_var": "api_response"
  }
}
```

### ai_process (LLM transformation)
```json
{
  "type": "ai_process",
  "config": {
    "prompt": "Summarize these emails in bullet points:\n{{emails}}",
    "input_var": "emails",
    "output_var": "summary",
    "max_tokens": 500
  }
}
```

### filter (conditional)
```json
{
  "type": "filter",
  "config": {
    "conditions": [
      {"field": "{{file.size}}", "op": "gt", "value": 1048576}
    ],
    "logic": "AND",
    "next_if_true": "node_scan",
    "next_if_false": "node_skip"
  }
}
```

### scan_file
```json
{
  "type": "scan_file",
  "config": {
    "path": "{{trigger.file_path}}",
    "deep": true,
    "output_var": "scan_result"
  }
}
```

### send_notification
```json
{
  "type": "send_notification",
  "config": {
    "title": "Workflow: {{workflow.name}}",
    "message": "{{result_message}}",
    "urgency": "normal"
  }
}
```

### write_file
```json
{
  "type": "write_file",
  "config": {
    "path": "~/Reports/{{date}}_report.md",
    "content": "{{report_content}}",
    "mode": "create"
  }
}
```

## Variable Interpolation
```
{{trigger.xxx}}     → values from trigger event
{{node_id.output}}  → output from a previous node
{{env.VAR_NAME}}    → environment variable
{{date}}            → current date (YYYY-MM-DD)
{{datetime}}        → current datetime (ISO 8601)
{{workflow.name}}   → current workflow name
```

## Error Handling
```json
{
  "id": "error_handler",
  "name": "Notify on error",
  "type": "send_notification",
  "config": {
    "title": "⚠️ Workflow Error: {{workflow.name}}",
    "message": "Error en nodo {{error.node}}: {{error.message}}",
    "urgency": "high"
  }
}
```

## Translating Natural Language to Workflows

| User says | Trigger | Nodes |
|-----------|---------|-------|
| "Cada lunes a las 9am, envíame resumen de emails" | schedule: `0 9 * * 1` | read_email → ai_process (summarize) → send_notification |
| "Cuando descargue un archivo, escanearlo" | file_watch: ~/Downloads | scan_file → filter (if threat) → send_notification + quarantine |
| "Cada día a medianoche, hacer backup de ~/Docs" | schedule: `0 0 * * *` | exec_command (tar backup) → send_notification |
| "Si recibo email de mi jefe, notificarme en Slack" | email: from=boss | send_slack → send_notification |
| "Cada hora comprobar si mi web está online" | schedule: `0 * * * *` | web_request (GET url) → filter (status!=200) → send_notification |
