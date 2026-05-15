"""Command-line interface for twat-speech."""
# this_file: src/twat_speech/__main__.py

from __future__ import annotations

import argparse
from pathlib import Path

from twat_speech import dub_plan, repair_subtitles, synthesize, transcribe


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="twat-speech", description="Speech, subtitle, TTS, and dubbing helpers.")
    sub = parser.add_subparsers(dest="command")

    trans = sub.add_parser("transcribe", help="Transcribe audio through twat_genai.")
    trans.add_argument("audio")
    trans.add_argument("--preprocess", action="store_true")

    repair = sub.add_parser("repair-srt", help="Repair SRT text.")
    repair.add_argument("input")
    repair.add_argument("output", nargs="?")

    synth = sub.add_parser("synthesize", help="Synthesize speech through twat_genai.")
    synth.add_argument("text")
    synth.add_argument("output", nargs="?")

    dub = sub.add_parser("dub", help="Create a dubbing plan from an SRT file.")
    dub.add_argument("media")
    dub.add_argument("srt")
    dub.add_argument("--language", default="en")
    dub.add_argument("--audio-dir", default="dub-audio")
    return parser


def main() -> None:
    """Run the twat-speech CLI."""
    parser = _parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return
    if args.command == "transcribe":
        print(transcribe(args.audio, preprocess=args.preprocess))
    elif args.command == "repair-srt":
        repaired = repair_subtitles(Path(args.input).read_text())
        if args.output:
            Path(args.output).write_text(repaired)
        else:
            print(repaired, end="")
    elif args.command == "synthesize":
        print(synthesize(args.text, output_path=args.output))
    elif args.command == "dub":
        plan = dub_plan(args.media, Path(args.srt).read_text(), language=args.language, audio_dir=args.audio_dir)
        for segment in plan.segments:
            print(f"{segment.index}	{segment.start}	{segment.end}	{segment.audio_path}	{segment.text}")


if __name__ == "__main__":
    main()
