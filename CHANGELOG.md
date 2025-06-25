# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `PLAN.md` for outlining project streamlining tasks.
- `TODO.md` for tracking progress of streamlining tasks.
- Added type hints to test functions in `tests/test_twat_speech.py`.
- Expanded assertions in `tests/test_twat_speech.py` for `process_data` function.
- Added `llms.txt` to `.gitignore`.

### Changed
- Updated `.cursor/rules/cleanup.mdc` to recommend `hatch` and `git` workflows instead of `cleanup.py`.
- Refined a debug log message in `src/twat_speech/twat_speech.py`.
- Modified `src/twat_speech/__init__.py` to use absolute imports to comply with project linting rules (`TID252`).
- Ensured all tests, linting (Ruff), and type checks (Mypy) pass using `hatch` commands.
- Regenerated `llms.txt` with latest changes.

### Removed
- `cleanup.py` script, as its functionality is better covered by `hatch`, `git`, and other standard tools.
- `VERSION.txt` (obsolete due to `hatch-vcs`).
- `REPO_CONTENT.txt` (obsolete, `llms.txt` is the preferred AI-consumable file).
- `CLEANUP.txt` (log file for the removed `cleanup.py`).
- (Confirmed `package.toml` was not present to remove).

[Unreleased]: https://github.com/twardoch/twat-speech/compare/v0.0.1...HEAD
<!-- Adjust v0.0.1 if the latest tag is different, or remove comparison if no tags exist yet. If no tags, this can be removed or pointed to the initial commit. -->
