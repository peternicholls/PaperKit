**CRITICAL: Read `open-agents/INSTRUCTIONS.md` immediately.**

---

## Academic Paper Writing System

This project uses an **Open Agent System** for planning, researching, structuring, and progressively drafting high-quality academic specification papers in LaTeX format.

### Quick Reference

| Agent | Trigger | Output |
|-------|---------|--------|
| Research Consolidator | "consolidate research on..." or "research..." | `open-agents/output-refined/research/` |
| Paper Architect | "outline the paper" or "structure the paper" | `open-agents/output-drafts/outlines/` |
| Section Drafter | "draft the introduction" or "draft section..." | `open-agents/output-drafts/sections/` |
| Quality Refiner | "refine this draft" or "improve section quality" | `open-agents/output-refined/sections/` |
| Reference Manager | "format references" or "create bibliography" | `open-agents/output-refined/references/` |
| LaTeX Assembler | "assemble the paper" or "build the document" | `latex/main.tex` + compiled PDF |

### Available Commands

- `/paper research [topic]` — Consolidate and synthesize research notes
- `/paper outline [scope]` — Generate paper outline and structure
- `/paper draft [section]` — Draft a specific section or subsection
- `/paper refine [filename]` — Improve and refine draft quality
- `/paper references [type]` — Format and manage bibliographic references
- `/paper build` — Assemble and compile final LaTeX document
- `/paper status` — Show current paper status and progress

For full documentation: Read `open-agents/INSTRUCTIONS.md`
