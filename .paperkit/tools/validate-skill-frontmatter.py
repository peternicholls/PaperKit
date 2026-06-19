#!/usr/bin/env python3
"""
Validate SKILL.md frontmatter against skill-frontmatter-schema.json.

This script validates Agent Skills in the .paperkit/_cfg/skills/ directory,
ensuring SKILL.md files conform to the agentskills.io specification.

Usage:
    python validate-skill-frontmatter.py [--path PATH] [--all] [--ci] [--verbose]

Options:
    --path PATH    Validate a specific skill directory
    --all          Validate all skills in .paperkit/_cfg/skills/
    --ci           Exit with non-zero code on validation errors
    --verbose      Show detailed output including successful validations
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    print("Error: jsonschema is required. Install with: pip install jsonschema")
    sys.exit(1)


# ANSI color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def colorize(text: str, color: str) -> str:
    """Add ANSI color codes to text."""
    return f"{color}{text}{Colors.RESET}"


def find_project_root() -> Path:
    """Find the project root by looking for .paperkit directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / '.paperkit').is_dir():
            return current
        current = current.parent
    # Fallback to current directory
    return Path.cwd()


def load_schema(project_root: Path) -> dict:
    """Load the skill frontmatter schema."""
    schema_path = project_root / '.paperkit' / '_cfg' / 'schemas' / 'skill-frontmatter-schema.json'
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_frontmatter(skill_md_path: Path) -> tuple[dict | None, str | None]:
    """
    Extract YAML frontmatter from SKILL.md file.

    Returns:
        Tuple of (frontmatter_dict, error_message)
    """
    if not skill_md_path.exists():
        return None, f"SKILL.md not found: {skill_md_path}"

    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for frontmatter delimiters
    if not content.startswith('---'):
        return None, "SKILL.md must start with YAML frontmatter (---)"

    # Find the closing delimiter
    lines = content.split('\n')
    end_index = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            end_index = i
            break

    if end_index is None:
        return None, "SKILL.md frontmatter missing closing delimiter (---)"

    # Parse YAML
    frontmatter_text = '\n'.join(lines[1:end_index])
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if frontmatter is None:
            return None, "SKILL.md frontmatter is empty"
        return frontmatter, None
    except yaml.YAMLError as e:
        return None, f"Invalid YAML in frontmatter: {e}"


def validate_skill(skill_dir: Path, schema: dict, verbose: bool = False) -> list[str]:
    """
    Validate a single skill directory.

    Returns:
        List of error messages (empty if valid)
    """
    errors: list[str] = []
    skill_name = skill_dir.name
    skill_md = skill_dir / 'SKILL.md'

    # Extract frontmatter
    frontmatter, error = extract_frontmatter(skill_md)
    if error or frontmatter is None:
        errors.append(f"{skill_name}: {error or 'Empty frontmatter'}")
        return errors

    # Validate against schema
    try:
        validate(instance=frontmatter, schema=schema)
    except ValidationError as e:
        # Format the error message nicely
        path = '.'.join(str(p) for p in e.absolute_path) if e.absolute_path else 'root'
        errors.append(f"{skill_name}: Schema validation failed at '{path}': {e.message}")
        return errors

    # Additional validations

    # 1. Name must match directory name
    if frontmatter.get('name') != skill_name:
        errors.append(
            f"{skill_name}: Frontmatter 'name' ({frontmatter.get('name')}) "
            f"does not match directory name ({skill_name})"
        )

    # 2. Description should include trigger keywords (warning, not error)
    description = frontmatter.get('description', '')
    trigger_words = ['when', 'use', 'for', 'help']
    has_trigger = any(word in description.lower() for word in trigger_words)
    if not has_trigger and verbose:
        print(colorize(
            f"  Warning: {skill_name}: Description should include when to use the skill",
            Colors.YELLOW
        ))

    # 3. Check for SKILL.md body content
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find end of frontmatter
    lines = content.split('\n')
    end_index = 0
    found_start = False
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if found_start:
                end_index = i + 1
                break
            found_start = True

    body = '\n'.join(lines[end_index:]).strip()
    if len(body) < 100:
        errors.append(f"{skill_name}: SKILL.md body is too short (< 100 characters)")

    return errors


def validate_all_skills(project_root: Path, schema: dict, verbose: bool = False) -> tuple[int, int, list[str]]:
    """
    Validate all skills in the skills directory.

    Returns:
        Tuple of (total_count, error_count, error_messages)
    """
    skills_dir = project_root / '.paperkit' / '_cfg' / 'skills'
    if not skills_dir.exists():
        return 0, 1, [f"Skills directory not found: {skills_dir}"]

    all_errors = []
    total = 0

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith('.'):
            continue

        total += 1
        errors = validate_skill(skill_dir, schema, verbose)

        if errors:
            all_errors.extend(errors)
        elif verbose:
            print(colorize(f"  ✓ {skill_dir.name}", Colors.GREEN))

    return total, len(all_errors), all_errors


def main():
    parser = argparse.ArgumentParser(
        description='Validate SKILL.md frontmatter against schema'
    )
    parser.add_argument(
        '--path',
        type=str,
        help='Path to specific skill directory to validate'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Validate all skills in .paperkit/_cfg/skills/'
    )
    parser.add_argument(
        '--ci',
        action='store_true',
        help='Exit with non-zero code on errors (for CI)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    # Default to --all if no specific path given
    if not args.path and not args.all:
        args.all = True

    project_root = find_project_root()

    if args.verbose:
        print(colorize("SKILL.md Frontmatter Validator", Colors.BOLD))
        print(f"Project root: {project_root}")
        print()

    # Load schema
    try:
        schema = load_schema(project_root)
    except FileNotFoundError as e:
        print(colorize(f"Error: {e}", Colors.RED))
        sys.exit(1)

    # Validate
    if args.path:
        skill_path = Path(args.path)
        if not skill_path.is_absolute():
            skill_path = project_root / skill_path

        if args.verbose:
            print(f"Validating: {skill_path}")

        errors = validate_skill(skill_path, schema, args.verbose)
        total = 1
        error_count = len(errors)
    else:
        if args.verbose:
            print("Validating all skills...")
            print()

        total, error_count, errors = validate_all_skills(project_root, schema, args.verbose)

    # Report results
    print()
    if error_count == 0:
        print(colorize(f"✓ All {total} skill(s) passed validation", Colors.GREEN))
    else:
        print(colorize(f"✗ {error_count} error(s) in {total} skill(s):", Colors.RED))
        print()
        for error in errors:
            print(colorize(f"  • {error}", Colors.RED))

    # Exit code
    if args.ci and error_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
