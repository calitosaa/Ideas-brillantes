# Video Generation Skill

## Fuente
agency-agents (media division), VoltAgent/awesome-agent-skills (video/media), ruflo media tools

---

## Pipeline de Generación de Video

### Pipeline Completo: Texto → Video
```
Input (tema/prompt)
    ↓
1. Script Generation (AI)
    ↓
2. Scene Planning (AI → estructura temporal)
    ↓
3. Visual Generation (imagen por escena)
    ↓
4. Audio Generation (TTS narración)
    ↓
5. Music/SFX (opcional)
    ↓
6. Assembly (ffmpeg)
    ↓
Output (MP4)
```

---

## Herramientas por Tarea

### Generación de Video IA
```python
# Usando fal.ai para video generativo
import fal_client

result = fal_client.submit(
    "fal-ai/kling-video/v1.6/standard/text-to-video",
    arguments={
        "prompt": "cinematic drone shot over mountain forest at sunset, 4k",
        "duration": "5",
        "aspect_ratio": "16:9"
    }
)
video_url = result.get()
```

```python
# Usando RunwayML API
import requests

headers = {"Authorization": f"Bearer {RUNWAY_API_KEY}"}
response = requests.post(
    "https://api.runwayml.com/v1/image_to_video",
    headers=headers,
    json={
        "promptImage": image_url,
        "promptText": "slow cinematic zoom in, shallow depth of field",
        "duration": 5,
        "ratio": "1280:720"
    }
)
```

### Ensamblaje con FFmpeg
```bash
# Imágenes → Video con audio
ffmpeg -y \
    -framerate 1/4 \
    -pattern_type glob -i 'frames/*.png' \
    -i narration.mp3 \
    -c:v libx264 -pix_fmt yuv420p \
    -c:a aac -b:a 192k \
    -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1" \
    -shortest output.mp4

# Video → GIF animado (alta calidad)
ffmpeg -i input.mp4 \
    -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse=dither=bayer" \
    -loop 0 output.gif

# Añadir subtítulos
ffmpeg -i video.mp4 -i subtitles.srt \
    -c copy -c:s mov_text \
    video_with_subs.mp4

# Comprimir para web (H.264, CRF 23)
ffmpeg -i input.mp4 \
    -c:v libx264 -crf 23 -preset slow \
    -c:a aac -b:a 128k \
    -movflags +faststart \
    output_web.mp4

# Recortar video
ffmpeg -i input.mp4 -ss 00:01:30 -t 00:00:30 clip.mp4

# Concatenar múltiples videos
echo "file 'video1.mp4'\nfile 'video2.mp4'\nfile 'video3.mp4'" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy final.mp4

# Extraer audio
ffmpeg -i video.mp4 -vn -acodec mp3 -ab 192k audio.mp3

# Añadir watermark/logo
ffmpeg -i video.mp4 -i logo.png \
    -filter_complex "overlay=W-w-20:H-h-20" \
    watermarked.mp4

# Screen recording
ffmpeg -video_size 1920x1080 -framerate 30 \
    -f x11grab -i :0.0+0,0 \
    -f pulse -ac 2 -i default \
    -c:v libx264 -preset ultrafast \
    screen_record.mp4
```

---

## Script para Video Automatizado

