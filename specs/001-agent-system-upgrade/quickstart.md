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

## Phase 2: Creating a New Skill

### 2.1 Skill File Location

```
.paperkit/_cfg/skills/{skill-name}.yaml
```

### 2.2 Skill Template

```yaml
# .paperkit/_cfg/skills/my-skill.yaml
name: my-skill
displayName: My Skill
description: What this skill does
version: 1.0.0
type: atomic  # or composite, conditional

prerequisites:
  - type: tool
    name: some-tool

steps:
  - action: do_something
    agent: some-agent
    inputs:
      - input_var
    outputs:
      - output_var

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

### 2.3 Validate Skill

```bash
python .paperkit/tools/validate-skills.py --file .paperkit/_cfg/skills/my-skill.yaml
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
│   ├── skills/*.yaml          # Skill definitions (NEW)
│   ├── tools/*.yaml           # Tool definitions
│   ├── schemas/               # JSON schemas for validation
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
