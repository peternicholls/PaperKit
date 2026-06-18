#!/usr/bin/env python3
"""
Replace a few remaining em-dash subclauses with comma-style wording
in 02_perceptual_foundations.tex.

This is intentionally conservative: it only replaces specific, known
fragments so it won't touch label separators like 'L --- Lightness'.
"""

from pathlib import Path
import shutil

FILE = Path("/Users/peternicholls/code/colorJourneyPlayground/PaperKit/latex/sections/02_perceptual_foundations.tex")

REPLACEMENTS = [
    # 1) Computational Approximation: not perfect—local curvature remains—...
    (
        r"The approximation is not perfect—local curvature remains \citep{hong2024}—but the error is small enough for practical interpolation tasks.",
        r"The approximation is not perfect, local curvature remains \citep{hong2024}, but the error is small enough for practical interpolation tasks.",
    ),

    # 2) Physical Interpretation: distortions—either ... or ...
    (
        r"must introduce distortions—either uneven discrimination thresholds (as in CIELAB) or hue-dependent perceptual compression (as in HSV/HSL).",
        r"must introduce distortions, either uneven discrimination thresholds (as in CIELAB) or hue-dependent perceptual compression (as in HSV/HSL).",
    ),

    # 3) OKLab implications bullet: smooth transition—unlike RGB...
    (
        r"produces a perceptually smooth transition—unlike RGB, where intermediate steps may appear desaturated or shift unexpectedly in hue.",
        r"produces a perceptually smooth transition, unlike RGB, where intermediate steps may appear desaturated or shift unexpectedly in hue.",
    ),

    # 4) Unbounded OKLab: unbounded—it can represent...—the engine must...
    (
        r"Because OKLab is unbounded—it can represent colors outside any physical display gamut—the engine must include explicit gamut mapping (\S\ref{sec:gamut-problem}).",
        r"Because OKLab is unbounded, and can represent colors outside any physical display gamut, the engine must include explicit gamut mapping (\S\ref{sec:gamut-problem}).",
    ),

    # 5) Temporal lead-in: differences—a distinction...
    (
        r"processes color changes over time differently from spatial color differences—a distinction with important implications for velocity constraints.",
        r"processes color changes over time differently from spatial color differences, a distinction with important implications for velocity constraints.",
    ),

    # 6) Leading space before "A fundamental result..."
    (
        r"\n A fundamental result in perceptual color theory",
        r"\nA fundamental result in perceptual color theory",
    ),
]

def main() -> None:
    if not FILE.exists():
        raise SystemExit(f"File not found: {FILE}")

    text = FILE.read_text(encoding="utf-8")

    # Backup
    bak = FILE.with_suffix(FILE.suffix + ".bak")
    shutil.copy2(FILE, bak)

    applied = 0
    missing = []

    for old, new in REPLACEMENTS:
        if old in text:
            text = text.replace(old, new)
            applied += 1
        else:
            missing.append(old)

    if applied == 0:
        print("No changes applied (nothing matched). Backup kept at:", bak)
        return

    FILE.write_text(text, encoding="utf-8")
    print(f"Applied {applied} replacement(s). Backup written to: {bak}")

    if missing:
        print("\nThe following patterns did not match exactly (maybe already edited or wording differs):")
        for m in missing:
            print("-", m)

if __name__ == "__main__":
    main()