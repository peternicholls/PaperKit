#!/usr/bin/env python3
"""
SKILL.md Frontmatter Validator

Validates Agent Skills in SKILL.md format per agentskills.io specification.
Each skill must be in its own directory with a SKILL.md file containing
YAML frontmatter with required fields.

Usage:
    python3 validate-skill-md.py [--ci] [--verbose]

Options:
    --ci       Exit with non-zero code on any error
    --verbose  Show detailed validation information

Exit codes:
    0 = All checks passed
    1 = Validation errors found
"""

import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

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
        if (path / "paperkit").is_file():
            return path
    return None


def load_json_schema(schema_path: Path) -> Optional[Dict]:
    """Load JSON Schema from file."""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(color(f"Error loading schema {schema_path}: {e}", Colors.RED))
        return None


def extract_frontmatter(content: str) -> Tuple[Optional[str], str]:
    """
    Extract YAML frontmatter from markdown content.
    Returns (frontmatter_yaml, body) or (None, content) if no frontmatter.
    """
    # Match frontmatter between --- delimiters at start of file
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if match:
        return match.group(1), match.group(2)
    return None, content


def parse_yaml_frontmatter(yaml_str: str) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Parse YAML frontmatter string.
    Returns (data, error_message) or (None, error_message) on failure.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML not installed"

    try:
        data = yaml.safe_load(yaml_str)
        return data, None
    except yaml.YAMLError as e:
        return None, str(e)


def validate_against_schema(data: Dict, schema: Dict) -> List[str]:
    """Validate data against JSON Schema. Returns list of error messages."""
    try:
        from jsonschema import Draft7Validator
    except ImportError:
        print(color("Error: jsonschema package not installed", Colors.RED))
        print("Install with: pip install 'jsonschema>=4.0'")
        sys.exit(1)

    errors = []
    validator = Draft7Validator(schema)

    for error in sorted(validator.iter_errors(data), key=lambda e: e.path):
        path = ".".join(str(p) for p in error.path) if error.path else "(root)"
        errors.append(f"[{path}] {error.message}")

    return errors


def validate_skill_name_matches_directory(skill_path: Path, frontmatter: Dict) -> List[str]:
    """Validate that skill name in frontmatter matches directory name."""
    errors = []

    if 'name' in frontmatter:
        expected_name = skill_path.parent.name  # Directory name
        actual_name = frontmatter['name']

        if actual_name != expected_name:
            errors.append(
                f"Skill name '{actual_name}' does not match directory name '{expected_name}'"
            )

    return errors


def validate_skill_directory_structure(skill_dir: Path, verbose: bool = False) -> List[str]:
    """Validate optional skill directory structure."""
    errors = []
    warnings = []

    # Check for optional directories (these are not errors, just informational)
    optional_dirs = ['scripts', 'references', 'assets']

    for dir_name in optional_dirs:
        dir_path = skill_dir / dir_name
        if dir_path.exists() and not dir_path.is_dir():
            errors.append(f"'{dir_name}' exists but is not a directory")

    return errors


def discover_skills(skills_dir: Path) -> List[Path]:
    """
    Discover all SKILL.md files in the skills directory.
    Skills are organized as: skills/{skill-name}/SKILL.md
    """
    skill_files = []

    if not skills_dir.exists():
        return []

    for entry in skills_dir.iterdir():
        if entry.is_dir():
            skill_md = entry / "SKILL.md"
            if skill_md.exists():
                skill_files.append(skill_md)

    return sorted(skill_files)


