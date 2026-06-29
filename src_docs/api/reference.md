# API Reference

All public names are re-exported from `twat_speech.__init__` and listed in `__all__`.

## Top-level imports

```python
from twat_speech import (
    # data classes
    SubtitleCue,
    DubSegment,
    DubPlan,
    # subtitle functions
    normalize_timestamp,
    parse_srt,
    format_srt,
    repair_srt,
    repair_subtitles,
    subtitle_transcript,
    # dubbing
    create_dub_plan,
    dub_plan,
    # provider adapters
    transcribe,
    synthesize,
    # version
    __version__,
)
```

---

## Data classes

### `SubtitleCue`

```python
@dataclass(frozen=True)
class SubtitleCue:
    index: int          # block index (as parsed from SRT)
    start: str          # normalized timestamp "HH:MM:SS,mmm"
    end: str            # normalized timestamp "HH:MM:SS,mmm"
    text: str           # subtitle text (may contain \n)
```

### `DubSegment`

```python
@dataclass(frozen=True)
class DubSegment:
    index: int
    start: str
    end: str
    text: str
    audio_path: Path    # deterministic: {audio_dir}/{index:04d}-{language}.wav
```

### `DubPlan`

```python
@dataclass(frozen=True)
class DubPlan:
    source_media: Path
    language: str
    segments: list[DubSegment]
```

---

## Subtitle functions

### `normalize_timestamp(value: str) -> str`

Convert a loose SRT timestamp to canonical `HH:MM:SS,mmm`.
Raises `ValueError` if the input does not match the SRT timestamp pattern.

### `parse_srt(text: str) -> list[SubtitleCue]`

Parse SRT text (any line ending) into cues. Blocks that lack a `-->` separator are skipped.

### `format_srt(cues: list[SubtitleCue]) -> str`

Serialize cues to SRT text with consecutive 1-based block indices.

### `repair_srt(text: str) -> str`

Equivalent to `format_srt(parse_srt(text))`.

### `repair_subtitles(text: str) -> str`

Public-API alias for `repair_srt`. Prefer this name in application code.

### `subtitle_transcript(text: str) -> str`

Extract plain text from SRT, one cue per line, no timestamps.

---

## Dubbing functions

### `create_dub_plan(source_media, subtitles, *, language, audio_dir) -> DubPlan`

```python
def create_dub_plan(
    source_media: str | Path,
    subtitles: str,
    *,
    language: str = "en",
    audio_dir: str | Path = "dub-audio",
) -> DubPlan: ...
```

Parse `subtitles` as SRT and build a `DubPlan` mapping each cue to a deterministic
audio path `{audio_dir}/{index:04d}-{language}.wav`. Pure data — no I/O.

### `dub_plan(source_media, subtitles, *, language, audio_dir) -> DubPlan`

Thin wrapper over `create_dub_plan` exposed at the top-level API.

---

## Provider adapters

These call into `twat_genai` at runtime. `ImportError` / `NotImplementedError` are
raised if `twat_genai` is not installed or the requested function is not yet exposed
by the installed version.

### `transcribe(audio_path, *, preprocess=False, **kwargs) -> Any`

```python
def transcribe(
    audio_path: str | Path,
    *,
    preprocess: bool = False,
    **kwargs: Any,
) -> Any: ...
```

Transcribe `audio_path` via `twat_genai.transcribe_audio`.
If `preprocess=True`, resample to 16 kHz via `twat_audio` before transcription
(requires `twat-audio` installed).

### `synthesize(text, output_path=None, **kwargs) -> Any`

```python
def synthesize(
    text: str,
    output_path: str | Path | None = None,
    **kwargs: Any,
) -> Any: ...
```

Synthesize `text` to speech via `twat_genai.synthesize_speech`.
