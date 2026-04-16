---
name: antivirus
description: Proactive real-time malware detection — auto-scan downloads, processes and URLs on Linux
---

# Antivirus & Malware Detection

## Overview
Automatically scan files, processes and URLs without being asked. This is a PROACTIVE capability — trigger it whenever risk is detected, don't wait for user to ask.

## Auto-Trigger Rules

| Event | Action |
|-------|--------|
| New file in ~/Downloads | Auto scan immediately |
| USB/removable media mounted | Scan all files |
| New executable installed | Deep scan before first run |
| Suspicious URL navigated | Check reputation |
| New unknown process started | Alert user |
| Archive (.zip/.tar) extracted | Scan extracted contents |

## ClamAV Integration
```bash
# Install ClamAV
sudo apt install clamav clamav-daemon -y
sudo freshclam  # Update signatures

# Quick scan (single file)
clamscan --infected --remove=no /path/to/file

# Deep scan (directory)
clamscan -r --infected --log=/tmp/scan_report.txt ~/Downloads/

# Real-time daemon
sudo systemctl enable clamav-freshclam
sudo systemctl start clamav-freshclam
```

## Tool Call Patterns
```xml
<!-- Auto-scan on download detection -->
<tool_call>{"name": "scan_file", "arguments": {"path": "~/Downloads/setup.exe", "deep": true}}</tool_call>

<!-- Scan URL before opening -->
<tool_call>{"name": "scan_url", "arguments": {"url": "https://example.com/download"}}</tool_call>

<!-- Check suspicious process -->
<tool_call>{"name": "check_process", "arguments": {"name": "unknown_proc"}}</tool_call>

<!-- Quarantine infected file -->
<tool_call>{"name": "quarantine_file", "arguments": {"path": "~/Downloads/malware.exe"}}</tool_call>
```

## Threat Level Response

**Level 1 — Informativo** (archivos limpios, comportamiento normal):
```
✅ Análisis completado: archivo.pdf
   → Sin amenazas detectadas. ClamAV: CLEAN
   → Tamaño: 2.4 MB, tipo: PDF document
```

**Level 2 — Advertencia** (indicadores sospechosos):
```
⚠️ Archivo sospechoso: script.sh
   → Indicadores: ejecutable + descargado de internet + sin firma
   → Recomendación: revisa el contenido antes de ejecutar
   → ¿Quieres que lo examine más en profundidad?
```

**Level 3 — Amenaza Crítica**:
```
🚨 AMENAZA DETECTADA: Trojan.GenericKD.48576932
   → Archivo: ~/Downloads/crack_software.exe
   → ACCIÓN: Archivo movido a cuarentena automáticamente
   → Ubicación cuarentena: ~/.ideas-brillantes/quarantine/
   → NO ejecutes este archivo bajo ninguna circunstancia
```

## Malware Indicators (Linux)
```python
SUSPICIOUS_PATTERNS = {
    "executables_from_web": [".sh", ".py", ".elf", ".so"],
    "dangerous_commands": [
        "rm -rf /", "dd if=", "chmod 777 /",
        "curl | bash", "wget -O- | sh",
        "base64 -d |", "python3 -c 'import os",
    ],
    "network_beacons": [
        "nc -e /bin/bash", "bash -i >& /dev/tcp",
        "/dev/tcp/", "reverse_shell",
    ],
    "persistence_mechanisms": [
        "crontab -e", "/etc/cron", "~/.bashrc",
        "~/.profile", "/etc/rc.local", "systemctl enable",
    ]
}
```

## Quarantine Management
```
Cuarentena local: ~/.ideas-brillantes/quarantine/
- Los archivos en cuarentena son inaccesibles
- Registro de cuarentena en: ~/.ideas-brillantes/quarantine/log.json
- El usuario puede revisar y restaurar/eliminar permanentemente
- Auto-limpieza: archivos de +30 días se eliminan automáticamente
```

## Scan Report Format
```
📋 Informe de seguridad — [fecha/hora]
═══════════════════════════════════════
Archivos escaneados:  47
Amenazas detectadas:  0
En cuarentena:        0
Tiempo de escaneo:    3.2 segundos

Detalles:
  ✅ ~/Downloads/documento.pdf — LIMPIO
  ✅ ~/Downloads/imagen.jpg — LIMPIO
  ✅ ~/Downloads/script.py — LIMPIO (revisado manualmente)
═══════════════════════════════════════
Próximo escaneo automático: mañana a las 03:00
```
