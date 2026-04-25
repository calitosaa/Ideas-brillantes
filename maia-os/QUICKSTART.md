# 🚀 Inicio Rápido - Maia OS

## Construir e Instalar en 5 Minutos

### 1. Clonar y Preparar
```bash
git clone https://github.com/maia-os/maia-os.git
cd maia-os
sudo ./scripts/setup-build-env.sh
```

### 2. Construir ISO
```bash
./scripts/build-iso.sh
```

### 3. Grabar en USB
```bash
sudo dd if=output/maia-os-stable-x86_64.iso of=/dev/sdX bs=4M status=progress
```

### 4. Bootear e Instalar
- Reiniciar PC
- Boot desde USB
- Seguir asistente de instalación

### 5. ¡Disfrutar!
✅ Sistema completo con Material 3 Expressive
✅ Aplicaciones nativas M3E
✅ GNOME personalizado
✅ Flatpak + Snap preconfigurados

---

**Más info**: Ver [README.md](README.md) y [docs/INSTALACION.md](docs/INSTALACION.md)