def check_skill_frontmatter(
    project_root: Path,
    verbose: bool = False
) -> Tuple[int, int, List[str]]:
    """Validate all SKILL.md files have valid frontmatter."""
    schema_path = project_root / ".paperkit/_cfg/schemas/skill-frontmatter-schema.json"
    skills_dir = project_root / ".paperkit/_cfg/skills"

    print(color("\n1. SKILL.md Frontmatter Validation", Colors.BOLD))
    print("-" * 50)

    schema = load_json_schema(schema_path)
    if not schema:
        return 0, 1, ["Skill frontmatter schema not found"]

    skill_files = discover_skills(skills_dir)

    if not skill_files:
        print(color("  No SKILL.md files found", Colors.YELLOW))
        return 0, 0, []

    passed = 0
    failed = 0
    all_errors = []

    for skill_path in skill_files:
        skill_name = skill_path.parent.name

        try:
            content = skill_path.read_text(encoding='utf-8')
        except Exception as e:
            failed += 1
            msg = f"{skill_name}: Failed to read: {e}"
            print(color(f"✗ {msg}", Colors.RED))
            all_errors.append(msg)
            continue

        # Extract frontmatter
        frontmatter_yaml, body = extract_frontmatter(content)

        if frontmatter_yaml is None:
            failed += 1
            msg = f"{skill_name}: No YAML frontmatter found (must start with ---)"
            print(color(f"✗ {msg}", Colors.RED))
            all_errors.append(msg)
            continue

        # Parse YAML
        frontmatter, parse_error = parse_yaml_frontmatter(frontmatter_yaml)

        if frontmatter is None:
            failed += 1
            msg = f"{skill_name}: Invalid YAML: {parse_error}"
            print(color(f"✗ {msg}", Colors.RED))
            all_errors.append(msg)
            continue

        # Validate against schema
        schema_errors = validate_against_schema(frontmatter, schema)

        # Validate name matches directory
        name_errors = validate_skill_name_matches_directory(skill_path, frontmatter)

        # Validate directory structure
        dir_errors = validate_skill_directory_structure(skill_path.parent, verbose)

        errors = schema_errors + name_errors + dir_errors

        if errors:
            failed += 1
            print(color(f"✗ {skill_name}/SKILL.md", Colors.RED))
            for err in errors:
                print(color(f"    {err}", Colors.RED))
                all_errors.append(f"{skill_name}: {err}")
        else:
            passed += 1
            if verbose:
                print(color(f"✓ {skill_name}/SKILL.md", Colors.GREEN))
                desc = frontmatter.get('description', '(no description)')[:60]
                print(color(f"    {desc}...", Colors.CYAN))

    if not verbose and passed > 0:
        print(color(f"✓ {passed} SKILL.md files valid", Colors.GREEN))

    return passed, failed, all_errors


def check_duplicate_skill_names(
    project_root: Path,
    verbose: bool = False
) -> Tuple[int, int, List[str]]:
    """Check for duplicate skill names."""
    skills_dir = project_root / ".paperkit/_cfg/skills"

    print(color("\n2. Duplicate Skill Name Check", Colors.BOLD))
    print("-" * 50)

    skill_files = discover_skills(skills_dir)

    names: Dict[str, List[str]] = {}
    errors = []

    for skill_path in skill_files:
        try:
            content = skill_path.read_text(encoding='utf-8')
            frontmatter_yaml, _ = extract_frontmatter(content)
            if frontmatter_yaml:
                frontmatter, _ = parse_yaml_frontmatter(frontmatter_yaml)
                if frontmatter and 'name' in frontmatter:
                    name = frontmatter['name']
                    if name not in names:
                        names[name] = []
                    names[name].append(skill_path.parent.name)
        except Exception:
            pass  # Already caught in frontmatter validation

    duplicates = {k: v for k, v in names.items() if len(v) > 1}

    if duplicates:
        for name, dirs in duplicates.items():
            msg = f"Duplicate skill name '{name}' in: {', '.join(dirs)}"
            print(color(f"✗ {msg}", Colors.RED))
            errors.append(msg)
        return 0, len(duplicates), errors
    else:
        print(color(f"✓ No duplicate skill names found ({len(names)} unique)", Colors.GREEN))
        return len(names), 0, []


def check_skill_body_content(
    project_root: Path,
    verbose: bool = False
) -> Tuple[int, int, List[str]]:
    """Check that SKILL.md files have meaningful body content."""
    skills_dir = project_root / ".paperkit/_cfg/skills"

    print(color("\n3. Skill Body Content Check", Colors.BOLD))
    print("-" * 50)

    skill_files = discover_skills(skills_dir)

    passed = 0
    failed = 0
    errors = []
    warnings = []

    MIN_BODY_LENGTH = 100  # Minimum characters in body

    for skill_path in skill_files:
        skill_name = skill_path.parent.name

        try:
            content = skill_path.read_text(encoding='utf-8')
            _, body = extract_frontmatter(content)

            body_stripped = body.strip()

            if len(body_stripped) < MIN_BODY_LENGTH:
                failed += 1
                msg = f"{skill_name}: Body too short ({len(body_stripped)} chars, minimum {MIN_BODY_LENGTH})"
                print(color(f"✗ {msg}", Colors.RED))
                errors.append(msg)
            else:
                passed += 1
                if verbose:
                    # Count approximate lines of instruction
                    lines = len([l for l in body_stripped.split('\n') if l.strip()])
                    print(color(f"✓ {skill_name}: {len(body_stripped)} chars, ~{lines} lines", Colors.GREEN))
        except Exception:
            pass  # Already caught in frontmatter validation

    if not verbose and passed > 0 and failed == 0:
        print(color(f"✓ All {passed} SKILL.md files have meaningful content", Colors.GREEN))

    return passed, failed, errors


