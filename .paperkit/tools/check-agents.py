#!/usr/bin/env python3
"""
Unified Agent System Checker

Validates the PaperKit agent system for:
1. Schema compliance of all YAML agent definitions
2. Duplicate agent names across files
3. Path reference integrity (YAML path fields point to existing files)
4. Manifest consistency

Usage:
    python3 check-agents.py [--ci] [--verbose]
    
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
from typing import Dict, List, Tuple, Optional

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


def check_yaml_schema_compliance(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Validate all YAML agent files against schema."""
    schema_path = project_root / ".paperkit/_cfg/schemas/agent-schema.json"
    agents_dir = project_root / ".paperkit/_cfg/agents"
    
    schema = load_json_schema(schema_path)
    if not schema:
        return 0, 1, ["Schema file not found"]
    
    print(color("\n1. YAML Schema Compliance", Colors.BOLD))
    print("-" * 50)
    
    passed = 0
    failed = 0
    all_errors = []
    
    for yaml_file in sorted(agents_dir.glob("*.yaml")):
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
        print(color(f"✓ {passed} YAML files valid", Colors.GREEN))
    
    return passed, failed, all_errors


def check_duplicate_names(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Check for duplicate agent names."""
    agents_dir = project_root / ".paperkit/_cfg/agents"
    
    print(color("\n2. Duplicate Agent Name Check", Colors.BOLD))
    print("-" * 50)
    
    names: Dict[str, List[str]] = {}
    errors = []
    
    for yaml_file in sorted(agents_dir.glob("*.yaml")):
        data = load_yaml_file(yaml_file)
        if data and 'name' in data:
            name = data['name']
            if name not in names:
                names[name] = []
            names[name].append(yaml_file.name)
    
    duplicates = {k: v for k, v in names.items() if len(v) > 1}
    
    if duplicates:
        for name, files in duplicates.items():
            msg = f"Duplicate name '{name}' in: {', '.join(files)}"
            print(color(f"✗ {msg}", Colors.RED))
            errors.append(msg)
        return 0, len(duplicates), errors
    else:
        print(color(f"✓ No duplicate agent names found ({len(names)} unique)", Colors.GREEN))
        return len(names), 0, []


def check_path_references(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Check that YAML path fields point to existing files."""
    agents_dir = project_root / ".paperkit/_cfg/agents"
    
    print(color("\n3. Path Reference Integrity", Colors.BOLD))
    print("-" * 50)
    
    valid = 0
    invalid = 0
    errors = []
    
    for yaml_file in sorted(agents_dir.glob("*.yaml")):
        data = load_yaml_file(yaml_file)
        if data and 'path' in data:
            path_value = data['path']
            # Remove leading ./ if present, but preserve the full path
            if path_value.startswith('./'):
                path_value = path_value[2:]
            ref_path = project_root / path_value
            
            if ref_path.exists():
                valid += 1
                if verbose:
                    print(color(f"✓ {yaml_file.name} -> {data['path']}", Colors.GREEN))
            else:
                invalid += 1
                msg = f"{yaml_file.name}: Path not found: {data['path']}"
                print(color(f"✗ {msg}", Colors.RED))
                errors.append(msg)
    
    if not verbose and valid > 0 and invalid == 0:
        print(color(f"✓ All {valid} path references valid", Colors.GREEN))
    
    return valid, invalid, errors


def check_manifest_consistency(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Check that manifest lists all agents in the agents directory."""
    manifest_path = project_root / ".paperkit/_cfg/agent-manifest.yaml"
    agents_dir = project_root / ".paperkit/_cfg/agents"
    
    print(color("\n4. Manifest Consistency", Colors.BOLD))
    print("-" * 50)
    
    errors = []
    
    manifest = load_yaml_file(manifest_path)
    if not manifest or 'agents' not in manifest:
        msg = "Manifest not found or missing 'agents' key"
        print(color(f"✗ {msg}", Colors.RED))
        return 0, 1, [msg]
    
    # Get agent names from manifest
    manifest_names = {agent['name'] for agent in manifest['agents']}
    
    # Get agent names from YAML files
    yaml_names = set()
    for yaml_file in agents_dir.glob("*.yaml"):
        data = load_yaml_file(yaml_file)
        if data and 'name' in data:
            yaml_names.add(data['name'])
    
    # Check for agents in YAML but not in manifest
    missing_from_manifest = yaml_names - manifest_names
    # Check for agents in manifest but not in YAML
    missing_from_yaml = manifest_names - yaml_names
    
    issues = 0
    
    if missing_from_manifest:
        for name in sorted(missing_from_manifest):
            msg = f"Agent '{name}' in YAML but missing from manifest"
            print(color(f"✗ {msg}", Colors.RED))
            errors.append(msg)
        issues += len(missing_from_manifest)
    
    if missing_from_yaml:
        for name in sorted(missing_from_yaml):
            msg = f"Agent '{name}' in manifest but no YAML file"
            print(color(f"✗ {msg}", Colors.RED))
            errors.append(msg)
        issues += len(missing_from_yaml)
    
    if issues == 0:
        print(color(f"✓ Manifest matches YAML directory ({len(yaml_names)} agents)", Colors.GREEN))
        return len(yaml_names), 0, []
    
    return len(yaml_names) - issues, issues, errors


def check_md_file_existence(project_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Check that all agents have corresponding MD files in core/specialist."""
    agents_dir = project_root / ".paperkit/_cfg/agents"
    core_agents = project_root / ".paperkit/core/agents"
    specialist_agents = project_root / ".paperkit/specialist/agents"
    
    print(color("\n5. MD File Coverage", Colors.BOLD))
    print("-" * 50)
    
    errors = []
    found = 0
    missing = 0
    
    for yaml_file in sorted(agents_dir.glob("*.yaml")):
        data = load_yaml_file(yaml_file)
        if not data:
            continue
            
        name = data.get('name', yaml_file.stem)
        module = data.get('module', 'core')
        
        if module == 'core':
            md_path = core_agents / f"{name}.md"
        else:
            md_path = specialist_agents / f"{name}.md"
        
        if md_path.exists():
            found += 1
            if verbose:
                print(color(f"✓ {name}.md exists", Colors.GREEN))
        else:
            missing += 1
            msg = f"{name}.md not found (expected at {md_path.relative_to(project_root)})"
            print(color(f"✗ {msg}", Colors.RED))
            errors.append(msg)
    
    if not verbose and found > 0 and missing == 0:
        print(color(f"✓ All {found} MD files exist", Colors.GREEN))
    
    return found, missing, errors


def main():
    parser = argparse.ArgumentParser(description="Unified Agent System Checker")
    parser.add_argument('--ci', action='store_true', help='Exit with error code on failures')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    args = parser.parse_args()
    
    project_root = find_project_root()
    if not project_root:
        print(color("Error: Could not find PaperKit project root", Colors.RED))
        sys.exit(1)
    
    print(color("╔═══════════════════════════════════════════════════╗", Colors.CYAN))
    print(color("║      PaperKit Unified Agent System Checker        ║", Colors.CYAN))
    print(color("╚═══════════════════════════════════════════════════╝", Colors.CYAN))
    print(color(f"Project: {project_root}", Colors.BLUE))
    
    total_passed = 0
    total_failed = 0
    all_errors = []
    
    # Run all checks
    checks = [
        check_yaml_schema_compliance,
        check_duplicate_names,
        check_path_references,
        check_manifest_consistency,
        check_md_file_existence,
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
