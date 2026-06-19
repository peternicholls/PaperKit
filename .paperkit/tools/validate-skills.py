#!/usr/bin/env python3
"""
PaperKit Skill Validator

Validates the PaperKit skill system for:
1. Schema compliance of all YAML skill definitions
2. Duplicate skill names across files
3. Prerequisite reference integrity (skills/tools exist)
4. Circular dependency detection
5. Maximum depth validation (5 levels)
6. Agent reference validation
7. Manifest consistency

Usage:
    python3 validate-skills.py [--ci] [--verbose]

Options:
    --ci       Exit with non-zero code on any error
    --verbose  Show detailed validation information

Exit codes:
    0 = All checks passed
    1 = Validation errors found
"""

import sys
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

# Maximum allowed skill composition depth
MAX_SKILL_DEPTH = 5

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


def load_yaml_file(yaml_path: Path) -> Optional[Dict]:
    """Load YAML file."""
    try:
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(color(f"  Error loading {yaml_path.name}: {e}", Colors.RED))
        return None


def validate_against_schema(data: Dict, schema: Dict, verbose: bool = False) -> List[str]:
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
        errors.append(f"  [{path}] {error.message}")

    return errors


def get_all_skills(project_root: Path) -> Dict[str, Dict]:
    """Load all skill definitions."""
    skills_dir = project_root / ".paperkit/_cfg/skills"
    skills = {}

    if not skills_dir.exists():
        return skills

    for yaml_file in skills_dir.glob("*.yaml"):
        data = load_yaml_file(yaml_file)
        if data and 'name' in data:
            skills[data['name']] = data

    return skills


def get_all_tools(project_root: Path) -> Set[str]:
    """Get all tool names from tool manifest."""
    manifest_path = project_root / ".paperkit/_cfg/tool-manifest.yaml"
    manifest = load_yaml_file(manifest_path)

    if not manifest or 'tools' not in manifest:
        return set()

    return {tool['name'] for tool in manifest['tools']}


def get_all_agents(project_root: Path) -> Set[str]:
    """Get all agent names from agent manifest."""
    manifest_path = project_root / ".paperkit/_cfg/agent-manifest.yaml"
    manifest = load_yaml_file(manifest_path)

    if not manifest or 'agents' not in manifest:
        return set()

    return {agent['name'] for agent in manifest['agents']}


