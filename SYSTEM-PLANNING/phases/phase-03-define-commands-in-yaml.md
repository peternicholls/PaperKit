# Phase 3: Define Commands in YAML

### Structure for each command YAML (example: init.yaml)

```yaml
# .copilot/commands/paper/init.yaml
name: "paper.init"
display-name: "Init session / capture goals"
description: "Initialize session and capture project goals"
category: "setup"
version: "1.0"

entry-points:
  primary: "/paper.init"
  alternates:
    - "*init"
    - "paper init"

routing:
  primary-agent: "paper-architect"
  workflow: "initialization"
  load-order:
    - "open-agents/INSTRUCTIONS.md"
    - "open-agents/agents/paper_architect.md"

inputs:
  mode:
    type: "choice"
    options:
      - "full-setup (goals + requirements + spec)"
      - "quick-setup (goals only)"
      - "resume-session (from working-reference)"
    default: "full-setup"
  
  collection-process:
    strategy: "progressive-questions"
    avoid-bombardment: true
    max-questions-per-round: 3

outputs:
  files:
    - "planning/0000-Project-Overview/aims-and-objectives.md"
    - "planning/0000-Project-Overview/requirements.md (conditional)"
    - "planning/0000-Project-Overview/content-specification.md (conditional)"
  memory:
    - "working-reference.md (updated)"

consent-required: false
tools-used: []

behavioral-rules:
  - "Ask progressively; don't bombardment"
  - "Detect user's working style (brief vs. detailed)"
  - "Adapt question depth accordingly"
  - "Record a concise working reference"
  - "If user skips init and jumps to tasks, perform lightweight inline intake"

success-criteria:
  - "User goal captured"
  - "Audience identified"
  - "Working reference updated"
  - "User ready for next phase"
```

**Commands to create (same structure):**

Setup phase:
- `.copilot/commands/paper/objectives.yaml`
- `.copilot/commands/paper/requirements.yaml`
- `.copilot/commands/paper/spec.yaml`

Sprint phase:
- `.copilot/commands/paper/sprint-plan.yaml`
- `.copilot/commands/paper/tasks.yaml`
- `.copilot/commands/paper/review.yaml`

Core workflow:
- `.copilot/commands/paper/plan.yaml`
- `.copilot/commands/paper/research.yaml`
- `.copilot/commands/paper/draft.yaml`
- `.copilot/commands/paper/refine.yaml`
- `.copilot/commands/paper/refs.yaml`
- `.copilot/commands/paper/assemble.yaml`

Specialist:
- `.copilot/commands/paper/specialist/brainstorm.yaml`
- `.copilot/commands/paper/specialist/solve.yaml`
- `.copilot/commands/paper/specialist/tutor-feedback.yaml`
- `.copilot/commands/paper/specialist/librarian-research.yaml`
- `.copilot/commands/paper/specialist/librarian-sources.yaml`
- `.copilot/commands/paper/specialist/librarian-gaps.yaml`

---

