**CRITICAL: Read `open-agents/INSTRUCTIONS.md` immediately.**

---

## Academic Specification Paper Writing System

This project uses a complete **Open Agent System** for planning, researching, structuring, drafting, refining, and publishing high-quality academic specification papers in LaTeX format.

### ⚡ Quick Start

1. **Understand the system:** Read `SYSTEM_GUIDE.md` (10 minutes)
2. **Full documentation:** Read `open-agents/INSTRUCTIONS.md` (20 minutes)
3. **Define your paper:** Tell agents what you want to write
4. **Follow the workflow:** Research → Structure → Draft → Refine → Assemble

### 🎯 Six Specialized Agents

| Agent | Purpose | When to Use |
|-------|---------|------------|
| **Research Consolidator** | Synthesize research into coherent documents | "Research [topic]" or "Consolidate..." |
| **Paper Architect** | Design paper structure and outline | "Outline the paper" or "Create structure" |
| **Section Drafter** | Write individual sections with rigor | "Draft [section]" or "Write intro..." |
| **Quality Refiner** | Improve clarity, flow, and polish | "Refine this draft" or "Improve quality" |
| **Reference Manager** | Manage citations and bibliography | "Format references" or "Create bibliography" |
| **LaTeX Assembler** | Integrate sections and compile PDF | "Assemble the paper" or "Build document" |

### 📊 Quick Reference Table

| You say... | Agent | Output |
|-----------|-------|--------|
| "Research X" | Research Consolidator | `output-refined/research/` |
| "Outline the paper" | Paper Architect | `output-drafts/outlines/` |
| "Draft section Y" | Section Drafter | `output-drafts/sections/` |
| "Refine this" | Quality Refiner | `output-refined/sections/` |
| "Manage citations" | Reference Manager | `output-refined/references/` |
| "Build the document" | LaTeX Assembler | `output-final/pdf/` |

### 📁 Key Folders

```
open-agents/
├── INSTRUCTIONS.md        ← Full documentation (READ THIS)
├── agents/               ← Agent definitions
├── source/               ← Your research inputs
├── output-drafts/        ← First drafts
├── output-refined/       ← Refined versions
├── output-final/         ← Ready for publication
├── memory/               ← System state (auto-updated)
└── tools/                ← Build and validation scripts

latex/                    ← Final LaTeX document
├── main.tex             ← Main document
├── preamble.tex         ← Configuration
├── sections/            ← One file per section
└── references/          ← Bibliography
```

### 🎯 Typical Workflow

1. **Define scope** → Tell agents what you're writing
2. **Research** → Consolidate materials into reference documents
3. **Structure** → Create paper outline with architecture agent
4. **Draft** → Write sections one at a time
5. **Refine** → Improve and polish each section
6. **Assemble** → Integrate and compile to PDF

### 🛠️ Tools Available

```bash
# Build and compile LaTeX document
./open-agents/tools/build-latex.sh

# Check LaTeX syntax before compilation
./open-agents/tools/lint-latex.sh

# Validate paper structure
python3 ./open-agents/tools/validate-structure.py
```

### 📖 Documentation Structure

- **SYSTEM_GUIDE.md** ← Start here (quick overview)
- **AGENTS.md** ← This file (entry point)
- **open-agents/INSTRUCTIONS.md** ← Complete system documentation
- **open-agents/agents/*.md** ← Individual agent specifications

### ✨ Key Features

✓ Progressive research and drafting workflow  
✓ Iterative refinement for academic quality  
✓ Modular LaTeX architecture (atomic sections)  
✓ Harvard citation style and bibliography management  
✓ Integrated build and validation tools  
✓ Memory system tracking progress  
✓ Multiple refinement passes supported  
✓ Clean, organized file structure  

### 🚀 Next Step

Read `SYSTEM_GUIDE.md` for quick start instructions, then dive into `open-agents/INSTRUCTIONS.md` for complete documentation.
