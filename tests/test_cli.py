# this_file: tests/test_cli.py
"""CLI smoke tests for twat-speech Fire entry points."""

from __future__ import annotations

import subprocess
import sys


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "twat_speech", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_help_exits_zero() -> None:
    """twat_speech --help exits 0."""
    result = _run("--help")
    assert result.returncode == 0, result.stderr


def test_help_lists_commands() -> None:
    """--help output mentions known subcommands."""
    result = _run("--help")
    assert result.returncode == 0
    out = result.stdout + result.stderr
    assert "version" in out
    assert "transcribe" in out
    assert "tts" in out


def test_version_exits_zero() -> None:
    """twat_speech version exits 0."""
    result = _run("version")
    assert result.returncode == 0, result.stderr


def test_version_prints_semver() -> None:
    """version subcommand prints a semver-ish string."""
    result = _run("version")
    assert result.returncode == 0
    out = (result.stdout + result.stderr).strip()
    assert out, "version output must not be empty"
    assert "." in out, f"Expected semver, got: {out!r}"


def test_transcribe_help_exits_zero() -> None:
    """twat_speech transcribe --help exits 0."""
    result = _run("transcribe", "--help")
    assert result.returncode == 0, result.stderr


def test_tts_help_exits_zero() -> None:
    """twat_speech tts --help exits 0."""
    result = _run("tts", "--help")
    assert result.returncode == 0, result.stderr


def test_repair_srt_help_exits_zero() -> None:
    """twat_speech repair-srt --help exits 0."""
    result = _run("repair-srt", "--help")
    assert result.returncode == 0, result.stderr


def test_dub_help_exits_zero() -> None:
    """twat_speech dub --help exits 0."""
    result = _run("dub", "--help")
    assert result.returncode == 0, result.stderr


def test_subtitle_transcript_help_exits_zero() -> None:
    """twat_speech subtitle-transcript --help exits 0."""
    result = _run("subtitle-transcript", "--help")
    assert result.returncode == 0, result.stderr
