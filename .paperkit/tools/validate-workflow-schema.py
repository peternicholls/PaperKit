#!/usr/bin/env python3

"""
Workflow Schema Validator

Validates workflow YAML definitions against JSON Schema to ensure completeness
and consistency of workflow metadata.

Usage:
    python3 validate-workflow-schema.py [OPTIONS]
    
Options:
    --workflow WORKFLOW_NAME    Validate specific workflow only
    --verbose                   Show detailed validation information
    --ci                        CI mode: exit with error code on validation failure
    --schema PATH               Path to JSON Schema file (overrides default)
    --workflows-dir PATH        Path to workflows directory (overrides default)
    
Environment Variables:
    PAPERKIT_WORKFLOW_SCHEMA_PATH    Override default schema path
    PAPERKIT_WORKFLOWS_DIR           Override default workflows directory
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
WORKFLOW_FILE_EXTENSION = '.yaml'


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


def load_workflow_yaml(yaml_path: Path) -> Dict:
    """Load workflow YAML definition"""
    try:
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Workflow file not found: {yaml_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in {yaml_path}: {e}")
        return None


def validate_workflow(workflow_data: Dict, schema: Dict, workflow_name: str) -> Tuple[bool, List[str]]:
    """Validate workflow data against schema"""
    errors = []
    
    # Validate against JSON Schema
    validator = Draft7Validator(schema)
    schema_errors = sorted(validator.iter_errors(workflow_data), key=lambda e: e.path)
    
    for error in schema_errors:
        path = ".".join(str(p) for p in error.path) if error.path else "root"
        errors.append(f"  [{path}] {error.message}")
    
    # Additional custom validations
    if workflow_data:
        # Check that name matches filename
        expected_name = workflow_name
        actual_name = workflow_data.get('name', '')
        if actual_name != expected_name:
            errors.append(f"  [name] Name '{actual_name}' doesn't match filename '{expected_name}.yaml'")
    
    return len(errors) == 0, errors


def find_workflow_files(workflows_dir: Path, specific_workflow: str = None) -> List[Path]:
    """Find all workflow YAML files or a specific one"""
    if specific_workflow:
        workflow_file = workflows_dir / f"{specific_workflow}{WORKFLOW_FILE_EXTENSION}"
        if workflow_file.exists():
            return [workflow_file]
        else:
            print(f"Error: Workflow '{specific_workflow}' not found")
            return []
    else:
        return sorted(workflows_dir.glob(f"*{WORKFLOW_FILE_EXTENSION}"))


def main():
    parser = argparse.ArgumentParser(description="Validate PaperKit workflow definitions")
    parser.add_argument('--workflow', help='Validate specific workflow only')
    parser.add_argument('--verbose', action='store_true', help='Show detailed information')
    parser.add_argument('--ci', action='store_true', help='CI mode: exit with error on failure')
    parser.add_argument('--schema', help='Path to JSON Schema file (default: .paper/_cfg/schemas/workflow-schema.json)')
    parser.add_argument('--workflows-dir', help='Path to workflows directory (default: .paper/_cfg/workflows)')
    args = parser.parse_args()
    
    # Paths - support environment variables and command-line overrides
    repo_root = Path(__file__).parent.parent.parent
    
    if args.schema:
        schema_path = Path(args.schema)
    else:
        schema_path = Path(os.getenv('PAPERKIT_WORKFLOW_SCHEMA_PATH', 
                                     repo_root / ".paper" / "_cfg" / "schemas" / "workflow-schema.json"))
    
    if args.workflows_dir:
        workflows_dir = Path(args.workflows_dir)
    else:
        workflows_dir = Path(os.getenv('PAPERKIT_WORKFLOWS_DIR',
                                        repo_root / ".paper" / "_cfg" / "workflows"))
    
    print("Workflow Schema Validation")
    print("=" * 70)
    
    # Load schema
    if args.verbose:
        print(f"\nLoading schema from: {schema_path}")
    schema = load_json_schema(schema_path)
    
    # Find workflow files
    workflow_files = find_workflow_files(workflows_dir, args.workflow)
    
    if not workflow_files:
        print("\nNo workflow files found to validate")
        sys.exit(1 if args.ci else 0)
    
    print(f"\nValidating {len(workflow_files)} workflow(s)...")
    print()
    
    # Validate each workflow
    results = []
    total_errors = 0
    
    for workflow_file in workflow_files:
        workflow_name = workflow_file.stem
        
        if args.verbose:
            print(f"Validating {workflow_name}...")
        
        workflow_data = load_workflow_yaml(workflow_file)
        
        if workflow_data is None:
            results.append((workflow_name, False, ["Failed to load YAML"]))
            total_errors += 1
            continue
        
        is_valid, errors = validate_workflow(workflow_data, schema, workflow_name)
        results.append((workflow_name, is_valid, errors))
        
        if not is_valid:
            total_errors += len(errors)
    
    # Display results
    for workflow_name, is_valid, errors in results:
        icon = "✓" if is_valid else "✗"
        status = "VALID" if is_valid else "INVALID"
        print(f"{icon} {workflow_name:25} {status}")
        
        if not is_valid:
            for error in errors:
                print(error)
            print()
    
    # Summary
    print("=" * 70)
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)
    invalid_count = len(results) - valid_count
    
    print(f"\nValidation Summary:")
    print(f"  Total workflows: {len(results)}")
    print(f"  Valid:           {valid_count}")
    print(f"  Invalid:         {invalid_count}")
    print(f"  Total errors:    {total_errors}")
    
    # Exit code
    if invalid_count > 0:
        print(f"\n⚠️  Validation failed with {invalid_count} invalid workflow(s)")
        sys.exit(1 if args.ci else 0)
    else:
        print("\n✓ All workflows validated successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()
