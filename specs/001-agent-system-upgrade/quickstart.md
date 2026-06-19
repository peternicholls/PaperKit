# Quickstart: Agent System Upgrade Development

**Feature**: 001-agent-system-upgrade
**Date**: 2026-01-20

## Prerequisites

- Python 3.8+
- Git
- VS Code with GitHub Copilot extension
- Activated virtual environment

```bash
cd /path/to/PaperKit
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Quick Validation

Verify the current system state before making changes:

```bash
# Run unified agent validation
python .paperkit/tools/check-agents.py --verbose

# Expected output: All checks should pass
```

---

## Phase 1: Consolidation Tasks

### 1.1 Fix Path References

```bash
# Find any remaining .paper/ references
grep -r "\.paper/" .paperkit/tools/ --include="*.py"

# Update to .paperkit/
# Example: sed -i '' 's/\.paper\//\.paperkit\//g' .paperkit/tools/validate.py
```

### 1.2 Remove YAML Frontmatter from MD Files

```bash
# Check for MD files with frontmatter
for f in .paperkit/core/agents/*.md .paperkit/specialist/agents/*.md; do
  if head -1 "$f" | grep -q "^---"; then
    echo "Has frontmatter: $f"
  fi
done

# Remove frontmatter (everything between first --- and second ---)
# Manual review recommended before deletion
```

### 1.3 Validate After Changes

```bash
python .paperkit/tools/check-agents.py --ci
# Exit code 0 = all good
```

---

## Phase 2: Two Skill Concepts

**IMPORTANT**: Phase 2 introduces TWO distinct concepts:

| Concept | Purpose | Format | Location |
|---------|---------|--------|----------|
| **Agent Skills** | Teach agents HOW (instructions) | SKILL.md | `.paperkit/_cfg/skills/{name}/SKILL.md` |
| **Compositional Workflows** | Define WHAT steps (orchestration) | YAML | `.paperkit/_cfg/workflows/{name}.yaml` |

---

## Phase 2a: Creating an Agent Skill (Industry Standard)

Agent Skills follow the [agentskills.io](https://agentskills.io) specification.

### 2a.1 Skill Directory Structure

```
.paperkit/_cfg/skills/{skill-name}/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: additional docs
└── assets/           # Optional: templates, data
```

### 2a.2 SKILL.md Template

```markdown
---
name: my-skill
description: What this skill does and when to use it. Include keywords that help agents identify relevant tasks.
metadata:
  author: your-name
  version: "1.0.0"
allowed-tools: Read Write Edit
---

# My Skill Name

You are [description of persona/role for this skill].

## When to Use

Use this skill when:
- [Trigger condition 1]
- [Trigger condition 2]

## Process

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Examples

### Input
[Example input]

### Output
[Example output]

## Guidelines

- [Guideline 1]
- [Guideline 2]

## Common Mistakes

- [Mistake to avoid]
```

### 2a.3 Validate Skill Frontmatter

```bash
python .paperkit/tools/validate-skill-frontmatter.py --path .paperkit/_cfg/skills/my-skill/
```

### 2a.4 Real Example: humanizer

```markdown
---
name: humanizer
description: Remove signs of AI-generated writing from text. Use when editing or reviewing text to make it sound more natural and human-written.
metadata:
  author: core-team
  version: "2.1.1"
allowed-tools: Read Write Edit Grep Glob
---

# Humanizer: Remove AI Writing Patterns

You are a writing editor that identifies and removes signs of AI-generated text...

[Full instructions follow]
```

---

## Phase 2b: Creating a Compositional Workflow

Compositional Workflows define WHAT steps to execute.

### 2b.1 Workflow File Location

```
.paperkit/_cfg/workflows/{workflow-name}.yaml
```

### 2b.2 Workflow Template

```yaml
# .paperkit/_cfg/workflows/my-workflow.yaml
name: my-workflow
displayName: My Workflow
description: What this workflow does
version: 1.0.0
type: composite  # or atomic, conditional

prerequisites:
  - type: tool
    name: some-tool

steps:
  - action: step-one
    agent: some-agent
    skill: relevant-skill     # Optional: load Agent Skill for context
    inputs:
      - input_var
    outputs:
      - intermediate_var
    onError: fail

  - action: step-two
    agent: another-agent
    inputs:
      - intermediate_var
    outputs:
      - output_var
    onError: fail

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
    output_var:
      type: string
      description: Description of output
  required:
    - output_var
```

### 2b.3 Validate Workflow

```bash
python .paperkit/tools/validate-workflows.py --file .paperkit/_cfg/workflows/my-workflow.yaml
```

---

## How Skills and Workflows Work Together

1. **Agent loads Skill**: Agent declares `suggestedSkills: [academic-writing]` → skill instructions loaded into context

2. **Workflow step loads Skill**: Workflow step specifies `skill: harvard-citations` → agent gets citation instructions for that step

3. **Skill references Workflow**: Skill instructions can say "run the cite-source workflow" → orchestrator executes workflow

Example integration:

```yaml
# Workflow that uses an Agent Skill
steps:
  - action: draft-section
    agent: section-drafter
    skill: academic-writing     # Load writing guidelines
    inputs: [section_name, outline]
    outputs: [draft_content]

  - action: format-citations
    agent: reference-manager
    skill: harvard-citations    # Load citation style guide
    inputs: [draft_content]
    outputs: [formatted_content]
```

---

## Phase 3: Testing Orchestration

### 3.1 Test Intent Classification

```python
# test_orchestrator.py
from paperkit.orchestrator import Orchestrator

orch = Orchestrator()

# Test single-intent request
result = orch.classify_intent("Draft the introduction section")
print(f"Intent: {result.intents}")
print(f"Top agent: {result.top_agent}")
print(f"Confidence: {result.confidence:.2f}")

# Test multi-intent request
result = orch.classify_intent("Research color perception and draft Related Work")
print(f"Intents: {result.intents}")
print(f"Workflow steps: {len(result.workflow.steps)}")
```

### 3.2 Test Routing Accuracy

```bash
# Run against test suite
python .paperkit/tools/test-orchestrator.py --requests tests/routing-test-cases.yaml
```

---

## Phase 4: Tool Integration

### 4.1 Register a New Tool

```yaml
# .paperkit/_cfg/tools/my-tool.yaml
name: my-tool
displayName: My Tool
description: What this tool does
version: 1.0.0
command: ./scripts/my-tool.sh
requiresConsent: true
consentLevel: session
timeout: 30000

inputSchema:
  type: object
  properties:
    input_file:
      type: string
  required:
    - input_file

outputSchema:
  type: object
  properties:
    result:
      type: string
  required:
    - result
```

### 4.2 Test Tool Invocation

```python
from paperkit.tools import ToolRegistry, InvocationContext

registry = ToolRegistry()

# Check consent status
status = registry.check_consent("my-tool")
print(f"Has consent: {status.has_consent}")

# Invoke with consent
result = registry.invoke_tool(
    name="my-tool",
    inputs={"input_file": "test.txt"},
    context=InvocationContext(agent_name="test-agent")
)
print(f"Success: {result.success}")
```

---

## Phase 5: Metrics Collection

### 5.1 Record a Metric

```python
from paperkit.metrics import MetricsCollector, MetricRecord, MetricCategory

collector = MetricsCollector()

collector.record_metric(MetricRecord(
    category=MetricCategory.AGENT,
    entity_name="section-drafter",
    action="draft_section",
    success=True,
    duration_ms=2500
))
```

### 5.2 Query Metrics

```python
# Get summary for an agent
summary = collector.get_summary(
    entity_name="section-drafter",
    category=MetricCategory.AGENT,
    days=30
)
print(f"Success rate: {summary.success_rate:.1%}")
print(f"Avg duration: {summary.avg_duration_ms:.0f}ms")

# Get overall routing accuracy
accuracy = collector.get_routing_accuracy(days=7)
print(f"7-day routing accuracy: {accuracy:.1%}")
```

---

## Common Commands

| Task | Command |
|------|---------|
| Validate all agents | `python .paperkit/tools/check-agents.py --ci` |
| Validate skills | `python .paperkit/tools/validate-skills.py --all` |
| Run tests | `pytest tests/ -v` |
| Build LaTeX | `./.paperkit/tools/build-latex.sh` |
| View metrics | `python -m paperkit.metrics --dashboard` |

---

## Directory Reference

```
.paperkit/
├── _cfg/
│   ├── agents/*.yaml          # Agent metadata (edit here)
│   ├── skills/                # Agent Skills (SKILL.md format - NEW)
│   │   ├── humanizer/
│   │   │   └── SKILL.md
│   │   ├── academic-writing/
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   └── harvard-citations/
│   │       └── SKILL.md
│   ├── workflows/             # Compositional Workflows (YAML - RENAMED)
│   │   ├── cite-source.yaml
│   │   ├── compile-latex.yaml
│   │   └── draft-section.yaml
│   ├── tools/*.yaml           # Tool definitions
│   ├── schemas/               # JSON schemas for validation
│   │   ├── skill-frontmatter-schema.json  # For SKILL.md
│   │   └── workflow-schema.json           # For workflow YAML
│   ├── routing.registry.yaml  # Intent routing rules
│   └── consent.registry.yaml  # Tool consent (NEW)
├── core/agents/*.md           # Agent instructions (no frontmatter)
├── specialist/agents/*.md     # Agent instructions (no frontmatter)
├── tools/                     # Python validation scripts
└── data/
    ├── metrics.db             # SQLite metrics (NEW)
    └── checkpoints/           # Workflow state (NEW)
```

---

## Troubleshooting

### "Schema validation failed"

Check that your YAML matches the required schema:

```bash
python .paperkit/tools/validate-agent-schema.py --file .paperkit/_cfg/agents/my-agent.yaml --verbose
```

### "Tool consent denied"

Consent is per-session by default. Restart your session or grant persistent consent:

```python
registry.request_consent("tool-name", ConsentLevel.PERSISTENT)
```

### "Skill depth exceeded"

Skills are limited to 5 levels of composition. Simplify your skill chain or flatten composite skills.

### "Routing confidence too low"

If confidence is below 0.7, the orchestrator presents top 3 agents. To improve:
1. Add more keywords to routing.registry.yaml
2. Improve `whenToUse` descriptions
3. Add `hardExclusions` to reduce false matches

---

## Next Steps

1. **Phase 1**: Run `check-agents.py` and fix any issues
2. **Phase 2**: Create your first skill using the template above
3. **Phase 3**: Test the orchestrator with your use cases
4. **Phase 4**: Register any custom tools
5. **Phase 5**: Monitor metrics after deployment

For detailed specifications, see:
- [spec.md](spec.md) - Full requirements
- [data-model.md](data-model.md) - Entity definitions
- [contracts/](contracts/) - API contracts
