"""Speech-domain API: transcription, subtitles, synthesis, and dubbing plans."""
# this_file: src/twat_speech/twat_speech.py

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any

from twat_speech.dubbing import DubPlan, create_dub_plan
from twat_speech.providers import synthesize as synthesize_speech
from twat_speech.providers import transcribe as transcribe_audio
from twat_speech.subtitles import SubtitleCue, format_srt, parse_srt, repair_srt


def transcribe(audio_path: str | Path, *, preprocess: bool = False, **kwargs: Any) -> Any:
    """Transcribe an audio file, optionally using twat_audio preprocessing first."""
    source: str | Path = audio_path
    if preprocess:
        twat_audio = import_module("twat_audio")
        path = Path(audio_path)
        prepared = path.with_name(f"{path.stem}-speech-16k.wav")
        twat_audio.resample_audio(twat_audio.AudioProcessConfig(path, prepared, target_samplerate=16000.0))
        source = prepared
    return transcribe_audio(source, **kwargs)


def synthesize(text: str, output_path: str | Path | None = None, **kwargs: Any) -> Any:
    """Synthesize text to speech through the configured twat_genai backend."""
    return synthesize_speech(text, output_path=output_path, **kwargs)


def repair_subtitles(text: str) -> str:
    """Repair SRT text and return normalized SRT."""
    return repair_srt(text)


def subtitle_transcript(text: str) -> str:
    """Extract plain transcript text from SRT content."""
    return "\n".join(cue.text for cue in parse_srt(text) if cue.text)


def dub_plan(source_media: str | Path, subtitles: str, *, language: str = "en", audio_dir: str | Path = "dub-audio") -> DubPlan:
    """Create a provider-agnostic dubbing plan from media and SRT text."""
    return create_dub_plan(source_media, subtitles, language=language, audio_dir=audio_dir)


__all__ = [
    "DubPlan",
    "SubtitleCue",
    "dub_plan",
    "format_srt",
    "parse_srt",
    "repair_subtitles",
    "subtitle_transcript",
    "synthesize",
    "transcribe",
]
