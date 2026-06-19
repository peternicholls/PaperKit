#!/usr/bin/env python3
"""
Code Duplication Analyzer for Agent Instructions

Analyzes agent MD instruction files to measure code duplication and identify
common patterns that could be extracted into reusable skills.

This establishes a baseline measurement for Phase 1 Success Criteria SC-007.

Usage:
    python3 measure-duplication.py [--verbose] [--output report.md]

Output:
    Generates a duplication report showing:
    - Overall duplication percentage
    - Common repeated patterns
    - Recommendations for skill extraction
"""

import sys
import argparse
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from collections import Counter, defaultdict
from datetime import datetime


# Color codes for terminal output
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'
    BOLD = '\033[1m'


def color(text: str, color_code: str) -> str:
    """Wrap text in color codes."""
    return f"{color_code}{text}{Colors.NC}"


def find_project_root() -> Optional[Path]:
    """Find the project root by looking for .paperkit/ directory."""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / ".paperkit").is_dir():
            return path
    return None


def get_agent_files(project_root: Path) -> List[Path]:
    """Get all agent MD instruction files."""
    files = []
    agent_dirs = [
        project_root / ".paperkit/core/agents",
        project_root / ".paperkit/specialist/agents"
    ]
    for d in agent_dirs:
        if d.is_dir():
            files.extend(d.glob("*.md"))
    return sorted(files)


