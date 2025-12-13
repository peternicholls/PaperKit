# Comprehensive Implementation Plan: Copilot Research Paper Assistant Kit Restructuring

**Date:** 13 December 2025  
**Status:** Planning Phase  
**Purpose:** Restructure the system following BMAD-METHOD patterns for improved scalability, maintainability, and user experience

---

## Executive Summary

This plan outlines a complete restructuring of the Copilot Research Paper Assistant Kit to:
1. Move all system agents and configurations into `.copilot/` (away from user content in `open-agents/`)
2. Implement a configuration-driven architecture using YAML registries and workflow definitions
3. Move memory management to protected `.copilot/memory/` directory
4. Adopt BMAD-METHOD patterns for modular, scalable design
5. Create explicit workflow orchestration (setup, sprint, writing)
6. Improve discoverability through master registries (agents, commands, workflows)

---

## Phase 1: Create Configuration Structure (Foundation)

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

## Phase 2: Convert Agent Specs to YAML

### Core Agents (to create)

**Structure for each agent YAML (example: research-consolidator.yaml):**

```yaml
# .copilot/agents/core/research-consolidator.yaml
name: "research-consolidator"
display-name: "Research Consolidator"
description: "Synthesizes research materials into coherent reference documents"
role: "Synthesizer"
category: "research"
version: "1.0"

personality:
  tone: "Academic but accessible"
  style: "Objective and narrative-driven"
  expertise: "Research synthesis, citation management, academic writing"

capabilities:
  primary: "Synthesize and organize research from multiple sources"
  secondary:
    - "Validate citations and academic rigor"
    - "Identify research gaps"
    - "Create Harvard-style bibliographies"

triggers:
  commands:
    - "research [topic]"
    - "consolidate research on [topic]"
    - "synthesize findings on [topic]"
  intents:
    - "User has collected research notes"
    - "User needs synthesis before drafting"
    - "Research is scattered and needs organization"

inputs:
  required:
    - research-materials: "Notes, links, excerpts, ideas"
    - goal: "What is this research for in the paper?"
  optional:
    - scope: "Broad overview or deep technical"
    - sources-to-exclude: "Known irrelevant sources"

outputs:
  primary:
    - path: "output-refined/research/"
      format: "markdown"
      naming: "[topic_name].md"
  secondary:
    - path: "memory/research-index.yaml"
      action: "update"
    - path: "memory/working-reference.md"
      action: "update"

output-template: |
  # [Research Topic Title]
  
  ## Overview
  [Scope and relevance to paper goal]
  
  ## [Major Topic 1]
  [Content with citations]
  
  ## Key Insights and Synthesis
  [Connecting themes across sources]
  
  ## Gaps and Future Research
  [What remains unknown]
  
  ## Bibliography
  [Harvard-formatted sources]

behavioral-rules:
  - "Never fabricate citations"
  - "Distinguish consensus from individual perspectives"
  - "Include qualifications (e.g., 'Recent research suggests...')"
  - "Flag areas needing more research"
  - "Ask clarifying questions when research goal is unclear"
  - "Synthesize, don't list (narrative not bullet-points)"

collaboration-hints:
  works-well-with:
    - "section-drafter"
    - "librarian"
  receives-input-from:
    - "librarian" (source recommendations)
  provides-input-to:
    - "section-drafter" (consolidated research)

quality-standards:
  citation-density: "Every factual claim cited"
  academic-tone: "Formal but readable"
  rigor: "Pragmatic" (or "strict")
  completeness: "Sufficient for paper integration"

constraints:
  max-output-size: "Large documents ok"
  context-usage: "Can load large research files"
  token-efficiency: "Use document sharding if needed"

spec-file: "open-agents/agents/research_consolidator.md"
load-instructions: |
  1. Read open-agents/INSTRUCTIONS.md
  2. Read open-agents/agents/research_consolidator.md (full spec)
  3. Synthesize input research materials
  4. Follow output-template structure
  5. Update memory files after completion
```

