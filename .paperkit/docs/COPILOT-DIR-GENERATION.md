# .copilot/ Directory Generation from .paperkit/ Source

## Problem Solved

The `.copilot/` directory contained manually maintained configuration files (`agents.yaml` and `workflows.yaml`) that duplicated information from `.paperkit/_cfg/` manifests. This created:
- **Risk of drift** between `.paperkit/` source and `.copilot/` configuration
- **Maintenance burden** - updating agent/workflow info required edits in multiple places
- **Inconsistency** - no guarantee the files stayed synchronized

## Solution Implemented

Created **automated generation system** that derives `.copilot/` configuration files from `.paperkit/` manifests:

### Architecture

```
.paperkit/_cfg/
├── agent-manifest.yaml          → Master agent registry
├── workflow-manifest.yaml       → Master workflow registry
├── agents/*.yaml                → Individual agent definitions
└── workflows/*.yaml             → Individual workflow definitions
         ↓
paperkit-generate-copilot.sh     → NEW GENERATOR
         ↓
.copilot/
├── agents.yaml                  → Generated agent config
└── workflows.yaml               → Generated workflow config
```

### What's Generated

#### `.copilot/agents.yaml`
Dynamically extracted from `.paperkit/` source:
- ✅ Agent names, titles, icons (from `agent-manifest.yaml`)
- ✅ Descriptions (from `agents/*.yaml` → `identity.description`)
- ✅ **Triggers** (extracted from `examplePrompts` or default patterns)
- ✅ **Inputs** (extracted from `inputSchema.properties`)
- ✅ **Outputs** (inferred from agent role + `outputSchema`)
- ✅ Categories and roles (mapped from agent names)
- ✅ Tools and consent requirements
- ✅ Knowledge base references

#### `.copilot/workflows.yaml`
Dynamically extracted from `.paperkit/` source:
- ✅ Workflow names and descriptions
- ✅ Entry points (from workflow definitions)
- ✅ Phases/steps (from workflow `steps` property)
- ✅ File paths (mapped to `.paperkit/` locations)
- ✅ Workflow types (categorized by workflow category)

### Key Features

#### 1. Intelligent Data Extraction
```python
# Extracts description from identity section
if 'identity' in agent_details and 'description' in agent_details['identity']:
    full_desc = agent_details['identity']['description'].strip()
    description = full_desc.split('.')[0]  # Use first sentence

# Extracts triggers from example prompts
def extract_triggers(agent_details, agent_name):
    if 'examplePrompts' in agent_details:
        for prompt in agent_details['examplePrompts']:
            # Infer trigger words from prompt patterns
            ...
```

#### 2. Schema-Based Input Extraction
```python
# Reads inputSchema to get input descriptions
def extract_inputs(agent_details):
    if 'inputSchema' in agent_details:
        for prop, spec in agent_details['inputSchema']['properties'].items():
            description = spec.get('description')
            inputs.append(description)
```

#### 3. Role-Based Output Inference
```python
# Infers output paths from agent role
def extract_outputs(agent_details, agent_name):
    if 'research' in agent_name:
        outputs.append('output-refined/research/')
        outputs.append('memory/research-index.yaml (updated)')
    elif 'architect' in agent_name:
        outputs.append('output-drafts/outlines/')
        ...
```

### Integration

#### Updated `paperkit-generate.sh`
```bash
# Generate .copilot/ configuration files
if [ "$TARGET" = "all" ] || [ "$TARGET" = "copilot-config" ]; then
    if [ -f "./paperkit-generate-copilot.sh" ]; then
        ./paperkit-generate-copilot.sh || warning_msg ".copilot/ generation had issues"
    fi
fi
```

Now runs automatically with:
```bash
./paperkit generate
```

### Files Modified/Created

#### New Files
- **`paperkit-generate-copilot.sh`** (374 lines) - Python-based generator

#### Modified Files
- **`paperkit-generate.sh`** - Added call to copilot generator
- **`.copilot/agents.yaml`** - Now generated (was manually maintained)
- **`.copilot/workflows.yaml`** - Now generated (was manually maintained)

