# Subtitle Repair

`twat-speech` provides a minimal but robust SRT parser and repairer that handles the common malformed output from ASR tools and video editors.

## What gets normalized

| Problem | Before | After |
|---|---|---|
| Windows line endings | `\r\n` | `\n` |
| Short hour field | `0:00:01,200` | `00:00:01,200` |
| Dot millisecond separator | `00:00:01.200` | `00:00:01,200` |
| Short milliseconds | `00:00:01,2` | `00:00:01,200` |
| Non-consecutive indices | `1, 3, 7` | `1, 2, 3` |
| Trailing blank blocks | — | removed |

## API

### `normalize_timestamp(value: str) -> str`

Normalize a single SRT timestamp string to `HH:MM:SS,mmm`.

```python
from twat_speech import normalize_timestamp

normalize_timestamp("0:00:01.2")   # "00:00:01,200"
normalize_timestamp("1:02:03,45")  # "01:02:03,450"
```

Raises `ValueError` for strings that do not match the SRT timestamp format.

---

### `parse_srt(text: str) -> list[SubtitleCue]`

Parse SRT text into a list of `SubtitleCue` dataclass instances.

```python
from twat_speech import parse_srt, SubtitleCue

cues: list[SubtitleCue] = parse_srt(open("captions.srt").read())
for cue in cues:
    print(cue.index, cue.start, cue.end, cue.text)
```

`SubtitleCue` fields:

| Field | Type | Description |
|---|---|---|
| `index` | `int` | Original block index |
| `start` | `str` | Normalized start timestamp |
| `end` | `str` | Normalized end timestamp |
| `text` | `str` | Subtitle text (may contain `\n`) |

---

### `format_srt(cues: list[SubtitleCue]) -> str`

Serialize cues back to SRT text with consecutive 1-based indices.

```python
from twat_speech import parse_srt, format_srt

cues = parse_srt(raw_srt)
fixed_srt = format_srt(cues)
```

---

### `repair_srt(text: str) -> str`

Convenience wrapper: `format_srt(parse_srt(text))`.

---

### `repair_subtitles(text: str) -> str`

Public API alias for `repair_srt`. Prefer this name in application code.

```python
from twat_speech import repair_subtitles

fixed = repair_subtitles(open("captions.srt").read())
```

---

### `subtitle_transcript(text: str) -> str`

Extract plain text from SRT, joining cue texts with newlines.

```python
from twat_speech import subtitle_transcript

plain = subtitle_transcript(open("captions.srt").read())
# "Hello world\nThis is line two"
```
