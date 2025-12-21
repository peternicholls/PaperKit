#!/bin/bash
# PaperKit .copilot/ Directory Generator
# Generates .copilot/ configuration files from .paperkit/ source of truth
# Usage: ./paperkit-generate-copilot.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPERKIT_ROOT="${SCRIPT_DIR}"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info_msg() { echo -e "${BLUE}ℹ ${NC}$1"; }
success_msg() { echo -e "${GREEN}✓ ${NC}$1"; }
error_msg() { echo -e "${RED}✗ ${NC}$1"; }

# Check .paperkit exists
if [ ! -d "${PAPERKIT_ROOT}/.paperkit" ]; then
    error_msg ".paperkit/ directory not found. Run from PaperKit root."
    exit 1
fi

# Check Python and pyyaml
# Use venv Python if available, otherwise fall back to system Python
if [ -f "${PAPERKIT_ROOT}/.venv/bin/python" ]; then
    PYTHON_CMD="${PAPERKIT_ROOT}/.venv/bin/python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    error_msg "Python 3 is required but not found."
    exit 1
fi

if ! "$PYTHON_CMD" -c "import yaml" 2>/dev/null; then
    error_msg "PyYAML is required. Install with: pip install pyyaml"
    exit 1
fi

info_msg "Generating .copilot/ files from .paperkit/ manifests..."

# Generate .copilot/agents.yaml and .copilot/workflows.yaml
"$PYTHON_CMD" << 'PYTHON_SCRIPT'
import yaml
import os
from pathlib import Path
from datetime import datetime

paperkit_root = Path(os.getcwd())
copilot_dir = paperkit_root / '.copilot'

# Load manifests
agent_manifest_path = paperkit_root / '.paperkit' / '_cfg' / 'agent-manifest.yaml'
workflow_manifest_path = paperkit_root / '.paperkit' / '_cfg' / 'workflow-manifest.yaml'

with open(agent_manifest_path) as f:
    agent_manifest = yaml.safe_load(f)

with open(workflow_manifest_path) as f:
    workflow_manifest = yaml.safe_load(f)

agents_list = agent_manifest['agents']
workflows_list = workflow_manifest['workflows']

# Separate agents by module
core_agents = [a for a in agents_list if a.get('module') == 'core']
specialist_agents = [a for a in agents_list if a.get('module') == 'specialist']

# Build .copilot/agents.yaml structure
copilot_agents = {
    'version': '1.0.0',
    'description': 'Registry of all agents available in the Copilot Research Paper Assistant Kit',
    'categories': {
        'core': 'Core paper writing agents (from Open Agent System)',
        'specialist': 'Support agents for brainstorming, problem-solving, feedback, research',
        'system': 'System agents for routing and orchestration'
    },
    'agents': {
        'core': {},
        'specialist': {},
        'system': {
            'paper-system': {
                'name': 'Paper System Router',
                'description': 'Routes commands to agents, manages consent, orchestrates workflows',
                'category': 'system',
                'role': 'Orchestrator',
                'spec-file': 'agents/paper-system.yaml',
                'internal': True
            }
        }
    }
}

# Map agent data from .paperkit to .copilot format
agent_category_map = {
    'research-consolidator': ('research', 'Synthesizer'),
    'paper-architect': ('planning', 'Architect'),
    'section-drafter': ('writing', 'Writer'),
    'quality-refiner': ('refinement', 'Editor'),
    'reference-manager': ('references', 'Bibliographer'),
    'latex-assembler': ('assembly', 'Engineer'),
    'brainstorm': ('ideation', 'Idea Generator'),
    'problem-solver': ('support', 'Problem Solver'),
    'tutor': ('feedback', 'Mentor'),
    'librarian': ('research', 'Research Guide')
}

# Helper to extract triggers from example prompts or generate defaults
def extract_triggers(agent_details, agent_name):
    # Check for explicit triggers
    if 'triggers' in agent_details:
        return agent_details['triggers']
    
    # Check for example prompts to infer triggers
    triggers = []
    if 'examplePrompts' in agent_details:
        for prompt in agent_details['examplePrompts']:
            # Extract key action words from example prompts
            lower_prompt = prompt.lower()
            if agent_name == 'research-consolidator':
                if any(word in lower_prompt for word in ['research', 'consolidate', 'synthesize']):
                    triggers.extend(['research', 'consolidate research', f'research [topic]'])
                    break
            elif agent_name == 'paper-architect':
                if any(word in lower_prompt for word in ['outline', 'design', 'structure', 'create']):
                    triggers.extend(['plan', 'outline', 'structure'])
                    break
            elif agent_name == 'section-drafter':
                if 'draft' in lower_prompt or 'write' in lower_prompt:
                    triggers.extend(['draft [section]', 'write'])
                    break
    
    # Default fallback
    if not triggers:
        triggers = [agent_name]
    
    return triggers

