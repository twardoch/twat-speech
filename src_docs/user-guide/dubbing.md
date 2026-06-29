# Dubbing Plans

`twat-speech` separates the *planning* of dubbing from the *execution*. `dub_plan` / `create_dub_plan` produce a `DubPlan` — a pure data structure that maps each subtitle cue to a deterministic output audio path. No audio is generated, no network calls are made.

This design lets you:

- Inspect the full segment list before committing to synthesis
- Parallelize synthesis across segments in any order
- Resume a partial dub run by checking which `.wav` files already exist
- Unit-test dubbing logic without provider credentials

## Data structures

### `DubSegment`

One planned segment, corresponding to a single SRT cue.

| Field | Type | Description |
|---|---|---|
| `index` | `int` | Cue index |
| `start` | `str` | Normalized start timestamp |
| `end` | `str` | Normalized end timestamp |
| `text` | `str` | Text to synthesize |
| `audio_path` | `Path` | Deterministic output path: `{audio_dir}/{index:04d}-{language}.wav` |

### `DubPlan`

The complete plan for one dubbing job.

| Field | Type | Description |
|---|---|---|
| `source_media` | `Path` | Source media file |
| `language` | `str` | Target language code |
| `segments` | `list[DubSegment]` | Ordered segment list |

## API

### `dub_plan(source_media, subtitles, *, language, audio_dir) -> DubPlan`

```python
from twat_speech import dub_plan

plan = dub_plan(
    "movie.mp4",
    open("captions.srt").read(),
    language="de",
    audio_dir="dub-audio",
)

for seg in plan.segments:
    # seg.audio_path == Path("dub-audio/0001-de.wav") etc.
    print(seg.index, seg.audio_path, repr(seg.text))
```

### `create_dub_plan(...)` 

Low-level alias exposed from `twat_speech.dubbing`. Identical signature to `dub_plan`.

## Synthesis loop pattern

```python
from pathlib import Path
from twat_speech import dub_plan, synthesize

plan = dub_plan("movie.mp4", open("captions.de.srt").read(), language="de")

for seg in plan.segments:
    if seg.audio_path.exists():
        continue  # resume support
    seg.audio_path.parent.mkdir(parents=True, exist_ok=True)
    synthesize(seg.text, str(seg.audio_path))
```
