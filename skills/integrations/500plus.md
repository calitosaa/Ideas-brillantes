---
name: integrations-500plus
description: Reference for 500+ service integrations — authentication patterns, common workflows and API usage
---

# 500+ Service Integrations (ComposioHQ-inspired)

## Categories & Top Integrations

### 📧 Email & Communication
| Service | Auth | Common Use |
|---------|------|-----------|
| Gmail | OAuth2 | Send/read/filter emails |
| Outlook | OAuth2 | Enterprise email management |
| Slack | OAuth2/Bot Token | Notifications, commands, channels |
| Discord | Bot Token | Server management, notifications |
| Telegram | Bot API | Personal automation, notifications |
| WhatsApp Business | API Key | Customer messaging |
| Twilio | API Key | SMS, voice calls |

### 📅 Productivity & Project Management
| Service | Auth | Common Use |
|---------|------|-----------|
| Notion | API Token | Notes, databases, wikis |
| Jira | API Token | Issue tracking, sprints |
| Asana | OAuth2 | Task management |
| ClickUp | API Key | Project management |
| Trello | API Key | Kanban boards |
| Linear | API Key | Engineering issue tracker |
| Monday.com | API Token | Team workflows |
| Google Calendar | OAuth2 | Events, scheduling |
| Calendly | API Key | Meeting scheduling |

### ☁️ Cloud & Storage
| Service | Auth | Common Use |
|---------|------|-----------|
| Google Drive | OAuth2 | File storage, sharing |
| Dropbox | OAuth2 | File sync, sharing |
| AWS S3 | Access Key + Secret | Object storage |
| OneDrive | OAuth2 | Microsoft file storage |
| Supabase | API Key | Postgres + Storage |

### 💻 Development
| Service | Auth | Common Use |
|---------|------|-----------|
| GitHub | Token/OAuth2 | Repos, PRs, Actions |
| GitLab | Personal Token | Self-hosted git |
| Bitbucket | App Password | Atlassian git |
| Vercel | Token | Deploy frontend |
| Netlify | Token | Deploy static sites |
| Docker Hub | Username/Token | Container registry |

### 💰 Finance & E-commerce
| Service | Auth | Common Use |
|---------|------|-----------|
| Stripe | Secret Key | Payments, subscriptions |
| PayPal | OAuth2 | Payment processing |
| Shopify | Admin Token | E-commerce management |
| QuickBooks | OAuth2 | Accounting |

### 📊 Data & Analytics
| Service | Auth | Common Use |
|---------|------|-----------|
| Google Sheets | OAuth2 | Spreadsheets, data storage |
| Airtable | API Key | Database + spreadsheet |
| HubSpot | API Key | CRM, marketing |
| Salesforce | OAuth2 | Enterprise CRM |
| Mixpanel | API Secret | Product analytics |
| PostHog | API Key | Open-source analytics |

### 🤖 AI & ML
| Service | Auth | Common Use |
|---------|------|-----------|
| OpenAI | API Key | GPT-4, DALL-E, Whisper |
| Anthropic | API Key | Claude API |
| Hugging Face | Token | Open models, inference |
| fal.ai | API Key | Image/video generation |
| ElevenLabs | API Key | TTS, voice cloning |
| Replicate | Token | Any ML model |

## Authentication Patterns

### OAuth2 (most common for user-facing apps)
```python
# Step 1: Redirect user to authorization URL
auth_url = f"{OAUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT}&scope={SCOPE}"

# Step 2: Exchange code for token
response = requests.post(TOKEN_URL, data={
    "grant_type": "authorization_code",
    "code": code,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
})
access_token = response.json()["access_token"]

# Step 3: Use token in requests
headers = {"Authorization": f"Bearer {access_token}"}
```

### API Key (simplest)
```python
# Store in environment variable, NEVER hardcode
import os
API_KEY = os.environ["SERVICE_API_KEY"]

headers = {"X-API-Key": API_KEY}
# or
headers = {"Authorization": f"Bearer {API_KEY}"}
```

## Common Integration Workflows

**Email → Slack notification:**
```
read_email(folder="INBOX", filter="unread") →
  filter(condition="from:important@client.com") →
  send_slack(channel="#alerts", message=email.subject)
```

**Form submission → CRM + Email:**
```
webhook(trigger="form_submit") →
  create_hubspot_contact(data=form_data) →
  send_email(to=form_data.email, template="welcome")
```

**New GitHub PR → Jira ticket:**
```
webhook(event="pull_request.opened") →
  create_jira_issue(
    title=pr.title,
    description=pr.body,
    labels=["review-needed"]
  )
```

## Rate Limiting
```python
import time
from functools import wraps

def rate_limited(calls_per_second=1):
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limited(calls_per_second=10)
def call_api(endpoint, data):
    return requests.post(endpoint, json=data)
```
