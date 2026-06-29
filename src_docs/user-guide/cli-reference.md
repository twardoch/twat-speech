# CLI Reference

`twat-speech` ships a [Fire](https://github.com/google/python-fire)-based CLI. Invoke it via:

```bash
python -m twat_speech <command> [args]
# or, after pip install:
twat-speech <command> [args]
```

## Commands

### `version`

Print the installed package version.

```bash
twat-speech version
# 2.7.9
```

Dedicated entry point: `twat-speech-version`

---

### `transcribe`

Transcribe an audio file to text via the configured `twat_genai` provider.

```
twat-speech transcribe AUDIO_PATH [--preprocess]
```

| Argument | Type | Default | Description |
|---|---|---|---|
| `audio_path` | `str` | required | Path to the audio file |
| `--preprocess` | `bool` | `False` | Resample to 16 kHz via `twat_audio` first |

Dedicated entry point: `twat-speech-transcribe`

---

### `tts`

Synthesize text to speech via the configured `twat_genai` provider.

```
twat-speech tts TEXT [OUTPUT_PATH]
```

| Argument | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | required | Text to synthesize |
| `output_path` | `str` | `None` | Save audio to this path; omit to use provider default |

Dedicated entry point: `twat-speech-tts`

---

### `repair-srt`

Read an SRT file, normalize timestamps and block indices, write repaired output.

```
twat-speech repair-srt INPUT_PATH [OUTPUT_PATH]
```

| Argument | Type | Default | Description |
|---|---|---|---|
| `input_path` | `str` | required | Input `.srt` file |
| `output_path` | `str` | `None` | Write repaired SRT here; omit to print to stdout |

Dedicated entry point: `twat-speech-repair-srt`

---

### `dub`

Create a dubbing plan from a media file and an SRT subtitle file, printed as JSON.

```
twat-speech dub MEDIA SRT [--language LANG] [--audio-dir DIR]
```

| Argument | Type | Default | Description |
|---|---|---|---|
| `media` | `str` | required | Source media path |
| `srt` | `str` | required | SRT subtitle file path |
| `--language` | `str` | `"en"` | Target dubbing language code |
| `--audio-dir` | `str` | `"dub-audio"` | Output directory for segment audio files |

Dedicated entry point: `twat-speech-dub`

---

### `subtitle-transcript`

Extract plain transcript text from an SRT file (one line per cue, no timestamps).

```
twat-speech subtitle-transcript INPUT_PATH
```

| Argument | Type | Default | Description |
|---|---|---|---|
| `input_path` | `str` | required | Input `.srt` file |

Dedicated entry point: `twat-speech-subtitle-transcript`