# Helper to extract inputs from inputSchema
def extract_inputs(agent_details):
    inputs = []
    if 'inputSchema' in agent_details and 'properties' in agent_details['inputSchema']:
        for prop, spec in agent_details['inputSchema']['properties'].items():
            description = spec.get('description', prop.replace('_', ' ').title())
            inputs.append(description)
    return inputs

# Helper to extract outputs from outputSchema or constraints
def extract_outputs(agent_details, agent_name):
    outputs = []
    
    # Try to get from outputSchema
    if 'outputSchema' in agent_details and 'properties' in agent_details['outputSchema']:
        # Map to typical output directories
        if 'document' in agent_details['outputSchema']['properties']:
            if 'research' in agent_name:
                outputs.append('output-refined/research/')
                outputs.append('memory/research-index.yaml (updated)')
            elif 'architect' in agent_name:
                outputs.append('output-drafts/outlines/')
                outputs.append('latex/sections/ (skeletons)')
                outputs.append('memory/paper-metadata.yaml (updated)')
            elif 'drafter' in agent_name:
                outputs.append('output-drafts/sections/')
                outputs.append('memory/section-status.yaml (updated)')
            elif 'refiner' in agent_name:
                outputs.append('output-refined/sections/')
                outputs.append('memory/section-status.yaml (updated)')
    
    # Reference manager special case
    if 'reference' in agent_name:
        outputs.append('latex/references/references.bib')
        outputs.append('output-refined/references/')
    
    # LaTeX assembler special case
    if 'latex' in agent_name or 'assembler' in agent_name:
        outputs.append('latex/ (integrated)')
        outputs.append('output-final/pdf/')
        outputs.append('Build logs')
    
    return outputs

# Process core agents
for agent in core_agents:
    name = agent['name']
    agent_key = name  # Use name directly as key
    
    # Load detailed agent YAML for additional info
    agent_yaml_path = paperkit_root / agent['path']
    agent_details = {}
    if agent_yaml_path.exists():
        with open(agent_yaml_path) as f:
            agent_details = yaml.safe_load(f) or {}
    
    category, role = agent_category_map.get(name, ('general', 'Agent'))
    
    # Extract description from identity section
    description = agent.get('title', agent['name'].replace('-', ' ').title())
    if 'identity' in agent_details and 'description' in agent_details['identity']:
        # Use first sentence or short version
        full_desc = agent_details['identity']['description'].strip()
        description = full_desc.split('.')[0] if '.' in full_desc else full_desc
        description = description.replace('\n', ' ').strip()
    
    agent_config = {
        'name': agent.get('title', agent['name'].replace('-', ' ').title()),
        'description': description,
        'category': category,
        'role': role,
        'triggers': extract_triggers(agent_details, name),
        'inputs': extract_inputs(agent_details),
        'outputs': extract_outputs(agent_details, name),
        'spec-file': f"agents/core/{name}.yaml",
        'doc-file': f"open-agents/agents/{name.replace('-', '_')}.md",
        'requires-tools': agent_details.get('tools', []),
        'requires-consent': bool(agent_details.get('tools'))
    }
    
    # Add workflows if present
    if 'workflows' in agent_details:
        agent_config['workflows'] = agent_details['workflows']
    
    # Add knowledge base if present  
    if 'knowledgeBase' in agent:
        agent_config['knowledgeBase'] = agent['knowledgeBase']
    
    copilot_agents['agents']['core'][agent_key] = agent_config

