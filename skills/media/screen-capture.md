# Screen Capture & Recording Skill

## Fuente
openclaw patterns (PC control), agency-agents (media), ruflo pc-control

---

## Captura de Pantalla

### scrot (Linux — CLI)
```bash
# Pantalla completa
scrot ~/Screenshots/screen_$(date +%Y%m%d_%H%M%S).png

# Con delay (para capturar menús)
scrot -d 3 screenshot.png

# Región interactiva (el usuario selecciona)
scrot -s region.png

# Ventana activa
scrot -u active_window.png

# Alta calidad (PNG por defecto, ya es lossless)
# Para JPEG:
scrot -q 95 screenshot.jpg
```

### gnome-screenshot
```bash
gnome-screenshot -f screenshot.png           # pantalla completa
gnome-screenshot -w -f window.png           # ventana activa
gnome-screenshot -a -f region.png           # región seleccionada
gnome-screenshot -d 5 -f delayed.png        # con delay 5s
```

### import (ImageMagick)
```bash
import -window root screenshot.png          # pantalla completa
import -window root -resize 50% small.png  # 50% resolución
```

### Python con pillow + python-xlib
```python
from PIL import ImageGrab  # solo en sistemas con Xvfb o Wayland
import subprocess
import os
from datetime import datetime
from pathlib import Path

def take_screenshot(output_dir: str = "~/Screenshots", 
                    quality: str = "high",
                    region: tuple = None) -> str:
    """Take screenshot and return file path."""
    
    output_dir = Path(output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = str(output_dir / f"screenshot_{timestamp}.png")
    
    if region:
        # Region: (x, y, width, height)
        x, y, w, h = region
        subprocess.run([
            "scrot", "-a", f"{x},{y},{w},{h}",
            output_path
        ], check=True)
    else:
        subprocess.run(["scrot", output_path], check=True)
    
    return output_path

def screenshot_window(window_name: str) -> str:
    """Screenshot a specific window by name."""
    output_path = f"/tmp/window_{window_name}.png"
    subprocess.run([
        "import", "-window", window_name, output_path
    ])
    return output_path
```

---

## Grabación de Pantalla

### FFmpeg (recomendado — mejor rendimiento)
```bash
# Grabar pantalla completa (X11)
ffmpeg -video_size 1920x1080 -framerate 30 \
    -f x11grab -i :0.0+0,0 \
    -c:v libx264 -preset ultrafast -crf 18 \
    ~/Videos/recording_$(date +%Y%m%d_%H%M%S).mp4

# Con audio del sistema
ffmpeg -video_size 1920x1080 -framerate 30 \
    -f x11grab -i :0.0+0,0 \
    -f pulse -ac 2 -i default \
    -c:v libx264 -preset ultrafast \
    -c:a aac -b:a 128k \
    recording_with_audio.mp4

# Con audio del micrófono
ffmpeg -video_size 1920x1080 -framerate 30 \
    -f x11grab -i :0.0+0,0 \
    -f pulse -ac 1 -i alsa_input.usb \
    -c:v libx264 -c:a aac \
    recording_mic.mp4

# Grabación de región específica
ffmpeg -video_size 800x600 -framerate 30 \
    -f x11grab -i :0.0+100,100 \
    region_recording.mp4

# Solo audio
ffmpeg -f pulse -ac 2 -i default \
    -c:a mp3 -b:a 192k \
    audio_only.mp3

# Grabar ventana específica (xdotool para obtener posición)
WIN_INFO=$(xdotool getactivewindow getwindowgeometry --shell)
eval "$WIN_INFO"
ffmpeg -video_size ${WIDTH}x${HEIGHT} -framerate 30 \
    -f x11grab -i :0.0+${X},${Y} \
    active_window.mp4

# Pantalla virtual (sin display físico, para headless)
Xvfb :99 -screen 0 1920x1080x24 &
DISPLAY=:99 ffmpeg -f x11grab -i :99 -r 30 recording.mp4
```

