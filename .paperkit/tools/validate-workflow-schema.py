#!/usr/bin/env python3

"""
Workflow Schema Validator

Validates workflow YAML definitions against JSON Schema to ensure completeness
and consistency of workflow metadata. Also validates references to agents, skills,
and tools exist (FR-016) and enforces workflow depth limits (FR-013).

Usage:
    python3 validate-workflow-schema.py [OPTIONS]
    
Options:
    --workflow WORKFLOW_NAME    Validate specific workflow only
    --verbose                   Show detailed validation information
    --ci                        CI mode: exit with error code on validation failure
    --schema PATH               Path to JSON Schema file (overrides default)
    --workflows-dir PATH        Path to workflows directory (overrides default)
    --skip-references           Skip validation of agent/skill/tool references
    --max-depth DEPTH           Maximum workflow composition depth (default: 5)
    
Environment Variables:
    PAPERKIT_WORKFLOW_SCHEMA_PATH    Override default schema path
    PAPERKIT_WORKFLOWS_DIR           Override default workflows directory
"""

import sys
import json
import yaml
import os
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
import argparse

try:
    from jsonschema import Draft7Validator
except ImportError:
    print("Error: jsonschema package not installed")
    print("Install with: pip install 'jsonschema>=4.0'")
    sys.exit(1)

# Constants
WORKFLOW_FILE_EXTENSION = '.yaml'
MAX_WORKFLOW_DEPTH = 5  # FR-013: Maximum workflow composition depth


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


def load_workflow_yaml(yaml_path: Path) -> Optional[Dict]:
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


def discover_available_agents(repo_root: Path) -> Set[str]:
    """Discover all available agent names from YAML definitions."""
    agents = set()
    agents_dir = repo_root / ".paperkit" / "_cfg" / "agents"
    
    if agents_dir.exists():
        for yaml_file in agents_dir.glob("*.yaml"):
            if yaml_file.name == "README.md":
                continue
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                if data and 'name' in data:
                    agents.add(data['name'])
            except Exception:
                pass
    
    return agents


def discover_available_skills(repo_root: Path) -> Set[str]:
    """Discover all available skill names from SKILL.md files."""
    skills = set()
    skills_dir = repo_root / ".paperkit" / "_cfg" / "skills"
    
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    # Try to extract name from frontmatter
                    try:
                        with open(skill_md, 'r') as f:
                            content = f.read()
                        if content.startswith('---'):
                            lines = content.split('\n')
                            end_idx = None
                            for i, line in enumerate(lines[1:], 1):
                                if line.strip() == '---':
                                    end_idx = i
                                    break
                            if end_idx:
                                frontmatter = yaml.safe_load('\n'.join(lines[1:end_idx]))
                                if frontmatter and 'name' in frontmatter:
                                    skills.add(frontmatter['name'])
                                else:
                                    skills.add(skill_dir.name)
                        else:
                            skills.add(skill_dir.name)
                    except Exception:
                        skills.add(skill_dir.name)
    
    return skills


def discover_available_tools(repo_root: Path) -> Set[str]:
    """Discover all available tool names from YAML definitions."""
    tools = set()
    tools_dir = repo_root / ".paperkit" / "_cfg" / "tools"
    
    if tools_dir.exists():
        for yaml_file in tools_dir.glob("*.yaml"):
            if yaml_file.name == "README.md":
                continue
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                if data and 'name' in data:
                    tools.add(data['name'])
            except Exception:
                pass
    
    return tools


def discover_available_workflows(repo_root: Path) -> Set[str]:
    """Discover all available workflow names from YAML definitions."""
    workflows = set()
    workflows_dir = repo_root / ".paperkit" / "_cfg" / "workflows"
    
    if workflows_dir.exists():
        for yaml_file in workflows_dir.glob("*.yaml"):
            if yaml_file.name == "README.md":
                continue
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                if data and 'name' in data:
                    workflows.add(data['name'])
            except Exception:
                pass
    
    return workflows


