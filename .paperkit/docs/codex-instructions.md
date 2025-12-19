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

All full agent definitions are in `.paperkit/`:
- Core agents: `.paperkit/core/agents/`
- Specialist agents: `.paperkit/specialist/agents/`

#### Source of Truth
- `.paperkit/` holds canonical definitions for agents, workflows, tools, and guides.
- Prompts in `.codex/prompts` mirror `.paper` — edit `.paper` and sync.

### Configuration

Module configs are in:
- `.paperkit/core/config.yaml`
- `.paperkit/specialist/config.yaml`

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

### Artifacts & Rigor (Forensic Audit)

- Agents should apply PhD-level rigor and leverage existing research artifacts:
	- open-agents/planning/20251218-group-tutor-reviews/tasks-artifacts
	- open-agents/planning/20251218-group-tutor-reviews/research-artifacts
- Librarian conducts forensic audits: extract quotable evidence with page numbers, prioritize quantitative anchors, and map findings to sections (§02–§12).
- Consolidator, Drafter, Refiner must revisit previously processed sources when needed; deeper quotes and validations often emerge on second pass.
- Reference Manager enforces page numbers for direct quotes (`\cite[p. <page>]{key}`) and maintains a citation map linking claims to BibTeX keys and sections.

````