def check_manifest_consistency(
    project_root: Path,
    verbose: bool = False
) -> Tuple[int, int, List[str]]:
    """Check skill manifest consistency with SKILL.md files."""
    manifest_path = project_root / ".paperkit/_cfg/skill-manifest.yaml"
    skills_dir = project_root / ".paperkit/_cfg/skills"

    print(color("\n4. Skill Manifest Consistency (Informational)", Colors.BOLD))
    print("-" * 50)

    if not manifest_path.exists():
        print(color("  Skill manifest not found (optional)", Colors.YELLOW))
        return 0, 0, []

    try:
        import yaml
        with open(manifest_path, 'r') as f:
            manifest = yaml.safe_load(f)
    except Exception as e:
        print(color(f"  Error loading manifest: {e}", Colors.YELLOW))
        return 0, 0, []

    # Get skill names from SKILL.md files
    skill_files = discover_skills(skills_dir)
    skillmd_names = {skill_path.parent.name for skill_path in skill_files}

    # Get skill names from manifest (only those with SKILL.md format)
    # Note: manifest may also contain YAML workflow entries
    manifest_skills = manifest.get('skills', [])

    print(color(f"  Found {len(skillmd_names)} SKILL.md directories", Colors.CYAN))
    print(color(f"  Manifest lists {len(manifest_skills)} entries", Colors.CYAN))

    # This is informational only - manifest may contain both Skills and Workflows
    print(color("  ✓ Note: Manifest may include both SKILL.md skills and YAML workflows", Colors.GREEN))

    return len(skillmd_names), 0, []


def print_progressive_disclosure_info(
    project_root: Path,
    verbose: bool = False
) -> None:
    """Print information about progressive disclosure token counts."""
    if not verbose:
        return

    skills_dir = project_root / ".paperkit/_cfg/skills"
    skill_files = discover_skills(skills_dir)

    print(color("\n5. Progressive Disclosure Analysis (Informational)", Colors.BOLD))
    print("-" * 50)

    # Rough token estimation: ~4 chars per token
    CHARS_PER_TOKEN = 4

    total_metadata_tokens = 0
    total_instruction_tokens = 0

    for skill_path in skill_files:
        skill_name = skill_path.parent.name

        try:
            content = skill_path.read_text(encoding='utf-8')
            frontmatter_yaml, body = extract_frontmatter(content)

            if frontmatter_yaml:
                metadata_tokens = len(frontmatter_yaml) // CHARS_PER_TOKEN
                instruction_tokens = len(body) // CHARS_PER_TOKEN

                total_metadata_tokens += metadata_tokens
                total_instruction_tokens += instruction_tokens

                print(color(
                    f"  {skill_name}: ~{metadata_tokens} metadata tokens, ~{instruction_tokens} instruction tokens",
                    Colors.CYAN
                ))
        except Exception:
            pass

    print(color(f"\n  Total metadata (loaded at startup): ~{total_metadata_tokens} tokens", Colors.BLUE))
    print(color(f"  Total instructions (loaded on demand): ~{total_instruction_tokens} tokens", Colors.BLUE))


def main():
    parser = argparse.ArgumentParser(description="SKILL.md Frontmatter Validator")
    parser.add_argument('--ci', action='store_true', help='Exit with error code on failures')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    args = parser.parse_args()

    project_root = find_project_root()
    if not project_root:
        print(color("Error: Could not find PaperKit project root", Colors.RED))
        sys.exit(1)

    print(color("╔═══════════════════════════════════════════════════╗", Colors.CYAN))
    print(color("║      PaperKit SKILL.md Frontmatter Validator      ║", Colors.CYAN))
    print(color("╚═══════════════════════════════════════════════════╝", Colors.CYAN))
    print(color(f"Project: {project_root}", Colors.BLUE))

    total_passed = 0
    total_failed = 0
    all_errors = []

    # Run all checks
    checks = [
        check_skill_frontmatter,
        check_duplicate_skill_names,
        check_skill_body_content,
        check_manifest_consistency,
    ]

    for check_func in checks:
        passed, failed, errors = check_func(project_root, args.verbose)
        total_passed += passed
        total_failed += failed
        all_errors.extend(errors)

    # Progressive disclosure analysis (informational only)
    print_progressive_disclosure_info(project_root, args.verbose)

    # Summary
    print(color("\n" + "=" * 50, Colors.BOLD))
    print(color("SUMMARY", Colors.BOLD))
    print("=" * 50)
    print(f"  Total Passed: {color(str(total_passed), Colors.GREEN)}")
    print(f"  Total Failed: {color(str(total_failed), Colors.RED if total_failed > 0 else Colors.GREEN)}")

    if total_failed > 0:
        print(color(f"\n⚠ {total_failed} issue(s) found", Colors.YELLOW))
        if args.ci:
            sys.exit(1)
    else:
        print(color("\n✓ All SKILL.md validation passed!", Colors.GREEN))

    sys.exit(0)


if __name__ == "__main__":
    main()
