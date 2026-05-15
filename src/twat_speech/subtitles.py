"""Subtitle parsing and repair helpers for twat-speech."""
# this_file: src/twat_speech/subtitles.py

from __future__ import annotations

import re
from dataclasses import dataclass

TIMESTAMP_RE = re.compile(r"(?P<h>\d{1,2}):(?P<m>\d{2}):(?P<s>\d{2})(?P<sep>[,.])(?P<ms>\d{1,3})")


@dataclass(frozen=True)
class SubtitleCue:
    """A minimal SRT cue."""

    index: int
    start: str
    end: str
    text: str


def normalize_timestamp(value: str) -> str:
    """Normalize an SRT timestamp to HH:MM:SS,mmm."""
    match = TIMESTAMP_RE.fullmatch(value.strip())
    if not match:
        msg = f"invalid SRT timestamp: {value!r}"
        raise ValueError(msg)
    return f"{int(match['h']):02d}:{int(match['m']):02d}:{int(match['s']):02d},{match['ms'][:3].ljust(3, '0')}"


def parse_srt(text: str) -> list[SubtitleCue]:
    """Parse basic SRT text into cue records."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    cues: list[SubtitleCue] = []
    for block in [item.strip() for item in normalized.split("\n\n") if item.strip()]:
        lines = block.split("\n")
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        start, end = [part.strip() for part in lines[1].split("-->", 1)]
        try:
            index = int(lines[0].strip())
        except ValueError:
            index = len(cues) + 1
        cues.append(SubtitleCue(index, normalize_timestamp(start), normalize_timestamp(end), "\n".join(lines[2:]).strip()))
    return cues


def format_srt(cues: list[SubtitleCue]) -> str:
    """Format cues as SRT text with consecutive indices."""
    blocks = [f"{pos}\n{cue.start} --> {cue.end}\n{cue.text.strip()}" for pos, cue in enumerate(cues, start=1)]
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def repair_srt(text: str) -> str:
    """Repair common SRT issues: CRLFs, dot milliseconds, padding, and numbering."""
    return format_srt(parse_srt(text))
