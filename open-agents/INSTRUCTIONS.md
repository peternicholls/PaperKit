# Starter Open Agent System

This system shows how to run markdown-defined agents inside an AI coding assistant. It provides a single starter agent that turns loose requests into actionable plans saved in the outputs folder.

---

## How This System Works

1. Entry point files (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `COPILOT.md`) direct the assistant to read this file first.
2. This file lists available agents and routing rules; full agent definitions live in `open-agents/agents/` and load only when needed.
3. Agents read/write within `open-agents/`, using `source/` for inputs and `output-*` for staged outputs.

---

## Project Structure

- `open-agents/README.md` — Human overview of this system
- `open-agents/INSTRUCTIONS.md` — Index, routing, and system rules (this file)
- `open-agents/agents/` — Agent definitions (load on demand)
- `open-agents/tools/` — Optional helper scripts created by agents
- `open-agents/source/` — User-provided inputs or stubs
- `open-agents/output-drafts/` — First-pass outputs
- `open-agents/output-refined/` — Reviewed/edited outputs
- `open-agents/output-final/` — Publish-ready outputs

---

## Available Agents

### 1) Starter Planner (`agents/starter_planner.md`)

**Purpose:** Convert open-ended requests into concise, actionable plans with file breadcrumbs and next steps.

**When to use:**
- User asks how to approach a task or project
- User wants a checklist or work breakdown for a goal
- User provides a stub in `source/` and asks what to do with it

**Output:** Markdown plans saved to `open-agents/output-drafts/` as `plan-[slug].md`

**To use this agent:** Read `open-agents/agents/starter_planner.md`

---

## Routing Logic

| User says... | Agent |
|--------------|-------|
| "Plan how to...", "What steps should I take..." | Starter Planner |
| "Make a checklist for...", "Help me scope..." | Starter Planner |

---

## Git Commit Protocol

- Keep working tree clean when possible; group related changes.
- Suggested message format: `Add starter agent plan` or similar.
- Do not amend existing commits unless explicitly asked.

---

## File Naming Conventions

- Plans: `plan-[short-slug].md` in `open-agents/output-drafts/`
- Tools/scripts: `open-agents/tools/{purpose}.{ext}`
- Additional agents: `open-agents/agents/{name}.md` (kebab or snake case)

---

## Quick Start

1. Trigger the Starter Planner with `/starter plan {goal}` or by asking in natural language.
2. Place any reference material in `open-agents/source/` before running the agent.
3. Find the generated plan in `open-agents/output-drafts/` and refine as needed.
