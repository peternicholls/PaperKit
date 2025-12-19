# Copilot Research Paper Assistant Kit - Quick Start Guide

Formerly: Academic Paper Writing System.

## 🎯 What You Have Now

A complete **Open Agent System** for writing high-quality academic specification papers in LaTeX. Six specialized agents work with you to research, structure, draft, refine, and publish your work.

---

## ⚡ Quick Start (3 Steps)

### 1. Define Your Paper's Goal

Start by telling the system what you want to write:

```
Read open-agents/INSTRUCTIONS.md to understand the workflow.

Then: "I want to write a specification paper about [your topic]. 
The goal is to [what you want to accomplish]. 
The audience is [who will read this]."
```

### 2. Create Paper Structure

Ask the **Paper Architect** agent:

```
"Outline the paper on [topic]. 
My scope is [what's included]. 
Target length is [X] words."
```

The agent will create:
- Detailed section outline
- Research roadmap
- LaTeX skeleton files ready to fill

### 3. Build the Paper Progressively

Then follow this workflow:

```
Research → Draft → Refine → Repeat for each section → Assemble → PDF
```

Each agent handles one phase. See routing table below.

---

## 🚀 Quick Reference: Which Agent to Use

| Your Request | Use This Agent | Output Location |
|---|---|---|
| "Research [topic]" or "Consolidate research..." | **Research Consolidator** | `open-agents/output-refined/research/` |
| "Outline the paper" or "Create structure" | **Paper Architect** | `open-agents/output-drafts/outlines/` |
| "Draft [section]" or "Write the intro..." | **Section Drafter** | `open-agents/output-drafts/sections/` |
| "Refine this draft" or "Improve clarity" | **Quality Refiner** | `open-agents/output-refined/sections/` |
| "Format bibliography" or "Manage citations" | **Reference Manager** | `open-agents/output-refined/references/` |
| "Assemble the paper" or "Build the document" | **LaTeX Assembler** | `latex/main.tex` → `output-final/pdf/` |

---

## 📁 Folder Structure You'll Use

```
open-agents/
├── INSTRUCTIONS.md          ← Full system documentation (READ THIS FIRST)
│
├── source/                  ← PUT YOUR INPUTS HERE
│   ├── research-notes/      ← Research materials, notes, links
│   ├── ideas/               ← Sparks of imagination, discussions
│   └── reference-materials/ ← PDFs, sources, references
│
├── output-drafts/           ← First drafts (rough)
│   ├── outlines/
│   └── sections/
│
├── output-refined/          ← Better versions (iterated)
│   ├── research/
│   ├── sections/
│   └── references/
│
└── latex/                   ← FINAL DOCUMENT HERE
    ├── main.tex
    ├── preamble.tex
    ├── sections/            ← One file per section
    └── references/          ← Bibliography database
```

---

## 🎓 Typical Workflow Example

### Scenario: Writing a Specification Paper on Color Science

**Step 1: Define Goal** (You)
```
"I'm writing a specification paper on mathematical approaches to 
color perception modeling. The audience is researchers in color science 
and computer vision. Target length: 10,000 words."
```

**Step 2: Create Structure** (Paper Architect)
```
User: "Outline the paper on color perception specification."
→ Agent creates 7-section outline with research requirements
```

**Step 3: Gather Research** (Research Consolidator)
```
User: "Research color theory foundations. I have 5 papers on cone cells 
and 3 on color spaces. I've added notes to source/research-notes/"
→ Agent synthesizes into coherent "Color Theory Foundations" document
```

**Step 4: Draft Introduction** (Section Drafter)
```
User: "Draft the introduction. Motivate the problem of color perception 
modeling."
→ Agent writes 2000-word introduction with citations, logical flow
```

**Step 5: Refine Introduction** (Quality Refiner)
```
User: "Refine the introduction for clarity. It feels a bit rushed."
→ Agent improves transitions, strengthens arguments, polishes prose
```

**Repeat Steps 4-5** for each section (Background, Methodology, etc.)

**Step 6: Final Assembly** (LaTeX Assembler)
```
User: "Assemble the paper. Build the document."
→ Agent integrates all sections, validates bibliography, compiles PDF
```

**Result:** `open-agents/output-final/pdf/main.pdf` ready for review

---

