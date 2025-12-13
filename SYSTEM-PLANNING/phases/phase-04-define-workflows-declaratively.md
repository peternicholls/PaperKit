# Phase 4: Define Workflows Declaratively

### Setup Workflow (initialization.yaml)

```yaml
# .copilot/workflows/setup/initialization.yaml
name: "initialization"
display-name: "Paper Project Initialization"
description: "Set up a new paper project with canonical docs (aims, requirements, spec)"
version: "1.0"

entry-points:
  - "paper.init"
  - "paper.objectives"
  startup: "guided-setup-option"

phases:
  - id: "collect-goals"
    agent: "paper-architect"
    command: "objectives"
    description: "Capture project vision, goals, and success criteria"
    inputs-from-user: true
    outputs:
      - file: "planning/0000-Project-Overview/aims-and-objectives.md"
      - memory: "working-reference"
    next:
      - "collect-requirements"
      - "review-objectives"
    skip-if: "user-mode=quick-setup"

  - id: "review-objectives"
    agent: "paper-system"
    type: "checkpoint"
    description: "Review captured objectives; user confirms or revises"
    inputs-from-user: true
    next:
      - "collect-requirements"
      - "collect-goals (revise)"

  - id: "collect-requirements"
    agent: "paper-architect"
    command: "requirements"
    description: "Define technical specs and quality standards"
    inputs-from-user: true
    outputs:
      - file: "planning/0000-Project-Overview/requirements.md"
      - memory: "working-reference"
    next:
      - "collect-spec"
      - "complete-setup"
    skip-if: "user-mode=quick-setup"

  - id: "collect-spec"
    agent: "paper-architect"
    command: "spec"
    description: "Define content direction, themes, and scope"
    inputs-from-user: true
    outputs:
      - file: "planning/0000-Project-Overview/content-specification.md"
      - memory: "working-reference"
    next:
      - "complete-setup"

  - id: "complete-setup"
    agent: "paper-system"
    type: "summary"
    description: "Summarize setup, confirm all canonical docs ready"
    inputs-from-user: false
    outputs:
      - summary: "Initialization complete"
      - memory: "working-reference (final)"
    next:
      - "END"

decision-points:
  - id: "mode-choice"
    prompt: "How would you like to set up?"
    options:
      - "full-setup"
      - "quick-setup"
      - "resume-session"

success-criteria:
  - "At least Aims & Objectives defined"
  - "Working reference updated"
  - "User understands next steps"

typical-duration: "15–30 minutes"
can-resume: true
checkpoint-interval: 5  # minutes
```

### Sprint Workflow (sprint.yaml)

```yaml
# .copilot/workflows/sprint/sprint.yaml
name: "sprint"
display-name: "Sprint Workflow"
description: "Execute a focused sprint with planning, task execution, and review"
version: "1.0"

entry-points:
  - "paper.sprint-plan"

phases:
  - id: "plan-sprint"
    agent: "paper-architect"
    command: "sprint-plan"
    description: "Create dated sprint folder and outline methodology"
    inputs-from-user: true
    outputs:
      - folder: "planning/YYYYMMDD-[name]/"
      - file: "planning/YYYYMMDD-[name]/plan.md"
      - file: "planning/YYYYMMDD-[name]/tasks.md (empty)"
      - memory: "working-reference"
    next:
      - "execute-tasks"

  - id: "execute-tasks"
    agent: "user + any-agent"
    command: "tasks"
    description: "Execute sprint tasks; agents complete work, user provides direction"
    type: "loop"
    loop-condition: "tasks-remain"
    inputs-from-user: true
    outputs:
      - file: "planning/YYYYMMDD-[name]/tasks.md (updated)"
      - memory: "working-reference (updated)"
    next:
      - "review-outcomes"
      - "execute-tasks (continue)"

  - id: "review-outcomes"
    agent: "paper-system"
    command: "review"
    description: "Reflect on sprint, identify learnings, decide next steps"
    inputs-from-user: true
    outputs:
      - file: "planning/YYYYMMDD-[name]/review.md"
      - memory: "working-reference"
    next:
      - "decide-next"

  - id: "decide-next"
    agent: "paper-system"
    type: "decision-point"
    description: "Choose: continue sprint, iterate, pivot, or new sprint"
    inputs-from-user: true
    next:
      - "execute-tasks (continue same sprint)"
      - "plan-sprint (new sprint)"
      - "END"

typical-duration: "Variable (1 day to 1 week)"
can-resume: true
supports-parallel-work: false  # one sprint at a time
```

### Core Writing Workflow (core-writing.yaml)

```yaml
# .copilot/workflows/paper/core-writing.yaml
name: "core-writing"
display-name: "Core Paper Writing Workflow"
description: "Main paper writing workflow (plan → research → draft → refine → refs → assemble)"
version: "1.0"

entry-points:
  - "paper.plan"
  - "paper.research"
  - "paper.draft"

phases:
  - id: "plan"
    agent: "paper-architect"
    command: "plan"
    description: "Create detailed paper outline within sprint"
    inputs-from-user: false  # uses existing setup
    outputs:
      - file: "output-drafts/outlines/"
      - file: "latex/sections/ (skeletons)"
    next:
      - "research"

  - id: "research"
    agent: "research-consolidator"
    command: "research"
    description: "Consolidate research into structured reference documents"
    inputs-from-user: true
    outputs:
      - file: "output-refined/research/"
      - memory: "research-index"
    next:
      - "draft"
      - "research (continue)"  # loop for multiple research areas

  - id: "draft"
    agent: "section-drafter"
    command: "draft"
    description: "Draft individual section in LaTeX"
    type: "loop"
    loop-condition: "sections-remain"
    inputs-from-user: true
    outputs:
      - file: "output-drafts/sections/"
      - memory: "section-status"
    next:
      - "draft (next-section)"
      - "optional-feedback"
      - "refine"

  - id: "optional-feedback"
    agent: "tutor"
    command: "tutor-feedback"
    description: "Get feedback on draft before refinement (optional)"
    inputs-from-user: false  # user initiates
    outputs:
      - file: "planning/YYYYMMDD-*/tutor-feedback.md"
    next:
      - "refine"
    skip-if: "user-declines-feedback"

  - id: "refine"
    agent: "quality-refiner"
    command: "refine"
    description: "Improve draft for clarity, coherence, and academic quality"
    type: "loop"
    loop-condition: "refinement-cycles-needed"
    inputs-from-user: true
    outputs:
      - file: "output-refined/sections/"
      - memory: "section-status"
    next:
      - "refine (next-cycle)"
      - "manage-references"

  - id: "manage-references"
    agent: "reference-manager"
    command: "refs"
    description: "Validate and format bibliography"
    inputs-from-user: false
    outputs:
      - file: "latex/references/references.bib"
    next:
      - "assemble"

  - id: "assemble"
    agent: "latex-assembler"
    command: "assemble"
    description: "Integrate sections and compile to PDF"
    inputs-from-user: false
    outputs:
      - file: "latex/main.tex (integrated)"
      - file: "output-final/pdf/main.pdf"
    next:
      - "END"
    requires-consent: true
    tools-used:
      - "lint-latex.sh"
      - "validate-structure.py"
      - "build-latex.sh"

typical-duration: "Varies by content and refinement cycles"
can-resume: true
supports-partial-completion: true  # can skip sections, come back later
```

---

