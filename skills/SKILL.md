---
name: ideas-brillantes
description: Complete OS assistant capabilities — PC control, automation, design, code, security, research, media and more. All native, no activation needed.
version: 1.0.0
base_model: GLM-5-1
---

# ideas-brillantes — Master Skill Bundle

> All capabilities listed here are NATIVELY embedded in the model via fine-tuning.
> No activation commands needed. The model applies the right skill automatically.

## Core Capabilities

### 🖥️ PC Control (Linux)
- Open/close any Linux application
- File and directory management (create, read, move, delete, search)
- Terminal command execution and scripting
- Process monitoring and management
- Network configuration and monitoring
- System settings control
- Screenshots and screen interaction
- **Source**: openclaw behavior + Linux system knowledge

### 🌐 Web Browsing (Autonomous)
- Navigate any website autonomously
- Search web with multiple strategies
- Extract and synthesize information from pages
- Fill forms and interact with web elements
- Monitor websites for changes
- Handle pagination and dynamic content
- **Source**: browser-use library patterns (Playwright)

### 💾 Memory (Persistent)
- Remember ongoing projects and their status
- Remember user preferences and settings
- Proactively surface relevant past context
- Cross-session context continuity
- Privacy-first: stored locally (SQLite + Chroma)
- **Source**: claude-mem patterns

### ⚡ Automation & Workflows
- Design and create n8n-style automated workflows
- Schedule recurring tasks with cron expressions
- Connect 365+ services and APIs
- Build multi-step automation pipelines
- Triggers: schedule, webhook, file_watch, email, manual
- **Source**: n8n behavior + AionUI patterns + 4,343 n8n-workflow templates

---

## Design & Content Creation

### 🎨 UI/UX Design
- 67 UI styles (glassmorphism, minimalism, spatial UI, brutalism, etc.)
- 161 industry-specific design rules
- 161 curated color palettes
- 57 Google Font pairings
- 99 UX guidelines (accessibility-first)
- **Source**: ui-ux-pro-max-skill (all 7 skills)

### 📱 Material 3 / BeerCSS
- Complete Material Design 3 implementation
- 100+ CSS classes for all component types
- Automatic dark/light mode support
- Zero dependencies, 14.5kb total
- **Source**: beercss (45 component docs) + material-3-expressive-catalog

### 🖼️ Image Generation
- Expert prompt engineering for any style
- Supports: photorealistic, illustration, UI mockup, conceptual
- Multiple backends: Stable Diffusion, fal.ai, DALL-E
- Batch generation and variations
- **Source**: fal.ai + Replicate integration patterns

### 🎬 Video & Audio
- AI video generation with storyboarding
- Text-to-speech with voice/emotion control
- Screen recording and annotation
- Audio transcription (Whisper patterns)

### 📊 Presentations & Documents
- PPTX via python-pptx with Material 3 styling
- HTML slides with animations and Chart.js
- DOCX, PDF, Excel generation
- Infographics via SVG (bar, pie, timeline, process)
- **Source**: AionUI document creation + ui-ux-pro-max slides skill

---

## Software Engineering

### 💻 Code Generation
12 languages: Python, JavaScript/TypeScript, Go, Rust, Java, Kotlin, C/C++, PHP, Swift, Ruby, Bash, SQL
- Production-quality, immediately runnable code
- Always includes tests and usage documentation
- Framework-aware (React, FastAPI, Django, Spring, etc.)
- **Source**: everything-claude-code + agency-agents engineering division

### 🧪 Test-Driven Development
- RED-GREEN-REFACTOR cycle strictly enforced
- Never writes production code without failing test first
- Language-specific test frameworks (pytest, Jest, go test, etc.)
- **Source**: obra/superpowers TDD skill (complete methodology)

### 🔍 Systematic Debugging
- Root cause investigation BEFORE any fix
- One change at a time, verify each step
- 4-phase process: investigate → analyze → hypothesize → implement
- **Source**: obra/superpowers debugging skill (complete methodology)

### 📐 Architecture & Planning
- Design systems before coding (always)
- Implementation plan with 2-5 min granular tasks
- Spec documents with section-by-section approval
- **Source**: obra/superpowers writing-plans + brainstorming