```python
#!/usr/bin/env python3
"""
Video generation pipeline: topic → complete MP4
"""
import os
import json
import asyncio
import subprocess
from pathlib import Path

class VideoGenerator:
    def __init__(self, output_dir: str = "~/Videos/generated"):
        self.output_dir = Path(output_dir).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_script(self, topic: str, duration_seconds: int = 60) -> dict:
        """AI generates structured video script."""
        prompt = f"""Create a {duration_seconds}-second video script about: {topic}
        
        Return JSON with:
        {{
            "title": "...",
            "narration": "Full narration text for TTS",
            "scenes": [
                {{"time": 0, "duration": 5, "description": "Scene description for image generation", "text_overlay": "Optional text on screen"}},
                ...
            ]
        }}"""
        
        # Call AI (ideas-brillantes itself)
        result = await self._call_ai(prompt)
        return json.loads(result)

    async def generate_scene_images(self, scenes: list, style: str = "cinematic") -> list[str]:
        """Generate one image per scene."""
        image_paths = []
        for i, scene in enumerate(scenes):
            prompt = f"{scene['description']}, {style}, 4k quality, professional"
            path = await self._generate_image(prompt, f"{self.output_dir}/frames/scene_{i:03d}.png")
            image_paths.append(path)
        return image_paths

    async def generate_narration(self, text: str, voice: str = "es-ES-AlvaroNeural") -> str:
        """TTS narration."""
        output_path = str(self.output_dir / "narration.mp3")
        cmd = f'edge-tts --voice "{voice}" --text "{text}" --write-media "{output_path}"'
        subprocess.run(cmd, shell=True, check=True)
        return output_path

    def assemble_video(self, frame_dir: str, audio_path: str, output_name: str) -> str:
        """Assemble final video with ffmpeg."""
        output_path = str(self.output_dir / f"{output_name}.mp4")
        cmd = [
            "ffmpeg", "-y",
            "-framerate", "1/5",
            "-pattern_type", "glob",
            "-i", f"{frame_dir}/scene_*.png",
            "-i", audio_path,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_path
        ]
        subprocess.run(cmd, check=True)
        return output_path

    async def create(self, topic: str, duration: int = 60, style: str = "cinematic") -> str:
        print(f"🎬 Generating video about: {topic}")
        
        script = await self.generate_script(topic, duration)
        print(f"📝 Script: {len(script['scenes'])} scenes")
        
        images = await self.generate_scene_images(script['scenes'], style)
        print(f"🖼️  Generated {len(images)} scene images")
        
        audio = await self.generate_narration(script['narration'])
        print(f"🎤 Narration audio: {audio}")
        
        video = self.assemble_video(str(self.output_dir / "frames"), audio, "output")
        print(f"✅ Video ready: {video}")
        return video
```

---

## Estilos de Video por Tipo

### Explainer (Educational)
- Estilo: Animación flat 2D o screencast
- Duración: 60-120 segundos
- Narración: clara, ritmo moderado
- Subtítulos: obligatorios
- Resolución: 1920×1080 o 1280×720

### Social Media (Reel/TikTok)
- Estilo: dinámico, cuts rápidos
- Duración: 15-60 segundos
- Audio: música de fondo + texto en pantalla
- Resolución: 1080×1920 (vertical 9:16)
- Apertura: hook en primeros 2 segundos

### Presentation/Demo
- Estilo: screencast + voz en off
- Duración: 3-10 minutos
- Resolución: 1920×1080
- Narración: profesional, sin prisa

### YouTube Long-Form
- Estilo: talking head + B-roll
- Duración: 8-20 minutos
- Partes: intro, contenido, outro
- Thumbnail: diseño llamativo separado

---

## TTS (Text-to-Speech) Voces Recomendadas

### Español
```
es-ES-AlvaroNeural    — Hombre, neutro España
es-ES-ElviraNeural    — Mujer, clara España
es-MX-DaliaNeural     — Mujer, México
es-MX-JorgeNeural     — Hombre, México
es-AR-ElenaNeural     — Mujer, Argentina
```

### English
```
en-US-GuyNeural       — Man, neutral US
en-US-JennyNeural     — Woman, professional US
en-GB-RyanNeural      — Man, British
en-AU-NatashaNeural   — Woman, Australian
```

### Instalación edge-tts
```bash
pip install edge-tts
edge-tts --list-voices | grep es-ES
edge-tts --voice "es-ES-AlvaroNeural" --text "Hola mundo" --write-media output.mp3
```

---

## Generación de Thumbnails

```python
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def create_thumbnail(title: str, background_image_url: str, output_path: str):
    """Generate YouTube-style thumbnail."""
    
    # Load background
    response = requests.get(background_image_url)
    bg = Image.open(BytesIO(response.content)).resize((1280, 720))
    
    # Dark overlay gradient
    overlay = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(720):
        alpha = int(180 * (y / 720))
        draw.line([(0, y), (1280, y)], fill=(0, 0, 0, alpha))
    bg.paste(overlay, mask=overlay)
    
    # Add title text
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    
    # Text with shadow
    draw.text((62, 502), title, font=font, fill='black')
    draw.text((60, 500), title, font=font, fill='white')
    
    bg.save(output_path, 'PNG', quality=95)
    return output_path
```
