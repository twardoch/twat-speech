# twat-speech

`twat-speech` is the speech-domain plugin for the [`twat`](https://github.com/twardoch/twat) ecosystem. It provides transcription orchestration, subtitle repair, text-to-speech (TTS) synthesis, and deterministic dubbing plans — while delegating provider clients to `twat_genai` and raw audio transforms to `twat_audio`.

## What it does

| Area | Functions |
|---|---|
| **Subtitle repair** | `parse_srt`, `format_srt`, `repair_srt`, `repair_subtitles` |
| **Transcript extraction** | `subtitle_transcript` |
| **Transcription** | `transcribe` (delegates to `twat_genai`) |
| **TTS synthesis** | `synthesize` (delegates to `twat_genai`) |
| **Dubbing orchestration** | `dub_plan`, `create_dub_plan` |

## Ecosystem boundaries

```
twat_genai   ← speech providers (STT / TTS engines, API keys)
twat_audio   ← audio-file transforms (resample, trim, normalize, extract)
twat_speech  ← speech orchestration, subtitles, transcripts, dubbing plans
```

`twat_speech` never owns credentials or raw audio I/O. It calls into the other two plugins via lazy imports so they remain optional.

## Quick example

```python
from twat_speech import repair_subtitles, dub_plan, transcribe, synthesize

# Fix a broken SRT file
fixed = repair_subtitles(open("captions.srt").read())

# Build a dubbing plan (no audio generated yet — purely structural)
plan = dub_plan("movie.mp4", fixed, language="de")
for seg in plan.segments:
    print(seg.index, seg.audio_path, seg.text)

# Transcribe audio (requires twat_genai + configured provider)
result = transcribe("speech.wav")

# Synthesize speech (requires twat_genai + configured provider)
out = synthesize("Hallo Welt", "hello.wav")
```