**Agents to create (same structure):**
- `.copilot/agents/core/paper-architect.yaml`
- `.copilot/agents/core/section-drafter.yaml`
- `.copilot/agents/core/quality-refiner.yaml`
- `.copilot/agents/core/reference-manager.yaml`
- `.copilot/agents/core/latex-assembler.yaml`

### Specialist Agents (to create)

Same YAML structure, created in:
- `.copilot/agents/specialist/brainstorm.yaml`
- `.copilot/agents/specialist/problem-solver.yaml`
- `.copilot/agents/specialist/tutor.yaml`
- `.copilot/agents/specialist/librarian.yaml`

---

## Phase 3: Define Commands in YAML

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

## Phase 4: Define Workflows Declaratively

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

## Phase 5: Move & Protect Memory

### Files to Migrate

**From:** `open-agents/memory/`  
**To:** `.copilot/memory/`

- `paper-metadata.yaml`
- `research-index.yaml`
- `section-status.yaml`
- `working-reference.md`
- `revision-log.md`

### Create Protection Layer

**New file:** `.copilot/memory/README.md`

```markdown
# Memory Files (System-Managed)

⚠️ These files are system-managed. Do not edit directly.

**Working Reference:** See [working-reference.md](working-reference.md) for a human-readable session handoff.

**System Memory Files:**
- `paper-metadata.yaml` — Project metadata (auto-updated by agents)
- `research-index.yaml` — Research tracking (auto-updated by Research Consolidator)
- `section-status.yaml` — Section progress (auto-updated by agents)
- `revision-log.md` — Change history (auto-updated by agents)

## Updating Memory

Agents update these files during their work. Do not edit manually.

## Questions About Progress?

Read `working-reference.md` — it's designed for human consumption and always kept current by agents.
```

---

## Phase 6: Clean Up Naming & Organization

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

## Phase 7: Create Master Registries

Registries created in Phase 1 act as single source of truth.

**Usage example:** When user types `/paper.plan`, the system:
1. Looks up `/paper.plan` in `commands.yaml`
2. Finds routing: `agent: "paper-architect"`, `spec-file: "commands/paper/plan.yaml"`
3. Loads the command spec (inputs, outputs, workflow)
4. Loads the agent spec from `agents.yaml`: `spec-file: "agents/core/paper-architect.yaml"`
5. Invokes the agent with proper context

---

## Phase 8: Create Configuration System

- `consent.yaml` — Manages consent scopes, policies, and logging
- `settings.yaml` — System defaults, paths, quality standards
- `tools.yaml` — Tool registry with metadata

---

## Phase 9: Documentation & Discovery

### Create READMEs

Each major folder gets a README explaining:
- Purpose and contents
- How items are organized
- How to add new items
- Key design decisions

**Files to create:**
- `.copilot/README.md` (overall structure)
- `.copilot/agents/README.md` (agent system)
- `.copilot/commands/README.md` (command system)
- `.copilot/workflows/README.md` (workflow system)
- `.copilot/memory/README.md` (memory management)
- `.copilot/modules/README.md` (module system, future)
- `.copilot/tools/README.md` (tool integration)
- `.copilot/config/README.md` (configuration)

### Create Migration Guide

**File:** `MIGRATION-GUIDE.md` (in repo root)

Maps old structure to new structure:
- Old agent paths → new YAML locations
- Old command files → new YAML specifications
- Old memory paths → new protected locations
- What changed and why

---

## Phase 10: Integration & Testing

### Wire Copilot Extension

The `paper-system.yaml` agent (router) must:
1. Read from master registries (agents, commands, workflows)
2. Route commands based on registry metadata
3. Load agent YAML specs instead of hardcoding
4. Support workflow orchestration

### Create Validation Script

**File:** `.copilot/tools/validate-system.sh` (shell) or `.copilot/tools/validate.py` (Python)

Checks:
- YAML syntax for all registries and specs
- All referenced files exist
- Agent/command completeness (required fields present)
- No missing prerequisites
- Workflow consistency

