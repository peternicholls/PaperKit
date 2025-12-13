# Phase 1: Create Configuration Structure (Foundation)

### Files to Create

**Master Registries (source of truth):**
- `.copilot/agents.yaml` — Master agent registry with metadata, capabilities, categories
- `.copilot/commands.yaml` — Command registry with routing, descriptions, prerequisites
- `.copilot/workflows.yaml` — Workflow definitions and entry points

**Tool & System Configuration:**
- `.copilot/tools/tools.yaml` — Tool/script registry with consent requirements
- `.copilot/config/settings.yaml` — System configuration and defaults
- `.copilot/config/consent.yaml` — Consent policy and scope definitions

**Folder Structure:**
```
.copilot/
├── README.md (updated)
├── agents.yaml (new)
├── commands.yaml (new)
├── workflows.yaml (new)
├── agents/
│   ├── paper-system.md (existing, updated)
│   ├── core/
│   ├── specialist/
│   └── README.md (new)
├── commands/
│   ├── paper/
│   └── README.md (new)
├── workflows/
│   ├── setup/
│   ├── sprint/
│   ├── paper/
│   └── README.md (new)
├── memory/ (moved from open-agents/)
│   ├── paper-metadata.yaml
│   ├── research-index.yaml
│   ├── section-status.yaml
│   ├── working-reference.md
│   ├── revision-log.md
│   └── README.md (new)
├── modules/
│   ├── modules.yaml (new, future-proofing)
│   └── README.md (new)
├── tools/
│   ├── tools.yaml (new)
│   └── README.md (new)
├── config/
│   ├── settings.yaml (new)
│   ├── consent.yaml (new)
│   └── README.md (new)
└── RESEARCH-AND-PLANNING.md (new, research notes)
```

### agents.yaml Structure

