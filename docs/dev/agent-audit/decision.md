# Agent System Unification Decision

Generated: 2026-01-06
Updated: 2026-01-06

## Decision

**Canonical Design** — Two-file split:

1. **`.paperkit/_cfg/agents/*.yaml`** = Schema-validated **metadata ONLY**
   - Contains all fields defined in `agent-schema.json`
   - Machine-readable, validated by CI
   - `path` field points to the corresponding MD file

2. **`.paperkit/{core,specialist}/agents/*.md`** = **Prompt/instructions content**
   - Contains the agent's behavioural instructions
   - Referenced by `path` field in the YAML file
   - Used by runtime/loaders to activate the agent persona

## Rationale

### Schema Design

The `agent-schema.json` defines what metadata belongs in YAML files:
- Required: `name`, `displayName`, `title`, `icon`, `identity`, `module`, `path`
- Optional: `version`, `capabilities`, `constraints`, `principles`, `inputSchema`, `outputSchema`, `examplePrompts`, `owner`
- `additionalProperties: false` — No extra keys allowed

The `path` property has a regex pattern that expects `.paperkit/(core|specialist)/agents/*.md` files.

### Why This Split?

1. **Separation of concerns**: Metadata (structured, validatable) vs. Instructions (prose, prompts)
2. **CI validation**: YAML files can be schema-validated without parsing markdown
3. **Runtime loading**: MD files contain the actual agent behavior loaded at runtime
4. **No duplication**: Metadata lives in YAML, instructions live in MD

### What Changed

1. **orchestrator.yaml**: Now contains ONLY schema-compliant metadata (no `instructions`, `decisionSchema`, etc.)
2. **orchestrator.md**: Now contains ONLY the agent's behavioral instructions (no YAML frontmatter)
3. **Validation**: Both `validate-agent-schema.py` and `check-agents.py` verify the system integrity

## Implementation Status

- [x] `orchestrator.yaml` is schema-compliant
- [x] `orchestrator.md` contains behavioral instructions
- [x] All 11 agent YAML files pass validation
- [x] All 11 agent MD files exist and are referenced correctly
- [x] `validate.py` uses correct `.paperkit/` paths
- [x] `check-agents.py` provides unified validation
- [x] CI workflow runs both validation checks