## 💾 Memory System

The system remembers your progress in `open-agents/memory/`:

- **paper-metadata.yaml** — Title, scope, goals, status
- **section-status.yaml** — Progress on each section (drafted, refined, etc.)
- **research-index.yaml** — All sources used in the paper
- **revision-log.md** — History of changes and decisions

These files help agents understand context without reloading everything.

---

## 🛠️ Available Tools

You can run these scripts from the terminal:

```bash
# Build the LaTeX document (compile to PDF)
./open-agents/tools/build-latex.sh

# Check LaTeX syntax before compilation
./open-agents/tools/lint-latex.sh

# Validate paper structure
python3 ./open-agents/tools/validate-structure.py

# Format and validate bibliography
python3 ./open-agents/tools/format-references.py --validate latex/references/references.bib
```

---

## 📖 Full Documentation

Everything is documented in:

**[AGENTS.md](AGENTS.md)** — Quick reference (entry point)  
**[open-agents/INSTRUCTIONS.md](open-agents/INSTRUCTIONS.md)** — Complete system documentation  
**[open-agents/agents/*.md](open-agents/agents/)** — Individual agent specifications

**Start by reading:** `open-agents/INSTRUCTIONS.md` (20-30 minutes)

---

## ⚙️ System Features

✓ **Six specialized agents** for different paper-writing tasks  
✓ **Progressive refinement** — multiple passes for quality  
✓ **Modular LaTeX** — atomic section files, not monolithic documents  
✓ **Citation management** — Harvard style, BibTeX integration  
✓ **Memory system** — tracks progress without context bloat  
✓ **Iterative workflow** — write, refine, redraft, improve  
✓ **Academic rigor** — proper citations, formal tone, logical structure  
✓ **Automation** — build, validate, compile with one command  

---

## 🎓 Academic Standards

This system enforces:

- **Harvard referencing** for citations
- **Proper LaTeX semantics** (equations, cross-references, etc.)
- **Academic tone** (formal, objective, well-reasoned)
- **Logical structure** (introduction → foundations → methods → results → conclusion)
- **Iterative improvement** (draft → refine → redraft → polish)
- **Citation integrity** (every claim is cited or clearly original)

---

## 🚨 Important Notes

### Start with Scope
Don't start writing. Start with **goal definition**.

Ask Paper Architect to outline FIRST. This prevents rework and false starts.

### Use Agents in Order
Don't skip steps. Research → Structure → Draft → Refine → Assemble

Jumping steps creates quality problems and rework.

### Iterate Responsibly
It's normal to refine sections 2-3 times.

Draft → Refine → Get Feedback → Refine Again is healthy.

### Keep Files Organized
- Put research in `source/research-notes/`
- Let drafts stay in `output-drafts/`
- Move refined versions to `output-refined/`
- Only final stuff in `output-final/`

This keeps your work clean and trackable.

---

## 🎯 Next Steps

1. **Read** `open-agents/INSTRUCTIONS.md` (complete overview)
2. **Define** your paper's scope and goals (what are you writing about?)
3. **Use Paper Architect** to create structure (outline)
4. **Begin researching** with Research Consolidator
5. **Draft sections** one at a time with Section Drafter
6. **Refine** each section with Quality Refiner
7. **Manage references** throughout with Reference Manager
8. **Assemble** into final PDF with LaTeX Assembler

---

## 💡 Pro Tips

- **Save often:** Git commit after each agent completes a task
- **Ask questions:** Agents will ask you to clarify if uncertain
- **Iterate freely:** Early drafts don't have to be perfect
- **Trust the process:** Multiple refinement passes produce better results than trying to write perfect first drafts
- **Use the tools:** Run lint-latex.sh before assembly to catch issues early

---

## 🤝 Need Help?

- **Understanding the system?** Read `open-agents/INSTRUCTIONS.md`
- **Which agent to use?** Check routing table above
- **How to cite?** See `open-agents/agents/reference_manager.md`
- **How to draft?** See `open-agents/agents/section_drafter.md`
- **How to compile?** Run `./open-agents/tools/build-latex.sh`

---

## 🎉 You're Ready!

Your Open Agent System is fully set up and ready to use.

**Begin by telling the system what you want to write.**

The agents will take care of the rest.

---

**Happy writing! 📝**