```yaml
# .copilot/agents.yaml
# Master agent registry - single source of truth for agent discovery and routing

version: "1.0.0"
description: "Registry of all agents available in the Copilot Research Paper Assistant Kit"

categories:
  core: "Core paper writing agents (from Open Agent System)"
  specialist: "Support agents for brainstorming, problem-solving, feedback, research"
  system: "System agents for routing and orchestration"

agents:
  core:
    research-consolidator:
      name: "Research Consolidator"
      description: "Synthesizes research materials into coherent reference documents"
      category: "research"
      role: "Synthesizer"
      triggers:
        - "research"
        - "consolidate research"
        - "research [topic]"
      inputs:
        - "Topic or research question"
        - "Available sources or notes"
        - "Depth/breadth preference"
      outputs:
        - "output-refined/research/"
        - "memory/research-index.yaml (updated)"
        - "memory/working-reference.md (updated)"
      spec-file: "agents/core/research-consolidator.yaml"
      doc-file: "open-agents/agents/research_consolidator.md"
      requires-tools: []
      requires-consent: false

    paper-architect:
      name: "Paper Architect"
      description: "Designs paper structure, outlines sections, establishes logical flow"
      category: "planning"
      role: "Architect"
      triggers:
        - "plan"
        - "outline"
        - "structure"
      inputs:
        - "Paper topic and scope"
        - "Audience and target length"
        - "Deadlines or constraints"
        - "Standards flexibility"
      outputs:
        - "output-drafts/outlines/"
        - "latex/sections/ (skeletons)"
        - "memory/paper-metadata.yaml (updated)"
      spec-file: "agents/core/paper-architect.yaml"
      doc-file: "open-agents/agents/paper_architect.md"
      requires-tools: []
      requires-consent: false

    section-drafter:
      name: "Section Drafter"
      description: "Writes individual paper sections with academic rigor and logical flow"
      category: "writing"
      role: "Writer"
      triggers:
        - "draft [section]"
        - "write"
      inputs:
        - "Section name"
        - "Outline context"
        - "Relevant research docs"
        - "Specific claims or constraints"
      outputs:
        - "output-drafts/sections/"
        - "memory/section-status.yaml (updated)"
      spec-file: "agents/core/section-drafter.yaml"
      doc-file: "open-agents/agents/section_drafter.md"
      requires-tools: []
      requires-consent: false

    quality-refiner:
      name: "Quality Refiner"
      description: "Improves drafts for clarity, coherence, grammar, and logical flow"
      category: "refinement"
      role: "Editor"
      triggers:
        - "refine"
        - "improve"
        - "polish"
      inputs:
        - "Target section draft path"
        - "Desired focus areas"
        - "Standards flexibility"
      outputs:
        - "output-refined/sections/"
        - "memory/section-status.yaml (updated)"
      spec-file: "agents/core/quality-refiner.yaml"
      doc-file: "open-agents/agents/quality_refiner.md"
      requires-tools: []
      requires-consent: false

    reference-manager:
      name: "Reference Manager"
      description: "Manages bibliographic data, formats citations, maintains bibliography"
      category: "references"
      role: "Bibliographer"
      triggers:
        - "refs"
        - "references"
        - "bibliography"
        - "citations"
      inputs:
        - "New sources or citation keys"
        - "Desired operations"
      outputs:
        - "latex/references/references.bib"
        - "output-refined/references/"
      spec-file: "agents/core/reference-manager.yaml"
      doc-file: "open-agents/agents/reference_manager.md"
      requires-tools:
        - "format-references.py"
      requires-consent: true

    latex-assembler:
      name: "LaTeX Assembler"
      description: "Integrates sections into complete LaTeX, validates, compiles to PDF"
      category: "assembly"
      role: "Engineer"
      triggers:
        - "assemble"
        - "build"
        - "compile"
      inputs:
        - "Refined sections status"
        - "Bibliography status"
        - "Build flags"
      outputs:
        - "latex/ (integrated)"
        - "output-final/pdf/"
        - "Build logs"
      spec-file: "agents/core/latex-assembler.yaml"
      doc-file: "open-agents/agents/latex_assembler.md"
      requires-tools:
        - "lint-latex.sh"
        - "validate-structure.py"
        - "build-latex.sh"
      requires-consent: true

  specialist:
    brainstorm:
      name: "Brainstorm Agent"
      description: "Help generate ideas, explore possibilities, think creatively"
      category: "ideation"
      role: "Idea Generator"
      triggers:
        - "brainstorm"
        - "explore ideas"
        - "think about"
      inputs:
        - "Topic or problem to brainstorm"
        - "Constraints (if any)"
        - "Current thinking"
      outputs:
        - "planning/YYYYMMDD-[name]/brainstorm.md"
      spec-file: "agents/specialist/brainstorm.yaml"
      doc-file: ".copilot/agents/brainstorm.md"
      requires-tools: []
      requires-consent: false

    problem-solver:
      name: "Problem-Solver Agent"
      description: "Identify, analyze, and solve blockers and gaps"
      category: "support"
      role: "Problem Solver"
      triggers:
        - "solve"
        - "stuck on"
        - "how do we handle"
      inputs:
        - "Problem or blocker description"
        - "Context and constraints"
      outputs:
        - "planning/YYYYMMDD-[name]/problem-solving.md"
      spec-file: "agents/specialist/problem-solver.yaml"
      doc-file: ".copilot/agents/problem-solver.md"
      requires-tools: []
      requires-consent: false

    tutor:
      name: "Tutor Agent"
      description: "Provide feedback on drafts, clarity, argument strength, academic quality"
      category: "feedback"
      role: "Mentor"
      triggers:
        - "tutor-feedback"
        - "review"
        - "feedback"
        - "critique"
      inputs:
        - "Draft text or section"
        - "Context and concerns"
      outputs:
        - "planning/YYYYMMDD-[name]/tutor-feedback.md"
      spec-file: "agents/specialist/tutor.yaml"
      doc-file: ".copilot/agents/tutor.md"
      requires-tools: []
      requires-consent: false

    librarian:
      name: "Librarian Agent"
      description: "Find, evaluate, organize research materials; track sources and gaps"
      category: "research"
      role: "Research Guide"
      triggers:
        - "librarian-research"
        - "librarian-sources"
        - "librarian-gaps"
        - "find sources"
      inputs:
        - "Research topic or gap"
        - "Scope and level"
      outputs:
        - "planning/YYYYMMDD-[name]/research-roadmap.md"
      spec-file: "agents/specialist/librarian.yaml"
      doc-file: ".copilot/agents/librarian.md"
      requires-tools: []
      requires-consent: false

  system:
    paper-system:
      name: "Paper System Router"
      description: "Routes commands to agents, manages consent, orchestrates workflows"
      category: "system"
      role: "Orchestrator"
      spec-file: "agents/paper-system.md"
      internal: true
```

