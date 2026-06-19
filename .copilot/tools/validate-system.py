#!/usr/bin/env python3
"""
Validate System Configuration

Checks the .copilot/ directory structure for:
- YAML syntax validity
- Required files existence
- Agent/command completeness
- Workflow consistency
- Registry integrity
"""

import os
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Base path
BASE_DIR = Path(__file__).parent.parent
COPILOT_DIR = BASE_DIR

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def load_yaml(filepath: Path) -> Tuple[Any, str]:
    """Load a YAML file and return (data, error)."""
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        return data, None
    except yaml.YAMLError as e:
        return None, f"YAML syntax error: {e}"
    except FileNotFoundError:
        return None, "File not found"
    except Exception as e:
        return None, str(e)

def check_yaml_files(directory: Path, pattern: str = "**/*.yaml") -> List[Dict]:
    """Check all YAML files in directory for syntax errors."""
    results = []
    for filepath in directory.glob(pattern):
        data, error = load_yaml(filepath)
        results.append({
            'file': str(filepath.relative_to(BASE_DIR)),
            'valid': error is None,
            'error': error,
            'data': data
        })
    return results

def check_required_files() -> List[Dict]:
    """Check that all required system files exist."""
    required = [
        'agents.yaml',
        'commands.yaml', 
        'workflows.yaml',
        'config/settings.yaml',
        'config/consent.yaml',
        'tools/tools.yaml',
        'memory/paper-metadata.yaml',
        'memory/research-index.yaml',
        'memory/section-status.yaml',
        'memory/working-reference.md',
        'memory/revision-log.md',
        'README.md',
    ]
    
    results = []
    for filepath in required:
        full_path = COPILOT_DIR / filepath
        exists = full_path.exists()
        results.append({
            'file': filepath,
            'exists': exists,
            'required': True
        })
    return results

def check_agent_registry() -> List[Dict]:
    """Validate agent registry completeness."""
    results = []
    agents_yaml, error = load_yaml(COPILOT_DIR / 'agents.yaml')
    
    if error:
        results.append({'check': 'agents.yaml', 'valid': False, 'error': error})
        return results
    
    # Check each agent has required fields
    required_fields = ['name', 'description', 'spec-file']
    
    agents_section = agents_yaml.get('agents', {})
    for category in ['core', 'specialist', 'system']:
        if category not in agents_section:
            results.append({
                'check': f'{category} section',
                'valid': False,
                'error': f'Missing {category} section in agents.yaml'
            })
            continue
            
        for agent_id, agent in agents_section.get(category, {}).items():
            if not isinstance(agent, dict):
                results.append({
                    'check': f'Agent: {agent_id}',
                    'valid': False,
                    'error': 'Invalid agent definition'
                })
                continue
                
            missing = [f for f in required_fields if f not in agent]
            
            if missing:
                results.append({
                    'check': f'Agent: {agent_id}',
                    'valid': False,
                    'error': f'Missing fields: {missing}'
                })
            else:
                # Check spec file exists
                spec_file = agent.get('spec-file')
                if spec_file:
                    full_path = COPILOT_DIR / spec_file
                    if not full_path.exists():
                        results.append({
                            'check': f'Agent: {agent_id}',
                            'valid': False,
                            'error': f'Spec file not found: {spec_file}'
                        })
                    else:
                        results.append({
                            'check': f'Agent: {agent_id}',
                            'valid': True,
                            'error': None
                        })
    
    return results

