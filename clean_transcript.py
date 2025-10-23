import re
import sys
from pathlib import Path


def should_drop(line: str) -> bool:
    """Return True if the line is a non-content line (index, timestamp, or blank)."""
    if re.match(r"^\s*\d+\s*$", line):
        return True

    if re.match(r"^\s*\d{1,2}:\d{2}:\d{2}(?:[.,]\d{3})?\s*-->\s*\d{1,2}:\d{2}:\d{2}(?:[.,]\d{3})?\s*$", line):
        return True

    if re.match(r"^\s*\d{1,2}:\d{2}:\d{2}(?:[.,]\d{3})?\s*$", line):
        return True

    if re.match(r"^\s*$", line):
        return True

    return False


def clean_file(input_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with input_path.open("r", encoding="utf-8", errors="replace") as fin, \
            output_path.open("w", encoding="utf-8", errors="replace") as fout:
        for raw_line in fin:
            if not should_drop(raw_line):
                fout.write(raw_line)


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print(
            "Usage: clean_transcript.py <input_txt> [<output_txt>]",
            file=sys.stderr,
        )
        return 2

    input_path = Path(argv[1]).expanduser().resolve()
    if len(argv) == 3:
        output_path = Path(argv[2]).expanduser().resolve()
    else:
        output_path = input_path.with_name(f"{input_path.stem}_clean{input_path.suffix}")

    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        return 1

    clean_file(input_path, output_path)
    print(f"Wrote cleaned transcript to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))


#python3 /Users/sofiaandreoli/Desktop/transcript/clean_transcript.py /Users/sofiaandreoli/Desktop/transcript/clase.txt