### commands.yaml Structure

```yaml
# .copilot/commands.yaml
# Master command registry - routes user input to agents and workflows

version: "1.0.0"
description: "Registry of all slash commands available in the Copilot Research Paper Assistant Kit"

command-groups:
  setup: "Project initialization and canonical document creation"
  sprint: "Sprint planning, task tracking, and review"
  core: "Core paper writing workflow"
  specialist: "Support agents for ideation, feedback, and problem-solving"

commands:
  # Setup Phase
  setup:
    paper.init:
      name: "paper.init"
      description: "Initialize session and capture project goals"
      display: "Init session / capture goals"
      agent: "paper-architect"
      triggers:
        - "/paper.init"
        - "*init"
        - "paper init"
      category: "setup"
      workflow: "initialization"
      spec-file: "commands/paper/init.yaml"
      requires-consent: false
      order: 1

    paper.objectives:
      name: "paper.objectives"
      description: "Set aims, objectives, and success criteria"
      display: "Set aims & objectives"
      agent: "paper-architect"
      triggers:
        - "/paper.objectives"
      category: "setup"
      workflow: "initialization"
      spec-file: "commands/paper/objectives.yaml"
      requires-consent: false
      order: 2

    paper.requirements:
      name: "paper.requirements"
      description: "Define technical requirements and specifications"
      display: "Set technical requirements"
      agent: "paper-architect"
      triggers:
        - "/paper.requirements"
      category: "setup"
      workflow: "initialization"
      spec-file: "commands/paper/requirements.yaml"
      requires-consent: false
      order: 3

    paper.spec:
      name: "paper.spec"
      description: "Define content specification and direction"
      display: "Set content specification"
      agent: "paper-architect"
      triggers:
        - "/paper.spec"
      category: "setup"
      workflow: "initialization"
      spec-file: "commands/paper/spec.yaml"
      requires-consent: false
      order: 4

  # Sprint Phase
  sprint:
    paper.sprint-plan:
      name: "paper.sprint-plan"
      description: "Create and plan a new sprint"
      display: "Plan a sprint"
      agent: "paper-architect"
      triggers:
        - "/paper.sprint-plan"
      category: "sprint"
      workflow: "sprint"
      spec-file: "commands/paper/sprint-plan.yaml"
      requires-consent: false

    paper.tasks:
      name: "paper.tasks"
      description: "Track and update sprint tasks"
      display: "Manage sprint tasks"
      agent: "paper-system"
      triggers:
        - "/paper.tasks"
      category: "sprint"
      workflow: "sprint"
      spec-file: "commands/paper/tasks.yaml"
      requires-consent: false

    paper.review:
      name: "paper.review"
      description: "Review sprint outcomes and plan next steps"
      display: "Review sprint"
      agent: "paper-system"
      triggers:
        - "/paper.review"
      category: "sprint"
      workflow: "sprint"
      spec-file: "commands/paper/review.yaml"
      requires-consent: false

  # Core Writing Workflow
  core:
    paper.plan:
      name: "paper.plan"
      description: "Create detailed paper outline and plan"
      display: "Plan paper outline"
      agent: "paper-architect"
      triggers:
        - "/paper.plan"
      category: "core"
      workflow: "core-writing"
      spec-file: "commands/paper/plan.yaml"
      requires-consent: false

    paper.research:
      name: "paper.research"
      description: "Consolidate research into reference documents"
      display: "Research & consolidate"
      agent: "research-consolidator"
      triggers:
        - "/paper.research"
      category: "core"
      workflow: "core-writing"
      spec-file: "commands/paper/research.yaml"
      requires-consent: false

    paper.draft:
      name: "paper.draft"
      description: "Draft individual paper section"
      display: "Draft section"
      agent: "section-drafter"
      triggers:
        - "/paper.draft"
      category: "core"
      workflow: "core-writing"
      spec-file: "commands/paper/draft.yaml"
      requires-consent: false

    paper.refine:
      name: "paper.refine"
      description: "Refine and improve draft section"
      display: "Refine section"
      agent: "quality-refiner"
      triggers:
        - "/paper.refine"
      category: "core"
      workflow: "core-writing"
      spec-file: "commands/paper/refine.yaml"
      requires-consent: false

    paper.refs:
      name: "paper.refs"
      description: "Manage bibliography and citations"
      display: "Manage references"
      agent: "reference-manager"
      triggers:
        - "/paper.refs"
      category: "core"
      workflow: "core-writing"
      spec-file: "commands/paper/refs.yaml"
      requires-consent: true
      tools-used:
        - "format-references.py"

    paper.assemble:
      name: "paper.assemble"
      description: "Integrate sections and compile PDF"
      display: "Assemble & compile"
      agent: "latex-assembler"
      triggers:
        - "/paper.assemble"
      category: "core"
      workflow: "core-writing"
      spec-file: "commands/paper/assemble.yaml"
      requires-consent: true
      tools-used:
        - "lint-latex.sh"
        - "validate-structure.py"
        - "build-latex.sh"

  # Specialist Commands
  specialist:
    paper.brainstorm:
      name: "paper.brainstorm"
      description: "Brainstorm ideas and explore creative options"
      display: "Brainstorm"
      agent: "brainstorm"
      triggers:
        - "/paper.brainstorm"
      category: "specialist"
      spec-file: "commands/paper/specialist/brainstorm.yaml"
      requires-consent: false

    paper.solve:
      name: "paper.solve"
      description: "Solve blockers and identify root causes"
      display: "Solve problem"
      agent: "problem-solver"
      triggers:
        - "/paper.solve"
      category: "specialist"
      spec-file: "commands/paper/specialist/solve.yaml"
      requires-consent: false

    paper.tutor-feedback:
      name: "paper.tutor-feedback"
      description: "Get feedback and critique on draft"
      display: "Get tutor feedback"
      agent: "tutor"
      triggers:
        - "/paper.tutor-feedback"
      category: "specialist"
      spec-file: "commands/paper/specialist/tutor-feedback.yaml"
      requires-consent: false

    paper.librarian-research:
      name: "paper.librarian-research"
      description: "Research and find sources"
      display: "Find sources"
      agent: "librarian"
      triggers:
        - "/paper.librarian-research"
      category: "specialist"
      spec-file: "commands/paper/specialist/librarian-research.yaml"
      requires-consent: false

    paper.librarian-sources:
      name: "paper.librarian-sources"
      description: "Evaluate and track sources"
      display: "Track sources"
      agent: "librarian"
      triggers:
        - "/paper.librarian-sources"
      category: "specialist"
      spec-file: "commands/paper/specialist/librarian-sources.yaml"
      requires-consent: false

    paper.librarian-gaps:
      name: "paper.librarian-gaps"
      description: "Identify research gaps"
      display: "Identify gaps"
      agent: "librarian"
      triggers:
        - "/paper.librarian-gaps"
      category: "specialist"
      spec-file: "commands/paper/specialist/librarian-gaps.yaml"
      requires-consent: false
```

