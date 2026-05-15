# twat-speech

`twat-speech` is the speech-domain package for the `twat` ecosystem. It owns transcription orchestration, subtitle repair, TTS calls, and deterministic dubbing plans while leaving provider clients in `twat_genai` and audio-file transforms in `twat_audio`.

## Python API

```python
from twat_speech import repair_subtitles, dub_plan, transcribe, synthesize

fixed = repair_subtitles(open("captions.srt").read())
plan = dub_plan("movie.mp4", fixed, language="de")
transcript = transcribe("speech.wav")
speech_file = synthesize("Hello", "hello.wav")
```

Implemented helpers:

- `parse_srt`, `format_srt`, `repair_srt`, `repair_subtitles`.
- `subtitle_transcript` for plain transcript extraction.
- `transcribe` and `synthesize` as thin `twat_genai` provider adapters.
- `dub_plan` / `create_dub_plan` for deterministic dubbing orchestration.
- optional `transcribe(..., preprocess=True)` delegates resampling to `twat_audio` before provider transcription.

## CLI

```bash
python -m twat_speech --help
python -m twat_speech repair-srt captions.srt captions.fixed.srt
python -m twat_speech dub movie.mp4 captions.fixed.srt --language de
python -m twat_speech transcribe speech.wav
python -m twat_speech synthesize "Hello" hello.wav
```

## Boundaries

- `twat_genai` owns speech providers for STT/TTS and future dubbing engines.
- `twat_audio` owns audio-file transforms such as resampling, trimming, normalization, and audio extraction.
- `twat_speech` owns speech-specific orchestration, subtitles, transcripts, and dubbing plans.

## Reference scripts

Reusable subtitle repair ideas from `srtmultifix.py`, extraction workflows from `mkv2srt.py`, and planning ideas from `vidpredub.py`/`viddub-*` are represented here as package APIs. Provider-specific or workstation-specific batch dubbing scripts remain in `reference/bin-img-vid/` because they combine local credentials, shell glue, and one-off media workflows.
