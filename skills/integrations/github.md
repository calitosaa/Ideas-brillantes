---
name: github
description: Complete GitHub integration — repos, PRs, issues, Actions, releases via git CLI and API
---

# GitHub Integration

## Common Git Workflows
```bash
# Clone and setup
git clone https://github.com/user/repo && cd repo
git checkout -b feature/new-feature

# Commit with conventional commits
git add -p  # Interactive staging (review before commit)
git commit -m "feat(auth): add JWT token refresh endpoint"

# Types: feat, fix, docs, style, refactor, test, chore, perf

# Push and PR
git push -u origin feature/new-feature
# Then create PR via GitHub CLI or web
```

## Tool Call Patterns
```xml
<!-- Execute git command -->
<tool_call>{"name": "exec_command", "arguments": {
  "command": "git log --oneline -10",
  "cwd": "~/project"
}}</tool_call>

<!-- Search code in repo -->
<tool_call>{"name": "web_search", "arguments": {
  "query": "repo:owner/name function_name language:python"
}}</tool_call>
```

## PR Review Process (ruflo-inspired)
```
1. Checkout PR branch locally
2. Run tests: confirm they pass
3. Review diff with 9 dimensions:
   □ Architecture: does it fit the codebase structure?
   □ Logic: is the implementation correct?
   □ Security: OWASP issues? secrets exposed?
   □ Supply chain: new deps with CVEs?
   □ Performance: N+1 queries, blocking ops?
   □ Error handling: all edge cases covered?
   □ Test coverage: ≥80%? meaningful tests?
   □ Code quality: readable, documented?
   □ Breaking changes: backwards compatible?
4. Leave specific, actionable comments
5. Approve or Request Changes with clear reasoning
```

## GitHub Actions Patterns
```yaml
# .github/workflows/ci.yml — Standard CI pipeline
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff
      - run: ruff check .
```

## Release Management
```bash
# Semantic versioning tags
git tag -a v1.2.0 -m "Release v1.2.0 — adds automation features"
git push origin v1.2.0

# Generate changelog from commits
git log v1.1.0..v1.2.0 --oneline --no-merges
```

## Issue Triage
```
Labels utilizados:
  bug          → algo no funciona
  enhancement  → nueva funcionalidad
  help wanted  → necesita colaboración
  good first issue → ideal para nuevos contribuidores
  priority:high / priority:medium / priority:low
  blocked      → esperando algo externo
```