def check_yaml_schema_compliance(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Validate all YAML skill files against schema."""
    schema_path = project_root / ".paperkit/_cfg/schemas/skill-schema.json"
    skills_dir = project_root / ".paperkit/_cfg/skills"

    if not skills_dir.exists():
        print(color("\n1. YAML Schema Compliance", Colors.BOLD))
        print("-" * 50)
        print(color("⚠ Skills directory not found (will be created)", Colors.YELLOW))
        return 0, 0, []

    schema = load_json_schema(schema_path)
    if not schema:
        return 0, 1, ["Skill schema file not found"]

    print(color("\n1. YAML Schema Compliance", Colors.BOLD))
    print("-" * 50)

    passed = 0
    failed = 0
    all_errors = []

    yaml_files = list(skills_dir.glob("*.yaml"))
    if not yaml_files:
        print(color("⚠ No skill files found yet", Colors.YELLOW))
        return 0, 0, []

    for yaml_file in sorted(yaml_files):
        data = load_yaml_file(yaml_file)
        if data is None:
            failed += 1
            all_errors.append(f"{yaml_file.name}: Failed to load")
            continue

        errors = validate_against_schema(data, schema, verbose)

        if errors:
            failed += 1
            print(color(f"✗ {yaml_file.name}", Colors.RED))
            for err in errors:
                print(color(err, Colors.RED))
                all_errors.append(f"{yaml_file.name}: {err}")
        else:
            passed += 1
            if verbose:
                print(color(f"✓ {yaml_file.name}", Colors.GREEN))

    if not verbose and passed > 0:
        print(color(f"✓ {passed} skill files valid", Colors.GREEN))

    return passed, failed, all_errors


def check_duplicate_names(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Check for duplicate skill names."""
    skills_dir = project_root / ".paperkit/_cfg/skills"

    print(color("\n2. Duplicate Skill Name Check", Colors.BOLD))
    print("-" * 50)

    if not skills_dir.exists():
        print(color("⚠ Skills directory not found", Colors.YELLOW))
        return 0, 0, []

    names: Dict[str, List[str]] = {}
    errors = []

    for yaml_file in sorted(skills_dir.glob("*.yaml")):
        data = load_yaml_file(yaml_file)
        if data and 'name' in data:
            name = data['name']
            if name not in names:
                names[name] = []
            names[name].append(yaml_file.name)

    if not names:
        print(color("⚠ No skills found yet", Colors.YELLOW))
        return 0, 0, []

    duplicates = {k: v for k, v in names.items() if len(v) > 1}

    if duplicates:
        for name, files in duplicates.items():
            msg = f"Duplicate name '{name}' in: {', '.join(files)}"
            print(color(f"✗ {msg}", Colors.RED))
            errors.append(msg)
        return 0, len(duplicates), errors
    else:
        print(color(f"✓ No duplicate skill names found ({len(names)} unique)", Colors.GREEN))
        return len(names), 0, []


def check_prerequisite_references(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Check that skill prerequisites reference existing skills/tools."""
    print(color("\n3. Prerequisite Reference Integrity", Colors.BOLD))
    print("-" * 50)

    skills = get_all_skills(project_root)
    tools = get_all_tools(project_root)

    if not skills:
        print(color("⚠ No skills found yet", Colors.YELLOW))
        return 0, 0, []

    skill_names = set(skills.keys())
    valid = 0
    invalid = 0
    errors = []

    for skill_name, skill_data in skills.items():
        prereqs = skill_data.get('prerequisites', [])
        skill_valid = True

        for prereq in prereqs:
            prereq_type = prereq.get('type')
            prereq_name = prereq.get('name')

            if prereq_type == 'skill' and prereq_name not in skill_names:
                msg = f"{skill_name}: Skill prerequisite '{prereq_name}' not found"
                print(color(f"✗ {msg}", Colors.RED))
                errors.append(msg)
                skill_valid = False
            elif prereq_type == 'tool' and prereq_name not in tools:
                msg = f"{skill_name}: Tool prerequisite '{prereq_name}' not found"
                print(color(f"✗ {msg}", Colors.RED))
                errors.append(msg)
                skill_valid = False

        if skill_valid:
            valid += 1
            if verbose:
                print(color(f"✓ {skill_name}: All prerequisites valid", Colors.GREEN))

    if not verbose and valid > 0 and invalid == 0:
        print(color(f"✓ All {valid} skills have valid prerequisites", Colors.GREEN))

    return valid, invalid, errors


def check_circular_dependencies(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Check for circular dependencies in skill prerequisites."""
    print(color("\n4. Circular Dependency Check", Colors.BOLD))
    print("-" * 50)

    skills = get_all_skills(project_root)

    if not skills:
        print(color("⚠ No skills found yet", Colors.YELLOW))
        return 0, 0, []

    # Build dependency graph
    deps: Dict[str, Set[str]] = defaultdict(set)
    for skill_name, skill_data in skills.items():
        for prereq in skill_data.get('prerequisites', []):
            if prereq.get('type') == 'skill':
                deps[skill_name].add(prereq.get('name'))

    # DFS to detect cycles
    def has_cycle(node: str, visited: Set[str], rec_stack: Set[str], path: List[str]) -> Optional[List[str]]:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in deps.get(node, set()):
            if neighbor not in visited:
                cycle_path = has_cycle(neighbor, visited, rec_stack, path)
                if cycle_path:
                    return cycle_path
            elif neighbor in rec_stack:
                # Found cycle
                cycle_start = path.index(neighbor)
                return path[cycle_start:] + [neighbor]

        path.pop()
        rec_stack.remove(node)
        return None

    errors = []
    cycles_found = set()

    for skill_name in skills:
        if skill_name not in cycles_found:
            cycle_path = has_cycle(skill_name, set(), set(), [])
            if cycle_path:
                cycle_str = " -> ".join(cycle_path)
                msg = f"Circular dependency detected: {cycle_str}"
                print(color(f"✗ {msg}", Colors.RED))
                errors.append(msg)
                cycles_found.update(cycle_path)

    if not errors:
        print(color(f"✓ No circular dependencies found", Colors.GREEN))
        return len(skills), 0, []

    return len(skills) - len(cycles_found), len(cycles_found), errors


def check_skill_depth(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Check that skill composition depth doesn't exceed maximum."""
    print(color("\n5. Skill Depth Validation", Colors.BOLD))
    print("-" * 50)

    skills = get_all_skills(project_root)

    if not skills:
        print(color("⚠ No skills found yet", Colors.YELLOW))
        return 0, 0, []

    # Build dependency graph
    deps: Dict[str, Set[str]] = defaultdict(set)
    for skill_name, skill_data in skills.items():
        for prereq in skill_data.get('prerequisites', []):
            if prereq.get('type') == 'skill':
                deps[skill_name].add(prereq.get('name'))

    # Calculate max depth for each skill
    def get_depth(skill_name: str, memo: Dict[str, int], visited: Set[str]) -> int:
        if skill_name in memo:
            return memo[skill_name]

        if skill_name in visited:
            return 0  # Cycle - handled separately

        visited.add(skill_name)

        prereq_depths = [get_depth(p, memo, visited) for p in deps.get(skill_name, set())]
        depth = 1 + max(prereq_depths, default=0)

        memo[skill_name] = depth
        visited.discard(skill_name)
        return depth

    errors = []
    memo: Dict[str, int] = {}
    valid = 0
    invalid = 0

    for skill_name in skills:
        depth = get_depth(skill_name, memo, set())

        if depth > MAX_SKILL_DEPTH:
            msg = f"{skill_name}: Depth {depth} exceeds maximum {MAX_SKILL_DEPTH}"
            print(color(f"✗ {msg}", Colors.RED))
            errors.append(msg)
            invalid += 1
        else:
            valid += 1
            if verbose:
                print(color(f"✓ {skill_name}: Depth {depth}", Colors.GREEN))

    if not verbose and valid > 0 and invalid == 0:
        print(color(f"✓ All {valid} skills within depth limit ({MAX_SKILL_DEPTH})", Colors.GREEN))

    return valid, invalid, errors


def check_agent_references(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Check that skill steps reference existing agents."""
    print(color("\n6. Agent Reference Validation", Colors.BOLD))
    print("-" * 50)

    skills = get_all_skills(project_root)
    agents = get_all_agents(project_root)

    if not skills:
        print(color("⚠ No skills found yet", Colors.YELLOW))
        return 0, 0, []

    valid = 0
    invalid = 0
    errors = []

    for skill_name, skill_data in skills.items():
        steps = skill_data.get('steps', [])
        skill_valid = True

        for i, step in enumerate(steps):
            agent = step.get('agent')
            if agent and agent not in agents:
                msg = f"{skill_name}: Step {i+1} references unknown agent '{agent}'"
                print(color(f"✗ {msg}", Colors.RED))
                errors.append(msg)
                skill_valid = False

        if skill_valid:
            valid += 1
            if verbose:
                print(color(f"✓ {skill_name}: All agent references valid", Colors.GREEN))

    if not verbose and valid > 0 and invalid == 0:
        print(color(f"✓ All {valid} skills have valid agent references", Colors.GREEN))

    return valid, invalid, errors


def check_manifest_consistency(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Check that manifest lists all skills in the skills directory."""
    manifest_path = project_root / ".paperkit/_cfg/skill-manifest.yaml"
    skills_dir = project_root / ".paperkit/_cfg/skills"

    print(color("\n7. Manifest Consistency", Colors.BOLD))
    print("-" * 50)

    if not manifest_path.exists():
        print(color("⚠ Skill manifest not found", Colors.YELLOW))
        return 0, 0, []

    if not skills_dir.exists():
        print(color("⚠ Skills directory not found", Colors.YELLOW))
        return 0, 0, []

    errors = []

    manifest = load_yaml_file(manifest_path)
    if not manifest or 'skills' not in manifest:
        msg = "Manifest not found or missing 'skills' key"
        print(color(f"✗ {msg}", Colors.RED))
        return 0, 1, [msg]

    # Get skill names from manifest
    manifest_names = {skill['name'] for skill in manifest['skills']}

    # Get skill names from YAML files
    yaml_names = set()
    for yaml_file in skills_dir.glob("*.yaml"):
        data = load_yaml_file(yaml_file)
        if data and 'name' in data:
            yaml_names.add(data['name'])

    if not yaml_names:
        print(color("⚠ No skill files found yet", Colors.YELLOW))
        return 0, 0, []

    # Check for skills in YAML but not in manifest
    missing_from_manifest = yaml_names - manifest_names
    # Check for skills in manifest but not in YAML
    missing_from_yaml = manifest_names - yaml_names

    issues = 0

    if missing_from_manifest:
        for name in sorted(missing_from_manifest):
            msg = f"Skill '{name}' in YAML but missing from manifest"
            print(color(f"✗ {msg}", Colors.RED))
            errors.append(msg)
        issues += len(missing_from_manifest)

    if missing_from_yaml:
        for name in sorted(missing_from_yaml):
            msg = f"Skill '{name}' in manifest but no YAML file"
            print(color(f"✗ {msg}", Colors.RED))
            errors.append(msg)
        issues += len(missing_from_yaml)

    if issues == 0:
        print(color(f"✓ Manifest matches skills directory ({len(yaml_names)} skills)", Colors.GREEN))
        return len(yaml_names), 0, []

    return len(yaml_names) - issues, issues, errors


def main():
    parser = argparse.ArgumentParser(description="PaperKit Skill Validator")
    parser.add_argument('--ci', action='store_true', help='Exit with error code on failures')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    args = parser.parse_args()

    project_root = find_project_root()
    if not project_root:
        print(color("Error: Could not find PaperKit project root", Colors.RED))
        sys.exit(1)

    print(color("╔═══════════════════════════════════════════════════╗", Colors.CYAN))
    print(color("║        PaperKit Skill Validator                   ║", Colors.CYAN))
    print(color("╚═══════════════════════════════════════════════════╝", Colors.CYAN))
    print(color(f"Project: {project_root}", Colors.BLUE))
    print(color(f"Max Skill Depth: {MAX_SKILL_DEPTH}", Colors.BLUE))

    total_passed = 0
    total_failed = 0
    all_errors = []

    # Run all checks
    checks = [
        check_yaml_schema_compliance,
        check_duplicate_names,
        check_prerequisite_references,
        check_circular_dependencies,
        check_skill_depth,
        check_agent_references,
        check_manifest_consistency,
    ]

    for check_func in checks:
        passed, failed, errors = check_func(project_root, args.verbose)
        total_passed += passed
        total_failed += failed
        all_errors.extend(errors)

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
        print(color("\n✓ All checks passed!", Colors.GREEN))

    sys.exit(0)


if __name__ == "__main__":
    main()
