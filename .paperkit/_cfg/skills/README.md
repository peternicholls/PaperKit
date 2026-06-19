# Agent Skills Directory

This directory contains **Agent Skills** following the [agentskills.io](https://agentskills.io) specification.

## What Are Agent Skills?

Agent Skills are instruction documents that teach AI agents **HOW** to perform specific tasks. They provide:
- Step-by-step guidance
- Best practices and patterns
- Examples and edge cases
- Domain expertise

**Skills are different from Workflows:**
- **Skills** = Instructions (teach HOW) → `skills/{name}/SKILL.md`
- **Workflows** = Orchestration (define WHAT steps) → `workflows/{name}.yaml`

## Directory Structure

Each skill is a folder containing at minimum a `SKILL.md` file:

```
skills/
├── humanizer/
│   └── SKILL.md              # Required: frontmatter + instructions
├── academic-writing/
│   └── SKILL.md
├── harvard-citations/
│   └── SKILL.md
└── latex-best-practices/
    └── SKILL.md
```

Skills may also include:
- `scripts/` - Executable code
- `references/` - Additional documentation
- `assets/` - Templates, data files

## SKILL.md Format

Every SKILL.md must have YAML frontmatter with at minimum `name` and `description`:

```yaml
---
name: skill-name
description: What this skill does AND when to use it. Include trigger keywords.
metadata:
  author: team-name
  version: "1.0.0"
---

# Skill Title

Instructions, examples, and guidance...
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | 1-64 chars, lowercase + hyphens, must match directory name |
| `description` | ✅ | 1-1024 chars, what it does AND when to use |
| `license` | ❌ | License name or reference to LICENSE file |
| `compatibility` | ❌ | Environment requirements |
| `metadata` | ❌ | Arbitrary key-value pairs (author, version, etc.) |

## Available Skills

| Skill | Purpose |
|-------|---------|
| [humanizer](humanizer/) | Remove AI writing patterns from text |
| [academic-writing](academic-writing/) | Academic paper composition guidelines |
| [harvard-citations](harvard-citations/) | Harvard citation style (Cite Them Right) |
| [latex-best-practices](latex-best-practices/) | LaTeX document best practices |

## Skill Activation

Skills can be activated in three ways:

1. **Description matching** - Agent detects relevance from skill descriptions
2. **Explicit invocation** - User or agent explicitly requests: `/skill humanizer`
3. **Agent hints** - Agents declare `suggestedSkills` to auto-load

## Progressive Disclosure

Skills use progressive disclosure to minimize context usage:

1. **Metadata** (~100 tokens): `name` + `description` loaded at startup for ALL skills
2. **Instructions** (<5000 tokens): Full SKILL.md body loaded when skill is ACTIVATED
3. **Resources** (as needed): scripts/, references/ loaded ON DEMAND

## Validation

Validate skill frontmatter with:

```bash
python .paperkit/tools/validate-skill-frontmatter.py --all --verbose
```

## Creating a New Skill

1. Create directory: `mkdir -p .paperkit/_cfg/skills/my-skill/`
2. Create SKILL.md with frontmatter
3. Add instructions in markdown body
4. Validate: `python .paperkit/tools/validate-skill-frontmatter.py --path .paperkit/_cfg/skills/my-skill/`

## Schema

Skills are validated against `.paperkit/_cfg/schemas/skill-frontmatter-schema.json`.

## Related

- **Workflows**: See `.paperkit/_cfg/workflows/` for orchestration definitions
- **Agents**: See `.paperkit/_cfg/agents/` for agent metadata
- **Guide**: See `.paperkit/_cfg/guides/harvard-citation-guide.md` for full Harvard style reference
