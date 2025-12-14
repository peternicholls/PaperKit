#!/usr/bin/env python3

"""
Agent Schema Validator

Validates agent YAML definitions against JSON Schema to ensure completeness
and consistency of agent metadata.

Usage:
    python3 validate-agent-schema.py [OPTIONS]
    
Options:
    --agent AGENT_NAME    Validate specific agent only
    --verbose             Show detailed validation information
    --ci                  CI mode: exit with error code on validation failure
    --schema PATH         Path to JSON Schema file (overrides default)
    --agents-dir PATH     Path to agents directory (overrides default)
    
Environment Variables:
    PAPERKIT_SCHEMA_PATH    Override default schema path
    PAPERKIT_AGENTS_DIR     Override default agents directory
"""

import sys
import json
import yaml
import os
from pathlib import Path
from typing import Dict, List, Tuple
import argparse

try:
    from jsonschema import validate, ValidationError, Draft7Validator
except ImportError:
    print("Error: jsonschema package not installed")
    print("Install with: pip install jsonschema>=4.0")
    sys.exit(1)

# Constants
AGENT_FILE_EXTENSION = '.yaml'


def load_json_schema(schema_path: Path) -> Dict:
    """Load JSON Schema from file"""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Schema file not found: {schema_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in schema file: {e}")
        sys.exit(1)


def load_agent_yaml(yaml_path: Path) -> Dict:
    """Load agent YAML definition"""
    try:
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Agent file not found: {yaml_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in {yaml_path}: {e}")
        return None


def validate_agent(agent_data: Dict, schema: Dict, agent_name: str) -> Tuple[bool, List[str]]:
    """Validate agent data against schema"""
    errors = []
    
    # Validate against JSON Schema
    validator = Draft7Validator(schema)
    schema_errors = sorted(validator.iter_errors(agent_data), key=lambda e: e.path)
    
    for error in schema_errors:
        path = ".".join(str(p) for p in error.path) if error.path else "root"
        errors.append(f"  [{path}] {error.message}")
    
    # Additional custom validations
    if agent_data:
        # Check that name matches filename
        expected_name = agent_name
        actual_name = agent_data.get('name', '')
        if actual_name != expected_name:
            errors.append(f"  [name] Name '{actual_name}' doesn't match filename '{expected_name}.yaml'")
        
        # Check that path exists
        agent_path = agent_data.get('path', '')
        if agent_path:
            full_path = Path(agent_path)
            if not full_path.exists():
                errors.append(f"  [path] Referenced agent file does not exist: {agent_path}")
    
    return len(errors) == 0, errors


def find_agent_files(agents_dir: Path, specific_agent: str = None) -> List[Path]:
    """Find all agent YAML files or a specific one"""
    if specific_agent:
        agent_file = agents_dir / f"{specific_agent}{AGENT_FILE_EXTENSION}"
        if agent_file.exists():
            return [agent_file]
        else:
            print(f"Error: Agent '{specific_agent}' not found")
            return []
    else:
        return sorted(agents_dir.glob(f"*{AGENT_FILE_EXTENSION}"))


def main():
    parser = argparse.ArgumentParser(description="Validate PaperKit agent definitions")
    parser.add_argument('--agent', help='Validate specific agent only')
    parser.add_argument('--verbose', action='store_true', help='Show detailed information')
    parser.add_argument('--ci', action='store_true', help='CI mode: exit with error on failure')
    parser.add_argument('--schema', help='Path to JSON Schema file (default: .paper/_cfg/schemas/agent-schema.json)')
    parser.add_argument('--agents-dir', help='Path to agents directory (default: .paper/_cfg/agents)')
    args = parser.parse_args()
    
    # Paths - support environment variables and command-line overrides
    repo_root = Path(__file__).parent.parent.parent
    
    if args.schema:
        schema_path = Path(args.schema)
    else:
        schema_path = Path(os.getenv('PAPERKIT_SCHEMA_PATH', 
                                     repo_root / ".paper" / "_cfg" / "schemas" / "agent-schema.json"))
    
    if args.agents_dir:
        agents_dir = Path(args.agents_dir)
    else:
        agents_dir = Path(os.getenv('PAPERKIT_AGENTS_DIR',
                                    repo_root / ".paper" / "_cfg" / "agents"))
    
    print("Agent Schema Validation")
    print("=" * 70)
    
    # Load schema
    if args.verbose:
        print(f"\nLoading schema from: {schema_path}")
    schema = load_json_schema(schema_path)
    
    # Find agent files
    agent_files = find_agent_files(agents_dir, args.agent)
    
    if not agent_files:
        print("\nNo agent files found to validate")
        sys.exit(1 if args.ci else 0)
    
    print(f"\nValidating {len(agent_files)} agent(s)...")
    print()
    
    # Validate each agent
    results = []
    total_errors = 0
    
    for agent_file in agent_files:
        agent_name = agent_file.stem
        
        if args.verbose:
            print(f"Validating {agent_name}...")
        
        agent_data = load_agent_yaml(agent_file)
        
        if agent_data is None:
            results.append((agent_name, False, ["Failed to load YAML"]))
            total_errors += 1
            continue
        
        is_valid, errors = validate_agent(agent_data, schema, agent_name)
        results.append((agent_name, is_valid, errors))
        
        if not is_valid:
            total_errors += len(errors)
    
    # Display results
    for agent_name, is_valid, errors in results:
        icon = "✓" if is_valid else "✗"
        status = "VALID" if is_valid else "INVALID"
        print(f"{icon} {agent_name:25} {status}")
        
        if not is_valid:
            for error in errors:
                print(error)
            print()
    
    # Summary
    print("=" * 70)
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)
    invalid_count = len(results) - valid_count
    
    print(f"\nValidation Summary:")
    print(f"  Total agents:   {len(results)}")
    print(f"  Valid:          {valid_count}")
    print(f"  Invalid:        {invalid_count}")
    print(f"  Total errors:   {total_errors}")
    
    # Exit code
    if invalid_count > 0:
        print(f"\n⚠️  Validation failed with {invalid_count} invalid agent(s)")
        sys.exit(1 if args.ci else 0)
    else:
        print("\n✓ All agents validated successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()