def validate_references(
    workflow_data: Dict,
    workflow_name: str,
    available_agents: Set[str],
    available_skills: Set[str],
    available_tools: Set[str],
    available_workflows: Set[str]
) -> List[str]:
    """
    Validate that all referenced agents, skills, tools, and workflows exist.
    Implements FR-016: System MUST validate that agents, skills, and tools 
    referenced by workflows actually exist.
    """
    errors = []
    
    # Check agents in steps
    for i, step in enumerate(workflow_data.get('steps', [])):
        agent = step.get('agent')
        if agent and agent not in available_agents:
            errors.append(f"  [steps.{i}.agent] Agent '{agent}' not found in .paperkit/_cfg/agents/")
        
        # Check skill reference in step
        skill = step.get('skill')
        if skill and skill not in available_skills:
            errors.append(f"  [steps.{i}.skill] Skill '{skill}' not found in .paperkit/_cfg/skills/")
        
        # Check tool reference in step (if present)
        tool = step.get('tool')
        if tool and tool not in available_tools:
            errors.append(f"  [steps.{i}.tool] Tool '{tool}' not found in .paperkit/_cfg/tools/")
    
    # Check workflow prerequisites
    for i, prereq in enumerate(workflow_data.get('prerequisites', [])):
        prereq_type = prereq.get('type')
        prereq_name = prereq.get('name')
        
        if prereq_type == 'workflow' and prereq_name not in available_workflows:
            errors.append(f"  [prerequisites.{i}] Workflow prerequisite '{prereq_name}' not found")
        elif prereq_type == 'tool' and prereq_name not in available_tools:
            errors.append(f"  [prerequisites.{i}] Tool prerequisite '{prereq_name}' not found")
    
    return errors


def calculate_workflow_depth(
    workflow_name: str,
    workflows_data: Dict[str, Dict],
    visited: Optional[Set[str]] = None,
    depth: int = 1
) -> Tuple[int, List[str]]:
    """
    Calculate the maximum depth of workflow composition.
    Implements FR-013: System MUST enforce maximum workflow composition depth of 5 levels.
    
    Returns:
        Tuple of (max_depth, path_to_max_depth)
    """
    if visited is None:
        visited = set()
    
    if workflow_name in visited:
        # Circular dependency detected
        return -1, [f"CIRCULAR: {workflow_name}"]
    
    if workflow_name not in workflows_data:
        return depth, [workflow_name]
    
    visited.add(workflow_name)
    workflow = workflows_data[workflow_name]
    
    max_depth = depth
    max_path = [workflow_name]
    
    # Check prerequisites for nested workflows
    for prereq in workflow.get('prerequisites', []):
        if prereq.get('type') == 'workflow':
            prereq_name = prereq.get('name')
            sub_depth, sub_path = calculate_workflow_depth(
                prereq_name, workflows_data, visited.copy(), depth + 1
            )
            if sub_depth > max_depth:
                max_depth = sub_depth
                max_path = [workflow_name] + sub_path
    
    return max_depth, max_path


def validate_workflow_depth(
    workflows_data: Dict[str, Dict],
    max_allowed_depth: int = MAX_WORKFLOW_DEPTH
) -> Dict[str, Tuple[int, List[str], bool]]:
    """
    Validate that no workflow exceeds the maximum composition depth.
    
    Returns:
        Dict mapping workflow_name to (depth, path, is_valid)
    """
    results = {}
    
    for workflow_name in workflows_data:
        depth, path = calculate_workflow_depth(workflow_name, workflows_data)
        is_valid = depth > 0 and depth <= max_allowed_depth
        results[workflow_name] = (depth, path, is_valid)
    
    return results


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