### workflows.yaml Structure

```yaml
# .copilot/workflows.yaml
# Master workflow registry - defines sequences and orchestration

version: "1.0.0"
description: "Registry of all workflows in the Copilot Research Paper Assistant Kit"

workflow-types:
  initialization: "Project setup with canonical documents"
  sprint: "Work sprint (plan → tasks → review)"
  writing: "Paper writing and refinement"

workflows:
  initialization:
    name: "Paper Project Initialization"
    description: "Set up a new paper project with canonical docs (aims, requirements, spec)"
    entry-points:
      - "paper.init"
      - "paper.objectives"
    file: "workflows/setup/initialization.yaml"
    typical-duration: "15-30 minutes"
    phases:
      - "collect-goals"
      - "collect-requirements"
      - "collect-spec"
      - "complete-setup"

  sprint:
    name: "Sprint Workflow"
    description: "Execute a focused sprint with planning, task execution, and review"
    entry-points:
      - "paper.sprint-plan"
    file: "workflows/sprint/sprint.yaml"
    typical-duration: "Variable (1 day to 1 week)"
    phases:
      - "plan-sprint"
      - "execute-tasks"
      - "review-outcomes"
      - "decide-next"

  core-writing:
    name: "Core Paper Writing Workflow"
    description: "Main paper writing workflow (plan → research → draft → refine → refs → assemble)"
    entry-points:
      - "paper.plan"
      - "paper.research"
      - "paper.draft"
    file: "workflows/paper/core-writing.yaml"
    typical-duration: "Varies by section"
    phases:
      - "plan"
      - "research"
      - "draft"
      - "optional-feedback"
      - "refine"
      - "manage-references"
      - "assemble"
```