# Process specialist agents
for agent in specialist_agents:
    name = agent['name']
    agent_key = name
    
    # Load detailed agent YAML
    agent_yaml_path = paperkit_root / agent['path']
    agent_details = {}
    if agent_yaml_path.exists():
        with open(agent_yaml_path) as f:
            agent_details = yaml.safe_load(f) or {}
    
    category, role = agent_category_map.get(name, ('support', 'Agent'))
    
    # Extract description
    description = agent.get('title', agent['name'].replace('-', ' ').title())
    if 'identity' in agent_details and 'description' in agent_details['identity']:
        full_desc = agent_details['identity']['description'].strip()
        description = full_desc.split('.')[0] if '.' in full_desc else full_desc
        description = description.replace('\n', ' ').strip()
    
    # Extract triggers for specialist agents
    triggers = []
    if name == 'brainstorm':
        triggers = ['brainstorm', 'explore ideas', 'think about']
    elif name == 'problem-solver':
        triggers = ['solve', 'stuck on', 'how do we handle']
    elif name == 'tutor':
        triggers = ['tutor-feedback', 'review', 'feedback', 'critique']
    elif name == 'librarian':
        triggers = ['librarian-research', 'librarian-sources', 'librarian-gaps', 'find sources']
    else:
        triggers = [name]
    
    # Outputs for specialist agents
    outputs = [f"planning/YYYYMMDD-[name]/{name}.md"] if name != 'librarian' else [f"planning/YYYYMMDD-[name]/research-roadmap.md"]
    
    agent_config = {
        'name': agent.get('title', agent['name'].replace('-', ' ').title()),
        'description': description,
        'category': category,
        'role': role,
        'triggers': triggers,
        'inputs': extract_inputs(agent_details),
        'outputs': outputs,
        'spec-file': f"agents/specialist/{name}.yaml",
        'doc-file': f".copilot/agents/{name}.md",
        'requires-tools': [],
        'requires-consent': False
    }
    
    copilot_agents['agents']['specialist'][agent_key] = agent_config

# Write .copilot/agents.yaml
agents_output_path = copilot_dir / 'agents.yaml'
with open(agents_output_path, 'w') as f:
    f.write("# .copilot/agents.yaml\n")
    f.write("# Master agent registry - single source of truth for agent discovery and routing\n")
    f.write(f"# Generated from .paperkit/ manifests - DO NOT EDIT MANUALLY\n")
    f.write(f"# Regenerate with: ./paperkit generate\n\n")
    yaml.dump(copilot_agents, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)

print(f"✓ Generated .copilot/agents.yaml")

# Build .copilot/workflows.yaml structure
workflow_type_map = {
    'research': 'writing',
    'planning': 'writing',
    'drafting': 'writing',
    'refinement': 'writing',
    'references': 'writing',
    'assembly': 'writing',
    'initialization': 'initialization',
    'sprint': 'sprint'
}

copilot_workflows = {
    'version': '1.0.0',
    'description': 'Registry of all workflows in the Copilot Research Paper Assistant Kit',
    'workflow-types': {
        'initialization': 'Project setup with canonical documents',
        'sprint': 'Work sprint (plan → tasks → review)',
        'writing': 'Paper writing and refinement'
    },
    'workflows': {}
}

# Group workflows
for workflow in workflows_list:
    name = workflow['name']
    category = workflow.get('category', 'general')
    
    # Load detailed workflow YAML for additional info
    workflow_yaml_path = paperkit_root / workflow['path']
    workflow_details = {}
    if workflow_yaml_path.exists():
        with open(workflow_yaml_path) as f:
            workflow_details = yaml.safe_load(f) or {}
    
    workflow_type = workflow_type_map.get(category, 'writing')
    
    # Map to .copilot workflow structure
    workflow_config = {
        'name': workflow.get('displayName', workflow['name'].replace('-', ' ').title()),
        'description': workflow_details.get('description', workflow.get('description', '')),
        'entry-points': workflow_details.get('entryPoints', [f"paper.{name}"]),
        'file': workflow['path'].replace('.paperkit/_cfg/', ''),
        'typical-duration': workflow_details.get('duration', 'Variable'),
        'phases': workflow_details.get('steps', workflow_details.get('phases', []))
    }
    
    copilot_workflows['workflows'][name] = workflow_config

# Write .copilot/workflows.yaml
workflows_output_path = copilot_dir / 'workflows.yaml'
with open(workflows_output_path, 'w') as f:
    f.write("---\n")
    f.write("# .copilot/workflows.yaml\n")
    f.write("# Master workflow registry - defines sequences and orchestration\n")
    f.write(f"# Generated from .paperkit/ manifests - DO NOT EDIT MANUALLY\n")
    f.write(f"# Regenerate with: ./paperkit generate\n\n")
    yaml.dump(copilot_workflows, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)

print(f"✓ Generated .copilot/workflows.yaml")

PYTHON_SCRIPT

success_msg ".copilot/ generation complete!"
info_msg "Generated: .copilot/agents.yaml, .copilot/workflows.yaml"
