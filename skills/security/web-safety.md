---
name: web-safety
description: Analyze URLs and web content for phishing, malware and suspicious behavior before interaction
---

# Web Safety — URL & Content Analysis

## Overview
Analyze URLs and web pages for threats BEFORE the user interacts with them. Proactively warn about suspicious links received in emails, chats, or documents.

## URL Analysis Checklist
```
1. Dominio
   □ ¿Imita una marca conocida? (paypa1.com vs paypal.com)
   □ ¿Dominio recién registrado? (<30 días = sospechoso)
   □ ¿TLD inusual para el servicio? (.xyz, .tk, .click para bancos)
   □ ¿Subdominios excesivos? (login.banco.attacker.com)

2. HTTPS/TLS
   □ ¿Usa HTTPS? (HTTP para login/pago = peligro)
   □ ¿Certificado válido y no expirado?
   □ ¿Coincide el dominio del certificado?

3. Contenido
   □ ¿Pide credenciales en página no oficial?
   □ ¿Urgencia artificial? ("Tu cuenta será eliminada en 24h")
   □ ¿Gramática/ortografía inusual?
   □ ¿Diseño que imita sitio conocido pero con diferencias?

4. Comportamiento
   □ ¿Redirige múltiples veces?
   □ ¿Descarga archivos automáticamente?
   □ ¿Intenta acceder a cámara/micrófono/localización?
   □ ¿Abre ventanas emergentes excesivas?
```

## Phishing Indicators
```python
PHISHING_SIGNALS = {
    "high_risk": [
        "login", "signin", "account", "verify", "secure",
        "update", "confirm", "password", "credential",
    ],
    "domain_tricks": [
        # Typosquatting
        "paypa1", "arnazon", "g00gle", "faceb00k",
        # Lookalike TLDs
        "paypal.com.phishing.site",
    ],
    "urgency_keywords": [
        "urgent", "immediate", "suspended", "locked",
        "verify now", "act now", "limited time",
        "urgente", "inmediato", "suspendida", "verificar ahora",
    ]
}
```

## Tool Call Pattern
```xml
<!-- Check URL before navigating -->
<tool_call>{"name": "scan_url", "arguments": {"url": "https://suspicious-link.com/login"}}</tool_call>
```

## Response Templates

**Safe URL:**
```
✅ URL analizada: https://github.com
   → Dominio: conocido y de confianza (GitHub Inc.)
   → SSL: válido, emitido hace 180 días
   → Reputación: sin historial de malware
   → Seguro para visitar
```

**Suspicious URL:**
```
⚠️ URL sospechosa: http://paypa1-secure.tk/login
   → SEÑALES DE ALERTA:
     • Imita PayPal pero con "1" en lugar de "l"
     • Sin HTTPS en página de login
     • Dominio .tk (historial de phishing)
     • Registrado hace 3 días
   → Recomendación: NO ingreses ningún dato
   → ¿Quieres reportar este sitio?
```

**Malware URL:**
```
🚨 URL peligrosa bloqueada: http://malware-host.ru/download.exe
   → Clasificación: Malware distributor (ClamAV DB)
   → Historial: reportado en 47 bases de datos de malware
   → ACCIÓN: Navegación bloqueada automáticamente
   → El archivo NO fue descargado
```

## Email Link Scanning
Al recibir emails con links, el modelo:
1. Extrae todas las URLs del email
2. Las analiza sin visitarlas (análisis de URL puro)
3. Muestra resumen de seguridad antes de que el usuario haga clic
4. Marca claramente los sospechosos con ⚠️ o 🚨
