# Skill: Native PC Linux Control

## Description and Purpose

This skill describes the native capability of Ideas-brillantes to control a Linux desktop and system environment directly. The model has been fine-tuned to understand Linux system architecture, common application paths, shell semantics, and GUI interaction patterns. This is not a plugin — it is embedded behavior that activates whenever the user asks to perform actions on their computer.

---

## When This Skill Applies

- User asks to open, close, or switch to an application ("open Firefox", "close the terminal", "switch to VS Code")
- User asks to manage files or directories ("move this file to Downloads", "create a folder called Projects")
- User asks about running processes or system resource usage
- User asks to configure network settings, check connectivity, or manage interfaces
- User asks to change system settings (display, sound, keyboard, locale)
- User asks to take a screenshot or inspect the screen
- User asks to run a shell command or script
- User asks to manage services ("start nginx", "enable ssh on boot")

---

## Core Behaviors

### 1. Application Management

The model knows the canonical binary names and `.desktop` entries for common Linux applications:

| Application | Binary / Command | Notes |
|---|---|---|
| Firefox | `firefox` | `--new-tab URL` to open URL |
| Chromium | `chromium-browser` or `chromium` | distro-dependent |
| VS Code | `code` | `code /path` to open folder |
| Nautilus (Files) | `nautilus` | `nautilus /path` to open folder |
| Terminal (GNOME) | `gnome-terminal` | |
| Terminal (KDE) | `konsole` | |
| Terminal (XFCE) | `xfce4-terminal` | |
| Text Editor | `gedit`, `kate`, `mousepad` | distro-dependent |
| Calculator | `gnome-calculator`, `kcalc` | |
| System Monitor | `gnome-system-monitor` | |
| VLC | `vlc` | |
| LibreOffice | `libreoffice --writer`, `--calc`, `--impress` | |
| Thunderbird | `thunderbird` | |
| GIMP | `gimp` | |
| Inkscape | `inkscape` | |

**Opening applications:**
```
Tool: exec_command
Command: "nohup firefox &"           # open in background
Command: "xdg-open /path/to/file"    # open with default app
Command: "gtk-launch app-name.desktop"
```

**Closing applications:**
```
Tool: exec_command
Command: "pkill -f firefox"          # by name
Command: "wmctrl -c 'Window Title'"  # by window title
Command: "xdotool search --name 'Firefox' windowclose"
```

**Listing open windows:**
```
Tool: exec_command
Command: "wmctrl -l"
Command: "xdotool search --onlyvisible --name ''"
```

---

### 2. File Management

**Via terminal (preferred for reliability):**
```
Tool: exec_command
Command: "ls -lah /home/user/Documents"
Command: "cp /source/file.txt /dest/"
Command: "mv /old/path /new/path"
Command: "rm -rf /path/to/dir"        # use with caution, always confirm
Command: "mkdir -p /path/to/new/dir"
Command: "find /home/user -name '*.pdf' -mtime -7"
Command: "du -sh /home/user/*"        # disk usage per folder
```

**Opening file manager at path:**
```
Tool: exec_command
Command: "nautilus /home/user/Downloads"
Command: "xdg-open /home/user/Documents"
```

**File permissions and ownership:**
```
Tool: exec_command
Command: "chmod +x /path/to/script.sh"
Command: "chown user:group /path/to/file"
Command: "ls -la /path"
```

**Searching file contents:**
```
Tool: exec_command
Command: "grep -r 'pattern' /path/to/dir"
Command: "find /home -name '*.conf' -exec grep -l 'keyword' {} \\;"
```

---

### 3. Process Management

**Listing processes:**
```
Tool: list_processes
# Returns: PID, name, CPU%, MEM%, command

Tool: exec_command
Command: "ps aux --sort=-%cpu | head -20"
Command: "pgrep -la firefox"
Command: "top -bn1 | head -20"
```

**Killing processes:**
```
Tool: exec_command
Command: "kill -15 <PID>"       # graceful (SIGTERM)
Command: "kill -9 <PID>"        # force (SIGKILL) — use only if SIGTERM fails
Command: "pkill -f 'process_name'"
Command: "killall firefox"
```

**Monitoring resources:**
```
Tool: exec_command
Command: "htop -d 5"            # snapshot
Command: "free -h"              # memory
Command: "df -h"                # disk
Command: "iostat -x 1 3"        # I/O stats
Command: "vmstat 1 5"           # virtual memory
```

---

### 4. Service Management (systemd)

```
Tool: exec_command
Command: "systemctl status nginx"
Command: "systemctl start nginx"
Command: "systemctl stop nginx"
Command: "systemctl restart nginx"
Command: "systemctl enable nginx"           # start on boot
Command: "systemctl disable nginx"
Command: "systemctl --user status syncthing"  # user services
Command: "journalctl -u nginx -n 50"         # service logs
Command: "systemctl list-units --type=service --state=running"
```

---

### 5. Network Management

**NetworkManager (nmcli):**
```
Tool: exec_command
Command: "nmcli device status"
Command: "nmcli connection show"
Command: "nmcli connection up 'NetworkName'"
Command: "nmcli connection down 'NetworkName'"
Command: "nmcli device wifi list"
Command: "nmcli device wifi connect 'SSID' password 'pass'"
Command: "nmcli radio wifi off"
```

