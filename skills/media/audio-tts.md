# Audio & TTS Skill

## Fuente
VoltAgent/awesome-agent-skills (audio/media), agency-agents, ruflo media agent

---

## Proveedores TTS

### 1. Edge-TTS (Microsoft — Gratuito, sin API key)
```bash
pip install edge-tts
```

```python
import asyncio
import edge_tts

async def generate_speech(text: str, voice: str, output_path: str):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

asyncio.run(generate_speech(
    text="Hola, soy ideas-brillantes, tu asistente de IA.",
    voice="es-ES-AlvaroNeural",
    output_path="output.mp3"
))
```

**Voces Edge-TTS Completas:**
```
# Español España
es-ES-AlvaroNeural         Male
es-ES-ElviraNeural         Female
es-ES-AbrilNeural          Female
es-ES-ArnauNeural          Male
es-ES-IsidoraNeural        Female

# Español México  
es-MX-DaliaNeural          Female
es-MX-JorgeNeural          Male
es-MX-BeatrizNeural        Female
es-MX-CandelaNeural        Female

# English US
en-US-JennyNeural          Female
en-US-GuyNeural            Male
en-US-AnaNeural            Female (child)
en-US-AriaNeural           Female
en-US-DavisNeural          Male
en-US-SaraNeural           Female
en-US-TonyNeural           Male

# English UK
en-GB-SoniaNeural          Female
en-GB-RyanNeural           Male
en-GB-LibbyNeural          Female

# Otros idiomas populares
fr-FR-DeniseNeural         Female
de-DE-KatjaNeural          Female
it-IT-ElsaNeural           Female
pt-BR-FranciscaNeural      Female
zh-CN-XiaoxiaoNeural       Female
ja-JP-NanamiNeural         Female
```

```bash
# Listar todas las voces disponibles
edge-tts --list-voices

# CLI directo
edge-tts --voice "es-ES-AlvaroNeural" \
    --text "Buenos días" \
    --write-media output.mp3 \
    --write-subtitles output.vtt
```

---

### 2. Piper TTS (Local, sin internet)
```bash
pip install piper-tts
```

```python
import subprocess

def piper_tts(text: str, model: str = "es_ES-mls-medium", output: str = "output.wav"):
    cmd = f'echo "{text}" | piper --model {model} --output_file {output}'
    subprocess.run(cmd, shell=True)
```

**Modelos Piper disponibles:**
```
es_ES-mls-medium       Español España
es_MX-claude-high      Español México  
en_US-lessac-medium    English US
en_GB-alan-medium      English UK
de_DE-thorsten-medium  Alemán
fr_FR-mls-medium       Francés
```

---

### 3. Bark (HuggingFace — Expresivo, emociones)
```python
from bark import SAMPLE_RATE, generate_audio, preload_models
import soundfile as sf

preload_models()

# Soporta marcadores de emoción y paralinguísticos
text = """
Buenos días a todos [clears throat] 
En esta sesión vamos a ver algo muy importante [laughs]
Espero que estén preparados... [sighs]
"""

audio_array = generate_audio(text, history_prompt="v2/es_speaker_0")
sf.write("output.wav", audio_array, SAMPLE_RATE)
```

**Speaker prompts Bark:**
```
v2/es_speaker_0 - v2/es_speaker_9    Español
v2/en_speaker_0 - v2/en_speaker_9    English
v2/fr_speaker_0 - v2/fr_speaker_9    Français
v2/de_speaker_0 - v2/de_speaker_9    Deutsch
```

---

### 4. Coqui TTS (Open source, multi-idioma)
```bash
pip install TTS
```

```python
from TTS.api import TTS

# Lista de modelos
tts = TTS().list_models()

# Español
tts = TTS("tts_models/es/css10/vits")
tts.tts_to_file("Hola mundo", file_path="output.wav")

# Multi-speaker con clonación
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.tts_to_file(
    text="Hello world",
    speaker_wav="reference_voice.wav",  # voz a clonar
    language="en",
    file_path="cloned_output.wav"
)
```

---

## Transcripción de Audio (Speech-to-Text)

### Whisper (OpenAI — Local)
```bash
pip install openai-whisper
```

```python
import whisper

model = whisper.load_model("medium")  # tiny/base/small/medium/large

result = model.transcribe(
    "audio.mp3",
    language="es",      # auto-detect si omites
    task="transcribe",  # o "translate" (→ inglés)
    word_timestamps=True
)

print(result["text"])

# Acceder a segmentos con timestamps
for segment in result["segments"]:
    print(f"[{segment['start']:.1f}s → {segment['end']:.1f}s] {segment['text']}")
```