### tools.yaml Structure

```yaml
# .copilot/tools/tools.yaml
# Tool and script registry with consent and execution metadata

version: "1.0.0"
description: "Registry of tools and scripts used by agents"

tools:
  build-latex:
    name: "build-latex.sh"
    description: "Compile LaTeX document to PDF"
    path: "open-agents/tools/build-latex.sh"
    type: "script"
    language: "shell"
    requires-consent: true
    risk-level: "medium"
    consent-scope: "once-per-session"
    working-directory: "repo-root"
    inputs:
      - "LaTeX source directory"
    outputs:
      - "Compiled PDF"
      - "Build log"
    side-effects:
      - "Creates output-final/pdf/"
      - "Modifies latex/ files (intermediate)"
    timeout: "30 seconds"
    rollback-capable: false

  lint-latex:
    name: "lint-latex.sh"
    description: "Check LaTeX syntax and common issues"
    path: "open-agents/tools/lint-latex.sh"
    type: "script"
    language: "shell"
    requires-consent: false
    risk-level: "low"
    working-directory: "repo-root"
    inputs:
      - "LaTeX source directory"
    outputs:
      - "Syntax check report"
    side-effects: []
    timeout: "10 seconds"
    rollback-capable: true

  validate-structure:
    name: "validate-structure.py"
    description: "Validate paper structure and section completeness"
    path: "open-agents/tools/validate-structure.py"
    type: "script"
    language: "python"
    requires-consent: false
    risk-level: "low"
    working-directory: "repo-root"
    inputs:
      - "Memory files path"
      - "Output directories"
    outputs:
      - "Structure validation report"
      - "Completion percentage"
    side-effects: []
    timeout: "5 seconds"
    rollback-capable: true

  format-references:
    name: "format-references.py"
    description: "Format and validate bibliography in Harvard style"
    path: "open-agents/tools/format-references.py"
    type: "script"
    language: "python"
    requires-consent: true
    risk-level: "medium"
    consent-scope: "once-per-session"
    working-directory: "repo-root"
    inputs:
      - "BibTeX file path"
      - "Citation keys"
    outputs:
      - "Formatted references.bib"
      - "Validation report"
    side-effects:
      - "Modifies latex/references/references.bib"
    timeout: "10 seconds"
    rollback-capable: true
    allows-undo: true
```

### settings.yaml Structure

