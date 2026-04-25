# Guia de Instalación de Maia OS

## Introducción

Esta guía te ayudará a instalar **Maia OS**, una distribución de Linux completa basada en Debian 12 con Material 3 Expressive.

---

## Paso 1: Descargar la ISO

### Opción A: ISO Pre-construida (Recomendado)

```bash
# Descargar desde el sitio oficial
wget https://releases.maia-os.org/v1.0/maia-os-1.0-stable-x86_64.iso

# Verificar integridad del archivo
sha256sum maia-os-1.0-stable-x86_64.iso

# El hash debe coincidir con el publicado en releases.maia-os.org
```

### Opción B: Construir tu Propia ISO

```bash
# Clonar repositorio
git clone https://github.com/maia-os/maia-os.git
cd maia-os

# Configurar entorno de construcción
sudo ./scripts/setup-build-env.sh

# Construir ISO
./scripts/build-iso.sh --variant stable

# La ISO estará en: output/maia-os-stable-x86_64.iso
```

---

## Paso 2: Crear USB Booteable

### Método 1: Usando `dd` (Linux/Mac)

```bash
# Identificar tu USB
lsblk

# Grabar ISO (REEMPLAZA sdX con tu dispositivo, ej: sdb)
sudo dd if=maia-os-1.0-stable-x86_64.iso of=/dev/sdX bs=4M status=progress

# Sincronizar y expulsar
sync
sudo eject /dev/sdX
```

### Método 2: BalenaEtcher (Windows/Mac/Linux)

1. Descargar BalenaEtcher desde https://www.balena.io/etcher/
2. Abrir Etcher
3. Seleccionar "Flash from file" y elegir la ISO de Maia OS
4. Seleccionar tu unidad USB
5. Click en "Flash!"

### Método 3: Ventoy (Multi-ISO)

1. Instalar Ventoy en tu USB
2. Copiar la ISO de Maia OS al USB
3. Bootear y seleccionar Maia OS del menú

---

## Paso 3: Arrancar desde USB

1. **Insertar el USB** en tu PC
2. **Reiniciar** el equipo
3. **Entrar a la BIOS/UEFI** (generalmente F2, F12, Del, o Esc durante el boot)
4. **Deshabilitar Secure Boot** (opcional pero recomendado)
5. **Cambiar orden de boot** para que USB sea primero
6. **Guardar cambios** y reiniciar

---

## Paso 4: Probar Maia OS (Live Session)

Al arrancar verás el menú GRUB con tema Material 3:

```
╔══════════════════════════════════════╗
║           Maia OS v1.0               ║
║                                      ║
║  ▶ Iniciar Maia OS                   ║
║    Modo seguro                       ║
║    Memtest86+                        ║
╚══════════════════════════════════════╝
```

Selecciona **"Iniciar Maia OS"** para probar el sistema sin instalar.

### Características de la Live Session:

- ✅ Sistema completo funcional
- ✅ Navegador web Firefox
- ✅ Gestor de archivos Maia Files
- ✅ Terminal
- ✅ Acceso a internet
- ✅ Prueba de hardware compatible

---

## Paso 5: Instalación en Disco Duro

### Desde el Escritorio Live:

1. **Doble click** en el icono "Instalar Maia OS"
2. **Seleccionar idioma** (Español recomendado)
3. **Configurar teclado** (Layout español por defecto)
4. **Elegir tipo de instalación**:

   | Opción | Descripción |
   |--------|-------------|
   | **Borrar disco e instalar** | Instala Maia OS ocupando todo el disco |
   | **Instalar junto a otro SO** | Dual-boot con Windows/otro Linux |
   | **Más opciones** | Particionado manual avanzado |

5. **Seleccionar ubicación** (zona horaria)
6. **Crear usuario**:
   - Nombre: Tu nombre
   - Nombre de usuario: tu_usuario
   - Contraseña: (mínimo 8 caracteres)
   
7. **Comenzar instalación** (durará 15-30 minutos)

### Esquema de Particionado Automático

El instalador creará:

| Partición | Tamaño | Tipo | Uso |
|-----------|--------|------|-----|
| `/boot/efi` | 512 MB | FAT32 | Boot UEFI |
| `/boot` | 1 GB | ext4 | Kernel |
| `/` | 40 GB | btrfs | Sistema |
| `/home` | Resto | btrfs | Datos usuario |
| `swap` | 8 GB | swap | Memoria virtual |

---

## Paso 6: Primer Boot

Después de la instalación:

1. **Retirar USB** cuando se solicite
2. **Presionar Enter** para reiniciar
3. **Ver GRUB** con Maia OS como opción principal
4. **Ingresar credenciales** de tu usuario

### Primer Inicio - Asistente de Bienvenida

Al primer boot verás el asistente de configuración:

- [ ] Actualizar sistema (recomendado)
- [ ] Instalar codecs multimedia
- [ ] Configurar impresoras
- [ ] Habilitar servicios adicionales
- [ ] Importar datos de otro SO

---

## Paso 7: Post-Instalación

### Actualizar Sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### Instalar Aplicaciones Adicionales

```bash
# Flatpaks recomendados
flatpak install flathub org.telegram.desktop
flatpak install flathub com.discordapp.Discord
flatpak install flathub com.spotify.Client

# Snap packages
sudo snap install code --classic
sudo snap install telegram-desktop
```

### Configurar Tema Material 3

El tema M3E viene preinstalado. Para personalizar:

```bash
# Cambiar entre modo claro/oscuro
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'

# Cambiar colores del tema
nano ~/.config/gtk-4.0/gtk.css
```

---

## Solución de Problemas

### No Arranca desde USB

- Verificar que el USB esté bien grabado
- Probar con otro puerto USB (preferiblemente USB 2.0)
- Deshabilitar Secure Boot en BIOS
- Verificar modo UEFI vs Legacy

### Pantalla Negra al Boot

- En GRUB, presionar `e` para editar opciones
- Añadir `nomodeset` al final de la línea `linux`
- Presionar F10 para bootear
- Una vez instalado, instalar drivers propietarios

### WiFi No Funciona

```bash
# Instalar firmware adicional
sudo apt install firmware-linux firmware-realtek firmware-iwlwifi

# Reiniciar
sudo reboot
```

### Dual-Boot con Windows

1. **Desactivar Fast Startup** en Windows
2. **Reducir partición** de Windows desde Administración de Discos
3. **Instalar Maia OS** en espacio libre
4. **GRUB detectará** Windows automáticamente

---

## Comandos Útiles

### Gestión de Paquetes

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar aplicación
sudo apt install nombre_paquete

# Buscar paquete
apt search palabra_clave

# Limpiar caché
sudo apt clean
```

### Sistema

```bash
# Ver información del sistema
neofetch

# Ver logs del sistema
journalctl -xe

# Reiniciar servicios
sudo systemctl restart servicio

# Ver uso de disco
df -h
```

---

## Soporte y Comunidad

Si tienes problemas:

- 📚 **Documentación**: https://docs.maia-os.org
- 💬 **Foro**: https://forum.maia-os.org
- 🐛 **Reportar bugs**: https://github.com/maia-os/bugs
- 💬 **Telegram**: https://t.me/maiaos
- 🎮 **Discord**: https://discord.gg/maiaos

---

## ¡Disfruta Maia OS!

Has completado la instalación. Ahora puedes:

✅ Navegar con Firefox  
✅ Gestionar archivos con Maia Files  
✅ Personalizar con Material 3 Expressive  
✅ Instalar apps desde Maia Store  
✅ Disfrutar de animaciones fluidas  

**Bienvenido/a a Maia OS** - *La esencia de Android, el poder de Linux*
