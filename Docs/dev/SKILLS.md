# PaperKit Skills & Workflows Architecture

**Version**: 2.0.0
**Last Updated**: 2026-01-20

---

## Overview

PaperKit uses a **dual architecture** for reusable capabilities:

| Concept | Format | Purpose | Location |
|---------|--------|---------|----------|
| **Agent Skills** | SKILL.md | HOW to do something (instructions) | `.paperkit/_cfg/skills/{name}/` |
| **Compositional Workflows** | YAML | WHAT steps to execute (orchestration) | `.paperkit/_cfg/workflows/` |

This separation follows the [agentskills.io](https://agentskills.io) specification for Agent Skills while maintaining backward compatibility with YAML workflows.

```
┌─────────────────────────────────────────────────────────────────┐
│                    DUAL ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌────────────────────┐     ┌────────────────────┐            │
│    │   AGENT SKILLS     │     │    WORKFLOWS       │            │
│    │    (SKILL.md)      │     │      (YAML)        │            │
│    ├────────────────────┤     ├────────────────────┤            │
│    │ HOW to do things   │     │ WHAT steps to run  │            │
│    │ • Instructions     │     │ • Step sequences   │            │
│    │ • Guidelines       │     │ • Agent routing    │            │
│    │ • Patterns         │     │ • I/O schemas      │            │
│    │ • Best practices   │     │ • Error handling   │            │
│    └────────────────────┘     └────────────────────┘            │
│              │                         │                         │
│              └─────────┬───────────────┘                         │
│                        │                                         │
│                        ▼                                         │
│              ┌──────────────────┐                                │
│              │      AGENT       │                                │
│              │  (Executes with  │                                │
│              │   skill context) │                                │
│              └──────────────────┘                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 1: Agent Skills (SKILL.md)

### What Are Agent Skills?

Agent Skills are **instructional documents** that teach an agent HOW to perform specific tasks. They follow the [agentskills.io](https://agentskills.io) specification—an emerging industry standard adopted by VS Code, Claude Code, Cursor, Gemini CLI, and other AI tools.

**Key characteristics:**
- **Format**: Markdown files with YAML frontmatter
- **Content**: Instructions, guidelines, patterns, examples
- **Loading**: Progressive disclosure (metadata first, full content on demand)
- **Size**: <5000 tokens for efficient context management

### Available Skills

| Skill | Description | Use Case |
|-------|-------------|----------|
| `humanizer` | Remove AI writing patterns | Editing AI-generated text |
| `academic-writing` | Academic paper composition | Writing formal papers |
| `harvard-citations` | Harvard citation style | Creating references |
| `latex-best-practices` | LaTeX document guidelines | Formatting documents |

### SKILL.md File Structure

Each skill lives in its own directory: `.paperkit/_cfg/skills/{skill-name}/SKILL.md`

```markdown
---
name: skill-name
description: Brief description (1-2 sentences)
metadata:
  author: author-name
  version: "1.0.0"
---

# Skill Title

## Your Task

When given [input], do [output]:

1. Step one
2. Step two
3. Step three

## Guidelines

### Section One
- Guideline 1
- Guideline 2

### Section Two
...

## Examples

### Good Example
...

### Bad Example
...
```

### Creating a New Skill

#### Step 1: Create Directory and SKILL.md

```bash
mkdir -p .paperkit/_cfg/skills/my-skill
```

Create `.paperkit/_cfg/skills/my-skill/SKILL.md`:

```markdown
---
name: my-skill
description: What this skill does in 1-2 sentences.
metadata:
  author: your-name
  version: "1.0.0"
---

# My Skill Name

## Your Task

When given [context], your job is to:

1. First thing to do
2. Second thing to do
3. Final output

## Guidelines

### Category One

- Specific guideline
- Another guideline
- Third guideline

### Category Two

...

## Examples

### Good Example

Input: ...
Output: ...

### Avoid

Input: ...
Why it's wrong: ...
```

#### Step 2: Validate

```bash
python .paperkit/tools/validate-skill-frontmatter.py --all
```

#### Step 3: Link to Agents (Optional)

Add to agent's `suggestedSkills` in `.paperkit/_cfg/agents/{agent}.yaml`:

```yaml
suggestedSkills:
  - my-skill
```

### Skill Frontmatter Schema

Required fields:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Machine identifier (kebab-case) |
| `description` | string | Brief description |

Optional fields:

| Field | Type | Description |
|-------|------|-------------|
| `metadata.author` | string | Skill author |
| `metadata.version` | string | Semantic version |
| `license` | string | License identifier |
| `compatibility` | string | Compatibility notes |

### Using the Skill Registry

#### Python API

```python
from skill_registry import AgentSkillRegistry

registry = AgentSkillRegistry()
registry.load_all()  # <50ms

# List all skills
skills = registry.list_skills()
for skill in skills:
    print(f"{skill.name}: {skill.description}")

# Search for skills
matches = registry.find_skills("citation harvard")
for match in matches:
    print(f"{match.skill.name} (score: {match.score})")

# Progressive disclosure: metadata only
skill = registry.get_skill("harvard-citations")
print(skill.name, skill.description)  # ~100 tokens

# Progressive disclosure: full content on demand
content = registry.load_skill_content("harvard-citations")  # <5000 tokens
```

#### CLI

```bash
# List all skills
python .paperkit/tools/skill_registry.py skills --list

# Search for skills
python .paperkit/tools/skill_registry.py skills --find "citation"

# Get skill metadata
python .paperkit/tools/skill_registry.py skills --get harvard-citations

# Load full content
python .paperkit/tools/skill_registry.py skills --content humanizer

# Benchmark load time (target: <50ms)
python .paperkit/tools/skill_registry.py skills --benchmark
```

---

## Part 2: Compositional Workflows (YAML)

### What Are Workflows?

Workflows define **WHAT steps** to execute and in WHAT order. They orchestrate multiple agents to complete complex tasks.

**Key characteristics:**
- **Format**: YAML definition files
- **Content**: Step sequences, agent routing, I/O schemas
- **Purpose**: Multi-step task automation
- **Integration**: Can reference Agent Skills for context

### Available Workflows

| Workflow | Type | Description | Agents Involved |
|----------|------|-------------|-----------------|
| `cite-source` | composite | Extract metadata and format citation | Reference Manager |
| `validate-citation` | conditional | Validate citation by type | Reference Manager |
| `draft-section` | composite | Draft paper section with outline | Section Drafter |
| `research-topic` | composite | Research and consolidate findings | Research Consolidator |
| `compile-latex` | atomic | Compile LaTeX to PDF | LaTeX Assembler |

### Workflow Types

#### 1. Atomic Workflows

Single agent, single action:

```yaml
name: compile-latex
type: atomic
steps:
  - action: compile-document
    agent: latex-assembler
    tool: build-latex
```

#### 2. Composite Workflows

Multi-step sequences:

```yaml
name: cite-source
type: composite
steps:
  - action: extract-metadata
    agent: reference-manager
    inputs: [source_url]
    outputs: [metadata]
  - action: format-citation
    agent: reference-manager
    skill: harvard-citations  # Loads skill context!
    inputs: [metadata]
    outputs: [citation, bibtex]
```

#### 3. Conditional Workflows

Branching logic:

```yaml
name: validate-citation
type: conditional
steps:
  - action: validate-doi
    agent: reference-manager
    condition: "citation_type == 'doi'"
  - action: validate-url
    condition: "citation_type == 'url'"
```

### Workflow + Skill Integration

Workflows can reference Agent Skills using the `skill` field:

```yaml
steps:
  - action: format-citation
    agent: reference-manager
    skill: harvard-citations  # Agent loads this skill for context
    inputs: [metadata]
    outputs: [citation]
```

When a step has a `skill` field:
1. The workflow executor loads the skill's full content
2. The skill instructions are injected into the agent's context
3. The agent executes with enhanced knowledge

### Creating a New Workflow

#### Step 1: Create YAML Definition

Create `.paperkit/_cfg/workflows/my-workflow.yaml`:

```yaml
name: my-workflow
displayName: My Workflow
description: What this workflow does
version: 1.0.0
type: composite

prerequisites:
  - type: skill
    name: required-skill
  - type: tool
    name: required-tool

steps:
  - action: step-one
    agent: agent-name
    skill: optional-skill  # Load skill context
    inputs:
      - input_var
    outputs:
      - intermediate_result
    onError: fail

  - action: step-two
    agent: another-agent
    inputs:
      - intermediate_result
    outputs:
      - final_output
    onError: skip

inputSchema:
  type: object
  properties:
    input_var:
      type: string
      description: Description of input
  required:
    - input_var

outputSchema:
  type: object
  properties:
    final_output:
      type: string
  required:
    - final_output

timeout: 60000
retryPolicy:
  maxRetries: 2
  backoffMs: 1000

metadata:
  author: your-name
  tags: [tag1, tag2]
  category: category-name
```

#### Step 2: Update Manifest

Add to `.paperkit/_cfg/workflow-manifest.yaml`:

```yaml
workflows:
  - name: my-workflow
    path: .paperkit/_cfg/workflows/my-workflow.yaml
    displayName: My Workflow
    type: composite
    description: What this workflow does
    category: category-name
    status: active
```

#### Step 3: Validate

```bash
python .paperkit/tools/validate-workflows.py --verbose
```

### Workflow Schema Reference

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Machine identifier (kebab-case) |
| `displayName` | string | Human-readable name |
| `description` | string | What the workflow does |
| `version` | string | Semantic version |
| `type` | enum | `atomic`, `composite`, `conditional` |
| `steps` | array | Ordered execution steps |
| `inputSchema` | object | JSON Schema for inputs |
| `outputSchema` | object | JSON Schema for outputs |

#### Step Fields

| Field | Required | Description |
|-------|----------|-------------|
| `action` | ✅ | Step identifier |
| `agent` | ✅ | Agent to execute |
| `inputs` | ✅ | Input variable names |
| `outputs` | ✅ | Output variable names |
| `skill` | ❌ | Agent Skill to load |
| `condition` | ❌ | Conditional expression |
| `onError` | ❌ | `fail`, `skip`, `retry` |

### Using the Workflow Registry

#### Python API

```python
from skill_registry import WorkflowRegistry

registry = WorkflowRegistry()

# List workflows
workflows = registry.list_workflows()

# Get specific workflow
workflow = registry.get_workflow("cite-source")

# Find by task
matches = registry.find_workflows_for_task("format citation")

# Get statistics
stats = registry.get_statistics()
```

#### CLI

```bash
# List workflows
python .paperkit/tools/skill_registry.py workflows --list

# Get workflow details
python .paperkit/tools/skill_registry.py workflows --get cite-source

# Find workflows
python .paperkit/tools/skill_registry.py workflows --find "citation"

# Statistics
python .paperkit/tools/skill_registry.py workflows --stats
```

---

## Part 3: When to Use Skills vs Workflows

### Use Agent Skills When:

- Teaching an agent **how to do something**
- Providing **guidelines, patterns, or best practices**
- Creating **reusable instructional content**
- Need **progressive disclosure** (load on demand)
- Content is **text-heavy** (instructions, examples)

**Examples:**
- Writing style guides
- Citation formatting rules
- Code patterns and conventions
- Review checklists

### Use Workflows When:

- Defining **what steps to execute**
- Orchestrating **multiple agents** in sequence
- Need **conditional branching** based on inputs
- Automating **multi-step processes**
- Defining **input/output contracts**

**Examples:**
- Paper drafting pipeline
- Citation validation process
- Research consolidation flow
- Document compilation

### Combined Usage

The most powerful pattern combines both:

```yaml
# Workflow defines WHAT to do
steps:
  - action: format-citation
    agent: reference-manager
    skill: harvard-citations  # Skill defines HOW to do it
```

---

## Part 4: Validation & CI

### Validate Agent Skills

```bash
# Validate all SKILL.md files
python .paperkit/tools/validate-skill-frontmatter.py --all

# CI mode (exit code on failure)
python .paperkit/tools/validate-skill-frontmatter.py --all --ci

# Validate specific skill
python .paperkit/tools/validate-skill-frontmatter.py \
  --path .paperkit/_cfg/skills/humanizer/SKILL.md
```

### Validate Workflows

```bash
# Validate all workflows
python .paperkit/tools/validate-workflows.py --verbose

# CI mode
python .paperkit/tools/validate-workflows.py --ci
```

### GitHub Actions

Both validators run automatically on PRs via `.github/workflows/validate-agent-metadata.yml`:

```yaml
- name: Validate Agent Skills (SKILL.md)
  run: python .paperkit/tools/validate-skill-frontmatter.py --all --ci

- name: Run unified agent system check
  run: python .paperkit/tools/check-agents.py --ci
```

---

## Part 5: Directory Structure

```
.paperkit/_cfg/
├── skills/                        # Agent Skills (SKILL.md)
│   ├── humanizer/
│   │   └── SKILL.md
│   ├── academic-writing/
│   │   └── SKILL.md
│   ├── harvard-citations/
│   │   └── SKILL.md
│   └── latex-best-practices/
│       └── SKILL.md
│
├── workflows/                     # Compositional Workflows (YAML)
│   ├── cite-source.yaml
│   ├── validate-citation.yaml
│   ├── draft-section.yaml
│   ├── research-topic.yaml
│   └── compile-latex.yaml
│
└── schemas/
    ├── skill-frontmatter-schema.json   # SKILL.md validation
    └── workflow-schema.json            # Workflow YAML validation
```

---

## Part 6: Migration from Legacy "Skills"

The original PaperKit "skills" were actually compositional workflows. The renaming clarifies:

| Old Name | New Name | Location |
|----------|----------|----------|
| Skills (YAML) | Workflows | `.paperkit/_cfg/workflows/` |
| — (new) | Agent Skills | `.paperkit/_cfg/skills/` |

If you have existing YAML "skills":
1. Move to `.paperkit/_cfg/workflows/`
2. Update any references from "skill" to "workflow"
3. Consider creating SKILL.md files for instructional content

---

## Related Documentation

- [Agent Schema](.paperkit/_cfg/schemas/agent-schema.json)
- [Skill Frontmatter Schema](.paperkit/_cfg/schemas/skill-frontmatter-schema.json)
- [Workflow Schema](.paperkit/_cfg/schemas/workflow-schema.json)
- [Harvard Citation Guide](.paperkit/_cfg/guides/harvard-citation-guide.md)
- [agentskills.io Specification](https://agentskills.io)
