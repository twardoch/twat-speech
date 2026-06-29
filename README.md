# twat-speech

`twat-speech` is the speech-domain plugin for the [`twat`](https://github.com/twardoch/twat) ecosystem. It provides:

- **Subtitle repair** — parse and normalize broken SRT files
- **Transcript extraction** — pull plain text from SRT without timestamps
- **Transcription** — delegate audio-to-text to the configured `twat_genai` provider
- **TTS synthesis** — delegate text-to-speech to the configured `twat_genai` provider
- **Dubbing plans** — build deterministic segment-to-audio-path mappings from SRT cues

## Ecosystem boundaries

```
twat_genai   ← speech providers (STT / TTS engines, API keys)
twat_audio   ← audio-file transforms (resample, trim, normalize, extract)
twat_speech  ← speech orchestration, subtitles, transcripts, dubbing plans
```

`twat_speech` never owns credentials or raw audio I/O. `twat_genai` and `twat_audio` are lazy optional imports — subtitle and dubbing-plan functions work with no extra dependencies.

## Install

```bash
pip install twat-speech
# with audio preprocessing support:
pip install "twat-speech[audio]"
```

## Python API

```python
from twat_speech import (
    repair_subtitles,
    subtitle_transcript,
    parse_srt, format_srt, normalize_timestamp,
    dub_plan, create_dub_plan,
    DubPlan, DubSegment, SubtitleCue,
    transcribe, synthesize,
)

# Repair a broken SRT file (no provider needed)
fixed = repair_subtitles(open("captions.srt").read())

# Extract plain transcript
plain = subtitle_transcript(fixed)

# Build a dubbing plan (pure data, no network calls)
plan = dub_plan("movie.mp4", fixed, language="de", audio_dir="dub-audio")
for seg in plan.segments:
    print(seg.index, seg.audio_path, seg.text)

# Transcribe audio (requires twat_genai + configured provider)
result = transcribe("speech.wav")
# With 16 kHz resampling via twat_audio:
result = transcribe("speech.wav", preprocess=True)

# Synthesize speech (requires twat_genai + configured provider)
out = synthesize("Hello world", "hello.wav")
```

## CLI

```bash
# Show all subcommands
python -m twat_speech --help

# Repair an SRT file
python -m twat_speech repair-srt captions.srt captions.fixed.srt

# Extract plain transcript from SRT
python -m twat_speech subtitle-transcript captions.srt

# Transcribe audio file
python -m twat_speech transcribe speech.wav

# Text-to-speech
python -m twat_speech tts "Hello world" hello.wav

# Build a dubbing plan (prints JSON)
python -m twat_speech dub movie.mp4 captions.srt --language de --audio-dir dub-audio

# Print version
python -m twat_speech version
```

Dedicated entry points are also installed: `twat-speech`, `twat-speech-transcribe`, `twat-speech-tts`, `twat-speech-repair-srt`, `twat-speech-dub`, `twat-speech-subtitle-transcript`, `twat-speech-version`.

## Subtitle repair details

| Problem | Before | After |
|---|---|---|
| Windows line endings | `\r\n` | `\n` |
| Short hour field | `0:00:01,200` | `00:00:01,200` |
| Dot millisecond separator | `00:00:01.2` | `00:00:01,200` |
| Short milliseconds | `00:00:01,2` | `00:00:01,200` |
| Non-consecutive indices | `1, 3, 7` | `1, 2, 3` |

## Dubbing plan

`dub_plan` / `create_dub_plan` return a `DubPlan` — a frozen dataclass holding a list of `DubSegment` objects. Each segment carries `index`, `start`, `end`, `text`, and a deterministic `audio_path` of the form `{audio_dir}/{index:04d}-{language}.wav`. No audio is produced; the plan is a pure specification for a synthesis loop.

```python
plan = dub_plan("movie.mp4", srt_text, language="de")
# plan.segments[0].audio_path == Path("dub-audio/0001-de.wav")
```

## Reference scripts

Reusable subtitle repair ideas from `srtmultifix.py`, extraction workflows from `mkv2srt.py`, and planning ideas from `vidpredub.py` / `viddub-*` are represented here as package APIs. Provider-specific or workstation-specific batch dubbing scripts remain in `reference/bin-img-vid/` because they combine local credentials, shell glue, and one-off media workflows.

## Development

```bash
# Run tests
uvx hatch test

# Lint + format
hatch run lint

# Type check
hatch run type-check

# Build docs (requires docs extras)
pip install "twat-speech[docs]"
mkdocs serve
```
