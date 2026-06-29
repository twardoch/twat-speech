# Quick Start

## Subtitle repair (no provider needed)

The most common standalone use is repairing broken SRT files produced by various tools:

```python
from twat_speech import repair_subtitles

broken = open("captions.srt").read()
fixed = repair_subtitles(broken)
open("captions.fixed.srt", "w").write(fixed)
```

What gets repaired:

- CRLF line endings normalized to LF
- Timestamps padded to `HH:MM:SS,mmm` format (e.g. `0:00:01.2` → `00:00:01,200`)
- Block indices renumbered consecutively
- Blank blocks removed

## Extract a plain transcript

```python
from twat_speech import subtitle_transcript

text = subtitle_transcript(open("captions.srt").read())
print(text)  # one line per subtitle cue, no timestamps
```

## Build a dubbing plan

```python
from twat_speech import dub_plan

plan = dub_plan("movie.mp4", open("captions.de.srt").read(), language="de")
for seg in plan.segments:
    print(f"[{seg.start} --> {seg.end}]  {seg.audio_path}  {seg.text!r}")
```

The plan is a pure data structure — no audio is generated, no network calls are made. Pass the segments to your synthesis loop.

## Transcribe audio (requires twat_genai)

```python
from twat_speech import transcribe

result = transcribe("speech.wav")
print(result["text"])
```

Add `preprocess=True` to resample to 16 kHz via `twat_audio` before sending to the provider:

```python
result = transcribe("speech.wav", preprocess=True)
```

## Synthesize speech (requires twat_genai)

```python
from twat_speech import synthesize

out_path = synthesize("Hello world", "hello.wav")
print(out_path)
```

## CLI

```bash
# Repair an SRT file
python -m twat_speech repair-srt captions.srt captions.fixed.srt

# Extract transcript
python -m twat_speech subtitle-transcript captions.srt

# Transcribe audio
python -m twat_speech transcribe speech.wav

# TTS
python -m twat_speech tts "Hello world" hello.wav

# Build dubbing plan (prints JSON)
python -m twat_speech dub movie.mp4 captions.srt --language de
```