### Run End-to-End Tests

1. **Test Setup Workflow:**
   - Run `/paper.init`
   - Verify canonical docs created
   - Check working reference updated

2. **Test Sprint Workflow:**
   - Run `/paper.sprint-plan`
   - Create tasks
   - Run `/paper.review`

3. **Test Writing Workflow:**
   - Run `/paper.plan` (outline)
   - Run `/paper.research` (research)
   - Run `/paper.draft` (draft section)
   - Run `/paper.refine` (refine)
   - Run `/paper.assemble` (build)

---

## Timeline & Dependencies

### Tier 1: Critical Foundation (Weeks 1–2)
- [ ] Create registries (agents.yaml, commands.yaml, workflows.yaml)
- [ ] Create configuration files (settings.yaml, consent.yaml, tools.yaml)
- [ ] Create folder structure
- [ ] Move memory files

### Tier 2: Refactoring Agents (Weeks 2–3)
- [ ] Convert agent specs to YAML
- [ ] Create agent registry metadata
- [ ] Link YAML specs to markdown docs

### Tier 3: Workflow System (Weeks 3–4)
- [ ] Define setup workflow (YAML)
- [ ] Define sprint workflow (YAML)
- [ ] Define writing workflow (YAML)

### Tier 4: Configuration System (Weeks 4–5)
- [ ] Finalize consent policy
- [ ] Finalize system settings
- [ ] Finalize tool registry

### Tier 5: Documentation & Integration (Weeks 5–6)
- [ ] Create all README files
- [ ] Create migration guide
- [ ] Wire up Copilot extension
- [ ] Create validation script

### Tier 6: Testing & Polish (Weeks 6+)
- [ ] End-to-end testing
- [ ] User feedback
- [ ] Refinements

---

## Success Criteria

- [x] Plan completed and documented
- [ ] All agents accessible via registry
- [ ] All commands accessible via registry
- [ ] Workflows explicitly defined
- [ ] Memory protected in `.copilot/`
- [ ] Structure mirrors BMAD's modular approach
- [ ] Configuration-driven (easy to extend)
- [ ] Documentation clear and complete
- [ ] End-to-end workflows functional
- [ ] User can't accidentally edit system configs
- [ ] Validation script passing
- [ ] End-to-end tests passing

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| YAML for config + Markdown for docs | YAML is parseable; markdown is readable. Both together = best of both. |
| Central registries | Single source of truth; easier discovery; better tooling. |
| Move memory to `.copilot/` | Keeps system data separate from user content; prevents accidental corruption. |
| Declarative workflows | Workflows are visible, testable, independent of agent implementations. |
| No XML, use YAML/JSON/CSV | Simpler, more readable, better for human collaboration. |
| BMAD-inspired architecture | Proven pattern; scales from simple to enterprise. |

---

## What Stays the Same

- ✓ `open-agents/INSTRUCTIONS.md` (master guide, still authoritative)
- ✓ `open-agents/agents/*.md` (documentation reference)
- ✓ `open-agents/tools/` (scripts themselves)
- ✓ `latex/` (source files)
- ✓ `planning/` (user documents)
- ✓ Core agent behaviors and capabilities

---

## What Moves/Changes

- ✓ System configuration → `.copilot/` (out of user directories)
- ✓ Memory → `.copilot/memory/` (protected)
- ✓ Agent specs → YAML in `.copilot/agents/` (machine-readable)
- ✓ Command specs → YAML in `.copilot/commands/` (machine-readable)
- ✓ Workflows → Declarative YAML in `.copilot/workflows/` (orchestrated)
- ✓ Agent naming → Dashes instead of underscores (consistency)

---

## Next Action

**Start Phase 1:** Create registries and folder structure in `.copilot/`.

This plan provides:
✓ A clear, phased approach  
✓ BMAD-inspired modular architecture  
✓ Configuration-driven extensibility  
✓ Protected system data  
✓ Explicit workflow orchestration  
✓ Improved maintainability and scalability  

All without breaking existing functionality.