```yaml
# .copilot/config/settings.yaml
# System-wide configuration and defaults

version: "1.0.0"
system:
  name: "Copilot Research Paper Assistant Kit"
  formal-name: "Copilot Research Paper Assistant Kit"
  former-name: "Academic Specification Paper Writing System"
  description: "GitHub Copilot integration for academic paper research and writing"
  version: "1.0.0"

paths:
  working-reference: "memory/working-reference.md"
  canonical-docs: "planning/0000-Project-Overview/"
  canonical-docs-list:
    - "aims-and-objectives.md"
    - "requirements.md"
    - "content-specification.md"
  sprint-folder-pattern: "planning/YYYYMMDD-*"
  drafts: "open-agents/output-drafts/"
  refined: "open-agents/output-refined/"
  final: "open-agents/output-final/"
  latex-source: "latex/"
  memory: "memory/"

defaults:
  standards-flexibility: "pragmatic"  # or "strict"
  allow-gap-deferral: true
  allow-placeholder-citations: true
  progressive-disclosure: true
  max-context-size: "large"
  session-type: "standard"  # or "quick", "enterprise"

memory:
  metadata-file: "memory/paper-metadata.yaml"
  research-index: "memory/research-index.yaml"
  section-status: "memory/section-status.yaml"
  revision-log: "memory/revision-log.md"
  auto-save: true
  save-interval: 300  # seconds

ui:
  progressive-questions: true
  bombardment-prevention: true
  suggestion-level: "moderate"  # or "minimal", "aggressive"
  visual-workflows: true

integrations:
  github-copilot: true
  vscode-native: true
  claude-projects: false
  chatgpt-custom: false

quality:
  require-citations: true
  require-sources: true
  harvard-style: true
  validate-on-save: true
  auto-lint: false
```

### consent.yaml Structure

```yaml
# .copilot/config/consent.yaml
# Consent policies and scope definitions

version: "1.0.0"
description: "Consent and permission management for tool execution"

consent-scopes:
  once:
    name: "Allow once"
    description: "Execute this tool one time only"
    duration: "single-execution"
    storage: "memory"
    expires-at: "end-of-call"
    can-batch: false
    icon: "⚡"

  session:
    name: "Allow for this session"
    description: "Execute this tool anytime in the current chat session"
    duration: "chat-session"
    storage: "workspaceState"
    expires-at: "session-end"
    can-batch: true
    icon: "💬"

  workspace:
    name: "Allow for this workspace"
    description: "Execute this tool anytime in this workspace"
    duration: "workspace-lifetime"
    storage: "workspaceState"
    expires-at: "never"
    can-batch: true
    icon: "📁"

  always:
    name: "Always allow on this machine"
    description: "Execute this tool anytime on this machine"
    duration: "machine-lifetime"
    storage: "globalState"
    expires-at: "never"
    can-batch: true
    icon: "🔓"

  batch-session:
    name: "Run all tools for this session"
    description: "Approve all pending tool executions for the entire session"
    duration: "chat-session"
    storage: "workspaceState"
    expires-at: "session-end"
    can-batch: true
    is-meta: true
    icon: "⚙️"

consent-prompt:
  title: "Execute tool?"
  message: "This action requires your permission"
  options-order:
    - "once"
    - "session"
    - "workspace"
    - "always"
    - "batch-session"
  include-description: true
  include-side-effects: true
  include-cancel: true

tool-policies:
  build-latex:
    requires-consent: true
    default-scope: "once"
    dangerous: true
    allows-undo: false
    log-execution: true
    requires-confirmation: true

  lint-latex:
    requires-consent: false
    read-only: true
    log-execution: false

  validate-structure:
    requires-consent: false
    read-only: true
    log-execution: false

  format-references:
    requires-consent: true
    default-scope: "once"
    allows-undo: true
    log-execution: true
    requires-confirmation: false

logging:
  consent-log-file: ".vscode/agent-consent.log"
  include-timestamp: true
  include-user: false
  include-scope: true
  include-tool: true
  retention: "persist"  # keep log file between sessions
  include-decline: true

reset:
  provide-palette-command: true
  palette-command-name: "Copilot: Reset Consent Approvals"
  allow-user-reset-all: true
  allow-user-reset-per-tool: true
  allow-clear-log: true
```

---

