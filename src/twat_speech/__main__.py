# this_file: src/twat_speech/__main__.py
"""Fire CLI entry point for twat-speech."""

from __future__ import annotations

import fire


def _version() -> str:
    """Print the installed twat-speech version."""
    from twat_speech.__version__ import __version__  # noqa: PLC0415

    return __version__


def _transcribe(audio_path: str, *, preprocess: bool = False) -> object:
    """Transcribe an audio file to text."""
    from twat_speech.twat_speech import transcribe  # noqa: PLC0415

    return transcribe(audio_path, preprocess=preprocess)


def _tts(text: str, output_path: str | None = None) -> object:
    """Synthesize text to speech (TTS)."""
    from twat_speech.twat_speech import synthesize  # noqa: PLC0415

    return synthesize(text, output_path=output_path)


def _repair_srt(input_path: str, output_path: str | None = None) -> object:
    """Repair and normalize an SRT subtitle file."""
    from pathlib import Path  # noqa: PLC0415

    from twat_speech.twat_speech import repair_subtitles  # noqa: PLC0415

    text = Path(input_path).read_text()
    repaired = repair_subtitles(text)
    if output_path:
        Path(output_path).write_text(repaired)
        return output_path
    return repaired


def _dub(
    media: str,
    srt: str,
    language: str = "en",
    audio_dir: str = "dub-audio",
) -> object:
    """Create a dubbing plan from media and SRT file."""
    from pathlib import Path  # noqa: PLC0415

    from twat_speech.twat_speech import dub_plan  # noqa: PLC0415

    plan = dub_plan(media, Path(srt).read_text(), language=language, audio_dir=audio_dir)
    return [
        {
            "index": seg.index,
            "start": seg.start,
            "end": seg.end,
            "audio_path": seg.audio_path,
            "text": seg.text,
        }
        for seg in plan.segments
    ]


def _subtitle_transcript(input_path: str) -> object:
    """Extract plain transcript text from an SRT file."""
    from pathlib import Path  # noqa: PLC0415

    from twat_speech.twat_speech import subtitle_transcript  # noqa: PLC0415

    return subtitle_transcript(Path(input_path).read_text())


COMMANDS: dict[str, object] = {
    "version": _version,
    "transcribe": _transcribe,
    "tts": _tts,
    "repair-srt": _repair_srt,
    "dub": _dub,
    "subtitle-transcript": _subtitle_transcript,
}


def main() -> None:
    """Fire CLI dispatcher for twat-speech."""
    fire.Fire(COMMANDS, name="twat-speech")


def cmd_version() -> None:
    """Print the installed twat-speech version."""
    fire.Fire(_version, name="twat-speech-version")


def cmd_transcribe() -> None:
    """Transcribe an audio file to text."""
    fire.Fire(_transcribe, name="twat-speech-transcribe")


def cmd_tts() -> None:
    """Synthesize text to speech (TTS)."""
    fire.Fire(_tts, name="twat-speech-tts")


def cmd_repair_srt() -> None:
    """Repair and normalize an SRT subtitle file."""
    fire.Fire(_repair_srt, name="twat-speech-repair-srt")


def cmd_dub() -> None:
    """Create a dubbing plan from media and SRT file."""
    fire.Fire(_dub, name="twat-speech-dub")


def cmd_subtitle_transcript() -> None:
    """Extract plain transcript text from an SRT file."""
    fire.Fire(_subtitle_transcript, name="twat-speech-subtitle-transcript")


if __name__ == "__main__":
    main()
