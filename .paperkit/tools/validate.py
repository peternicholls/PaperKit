#!/usr/bin/env python3
"""
PaperKit Schema Validator

Validates agent, workflow, and tool YAML definitions against their
JSON schemas in .paper/_cfg/schemas/.

Usage:
    python3 paperkit-validate.py [--verbose] [--fix-missing]

Requirements:
    pip install jsonschema pyyaml

Exit codes:
    0 = All validations passed
    1 = Validation errors found
    2 = Missing dependencies or configuration error
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# Color codes for terminal output
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color
    BOLD = '\033[1m'

def color(text: str, color_code: str) -> str:
    """Wrap text in color codes."""
    return f"{color_code}{text}{Colors.NC}"

def check_dependencies() -> bool:
    """Check if required Python packages are available."""
    missing = []
    
    try:
        import yaml
    except ImportError:
        missing.append("pyyaml")
    
    try:
        import jsonschema
    except ImportError:
        missing.append("jsonschema")
    
    if missing:
        print(color("Missing required packages:", Colors.RED))
        print(f"  pip install {' '.join(missing)}")
        return False
    
    return True


def find_project_root() -> Optional[Path]:
    """Find the project root by looking for .paper/ directory."""
    current = Path.cwd()
    
    # Check current directory and parents
    for path in [current] + list(current.parents):
        if (path / ".paper").is_dir():
            return path
        if (path / "paperkit").is_file():
            return path
    
    return None


def load_json_schema(schema_path: Path) -> Optional[Dict]:
    """Load a JSON schema file."""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(color(f"Error loading schema {schema_path}: {e}", Colors.RED))
        return None


def extract_yaml_frontmatter(file_path: Path) -> Optional[Dict]:
    """
    Extract YAML frontmatter from a Markdown file.
    
    Frontmatter is expected to be between --- markers at the start of the file:
    ---
    name: example
    displayName: Example Agent
    ---
    """
    import yaml
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Check for frontmatter start
        if not lines or lines[0].strip() != '---':
            return None
        
        # Find the closing ---
        end_idx = None
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                end_idx = i
                break
        
        if end_idx is None:
            return None
        
        # Parse the YAML frontmatter
        frontmatter = '\n'.join(lines[1:end_idx])
        return yaml.safe_load(frontmatter)
    
    except Exception as e:
        print(color(f"  Error parsing {file_path.name}: {e}", Colors.RED))
        return None


def load_yaml_file(file_path: Path) -> Optional[Dict]:
    """Load a YAML file."""
    import yaml
    
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(color(f"  Error loading {file_path.name}: {e}", Colors.RED))
        return None


def validate_against_schema(data: Dict, schema: Dict, file_name: str, verbose: bool = False) -> List[str]:
    """Validate data against a JSON schema. Returns list of error messages."""
    from jsonschema import Draft7Validator, ValidationError
    
    errors = []
    validator = Draft7Validator(schema)
    
    for error in sorted(validator.iter_errors(data), key=lambda e: e.path):
        path = ".".join(str(p) for p in error.path) if error.path else "(root)"
        errors.append(f"  {path}: {error.message}")
        
        if verbose and error.context:
            for suberror in error.context:
                errors.append(f"    → {suberror.message}")
    
    return errors


def validate_agents(project_root: Path, verbose: bool = False) -> Tuple[int, int]:
    """Validate all agent definitions. Returns (passed, failed) counts."""
    import yaml
    
    schema_path = project_root / ".paper/_cfg/schemas/agent-schema.json"
    schema = load_json_schema(schema_path)
    
    if not schema:
        print(color("Cannot validate agents: schema not found", Colors.YELLOW))
        return 0, 0
    
    print(color("\n📋 Validating Agent Definitions", Colors.BOLD))
    print("-" * 40)
    
    passed = 0
    failed = 0
    
    # Check both core and specialist agents
    agent_dirs = [
        project_root / ".paper/core/agents",
        project_root / ".paper/specialist/agents"
    ]
    
    for agent_dir in agent_dirs:
        if not agent_dir.is_dir():
            continue
        
        for agent_file in agent_dir.glob("*.md"):
            # Extract YAML frontmatter
            data = extract_yaml_frontmatter(agent_file)
            
            if data is None:
                print(color(f"⚠ {agent_file.name}: No YAML frontmatter found", Colors.YELLOW))
                failed += 1
                continue
            
            errors = validate_against_schema(data, schema, agent_file.name, verbose)
            
            if errors:
                print(color(f"✗ {agent_file.name}", Colors.RED))
                for err in errors:
                    print(color(err, Colors.RED))
                failed += 1
            else:
                print(color(f"✓ {agent_file.name}", Colors.GREEN))
                passed += 1
    
    return passed, failed


def validate_workflows(project_root: Path, verbose: bool = False) -> Tuple[int, int]:
    """Validate all workflow definitions. Returns (passed, failed) counts."""
    schema_path = project_root / ".paper/_cfg/schemas/workflow-schema.json"
    schema = load_json_schema(schema_path)
    
    if not schema:
        print(color("Cannot validate workflows: schema not found", Colors.YELLOW))
        return 0, 0
    
    print(color("\n📋 Validating Workflow Definitions", Colors.BOLD))
    print("-" * 40)
    
    passed = 0
    failed = 0
    
    # Check both core and specialist workflows
    workflow_dirs = [
        project_root / ".paper/core/workflows",
        project_root / ".paper/specialist/workflows",
        project_root / ".paper/_cfg/workflows"
    ]
    
    for workflow_dir in workflow_dirs:
        if not workflow_dir.is_dir():
            continue
        
        for workflow_file in workflow_dir.glob("*.yaml"):
            data = load_yaml_file(workflow_file)
            
            if data is None:
                failed += 1
                continue
            
            errors = validate_against_schema(data, schema, workflow_file.name, verbose)
            
            if errors:
                print(color(f"✗ {workflow_file.name}", Colors.RED))
                for err in errors:
                    print(color(err, Colors.RED))
                failed += 1
            else:
                print(color(f"✓ {workflow_file.name}", Colors.GREEN))
                passed += 1
    
    if passed == 0 and failed == 0:
        print(color("  No workflow YAML files found", Colors.YELLOW))
    
    return passed, failed


def validate_tools(project_root: Path, verbose: bool = False) -> Tuple[int, int]:
    """Validate all tool definitions. Returns (passed, failed) counts."""
    schema_path = project_root / ".paper/_cfg/schemas/tool-schema.json"
    schema = load_json_schema(schema_path)
    
    if not schema:
        print(color("Cannot validate tools: schema not found", Colors.YELLOW))
        return 0, 0
    
    print(color("\n📋 Validating Tool Definitions", Colors.BOLD))
    print("-" * 40)
    
    passed = 0
    failed = 0
    
    tool_dir = project_root / ".paper/_cfg/tools"
    
    if not tool_dir.is_dir():
        print(color("  No tool definitions directory found", Colors.YELLOW))
        return 0, 0
    
    for tool_file in tool_dir.glob("*.yaml"):
        data = load_yaml_file(tool_file)
        
        if data is None:
            failed += 1
            continue
        
        errors = validate_against_schema(data, schema, tool_file.name, verbose)
        
        if errors:
            print(color(f"✗ {tool_file.name}", Colors.RED))
            for err in errors:
                print(color(err, Colors.RED))
            failed += 1
        else:
            print(color(f"✓ {tool_file.name}", Colors.GREEN))
            passed += 1
    
    if passed == 0 and failed == 0:
        print(color("  No tool YAML files found", Colors.YELLOW))
    
    return passed, failed


def validate_manifests(project_root: Path, verbose: bool = False) -> Tuple[int, int]:
    """Validate manifest files structure. Returns (passed, failed) counts."""
    print(color("\n📋 Validating Manifests", Colors.BOLD))
    print("-" * 40)
    
    passed = 0
    failed = 0
    
    manifests = [
        ("agent-manifest.yaml", ["agents"]),
        ("workflow-manifest.yaml", ["workflows"]),
        ("tool-manifest.yaml", ["tools"])
    ]
    
    for manifest_name, required_keys in manifests:
        manifest_path = project_root / f".paper/_cfg/{manifest_name}"
        
        if not manifest_path.exists():
            print(color(f"⚠ {manifest_name}: Not found", Colors.YELLOW))
            failed += 1
            continue
        
        data = load_yaml_file(manifest_path)
        
        if data is None:
            failed += 1
            continue
        
        # Check required top-level keys
        missing_keys = [k for k in required_keys if k not in data]
        
        if missing_keys:
            print(color(f"✗ {manifest_name}: Missing keys: {missing_keys}", Colors.RED))
            failed += 1
        else:
            item_count = len(data.get(required_keys[0], []))
            print(color(f"✓ {manifest_name} ({item_count} items)", Colors.GREEN))
            passed += 1
    
    return passed, failed


def validate_ide_sync(project_root: Path, verbose: bool = False) -> Tuple[int, int]:
    """Check if IDE files are in sync with .paper/ source. Returns (passed, failed) counts."""
    print(color("\n📋 Checking IDE File Sync", Colors.BOLD))
    print("-" * 40)
    
    passed = 0
    failed = 0
    
    # Find all agent definitions
    agent_names = []
    for agent_dir in [project_root / ".paper/core/agents", project_root / ".paper/specialist/agents"]:
        if agent_dir.is_dir():
            for f in agent_dir.glob("*.md"):
                # Extract name from filename (paper-xxx.md -> xxx)
                name = f.stem
                if name.startswith("paper-"):
                    name = name[6:]  # Remove paper- prefix
                agent_names.append(name)
    
    # Check Copilot files
    copilot_dir = project_root / ".github/agents"
    if copilot_dir.is_dir():
        for agent_name in agent_names:
            copilot_file = copilot_dir / f"paper-{agent_name}.agent.md"
            if copilot_file.exists():
                passed += 1
                if verbose:
                    print(color(f"✓ Copilot: paper-{agent_name}.agent.md", Colors.GREEN))
            else:
                failed += 1
                print(color(f"✗ Copilot: Missing paper-{agent_name}.agent.md", Colors.RED))
    else:
        print(color("  .github/agents/ directory not found (Copilot not installed)", Colors.YELLOW))
    
    # Check Codex files
    codex_dir = project_root / ".codex/prompts"
    if codex_dir.is_dir():
        for agent_name in agent_names:
            codex_file = codex_dir / f"paper-{agent_name}.md"
            if codex_file.exists():
                passed += 1
                if verbose:
                    print(color(f"✓ Codex: paper-{agent_name}.md", Colors.GREEN))
            else:
                failed += 1
                print(color(f"✗ Codex: Missing paper-{agent_name}.md", Colors.RED))
    else:
        print(color("  .codex/prompts/ directory not found (Codex not installed)", Colors.YELLOW))
    
    if passed > 0 and failed == 0:
        print(color(f"✓ All {passed} IDE files in sync", Colors.GREEN))
    
    return passed, failed


def main():
    parser = argparse.ArgumentParser(
        description="Validate PaperKit agent, workflow, and tool definitions"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed validation output"
    )
    parser.add_argument(
        "--agents-only",
        action="store_true",
        help="Only validate agent definitions"
    )
    parser.add_argument(
        "--workflows-only",
        action="store_true",
        help="Only validate workflow definitions"
    )
    parser.add_argument(
        "--tools-only",
        action="store_true",
        help="Only validate tool definitions"
    )
    parser.add_argument(
        "--ide-sync",
        action="store_true",
        help="Check IDE file synchronization"
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(2)
    
    # Find project root
    project_root = find_project_root()
    if not project_root:
        print(color("Error: Could not find PaperKit project root (.paper/ directory)", Colors.RED))
        print("Make sure you're running from within a PaperKit project.")
        sys.exit(2)
    
    print(color(f"🔍 PaperKit Schema Validator", Colors.BOLD))
    print(color(f"   Project: {project_root}", Colors.CYAN))
    
    # Track totals
    total_passed = 0
    total_failed = 0
    
    # Determine what to validate
    validate_all = not (args.agents_only or args.workflows_only or args.tools_only or args.ide_sync)
    
    # Run validations
    if validate_all or args.agents_only:
        p, f = validate_agents(project_root, args.verbose)
        total_passed += p
        total_failed += f
    
    if validate_all or args.workflows_only:
        p, f = validate_workflows(project_root, args.verbose)
        total_passed += p
        total_failed += f
    
    if validate_all or args.tools_only:
        p, f = validate_tools(project_root, args.verbose)
        total_passed += p
        total_failed += f
    
    if validate_all:
        p, f = validate_manifests(project_root, args.verbose)
        total_passed += p
        total_failed += f
    
    if validate_all or args.ide_sync:
        p, f = validate_ide_sync(project_root, args.verbose)
        total_passed += p
        total_failed += f
    
    # Summary
    print(color("\n" + "=" * 40, Colors.BOLD))
    print(color("Summary", Colors.BOLD))
    print("=" * 40)
    print(f"  Passed: {color(str(total_passed), Colors.GREEN)}")
    print(f"  Failed: {color(str(total_failed), Colors.RED if total_failed > 0 else Colors.GREEN)}")
    
    if total_failed > 0:
        print(color("\n⚠ Validation completed with errors", Colors.YELLOW))
        sys.exit(1)
    else:
        print(color("\n✓ All validations passed", Colors.GREEN))
        sys.exit(0)


if __name__ == "__main__":
    main()