def check_command_registry() -> List[Dict]:
    """Validate command registry completeness."""
    results = []
    commands_yaml, error = load_yaml(COPILOT_DIR / 'commands.yaml')
    
    if error:
        results.append({'check': 'commands.yaml', 'valid': False, 'error': error})
        return results
    
    required_fields = ['id', 'display-name', 'agent']
    
    for group in commands_yaml.get('groups', []):
        group_id = group.get('id', 'unknown')
        
        for command in group.get('commands', []):
            cmd_id = command.get('id', 'unknown')
            missing = [f for f in required_fields if f not in command]
            
            if missing:
                results.append({
                    'check': f'Command: {cmd_id}',
                    'valid': False,
                    'error': f'Missing fields: {missing}'
                })
            else:
                # Check spec file exists
                spec_file = command.get('spec-file')
                if spec_file:
                    full_path = COPILOT_DIR / spec_file
                    if not full_path.exists():
                        results.append({
                            'check': f'Command: {cmd_id}',
                            'valid': False,
                            'error': f'Spec file not found: {spec_file}'
                        })
                    else:
                        results.append({
                            'check': f'Command: {cmd_id}',
                            'valid': True,
                            'error': None
                        })
    
    return results

def check_workflow_registry() -> List[Dict]:
    """Validate workflow registry completeness."""
    results = []
    workflows_yaml, error = load_yaml(COPILOT_DIR / 'workflows.yaml')
    
    if error:
        results.append({'check': 'workflows.yaml', 'valid': False, 'error': error})
        return results
    
    workflows = workflows_yaml.get('workflows', {})
    for wf_id, workflow in workflows.items():
        if not isinstance(workflow, dict):
            results.append({
                'check': f'Workflow: {wf_id}',
                'valid': False,
                'error': 'Invalid workflow definition'
            })
            continue
            
        spec_file = workflow.get('file')
        
        if spec_file:
            full_path = COPILOT_DIR / spec_file
            if not full_path.exists():
                results.append({
                    'check': f'Workflow: {wf_id}',
                    'valid': False,
                    'error': f'Spec file not found: {spec_file}'
                })
            else:
                results.append({
                    'check': f'Workflow: {wf_id}',
                    'valid': True,
                    'error': None
                })
    
    return results

def print_results(title: str, results: List[Dict], key_field: str = 'file'):
    """Print validation results in a formatted way."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)
    
    passed = 0
    failed = 0
    
    for result in results:
        identifier = result.get(key_field, result.get('check', 'unknown'))
        is_valid = result.get('valid', result.get('exists', False))
        error = result.get('error')
        
        if is_valid:
            print(f"  {GREEN}✓{RESET} {identifier}")
            passed += 1
        else:
            print(f"  {RED}✗{RESET} {identifier}")
            if error:
                print(f"    {YELLOW}→ {error}{RESET}")
            failed += 1
    
    print(f"\n  {GREEN}{passed} passed{RESET}, {RED}{failed} failed{RESET}")
    return passed, failed

def main():
    print("\n" + "="*60)
    print(" .copilot/ System Validation")
    print("="*60)
    
    total_passed = 0
    total_failed = 0
    
    # Check required files
    results = check_required_files()
    p, f = print_results("Required Files", results, 'file')
    total_passed += p
    total_failed += f
    
    # Check YAML syntax
    results = check_yaml_files(COPILOT_DIR)
    p, f = print_results("YAML Syntax", results, 'file')
    total_passed += p
    total_failed += f
    
    # Check agent registry
    results = check_agent_registry()
    p, f = print_results("Agent Registry", results, 'check')
    total_passed += p
    total_failed += f
    
    # Check command registry
    results = check_command_registry()
    p, f = print_results("Command Registry", results, 'check')
    total_passed += p
    total_failed += f
    
    # Check workflow registry
    results = check_workflow_registry()
    p, f = print_results("Workflow Registry", results, 'check')
    total_passed += p
    total_failed += f
    
    # Summary
    print("\n" + "="*60)
    print(" SUMMARY")
    print("="*60)
    print(f"  Total: {GREEN}{total_passed} passed{RESET}, {RED}{total_failed} failed{RESET}")
    
    if total_failed > 0:
        print(f"\n  {RED}Validation FAILED{RESET}")
        sys.exit(1)
    else:
        print(f"\n  {GREEN}Validation PASSED{RESET}")
        sys.exit(0)

if __name__ == '__main__':
    main()
