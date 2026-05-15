"""Package smoke tests for twat_speech."""
# this_file: tests/test_twat_speech.py

from twat_speech import __all__, __version__


def test_version_is_string() -> None:
    """Verify package exposes version."""
    assert isinstance(__version__, str)
    assert __version__


def test_public_exports_include_domain_functions() -> None:
    """Verify the public API advertises speech-domain functions."""
    assert "transcribe" in __all__
    assert "repair_subtitles" in __all__
    assert "dub_plan" in __all__
