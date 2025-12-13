# Phase 6: Clean Up Naming & Organization

### Rename Agents

All agent files will use dashes instead of underscores:
- `research_consolidator.md` → keep original for reference, use `research-consolidator.yaml`
- `paper_architect.md` → keep original for reference, use `paper-architect.yaml`
- etc.

### Reorganize Directories

**Structure after Phase 6:**

```
.copilot/
├── agents/
│   ├── paper-system.md (kept for reference)
│   ├── paper-system.yaml (new config)
│   ├── core/
│   │   ├── research-consolidator.yaml
│   │   ├── paper-architect.yaml
│   │   ├── section-drafter.yaml
│   │   ├── quality-refiner.yaml
│   │   ├── reference-manager.yaml
│   │   └── latex-assembler.yaml
│   ├── specialist/
│   │   ├── brainstorm.yaml
│   │   ├── problem-solver.yaml
│   │   ├── tutor.yaml
│   │   └── librarian.yaml
│   └── README.md
├── commands/
│   ├── paper/
│   │   ├── init.yaml
│   │   ├── objectives.yaml
│   │   ├── requirements.yaml
│   │   ├── spec.yaml
│   │   ├── plan.yaml
│   │   ├── sprint-plan.yaml
│   │   ├── tasks.yaml
│   │   ├── review.yaml
│   │   ├── research.yaml
│   │   ├── draft.yaml
│   │   ├── refine.yaml
│   │   ├── refs.yaml
│   │   ├── assemble.yaml
│   │   └── specialist/
│   │       ├── brainstorm.yaml
│   │       ├── solve.yaml
│   │       ├── tutor-feedback.yaml
│   │       ├── librarian-research.yaml
│   │       ├── librarian-sources.yaml
│   │       └── librarian-gaps.yaml
│   └── README.md
└── (rest of structure)
```

---