### Python: Control Programático de Grabación
```python
import subprocess
import signal
import os
from datetime import datetime
from pathlib import Path
import threading

class ScreenRecorder:
    def __init__(self, output_dir: str = "~/Videos"):
        self.output_dir = Path(output_dir).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._process = None
        self._recording = False

    def start(self, 
              resolution: str = "1920x1080",
              fps: int = 30,
              include_audio: bool = False,
              region: tuple = None) -> str:
        """Start recording. Returns output file path."""
        
        if self._recording:
            raise RuntimeError("Already recording")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = str(self.output_dir / f"recording_{timestamp}.mp4")
        
        # Build ffmpeg command
        display = ":0.0"
        if region:
            x, y, w, h = region
            display = f":0.0+{x},{y}"
            resolution = f"{w}x{h}"
        
        cmd = [
            "ffmpeg", "-y",
            "-video_size", resolution,
            "-framerate", str(fps),
            "-f", "x11grab",
            "-i", display,
        ]
        
        if include_audio:
            cmd += ["-f", "pulse", "-ac", "2", "-i", "default"]
            cmd += ["-c:a", "aac", "-b:a", "128k"]
        
        cmd += [
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "18",
            output_path
        ]
        
        self._process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        self._recording = True
        self._output_path = output_path
        return output_path

    def stop(self) -> str:
        """Stop recording and return file path."""
        if not self._recording:
            raise RuntimeError("Not recording")
        
        self._process.stdin.write(b'q')
        self._process.stdin.flush()
        self._process.wait(timeout=10)
        self._recording = False
        return self._output_path

    @property
    def is_recording(self) -> bool:
        return self._recording
```

---

## Creación de GIFs desde Pantalla

```bash
# Captura → GIF de alta calidad
ffmpeg -video_size 800x600 -framerate 15 \
    -f x11grab -i :0.0+0,0 \
    -t 10 \
    -vf "fps=15,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
    -loop 0 demo.gif

# Convertir video existente a GIF
ffmpeg -i recording.mp4 \
    -vf "fps=10,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse=dither=bayer" \
    -loop 0 output.gif

# GIF optimizado con gifsicle
gifsicle -O3 --colors 256 input.gif > optimized.gif
```

---

## Anotación de Capturas

```python
from PIL import Image, ImageDraw, ImageFont

def annotate_screenshot(image_path: str, annotations: list, output_path: str = None):
    """
    Add arrows, circles, and text to screenshots.
    
    annotations: [
        {"type": "circle", "x": 100, "y": 200, "radius": 30, "color": "red"},
        {"type": "arrow", "from": (100, 100), "to": (300, 200), "color": "blue"},
        {"type": "text", "x": 50, "y": 50, "text": "Click here!", "color": "red", "size": 24},
        {"type": "rectangle", "x1": 100, "y1": 100, "x2": 300, "y2": 200, "color": "yellow"}
    ]
    """
    img = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for ann in annotations:
        t = ann.get("type")
        color = ann.get("color", "red")
        
        if t == "circle":
            x, y, r = ann["x"], ann["y"], ann.get("radius", 25)
            draw.ellipse([x-r, y-r, x+r, y+r], outline=color, width=3)
        
        elif t == "rectangle":
            draw.rectangle([ann["x1"], ann["y1"], ann["x2"], ann["y2"]],
                           outline=color, width=3)
        
        elif t == "text":
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 
                                         ann.get("size", 20))
            except:
                font = ImageFont.load_default()
            # Shadow
            draw.text((ann["x"]+2, ann["y"]+2), ann["text"], font=font, fill="black")
            draw.text((ann["x"], ann["y"]), ann["text"], font=font, fill=color)
    
    result = Image.alpha_composite(img, overlay).convert("RGB")
    
    if output_path is None:
        output_path = image_path.replace(".png", "_annotated.png")
    
    result.save(output_path)
    return output_path
```

---

## OCR (Extraer texto de imágenes/pantallas)

```bash
# tesseract
sudo apt install tesseract-ocr tesseract-ocr-spa  # español
tesseract screenshot.png output -l spa            # español
tesseract screenshot.png output -l eng+spa        # multi-idioma
```

```python
import pytesseract
from PIL import Image

def extract_text_from_screenshot(image_path: str, lang: str = "spa+eng") -> str:
    """Extract text from screenshot using OCR."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang=lang)
    return text.strip()

def screenshot_and_extract(region=None) -> str:
    """Take screenshot and extract text in one step."""
    screenshot_path = take_screenshot(region=region)
    return extract_text_from_screenshot(screenshot_path)
```
