"""twat-speech: transcription, subtitles, TTS, and dubbing orchestration."""
# this_file: src/twat_speech/__init__.py

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("twat-speech")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

from twat_speech.dubbing import DubPlan, DubSegment, create_dub_plan
from twat_speech.subtitles import SubtitleCue, format_srt, normalize_timestamp, parse_srt, repair_srt
from twat_speech.twat_speech import dub_plan, repair_subtitles, subtitle_transcript, synthesize, transcribe


def main() -> None:
    """CLI entry point for twat-speech."""
    from twat_speech.__main__ import main as cli_main  # noqa: PLC0415

    cli_main()


__all__ = [
    "DubPlan",
    "DubSegment",
    "SubtitleCue",
    "__version__",
    "create_dub_plan",
    "dub_plan",
    "format_srt",
    "main",
    "normalize_timestamp",
    "parse_srt",
    "repair_srt",
    "repair_subtitles",
    "subtitle_transcript",
    "synthesize",
    "transcribe",
]