def find_workflow_files(workflows_dir: Path, specific_workflow: Optional[str] = None) -> List[Path]:
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
    parser.add_argument('--schema', help='Path to JSON Schema file (default: .paperkit/_cfg/schemas/workflow-schema.json)')
    parser.add_argument('--workflows-dir', help='Path to workflows directory (default: .paperkit/_cfg/workflows)')
    parser.add_argument('--skip-references', action='store_true', help='Skip validation of agent/skill/tool references')
    parser.add_argument('--max-depth', type=int, default=MAX_WORKFLOW_DEPTH, help=f'Maximum workflow depth (default: {MAX_WORKFLOW_DEPTH})')
    args = parser.parse_args()
    
    # Paths - support environment variables and command-line overrides
    repo_root = Path(__file__).parent.parent.parent
    
    if args.schema:
        schema_path = Path(args.schema)
    else:
        schema_path = Path(os.getenv('PAPERKIT_WORKFLOW_SCHEMA_PATH', 
                                     repo_root / ".paperkit" / "_cfg" / "schemas" / "workflow-schema.json"))
    
    if args.workflows_dir:
        workflows_dir = Path(args.workflows_dir)
    else:
        workflows_dir = Path(os.getenv('PAPERKIT_WORKFLOWS_DIR',
                                        repo_root / ".paperkit" / "_cfg" / "workflows"))
    
    print("Workflow Schema Validation")
    print("=" * 70)
    
    # Load schema
    if args.verbose:
        print(f"\nLoading schema from: {schema_path}")
    schema = load_json_schema(schema_path)
    
    # Discover available resources for reference validation (FR-016)
    available_agents: Set[str] = set()
    available_skills: Set[str] = set()
    available_tools: Set[str] = set()
    available_workflows: Set[str] = set()
    
    if not args.skip_references:
        if args.verbose:
            print("\nDiscovering available agents, skills, tools, and workflows...")
        available_agents = discover_available_agents(repo_root)
        available_skills = discover_available_skills(repo_root)
        available_tools = discover_available_tools(repo_root)
        available_workflows = discover_available_workflows(repo_root)
        
        if args.verbose:
            print(f"  Found {len(available_agents)} agents")
            print(f"  Found {len(available_skills)} skills")
            print(f"  Found {len(available_tools)} tools")
            print(f"  Found {len(available_workflows)} workflows")
    
    # Find workflow files
    workflow_files = find_workflow_files(workflows_dir, args.workflow)
    
    if not workflow_files:
        print("\nNo workflow files found to validate")
        sys.exit(1 if args.ci else 0)
    
    print(f"\nValidating {len(workflow_files)} workflow(s)...")
    print()
    
    # Load all workflows for depth validation
    workflows_data: Dict[str, Dict] = {}
    
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
        
        # Store for depth validation
        workflows_data[workflow_name] = workflow_data
        
        # Schema validation
        is_valid, errors = validate_workflow(workflow_data, schema, workflow_name)
        
        # Reference validation (FR-016)
        if not args.skip_references:
            ref_errors = validate_references(
                workflow_data,
                workflow_name,
                available_agents,
                available_skills,
                available_tools,
                available_workflows
            )
            errors.extend(ref_errors)
            if ref_errors:
                is_valid = False
        
        results.append((workflow_name, is_valid, errors))
        
        if not is_valid:
            total_errors += len(errors)
    
    # Depth validation (FR-013)
    depth_results = validate_workflow_depth(workflows_data, args.max_depth)
    depth_violations = []
    
    for workflow_name, (depth, path, is_depth_valid) in depth_results.items():
        if not is_depth_valid:
            if depth < 0:
                depth_violations.append(
                    f"  {workflow_name}: CIRCULAR DEPENDENCY detected in path: {' -> '.join(path)}"
                )
            else:
                depth_violations.append(
                    f"  {workflow_name}: Depth {depth} exceeds limit {args.max_depth} (path: {' -> '.join(path)})"
                )
    
    # Display results
    for workflow_name, is_valid, errors in results:
        icon = "✓" if is_valid else "✗"
        status = "VALID" if is_valid else "INVALID"
        print(f"{icon} {workflow_name:25} {status}")
        
        if not is_valid:
            for error in errors:
                print(error)
            print()
    
    # Display depth violations
    if depth_violations:
        print("\nWorkflow Depth Violations (FR-013):")
        for violation in depth_violations:
            print(violation)
        print()
        total_errors += len(depth_violations)
    
    # Summary
    print("=" * 70)
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)
    invalid_count = len(results) - valid_count
    
    print(f"\nValidation Summary:")
    print(f"  Total workflows:      {len(results)}")
    print(f"  Schema valid:         {valid_count}")
    print(f"  Schema invalid:       {invalid_count}")
    print(f"  Depth violations:     {len(depth_violations)}")
    print(f"  Total errors:         {total_errors}")
    
    if not args.skip_references:
        print(f"\nReference Validation (FR-016):")
        print(f"  Available agents:     {len(available_agents)}")
        print(f"  Available skills:     {len(available_skills)}")
        print(f"  Available tools:      {len(available_tools)}")
        print(f"  Available workflows:  {len(available_workflows)}")
    
    print(f"\nDepth Validation (FR-013):")
    print(f"  Max allowed depth:    {args.max_depth}")
    
    # Exit code
    if invalid_count > 0 or depth_violations:
        print(f"\n⚠️  Validation failed with {invalid_count + len(depth_violations)} issue(s)")
        sys.exit(1 if args.ci else 0)
    else:
        print("\n✓ All workflows validated successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()
