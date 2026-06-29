---
this_file: CHANGELOG.md
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- MkDocs Material documentation site (`mkdocs.yml` + `src_docs/`) covering
  installation, quick-start, CLI reference, subtitle repair, dubbing plans, and
  full API reference.
- `src_docs/` directory with pages: index, getting-started, user-guide, api, about.

## [v2.7.9] - 2026-06-29

### Added

- Full implementation of `subtitles.py`: `normalize_timestamp`, `parse_srt`,
  `format_srt`, `repair_srt` with robust handling of CRLF, dot-millisecond
  separators, short hour fields, and non-consecutive block indices.
- `SubtitleCue` frozen dataclass for typed cue representation.
- `dubbing.py`: `DubSegment`, `DubPlan` frozen dataclasses and `create_dub_plan`
  that maps SRT cues to deterministic `{audio_dir}/{index:04d}-{language}.wav` paths.
- `providers.py`: lazy-import adapters `transcribe` / `synthesize` delegating to
  `twat_genai.transcribe_audio` / `twat_genai.synthesize_speech` with clear
  `RuntimeError` / `NotImplementedError` messages when the provider is absent.
- `twat_speech.py` domain API: `transcribe` (with optional `twat_audio` preprocessing),
  `synthesize`, `repair_subtitles`, `subtitle_transcript`, `dub_plan`.
- Fire-based CLI in `__main__.py` with subcommands: `version`, `transcribe`, `tts`,
  `repair-srt`, `dub`, `subtitle-transcript`; dedicated entry-point functions for each.
- Full public `__all__` in `__init__.py` re-exporting all types and functions.
- `py.typed` marker for PEP 561 compliance.
- Test suite: 15 tests across `test_twat_speech.py`, `test_speech_domain.py`,
  `test_cli.py` — all passing with no external dependencies required.
- `pyproject.toml` with hatchling + hatch-vcs, ruff, mypy, pytest matrix for
  Python 3.10–3.12.

## [v0.0.1] - 2025-02-15

### Added

- Initial release of the twat-speech package.
- Basic project structure with modern Python packaging (PEP 621 compliance).
- Development workflow using Hatch.
- Type hints and runtime type checking setup.
- Test suite configuration.
- CI/CD configuration in `.github` directory.
- Basic documentation in `README.md`.

### Changed

- Restructured source code: moved `twat_speech.py` into proper package structure.
- Updated `.gitignore` with comprehensive Python-specific ignores.

[Unreleased]: https://github.com/twardoch/twat-speech/compare/v2.7.9...HEAD
[v2.7.9]: https://github.com/twardoch/twat-speech/compare/v0.0.1...v2.7.9
[v0.0.1]: https://github.com/twardoch/twat-speech/releases/tag/v0.0.1
