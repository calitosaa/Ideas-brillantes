---
name: code-audit
description: Security audit code for OWASP Top 10, secrets, vulnerable dependencies and logic flaws
---

# Code Security Audit — AgentShield-inspired

## Overview
Audit any code for security vulnerabilities before execution or deployment. Apply automatically when user asks to run code they didn't write or before deploying to production.

## OWASP Top 10 — Quick Reference

### A01 — Broken Access Control
```python
# ❌ BAD: No authorization check
def get_user_data(user_id):
    return db.query(f"SELECT * FROM users WHERE id={user_id}")

# ✅ GOOD: Check ownership
def get_user_data(user_id, current_user):
    if current_user.id != user_id and not current_user.is_admin:
        raise PermissionError("Access denied")
    return db.query("SELECT * FROM users WHERE id=?", [user_id])
```

### A02 — Cryptographic Failures
```python
# ❌ BAD: MD5 for passwords, hardcoded key
password_hash = md5(password)
SECRET_KEY = "mysecretkey123"

# ✅ GOOD: bcrypt, env vars
from bcrypt import hashpw, gensalt
import os
password_hash = hashpw(password.encode(), gensalt())
SECRET_KEY = os.environ["SECRET_KEY"]
```

### A03 — SQL Injection
```python
# ❌ BAD: String formatting
query = f"SELECT * FROM users WHERE name='{username}'"

# ✅ GOOD: Parameterized
query = "SELECT * FROM users WHERE name=?"
cursor.execute(query, [username])
```

### A07 — XSS (Cross-Site Scripting)
```javascript
// ❌ BAD: innerHTML with user data
element.innerHTML = userInput;

// ✅ GOOD: textContent or sanitize
element.textContent = userInput;
// Or: DOMPurify.sanitize(userInput)
```

### A09 — Security Logging Failures
```python
# ❌ BAD: No logging of security events
def login(username, password):
    if auth_failed:
        return {"error": "wrong password"}

# ✅ GOOD: Log all security events
import logging
def login(username, password):
    if auth_failed:
        logging.warning(f"Failed login attempt for {username} from {ip}")
        return {"error": "wrong password"}
```

## Secret Detection Patterns
```python
SECRET_PATTERNS = [
    r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[\w\-]{20,}',
    r'(?i)(password|passwd|pwd)\s*[=:]\s*["\'][^"\']{6,}',
    r'(?i)(secret|token)\s*[=:]\s*["\'][\w\-]{10,}',
    r'(?i)aws[_-]?(access[_-]?key|secret)[_-]?id\s*[=:]',
    r'ssh-rsa AAAA[0-9A-Za-z+/]+',
    r'-----BEGIN (RSA |EC )?PRIVATE KEY-----',
    r'(?i)bearer [A-Za-z0-9\-._~+/]+=*',
]
```

## Audit Report Format
```
🔍 AUDITORÍA DE SEGURIDAD
═══════════════════════════
Archivo: app.py (247 líneas)
Fecha: 2025-04-16

CRÍTICO (bloquea despliegue):
  [L.47] SQL Injection — input directo en query
  [L.112] Credenciales hardcodeadas: API_KEY="sk-..."

ALTO:
  [L.89] Sin validación de input en endpoint /upload
  [L.203] Contraseñas sin hash (texto plano en DB)

MEDIO:
  [L.34] Sin rate limiting en endpoint de login
  [L.167] Logs exponen datos sensibles de usuario

BAJO:
  [L.5] Dependencia desactualizada: requests==2.25.0 (CVE-2023-32681)

RESUMEN: 2 críticos, 2 altos, 2 medios, 1 bajo
RECOMENDACIÓN: No desplegar hasta resolver los críticos
═══════════════════════════
```

## Auto-Audit Triggers
- Antes de ejecutar scripts descargados de internet
- Al revisar PRs o commits con cambios de seguridad
- Al añadir nuevas dependencias (buscar CVEs)
- Al crear endpoints de API
- Al implementar autenticación
