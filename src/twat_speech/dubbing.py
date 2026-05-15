"""Dubbing orchestration helpers for twat-speech."""
# this_file: src/twat_speech/dubbing.py

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from twat_speech.subtitles import SubtitleCue, parse_srt


@dataclass(frozen=True)
class DubSegment:
    """One planned dubbing segment."""

    index: int
    start: str
    end: str
    text: str
    audio_path: Path


@dataclass(frozen=True)
class DubPlan:
    """A deterministic plan for provider-backed dubbing."""

    source_media: Path
    language: str
    segments: list[DubSegment] = field(default_factory=list)


def create_dub_plan(source_media: str | Path, subtitles: str, *, language: str = "en", audio_dir: str | Path = "dub-audio") -> DubPlan:
    """Create a deterministic dubbing plan from SRT text."""
    media = Path(source_media)
    base = Path(audio_dir)
    segments = [
        DubSegment(cue.index, cue.start, cue.end, cue.text, base / f"{cue.index:04d}-{language}.wav")
        for cue in parse_srt(subtitles)
    ]
    return DubPlan(media, language, segments)


def cues_to_plain_text(cues: list[SubtitleCue]) -> str:
    """Flatten subtitle cues to transcript text."""
    return "\n".join(cue.text for cue in cues if cue.text)
