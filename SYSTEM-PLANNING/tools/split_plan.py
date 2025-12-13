#!/usr/bin/env python3
"""
split_plan.py

Utility script to split the monolithic IMPLEMENTATION-PLAN.md into per-phase markdown files.

Features:
- Detects phase headings matching "## Phase <number>: <title>".
- Writes each phase to phases/phase-XX-<slug>.md (configurable).
- Supports dry-run mode to preview outputs without writing files.
- Refuses to overwrite existing files unless --overwrite is provided.

Usage examples:
  python tools/split_plan.py                         # split using defaults
  python tools/split_plan.py --dry-run               # show what would be written
  python tools/split_plan.py --input ../path.md      # custom input file
  python tools/split_plan.py --output ../phases      # custom output directory
  python tools/split_plan.py --prefix plan- --overwrite
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

PHASE_HEADING_RE = re.compile(r"^##\s+Phase\s+(\d+):\s*(.+)$")


@dataclass
class Phase:
    number: int
    title: str
    lines: List[str]

    @property
    def slug(self) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", self.title.strip().lower()).strip("-")
        return slug or "phase"

    def filename(self, prefix: str) -> str:
        return f"{prefix}{self.number:02d}-{self.slug}.md"

    def render(self) -> str:
        rendered = []
        heading_replaced = False
        for line in self.lines:
            if not heading_replaced and line.startswith("## Phase"):
                rendered.append(f"# Phase {self.number}: {self.title}\n")
                heading_replaced = True
            else:
                rendered.append(line)
        if not heading_replaced:
            rendered.insert(0, f"# Phase {self.number}: {self.title}\n")
        return "".join(rendered)


def parse_phases(text: str) -> Tuple[List[str], List[Phase], List[str]]:
    lines = text.splitlines(keepends=True)
    phases: List[Phase] = []
    preamble: List[str] = []
    tail: List[str] = []

    current_lines: List[str] = []
    current_num: int | None = None
    current_title: str | None = None
    seen_first_phase = False

    for line in lines:
        match = PHASE_HEADING_RE.match(line)
        if match:
            if current_num is not None and current_title is not None:
                phases.append(Phase(number=current_num, title=current_title, lines=current_lines))
                current_lines = []
            current_num = int(match.group(1))
            current_title = match.group(2).strip()
            seen_first_phase = True
            current_lines.append(line)
        else:
            if seen_first_phase:
                current_lines.append(line)
            else:
                preamble.append(line)

    if current_num is not None and current_title is not None:
        phases.append(Phase(number=current_num, title=current_title, lines=current_lines))
    else:
        tail = current_lines

    return preamble, phases, tail


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def split_plan(input_path: Path, output_dir: Path, prefix: str, overwrite: bool, dry_run: bool) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    text = input_path.read_text(encoding="utf-8")
    preamble, phases, tail = parse_phases(text)

    if not phases:
        raise ValueError("No phases found. Expected headings like '## Phase 1: <title>'.")

    ensure_output_dir(output_dir)

    writes: List[Tuple[Path, str]] = []
    for phase in phases:
        target = output_dir / phase.filename(prefix)
        content = phase.render()
        writes.append((target, content))

    if dry_run:
        print("Dry run: would create the following files:\n")
        for target, _ in writes:
            print(f"- {target}")
        return

    for target, content in writes:
        if target.exists() and not overwrite:
            raise FileExistsError(f"Refusing to overwrite existing file: {target}")
        target.write_text(content, encoding="utf-8")

    print("Wrote phase files:")
    for target, _ in writes:
        print(f"- {target}")

    if preamble:
        print("\nNote: Preamble content before the first phase was not written to per-phase files.")
    if tail:
        print("Note: Content after the last phase was not written to per-phase files.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Split IMPLEMENTATION-PLAN.md into per-phase files.")
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "IMPLEMENTATION-PLAN.md",
        help="Path to the implementation plan markdown file.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path(__file__).resolve().parent / "../phases",
        help="Directory to write per-phase files into.",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="phase-",
        help="Filename prefix for generated phase files.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting existing files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned outputs without writing files.",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        split_plan(
            input_path=args.input,
            output_dir=args.output.resolve(),
            prefix=args.prefix,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    sys.exit(main())
