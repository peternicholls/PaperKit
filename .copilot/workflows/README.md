# Workflow Definitions

This directory contains YAML specifications for orchestrated workflows.

## Organization

```
workflows/
├── README.md      ← You are here
├── setup/         ← Project initialization
│   └── initialization.yaml
├── sprint/        ← Sprint management
│   └── sprint.yaml
└── paper/         ← Core writing workflow
    └── core-writing.yaml
```

## Available Workflows

### Initialization Workflow
**File:** `setup/initialization.yaml`

Sets up a new paper project with canonical documents:

```
collect-goals → review-objectives → collect-requirements → collect-spec → complete-setup
```

**Entry points:** `/paper.init`, `/paper.objectives`  
**Duration:** 15-30 minutes  
**Outputs:** 
- `planning/0000-Project-Overview/aims-and-objectives.md`
- `planning/0000-Project-Overview/requirements.md`
- `planning/0000-Project-Overview/content-specification.md`

### Sprint Workflow
**File:** `sprint/sprint.yaml`

Executes focused work sessions with planning and review:

```
plan-sprint → execute-tasks (loop) → review-outcomes → decide-next
```

**Entry points:** `/paper.sprint-plan`  
**Duration:** Variable (1 day to 1 week)  
**Outputs:**
- `planning/YYYYMMDD-[name]/plan.md`
- `planning/YYYYMMDD-[name]/tasks.md`
- `planning/YYYYMMDD-[name]/review.md`

### Core Writing Workflow
**File:** `paper/core-writing.yaml`

Main paper writing workflow from planning to publication:

```
plan → research → draft (loop) → optional-feedback → refine → manage-references → assemble
```

**Entry points:** `/paper.plan`, `/paper.research`, `/paper.draft`  
**Duration:** Varies by content  
**Outputs:**
- `output-drafts/outlines/`
- `output-refined/research/`
- `output-drafts/sections/`
- `output-refined/sections/`
- `output-final/pdf/`

## Workflow YAML Structure

Each workflow YAML file includes:

```yaml
name: "workflow-name"
display-name: "Human Readable Name"
description: "What this workflow accomplishes"
version: "1.0"

entry-points:
  - "paper.command1"
  - "paper.command2"
  startup: "guided-setup-option"

phases:
  - id: "phase-id"
    agent: "agent-name"
    command: "command-name"
    description: "What this phase does"
    inputs-from-user: true|false
    outputs:
      - file: "output/path.md"
      - memory: "memory-file"
    next:
      - "next-phase-id"
      - "alternative-phase"
    skip-if: "condition"
    type: "normal|checkpoint|loop|decision-point|summary"

  - id: "loop-phase"
    type: "loop"
    loop-condition: "items-remain"
    # ... other properties

  - id: "decision-phase"
    type: "decision-point"
    description: "Choose next direction"
    options:
      - "option1"
      - "option2"

decision-points:
  - id: "decision-id"
    prompt: "Question for user"
    options:
      - "option1"
      - "option2"

success-criteria:
  - "Criterion 1"
  - "Criterion 2"

typical-duration: "15-30 minutes"
can-resume: true
checkpoint-interval: 5
```

## Workflow Concepts

### Phases
Individual steps in the workflow, each with:
- **Agent:** Which agent handles this phase
- **Command:** Which command to execute
- **Inputs/Outputs:** Data flow
- **Next:** Possible transitions

### Decision Points
Branch points where user input determines the path:
- **Checkpoint:** Review and confirm progress
- **Decision:** Choose between alternatives
- **Loop condition:** Continue or break out

### Phase Types
- **normal:** Standard phase execution
- **checkpoint:** Pause for user review
- **loop:** Repeat until condition met
- **decision-point:** Branch based on choice
- **summary:** Summarize and conclude

## Adding a New Workflow

1. Create YAML file in appropriate folder
2. Define all phases and transitions
3. Register in `.copilot/workflows.yaml` master registry
4. Ensure all referenced commands and agents exist
5. Test end-to-end execution