def normalize_text(text: str) -> str:
    """Normalize text for comparison (lowercase, strip whitespace, normalize spaces)."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def extract_sections(content: str) -> Dict[str, str]:
    """Extract markdown sections from content."""
    sections = {}
    current_section = "preamble"
    current_content = []

    for line in content.split('\n'):
        if line.startswith('#'):
            if current_content:
                sections[current_section] = '\n'.join(current_content)
            # Extract section title
            match = re.match(r'^#+\s+(.+)$', line)
            if match:
                current_section = normalize_text(match.group(1))
            current_content = [line]
        else:
            current_content.append(line)

    if current_content:
        sections[current_section] = '\n'.join(current_content)

    return sections


def compute_ngrams(text: str, n: int = 5) -> List[str]:
    """Compute n-word grams from text."""
    words = text.split()
    if len(words) < n:
        return []
    return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]


def find_duplicate_ngrams(files: List[Path], n: int = 5) -> Dict[str, List[Tuple[str, int]]]:
    """Find n-grams that appear in multiple files."""
    ngram_locations = defaultdict(list)

    for file_path in files:
        content = file_path.read_text(encoding='utf-8')
        normalized = normalize_text(content)
        ngrams = compute_ngrams(normalized, n)

        seen_in_file = set()
        for i, ngram in enumerate(ngrams):
            if ngram not in seen_in_file:
                ngram_locations[ngram].append((file_path.name, i))
                seen_in_file.add(ngram)

    # Filter to only duplicates (appear in 2+ files)
    duplicates = {k: v for k, v in ngram_locations.items() if len(v) >= 2}
    return duplicates


def find_common_sections(files: List[Path]) -> Dict[str, List[str]]:
    """Find section titles that appear in multiple files."""
    section_files = defaultdict(list)

    for file_path in files:
        content = file_path.read_text(encoding='utf-8')
        sections = extract_sections(content)
        for section_name in sections.keys():
            section_files[section_name].append(file_path.name)

    # Filter to common sections (in 2+ files)
    common = {k: v for k, v in section_files.items() if len(v) >= 2}
    return common


def compute_jaccard_similarity(text1: str, text2: str) -> float:
    """Compute Jaccard similarity between two texts."""
    words1 = set(normalize_text(text1).split())
    words2 = set(normalize_text(text2).split())

    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0

    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return intersection / union


def find_similar_files(files: List[Path], threshold: float = 0.3) -> List[Tuple[str, str, float]]:
    """Find pairs of files with high similarity."""
    similarities = []

    contents = {}
    for f in files:
        contents[f.name] = f.read_text(encoding='utf-8')

    file_names = list(contents.keys())
    for i in range(len(file_names)):
        for j in range(i + 1, len(file_names)):
            sim = compute_jaccard_similarity(
                contents[file_names[i]],
                contents[file_names[j]]
            )
            if sim >= threshold:
                similarities.append((file_names[i], file_names[j], sim))

    return sorted(similarities, key=lambda x: x[2], reverse=True)


def count_total_words(files: List[Path]) -> Tuple[int, Dict[str, int]]:
    """Count total words across all files."""
    total = 0
    per_file = {}

    for f in files:
        content = f.read_text(encoding='utf-8')
        words = len(content.split())
        per_file[f.name] = words
        total += words

    return total, per_file


def estimate_duplication_percentage(
    files: List[Path],
    duplicates: Dict[str, List[Tuple[str, int]]],
    n: int = 5
) -> float:
    """Estimate percentage of duplicated content."""
    total_words, _ = count_total_words(files)

    # Each duplicate n-gram represents n words appearing in multiple places
    # We count unique n-grams that appear in 2+ files
    duplicated_words = len(duplicates) * n

    # This is a rough estimate - actual duplication may be higher or lower
    if total_words == 0:
        return 0.0

    return min(100.0, (duplicated_words / total_words) * 100)


def identify_skill_candidates(
    common_sections: Dict[str, List[str]],
    duplicates: Dict[str, List[Tuple[str, int]]]
) -> List[Dict]:
    """Identify potential skills based on duplication patterns."""
    candidates = []

    # Common sections are good skill candidates
    for section_name, files in common_sections.items():
        if len(files) >= 3 and section_name not in ['preamble']:
            candidates.append({
                'type': 'section',
                'name': section_name,
                'occurrences': len(files),
                'files': files,
                'recommendation': f"Extract '{section_name}' into a reusable skill"
            })

    # Frequently duplicated phrases
    phrase_counts = Counter()
    for ngram, locations in duplicates.items():
        if len(locations) >= 3:
            phrase_counts[ngram] = len(locations)

    for phrase, count in phrase_counts.most_common(10):
        if count >= 3:
            candidates.append({
                'type': 'phrase',
                'name': phrase[:50] + '...' if len(phrase) > 50 else phrase,
                'occurrences': count,
                'recommendation': f"Extract common phrase pattern into skill"
            })

    return candidates


def generate_report(
    files: List[Path],
    total_words: int,
    word_counts: Dict[str, int],
    duplication_pct: float,
    similarities: List[Tuple[str, str, float]],
    common_sections: Dict[str, List[str]],
    skill_candidates: List[Dict],
    output_path: Optional[Path] = None
) -> str:
    """Generate a markdown duplication report."""
    report = []
    report.append("# Agent Instruction Code Duplication Report")
    report.append("")
    report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Purpose**: Baseline measurement for Phase 2 Skills Framework (SC-007)")
    report.append("")
    report.append("---")
    report.append("")

    # Summary
    report.append("## Summary")
    report.append("")
    report.append(f"| Metric | Value |")
    report.append(f"|--------|-------|")
    report.append(f"| Total Agent Files | {len(files)} |")
    report.append(f"| Total Words | {total_words:,} |")
    report.append(f"| Estimated Duplication | {duplication_pct:.1f}% |")
    report.append(f"| Similar File Pairs | {len(similarities)} |")
    report.append(f"| Common Sections | {len(common_sections)} |")
    report.append(f"| Skill Candidates | {len(skill_candidates)} |")
    report.append("")

    # File sizes
    report.append("## File Analysis")
    report.append("")
    report.append("| File | Words |")
    report.append("|------|-------|")
    for name, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
        report.append(f"| {name} | {count:,} |")
    report.append("")

    # Similar files
    if similarities:
        report.append("## File Similarity")
        report.append("")
        report.append("Files with >30% word overlap (Jaccard similarity):")
        report.append("")
        report.append("| File 1 | File 2 | Similarity |")
        report.append("|--------|--------|------------|")
        for f1, f2, sim in similarities[:10]:
            report.append(f"| {f1} | {f2} | {sim:.1%} |")
        report.append("")

    # Common sections
    if common_sections:
        report.append("## Common Section Names")
        report.append("")
        report.append("Section names appearing in multiple agents:")
        report.append("")
        report.append("| Section | # Files | Files |")
        report.append("|---------|---------|-------|")
        for section, files_list in sorted(common_sections.items(), key=lambda x: len(x[1]), reverse=True):
            if len(files_list) >= 2:
                files_str = ', '.join(files_list[:3])
                if len(files_list) > 3:
                    files_str += f", +{len(files_list)-3} more"
                report.append(f"| {section} | {len(files_list)} | {files_str} |")
        report.append("")

    # Skill candidates
    if skill_candidates:
        report.append("## Recommended Skill Extractions")
        report.append("")
        report.append("Patterns that could be extracted into reusable skills:")
        report.append("")
        for i, candidate in enumerate(skill_candidates[:10], 1):
            report.append(f"### {i}. {candidate['name'][:40]}")
            report.append(f"- **Type**: {candidate['type']}")
            report.append(f"- **Occurrences**: {candidate['occurrences']}")
            report.append(f"- **Recommendation**: {candidate['recommendation']}")
            report.append("")

    # Next steps
    report.append("## Next Steps for Phase 2")
    report.append("")
    report.append("1. Review common sections for skill extraction candidates")
    report.append("2. Create skill definitions in `.paperkit/_cfg/skills/`")
    report.append("3. Refactor agent instructions to reference skills")
    report.append("4. Re-measure duplication after skill implementation")
    report.append("")
    report.append("---")
    report.append("")
    report.append("*This baseline report will be compared against Phase 2 results to measure improvement.*")

    report_text = '\n'.join(report)

    if output_path:
        output_path.write_text(report_text, encoding='utf-8')

    return report_text


def main():
    parser = argparse.ArgumentParser(
        description="Measure code duplication in agent instruction files"
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output report to file (default: print to stdout)'
    )

    args = parser.parse_args()

    project_root = find_project_root()
    if not project_root:
        print(color("Error: Could not find PaperKit project root", Colors.RED))
        sys.exit(1)

    print(color("╔═══════════════════════════════════════════════════╗", Colors.CYAN))
    print(color("║    Agent Instruction Duplication Analyzer         ║", Colors.CYAN))
    print(color("╚═══════════════════════════════════════════════════╝", Colors.CYAN))
    print(color(f"Project: {project_root}", Colors.BLUE))

    # Get agent files
    print(color("\nAnalyzing agent instruction files...", Colors.BOLD))
    files = get_agent_files(project_root)
    print(f"  Found {len(files)} agent files")

    if not files:
        print(color("No agent files found", Colors.YELLOW))
        sys.exit(0)

    # Word count
    print("  Counting words...")
    total_words, word_counts = count_total_words(files)
    print(f"  Total words: {total_words:,}")

    # Find duplicates
    print("  Finding duplicate patterns...")
    duplicates = find_duplicate_ngrams(files, n=5)
    print(f"  Found {len(duplicates)} duplicated 5-grams")

    # Estimate duplication
    duplication_pct = estimate_duplication_percentage(files, duplicates)
    print(f"  Estimated duplication: {duplication_pct:.1f}%")

    # Find similar files
    print("  Computing file similarities...")
    similarities = find_similar_files(files, threshold=0.3)
    print(f"  Found {len(similarities)} similar file pairs")

    # Find common sections
    print("  Analyzing section structure...")
    common_sections = find_common_sections(files)
    print(f"  Found {len(common_sections)} common section names")

    # Identify skill candidates
    print("  Identifying skill candidates...")
    skill_candidates = identify_skill_candidates(common_sections, duplicates)
    print(f"  Identified {len(skill_candidates)} potential skills")

    # Generate report
    print(color("\nGenerating report...", Colors.BOLD))
    output_path = None
    if args.output:
        output_path = Path(args.output)
    else:
        # Default output location
        output_path = project_root / ".paperkit/data/duplication-baseline.md"

    report = generate_report(
        files=files,
        total_words=total_words,
        word_counts=word_counts,
        duplication_pct=duplication_pct,
        similarities=similarities,
        common_sections=common_sections,
        skill_candidates=skill_candidates,
        output_path=output_path
    )

    if output_path:
        print(color(f"\n✓ Report written to: {output_path}", Colors.GREEN))

    # Summary
    print(color("\n" + "=" * 50, Colors.BOLD))
    print(color("BASELINE METRICS (Phase 1)", Colors.BOLD))
    print("=" * 50)
    print(f"  Total Files:        {len(files)}")
    print(f"  Total Words:        {total_words:,}")
    print(f"  Duplication:        {color(f'{duplication_pct:.1f}%', Colors.YELLOW)}")
    print(f"  Skill Candidates:   {len(skill_candidates)}")
    print(color("\n✓ Baseline measurement complete", Colors.GREEN))


if __name__ == "__main__":
    main()