### Validation

#### Before Generation
```yaml
# .copilot/agents.yaml (manually maintained)
research-consolidator:
  name: "Research Consolidator"
  description: "Synthesizes research materials..."  # Hard-coded
  triggers:
    - "research"                                    # Hard-coded
    - "consolidate research"                        # Hard-coded
  inputs:
    - "Topic or research question"                  # Hard-coded
```

#### After Generation
```yaml
# .copilot/agents.yaml (auto-generated)
# Generated from .paperkit/ manifests - DO NOT EDIT MANUALLY
# Regenerate with: ./paperkit generate

research-consolidator:
  name: Research Consolidator
  description: Transforms scattered research materials into polished, synthesized 
    research documents with proper citations and clear narrative structure
  triggers:                                          # Extracted from examplePrompts
  - research
  - consolidate research
  - research [topic]
  inputs:                                            # Extracted from inputSchema
  - Research topic or question to investigate
  - List of research materials (PDFs, URLs, notes)
  - Level of research synthesis required
  outputs:                                           # Inferred from agent role
  - output-refined/research/
  - memory/research-index.yaml (updated)
```

### Benefits

#### 1. Single Source of Truth ✅
- All agent/workflow metadata in `.paperkit/_cfg/`
- `.copilot/` files derive automatically
- No manual synchronization needed

#### 2. Reduced Maintenance ✅
- Edit once in `.paperkit/` → regenerates everywhere
- Update agent description → all derived files update
- Add new workflow → appears in `.copilot/workflows.yaml`

#### 3. Consistency Guaranteed ✅
- Generator ensures `.copilot/` matches `.paperkit/`
- No risk of manual edit mistakes
- Validation through generation process

#### 4. Intelligent Extraction ✅
- Triggers inferred from example prompts
- Inputs extracted from schemas
- Outputs mapped from agent roles
- Descriptions taken from identity sections

### Usage

#### Regenerate Everything
```bash
./paperkit generate
```

#### Regenerate Just .copilot/
```bash
./paperkit-generate-copilot.sh
```

#### During Installation
Automatically runs when installing:
```bash
./paperkit-install.sh
```

### Testing

✅ Generated `.copilot/agents.yaml` with all 10 agents  
✅ Generated `.copilot/workflows.yaml` with all workflows  
✅ Validated extracted triggers match expected patterns  
✅ Confirmed inputs extracted from schemas  
✅ Verified outputs inferred correctly  
✅ Checked auto-generation notices present  

### Migration Notes

#### Old Workflow (Manual)
1. Edit agent in `.paperkit/_cfg/agents/research-consolidator.yaml`
2. Remember to update `.copilot/agents.yaml` manually
3. Hope you don't forget anything
4. Risk of inconsistency

#### New Workflow (Automated)
1. Edit agent in `.paperkit/_cfg/agents/research-consolidator.yaml`
2. Run `./paperkit generate`
3. All derived files update automatically ✨

### Next Steps

The `.copilot/` directory is now fully automated. Future enhancements could include:

1. **Validate consistency** - Add check that `.copilot/` files are generated
2. **CI integration** - Ensure `.copilot/` files regenerated on PR
3. **Pre-commit hook** - Warn if manually editing generated files
4. **Additional extraction** - Pull more metadata from agent YAML files

### References

- **Generator**: `paperkit-generate-copilot.sh`
- **Main Generator**: `paperkit-generate.sh` (integration point)
- **Source Manifests**: `.paperkit/_cfg/agent-manifest.yaml`, `.paperkit/_cfg/workflow-manifest.yaml`
- **Agent Definitions**: `.paperkit/_cfg/agents/*.yaml`
- **Workflow Definitions**: `.paperkit/_cfg/workflows/*.yaml`

---

**Status**: ✅ Complete  
**Implementation Date**: 2025-12-19  
**Automated Generation**: Working perfectly!