**Network diagnostics:**
```
Tool: exec_command
Command: "ip addr show"
Command: "ip route show"
Command: "ping -c 4 8.8.8.8"
Command: "traceroute google.com"
Command: "ss -tulpn"                  # open ports (modern)
Command: "netstat -tulpn"             # open ports (legacy)
Command: "curl -I https://example.com"
Command: "nmap -sn 192.168.1.0/24"   # scan local network
```

---

### 6. System Settings Control

**GNOME Settings (dconf/gsettings):**
```
Tool: exec_command
Command: "gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'"
Command: "gsettings set org.gnome.desktop.sound event-sounds false"
Command: "gsettings set org.gnome.desktop.wm.preferences button-layout ':minimize,maximize,close'"
Command: "xrandr --output HDMI-1 --brightness 0.8"
Command: "pactl set-sink-volume @DEFAULT_SINK@ 70%"
Command: "pactl set-sink-mute @DEFAULT_SINK@ toggle"
```

**Display:**
```
Tool: exec_command
Command: "xrandr"                             # list displays
Command: "xrandr --output eDP-1 --mode 1920x1080 --rate 60"
Command: "arandr"                             # GUI display manager
```

**KDE Settings:**
```
Tool: exec_command
Command: "kwriteconfig5 --file kdeglobals --group KDE --key ColorScheme 'BreezeDark'"
Command: "qdbus org.kde.kglobalaccel /component/..."
```

---

### 7. Screenshot and Screen Interaction

**Taking screenshots:**
```
Tool: take_screenshot
# Returns: image path or base64 image data

Tool: exec_command
Command: "scrot /tmp/screenshot.png"                      # full screen
Command: "scrot -s /tmp/screenshot.png"                   # select region
Command: "gnome-screenshot -f /tmp/shot.png"
Command: "import -window root /tmp/shot.png"              # ImageMagick
Command: "grim /tmp/shot.png"                             # Wayland
Command: "grim -g '$(slurp)' /tmp/shot.png"              # Wayland region
```

**Mouse and keyboard automation:**
```
Tool: exec_command
Command: "xdotool mousemove 500 300"
Command: "xdotool click 1"                    # left click
Command: "xdotool type 'Hello World'"
Command: "xdotool key ctrl+c"
Command: "xdotool key super"                  # open app launcher
```

**Screen reading (OCR):**
```
Tool: exec_command
Command: "tesseract /tmp/screenshot.png stdout"
Command: "gocr /tmp/screenshot.png"
```

---

### 8. Tool Call Reference

| Tool | Purpose | Key Parameters |
|---|---|---|
| `exec_command` | Run any shell command | `command: string`, `timeout: int` |
| `list_processes` | Get running processes | `filter: string` (optional) |
| `open_app` | Launch application by name | `app_name: string` |
| `close_app` | Close application by name | `app_name: string`, `force: bool` |
| `take_screenshot` | Capture the screen | `region: [x,y,w,h]` (optional) |
| `read_file` | Read file contents | `path: string` |
| `write_file` | Write or overwrite a file | `path: string`, `content: string` |

---

## Examples

### Example 1: Open a project in VS Code
```
User: "Open the ~/Projects/myapp folder in VS Code"

Tool: open_app
  app_name: "code"
  args: "/home/user/Projects/myapp"

# Fallback if open_app not available:
Tool: exec_command
  command: "code /home/user/Projects/myapp"
```

### Example 2: Find and kill a frozen process
```
User: "Firefox is frozen, kill it"

Tool: list_processes
  filter: "firefox"
# → Returns PID 4821

Tool: exec_command
  command: "kill -15 4821"
# Wait 3s, check if still running

Tool: list_processes
  filter: "firefox"
# If still running:
Tool: exec_command
  command: "kill -9 4821"
```

### Example 3: Connect to Wi-Fi
```
User: "Connect to Wi-Fi network 'HomeNet'"

Tool: exec_command
  command: "nmcli device wifi list"
# → Shows available networks including HomeNet

Tool: exec_command
  command: "nmcli connection show | grep HomeNet"
# If known network:
Tool: exec_command
  command: "nmcli connection up 'HomeNet'"
# If new:
# Ask user for password, then:
Tool: exec_command
  command: "nmcli device wifi connect 'HomeNet' password 'user_provided_password'"
```

### Example 4: Check what's using port 8080
```
User: "Something is using port 8080, what is it?"

Tool: exec_command
  command: "ss -tulpn | grep :8080"
# → Returns PID and process name

Tool: exec_command
  command: "ps -p <PID> -o pid,ppid,cmd,%cpu,%mem"
```

### Example 5: Take screenshot and describe what's on screen
```
User: "What's currently on my screen?"

Tool: take_screenshot
# → Returns screenshot

# Model analyzes the screenshot visually and describes the contents
# to the user
```

---

## Linux-Specific Knowledge

- **XDG directories:** `$HOME/.config`, `$HOME/.local/share`, `$HOME/.cache`
- **Executable paths:** `/usr/bin`, `/usr/local/bin`, `/opt/`, `~/.local/bin`
- **Config files:** Usually in `~/.config/appname/` or `~/.appnamerc`
- **Logs:** `/var/log/`, `journalctl`, `~/.local/share/appname/logs`
- **Package managers:** `apt` (Debian/Ubuntu), `dnf` (Fedora), `pacman` (Arch), `zypper` (openSUSE)
- **Desktop environments:** GNOME, KDE Plasma, XFCE, Cinnamon — commands differ slightly
- **Display servers:** X11 (xdotool, xrandr) vs Wayland (wlr-randr, grim, ydotool)
- **PATH awareness:** Always check if a binary exists before running it: `which appname`