```bash
# CLI
whisper audio.mp3 --language es --model medium --output_format srt
whisper audio.mp3 --model large-v3 --task translate  # → English
```

### faster-whisper (2-4x más rápido)
```python
from faster_whisper import WhisperModel

model = WhisperModel("medium", device="cuda", compute_type="float16")
segments, info = model.transcribe("audio.mp3", language="es")

full_text = " ".join([s.text for s in segments])
```

---

## Procesamiento de Audio con FFmpeg

```bash
# Convertir formatos
ffmpeg -i input.wav -q:a 2 output.mp3
ffmpeg -i input.mp3 output.wav
ffmpeg -i input.m4a -c:a libmp3lame output.mp3

# Normalizar volumen
ffmpeg -i input.mp3 -filter:a loudnorm output.mp3

# Recortar audio
ffmpeg -i input.mp3 -ss 00:00:30 -t 00:01:00 clip.mp3

# Amplificar/reducir volumen
ffmpeg -i input.mp3 -filter:a "volume=2.0" louder.mp3   # 2x
ffmpeg -i input.mp3 -filter:a "volume=0.5" quieter.mp3  # 50%

# Eliminar ruido (reducción de ruido básica)
ffmpeg -i input.mp3 -af "highpass=f=200,lowpass=f=3000" clean.mp3

# Combinar audio + video
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac output.mp4

# Mezclar dos pistas de audio
ffmpeg -i speech.mp3 -i music.mp3 \
    -filter_complex "[0:a]volume=1.0[a0];[1:a]volume=0.15[a1];[a0][a1]amix=inputs=2" \
    mixed.mp3

# Silenciar segmento de audio
ffmpeg -i input.mp3 \
    -af "volume=enable='between(t,30,45)':volume=0" \
    with_silence.mp3

# Detectar silencios
ffmpeg -i input.mp3 -af silencedetect=n=-50dB:d=0.5 -f null - 2>&1 | grep silence

# Separar voz de música (requiere demucs)
# python3 -m demucs --two-stems=vocals input.mp3
```

---

## Generación de Música con IA

### AudioCraft (Meta — Local)
```python
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

model = MusicGen.get_pretrained('medium')
model.set_generation_params(duration=30)

descriptions = [
    "epic cinematic orchestral music, dramatic tension building",
    "lo-fi hip hop beats, relaxing study music, chill vibes"
]

wav = model.generate(descriptions)

for idx, one_wav in enumerate(wav):
    audio_write(f'music_{idx}', one_wav.cpu(), model.sample_rate)
```

### ElevenLabs (API — Alta calidad)
```python
from elevenlabs import ElevenLabs, VoiceSettings

client = ElevenLabs(api_key="your_api_key")

audio = client.text_to_speech.convert(
    voice_id="pNInz6obpgDQGcFmaJgB",  # Adam
    text="Bienvenido a ideas-brillantes",
    model_id="eleven_multilingual_v2",
    voice_settings=VoiceSettings(
        stability=0.5,
        similarity_boost=0.75,
        style=0.0,
        use_speaker_boost=True
    )
)

with open("elevenlabs_output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

---

## Flujo Completo: Podcast Automatizado

```python
async def generate_podcast(topic: str) -> str:
    """Generate complete podcast episode from topic."""
    
    # 1. Generate script
    script = await ai.generate(f"""
        Write a 5-minute podcast script about: {topic}
        Format: intro, 3 main points, conclusion
        Style: conversational, engaging, informative
    """)
    
    # 2. Generate host voice (TTS)
    host_audio = await edge_tts_generate(
        script, 
        voice="en-US-GuyNeural",
        output="/tmp/host.mp3"
    )
    
    # 3. Generate background music
    music = musicgen.generate(
        "calm podcast background music, minimal, professional",
        duration=300  # 5 minutes
    )
    
    # 4. Mix voice + music
    subprocess.run([
        "ffmpeg", "-y",
        "-i", host_audio,
        "-i", music_path,
        "-filter_complex", "[1:a]volume=0.08[bg];[0:a][bg]amix=inputs=2:duration=first",
        "-c:a", "libmp3lame", "-b:a", "192k",
        "podcast_episode.mp3"
    ])
    
    return "podcast_episode.mp3"
```
