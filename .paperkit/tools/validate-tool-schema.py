#!/usr/bin/env python3

"""
Tool Schema Validator

Validates tool YAML definitions against JSON Schema to ensure completeness
and consistency of tool metadata.

Usage:
    python3 validate-tool-schema.py [OPTIONS]
    
Options:
    --tool TOOL_NAME      Validate specific tool only
    --verbose             Show detailed validation information
    --ci                  CI mode: exit with error code on validation failure
    --schema PATH         Path to JSON Schema file (overrides default)
    --tools-dir PATH      Path to tools directory (overrides default)
    
Environment Variables:
    PAPERKIT_TOOL_SCHEMA_PATH    Override default schema path
    PAPERKIT_TOOLS_DIR           Override default tools directory
"""

import sys
import json
import yaml
import os
from pathlib import Path
from typing import Dict, List, Tuple
import argparse

try:
    from jsonschema import Draft7Validator
except ImportError:
    print("Error: jsonschema package not installed")
    print("Install with: pip install 'jsonschema>=4.0'")
    sys.exit(1)

# Constants
TOOL_FILE_EXTENSION = '.yaml'


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


def load_tool_yaml(yaml_path: Path) -> Dict:
    """Load tool YAML definition"""
    try:
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Tool file not found: {yaml_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in {yaml_path}: {e}")
        return None


def validate_tool(tool_data: Dict, schema: Dict, tool_name: str) -> Tuple[bool, List[str]]:
    """Validate tool data against schema"""
    errors = []
    
    # Validate against JSON Schema
    validator = Draft7Validator(schema)
    schema_errors = sorted(validator.iter_errors(tool_data), key=lambda e: e.path)
    
    for error in schema_errors:
        path = ".".join(str(p) for p in error.path) if error.path else "root"
        errors.append(f"  [{path}] {error.message}")
    
    # Additional custom validations
    if tool_data:
        # Check that name matches filename
        expected_name = tool_name
        actual_name = tool_data.get('name', '')
        if actual_name != expected_name:
            errors.append(f"  [name] Name '{actual_name}' doesn't match filename '{expected_name}.yaml'")
        
        # Check that path exists (tool script)
        tool_path = tool_data.get('path', '')
        if tool_path:
            # Path is relative to repo root
            repo_root = Path(__file__).parent.parent.parent
            full_path = repo_root / tool_path
            if not full_path.exists():
                errors.append(f"  [path] Referenced tool file does not exist: {tool_path}")
    
    return len(errors) == 0, errors


def find_tool_files(tools_dir: Path, specific_tool: str = None) -> List[Path]:
    """Find all tool YAML files or a specific one"""
    if specific_tool:
        tool_file = tools_dir / f"{specific_tool}{TOOL_FILE_EXTENSION}"
        if tool_file.exists():
            return [tool_file]
        else:
            print(f"Error: Tool '{specific_tool}' not found")
            return []
    else:
        return sorted(tools_dir.glob(f"*{TOOL_FILE_EXTENSION}"))


def main():
    parser = argparse.ArgumentParser(description="Validate PaperKit tool definitions")
    parser.add_argument('--tool', help='Validate specific tool only')
    parser.add_argument('--verbose', action='store_true', help='Show detailed information')
    parser.add_argument('--ci', action='store_true', help='CI mode: exit with error on failure')
    parser.add_argument('--schema', help='Path to JSON Schema file (default: .paper/_cfg/schemas/tool-schema.json)')
    parser.add_argument('--tools-dir', help='Path to tools directory (default: .paper/_cfg/tools)')
    args = parser.parse_args()
    
    # Paths - support environment variables and command-line overrides
    repo_root = Path(__file__).parent.parent.parent
    
    if args.schema:
        schema_path = Path(args.schema)
    else:
        schema_path = Path(os.getenv('PAPERKIT_TOOL_SCHEMA_PATH', 
                                     repo_root / ".paper" / "_cfg" / "schemas" / "tool-schema.json"))
    
    if args.tools_dir:
        tools_dir = Path(args.tools_dir)
    else:
        tools_dir = Path(os.getenv('PAPERKIT_TOOLS_DIR',
                                    repo_root / ".paper" / "_cfg" / "tools"))
    
    print("Tool Schema Validation")
    print("=" * 70)
    
    # Load schema
    if args.verbose:
        print(f"\nLoading schema from: {schema_path}")
    schema = load_json_schema(schema_path)
    
    # Find tool files
    tool_files = find_tool_files(tools_dir, args.tool)
    
    if not tool_files:
        print("\nNo tool files found to validate")
        sys.exit(1 if args.ci else 0)
    
    print(f"\nValidating {len(tool_files)} tool(s)...")
    print()
    
    # Validate each tool
    results = []
    total_errors = 0
    
    for tool_file in tool_files:
        tool_name = tool_file.stem
        
        if args.verbose:
            print(f"Validating {tool_name}...")
        
        tool_data = load_tool_yaml(tool_file)
        
        if tool_data is None:
            results.append((tool_name, False, ["Failed to load YAML"]))
            total_errors += 1
            continue
        
        is_valid, errors = validate_tool(tool_data, schema, tool_name)
        results.append((tool_name, is_valid, errors))
        
        if not is_valid:
            total_errors += len(errors)
    
    # Display results
    for tool_name, is_valid, errors in results:
        icon = "✓" if is_valid else "✗"
        status = "VALID" if is_valid else "INVALID"
        print(f"{icon} {tool_name:25} {status}")
        
        if not is_valid:
            for error in errors:
                print(error)
            print()
    
    # Summary
    print("=" * 70)
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)
    invalid_count = len(results) - valid_count
    
    print(f"\nValidation Summary:")
    print(f"  Total tools:    {len(results)}")
    print(f"  Valid:          {valid_count}")
    print(f"  Invalid:        {invalid_count}")
    print(f"  Total errors:   {total_errors}")
    
    # Exit code
    if invalid_count > 0:
        print(f"\n⚠️  Validation failed with {invalid_count} invalid tool(s)")
        sys.exit(1 if args.ci else 0)
    else:
        print("\n✓ All tools validated successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()
