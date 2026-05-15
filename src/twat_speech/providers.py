"""Thin provider adapters from twat-speech to twat-genai."""
# this_file: src/twat_speech/providers.py

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any


def _provider(name: str) -> Any:
    try:
        twat_genai = import_module("twat_genai")
    except ImportError as exc:
        msg = "twat_genai is required for speech provider operations. Install twat-genai and configure a provider."
        raise RuntimeError(msg) from exc
    fn = getattr(twat_genai, name, None)
    if fn is None:
        msg = f"Installed twat_genai does not expose {name} yet."
        raise NotImplementedError(msg)
    return fn


def transcribe(audio_path: str | Path, **kwargs: Any) -> Any:
    """Transcribe speech audio through twat_genai."""
    return _provider("transcribe_audio")(audio_path=audio_path, **kwargs)


def synthesize(text: str, output_path: str | Path | None = None, **kwargs: Any) -> Any:
    """Synthesize speech through twat_genai."""
    return _provider("synthesize_speech")(text=text, output_path=output_path, **kwargs)
