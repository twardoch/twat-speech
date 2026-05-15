"""Tests for twat_speech domain behavior."""
# this_file: tests/test_speech_domain.py

from pathlib import Path
from pytest import MonkeyPatch
from unittest import mock

from twat_speech import (
    dub_plan,
    normalize_timestamp,
    parse_srt,
    repair_subtitles,
    subtitle_transcript,
    synthesize,
    transcribe,
)

SRT = "1\r\n0:00:01.2 --> 0:00:02,30\r\nHello world\r\n\r\n2\n00:00:03,000 --> 00:00:04,000\nAgain\n"


def test_normalize_timestamp_and_repair_srt() -> None:
    assert normalize_timestamp("0:00:01.2") == "00:00:01,200"
    repaired = repair_subtitles(SRT)
    assert "00:00:01,200 --> 00:00:02,300" in repaired
    assert repaired.startswith("1\n")


def test_parse_srt_and_transcript() -> None:
    cues = parse_srt(SRT)
    assert len(cues) == 2
    assert subtitle_transcript(SRT) == "Hello world\nAgain"


def test_dub_plan_creates_segment_audio_paths() -> None:
    plan = dub_plan(Path("movie.mp4"), SRT, language="de", audio_dir="audio")
    assert plan.language == "de"
    assert plan.segments[0].audio_path == Path("audio/0001-de.wav")


def test_provider_calls_are_delegated(monkeypatch: MonkeyPatch) -> None:
    fake = mock.Mock()
    fake.transcribe_audio.return_value = {"text": "hello"}
    fake.synthesize_speech.return_value = Path("out.wav")
    monkeypatch.setitem(__import__("sys").modules, "twat_genai", fake)
    assert transcribe("voice.wav") == {"text": "hello"}
    assert synthesize("hello", "out.wav") == Path("out.wav")
