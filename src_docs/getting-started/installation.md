# Installation

## Requirements

- Python 3.10 or later
- `twat >= 1.8.1` (installed automatically)

## Install from PyPI

```bash
pip install twat-speech
```

Or with `uv`:

```bash
uv add twat-speech
```

## Optional extras

| Extra | Installs | Use case |
|---|---|---|
| `audio` | `twat-audio[all]` | `transcribe(..., preprocess=True)` resampling |
| `all` | `twat` + `twat-audio[all]` | Full local pipeline |
| `docs` | mkdocs-material + mkdocstrings | Build this documentation |
| `dev` | ruff, mypy, pre-commit | Development |
| `test` | pytest, pytest-cov, pytest-xdist | Running tests |

Install an extra:

```bash
pip install "twat-speech[audio]"
```

## Provider dependencies

`twat_speech` calls `twat_genai` lazily for `transcribe()` and `synthesize()`. Install and configure `twat-genai` separately to use those functions:

```bash
pip install twat-genai
```

The subtitle and dubbing-plan functions (`repair_subtitles`, `dub_plan`, `parse_srt`, etc.) work without any provider dependency.

## Verify installation

```bash
python -m twat_speech version
```