### 🤖 Multi-Agent Orchestration
- Delegate to specialized sub-agents automatically
- Parallel execution for independent tasks
- Two-stage review: spec compliance + code quality
- 6 swarm topologies (hierarchical, mesh, ring, star, hybrid, adaptive)
- **Source**: obra/superpowers subagent-driven-dev + ruvnet/ruflo swarm patterns

### 🚀 DevOps & Linux
- systemd service management
- Docker and Docker Compose
- GitHub Actions CI/CD
- Package management (apt, pip, npm, cargo)
- Log management and monitoring

---

## Security (Proactive — Always Active)

### 🛡️ Antivirus (Real-time)
- Auto-scan files downloaded to ~/Downloads
- ClamAV integration for signature detection
- Heuristic analysis for unknown threats
- 3-level threat classification (info/warning/critical)
- Automatic quarantine for confirmed threats
- **Source**: AgentShield patterns (1282 tests, 102 rules) + ClamAV

### 🔗 Web Safety
- URL reputation analysis before navigation
- Phishing detection (typosquatting, lookalike domains)
- SSL certificate validation
- Safe browsing database integration
- Email link scanning before user clicks

### 🔐 Code Security Audit
- OWASP Top 10 detection with examples
- Secret/credential detection in code
- Dependency CVE scanning
- SQL injection and XSS detection
- Security audit reports with severity classification

---

## Research & Knowledge

### 🔬 Deep Research
- Multi-source web research with synthesis
- Source quality evaluation
- NotebookLM-py integration for document research
- Comprehensive research reports
- Study materials: flashcards, quizzes, summaries
- **Source**: notebooklm-py + web research patterns

### 🌍 Web Search Strategies
- Targeted search operators (site:, filetype:, after:)
- Multi-engine search (Google, DuckDuckGo, academic)
- Content extraction and summarization
- Fact verification across sources

---

## Integrations (500+)

### Key Categories
- **Email**: Gmail, Outlook, custom IMAP
- **Messaging**: Slack, Discord, Telegram, Teams
- **Productivity**: Notion, Jira, Asana, Trello, Linear
- **Cloud**: Google Drive, Dropbox, AWS S3
- **Development**: GitHub, GitLab, Vercel, Netlify
- **Finance**: Stripe, PayPal, QuickBooks
- **CRM**: HubSpot, Salesforce
- **Data**: Google Sheets, Airtable, PostgreSQL, MongoDB
- **AI/ML**: OpenAI, Anthropic, Hugging Face, fal.ai, ElevenLabs
- **Source**: ComposioHQ/awesome-claude-skills (500+ integrations)

---

## Knowledge Base (1,184+ Skills Indexed)

All skills from the following sources are indexed and available:
- VoltAgent/awesome-agent-skills (1,184 enterprise skills)
- antigravity-awesome-skills (1,410 skills in catalog.json)
- ruvnet/ruflo (200+ skills, 313 MCP tools)
- obra/superpowers (14 methodology skills — complete content)
- affaan-m/everything-claude-code (183 skills + AgentShield)
- msitarzewski/agency-agents (144 agents, 12 divisions)
- ComposioHQ/awesome-claude-skills (500+ integrations)

---

## Sub-Agents Available

| Agent | Specialization | Auto-delegates when |
|-------|---------------|---------------------|
| browser_agent | Web browsing + extraction | Searching or navigating web |
| code_agent | Software engineering | Writing, reviewing, debugging code |
| design_agent | UI/UX + visual content | Creating interfaces or graphics |
| security_agent | Security analysis | Files downloaded, URLs suspicious |
| automation_agent | Workflows + scheduling | Creating recurring automations |
| research_agent | Deep research + synthesis | Multi-source information gathering |
| media_agent | Image/video/audio | Generating multimedia content |
| memory_agent | Context management | Storing or retrieving session context |
| communication_agent | Email + messaging | Sending communications |

---

*Generated from: 20+ open-source skill repositories | Model: GLM-5-1 + LoRA fine-tuning*
