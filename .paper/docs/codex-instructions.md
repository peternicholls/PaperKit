````markdown
# Copilot Research Paper Assistant Kit - Codex Instructions

## Activating Agents

Paper agents are installed as custom prompts in `.codex/prompts/paper-*.md` files.

### Available Prompts

```
/paper-research-consolidator - Synthesize research materials
/paper-architect - Design paper structure and outlines
/paper-section-drafter - Write paper sections
/paper-quality-refiner - Improve draft quality
/paper-reference-manager - Manage citations and bibliography
/paper-latex-assembler - Build and compile document
/paper-brainstorm - Creative ideation
/paper-problem-solver - Analyze and solve blockers
/paper-tutor - Get feedback on drafts
/paper-librarian - Find and organize sources
```

### Examples

```
/paper-architect - Activate architect agent to create paper outline
/paper-section-drafter - Activate drafter to write introduction
/paper-quality-refiner - Activate refiner to improve draft
```

### Agent Directory

All full agent definitions are in `.paper/`:
- Core agents: `.paper/core/agents/`
- Specialist agents: `.paper/specialist/agents/`

### Configuration

Module configs are in:
- `.paper/core/config.yaml`
- `.paper/specialist/config.yaml`

### Notes

- Prompts are autocompleted when you type `/`
- Agent remains active for the conversation
- Start a new conversation to switch agents
- Each agent presents a menu after greeting

### Academic Integrity Requirements

**ALL agents follow these critical principles:**

- **Academic integrity is paramount** - Always prioritize reputable sources and proper citation practices
- **Proper attribution required** - Academic papers cannot be summarized or quoted without attribution and accurate referencing to the original work in Harvard style
- **Complete citations mandatory** - Every quote requires: the quote text, page number, and full citation for both text and bibliography
- **Open access only** - If a paper needs downloading, only use open access channels
- **Never fabricate** - Never make up citations or guess at attribution; flag uncertainties for verification

These principles are embedded in all agent behaviors and workflows.

````
