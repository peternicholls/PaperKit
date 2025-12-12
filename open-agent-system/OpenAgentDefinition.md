# Open Agent System Definition

A comprehensive specification for building and managing Open Agent Systems—project structures that transform AI coding assistants into general-purpose agents for any domain.

---

## Table of Contents

1. [What Is an Open Agent System?](#1-what-is-an-open-agent-system)
2. [Core Architecture](#2-core-architecture)
   - [The Mandatory Read Directive](#critical-the-mandatory-read-directive) ← **Most important requirement**
3. [Folder Structure](#3-folder-structure)
4. [Agent File Anatomy](#4-agent-file-anatomy)
   - [Agent-Created Tools](#agent-created-tools)
5. [The Command System](#5-the-command-system)
6. [The INSTRUCTIONS.md File](#6-the-instructionsmd-file)
7. [Operations Guide](#7-operations-guide)
8. [Adding to an Existing Project](#8-adding-to-an-existing-project)
9. [Complete Example](#9-complete-example)

---

## 1. What Is an Open Agent System?

### Definition

An **Open Agent System** is a folder structure and set of markdown files that reconfigures AI coding assistants (Claude Code, Gemini CLI, Codex, etc.) to perform specialized, non-coding tasks. Instead of writing code, the AI manages files, performs research, transforms content, and executes domain-specific workflows.

### The Core Insight

Claude Code, Gemini CLI, and similar tools are **general-purpose agent frameworks** that happen to be configured for coding by default. Their fundamental capability is:

- Reading and writing files
- Following complex instructions
- Using tools (web search, shell commands, etc.)
- Managing context across conversations

This capability set works for *any* file-based workflow—not just code. An Open Agent System provides the structure to redirect these capabilities toward your specific domain.

### Why This Pattern Exists

**Problem:** Building custom AI agents requires software engineering—writing code, managing deployments, building UIs, maintaining infrastructure.

**Solution:** Open Agent Systems let you define agent behavior in markdown files. No code required. The AI reads your instructions and becomes that agent.

**Benefit:** You can create sophisticated multi-agent workflows using nothing but folders and markdown files, runnable in any AI coding assistant.

### Tool Agnosticism

A key feature of Open Agent Systems is **tool agnosticism**. The same system works with:
- Claude Code (via `CLAUDE.md`)
- Codex (via `AGENTS.md`)
- Gemini CLI (via `GEMINI.md`)

All three point to the same `INSTRUCTIONS.md` file. You write your agents once and use them with any tool.

---

## 2. Core Architecture

### The Pointer Pattern

Open Agent Systems use a three-layer architecture:

```
┌─────────────────────────────────────────────────────────┐
│  CLAUDE.md  /  AGENTS.md  /  GEMINI.md                  │
│  (Tool-specific entry points - augmented with pointer)  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│           open-agents/INSTRUCTIONS.md                    │
│  (Agent index: lists all agents with descriptions)      │
│  (Routing logic: when to use which agent)               │
│  (Loaded into context at conversation start)            │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼ (on demand only)
┌─────────────────────────────────────────────────────────┐
│  open-agents/agents/researcher.md    transformer.md ...  │
│  (Full agent definitions - loaded when triggered)        │
└─────────────────────────────────────────────────────────┘
```

### Critical: The Mandatory Read Directive

**This is the most important requirement of the entire system.**

Each entry point file (CLAUDE.md, AGENTS.md, GEMINI.md) MUST include a read directive at the top. Without this, the agent system won't function.

#### Required Format

```markdown
**CRITICAL: Read `open-agents/INSTRUCTIONS.md` immediately.**
```

That's it. One line. The AI will read the file and understand the system.

#### Creating Entry Point Files

When setting up an Open Agent System, **always create entry point files if they don't exist**:

- `CLAUDE.md` — for Claude Code
- `AGENTS.md` — for Codex
- `GEMINI.md` — for Gemini CLI

Since you're already creating `.claude/commands/` and `.gemini/commands/` folders, create these files too. A minimal entry point file is just:

```markdown
**CRITICAL: Read `open-agents/INSTRUCTIONS.md` immediately.**
```

If the project already has these files, add the directive at the top.

---

### Why This Pattern?

**Progressive Disclosure:** Agent definitions can be large (hundreds of lines). Loading all agents into context at once wastes tokens and creates noise. Instead:

1. At conversation start, only `INSTRUCTIONS.md` is loaded
2. `INSTRUCTIONS.md` contains brief descriptions of each agent
3. Full agent files are loaded only when that agent is triggered

**Context Management:** AI assistants have limited context windows. The pointer pattern keeps initial context small while allowing complex agent definitions.

**Single Source of Truth:** All tool-specific entry points (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) point to the same instructions. Update once, works everywhere.

**Non-Disruptive:** The Open Agent System lives in its own folder (`open-agents/`) and augments existing project files rather than replacing them.

### Layer Responsibilities

| Layer | File(s) | Responsibility |
|-------|---------|----------------|
| Entry | `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` | Tool detection, pointer to instructions |
| Index | `open-agents/INSTRUCTIONS.md` | Agent catalog, routing logic, workflow docs |
| Agents | `open-agents/agents/*.md` | Full agent definitions, behaviors, formats |

---

## 3. Folder Structure

### The open-agents/ Container

Open Agent Systems live in a single `open-agents/` folder at the project root. This isolates the agent system from the rest of the project and prevents conflicts with existing files.

```
existing-project/
├── (existing project files...)
├── CLAUDE.md                    # Augmented with pointer
├── AGENTS.md                    # Augmented with pointer
├── GEMINI.md                    # Augmented with pointer
│
└── open-agents/                 # The agent system container
    ├── README.md                # Human-readable intro
    ├── INSTRUCTIONS.md          # Agent index and routing
    │
    ├── agents/                  # Agent definitions
    │   ├── researcher.md
    │   ├── transformer.md
    │   └── publisher.md
    │
    ├── tools/                   # Agent-created scripts (optional)
    │   └── (scripts created by agents)
    │
    ├── source/                  # User inputs
    │   └── (raw materials, requests, stubs)
    │
    ├── output-drafts/           # First-stage outputs
    │   └── (initial processing results)
    │
    ├── output-refined/          # Second-stage outputs
    │   └── (refined, reviewed content)
    │
    └── output-final/            # Final deliverables
        └── (publication-ready materials)
```

### Why This Structure?

1. **Isolation:** The entire agent system is contained in one folder
2. **Non-disruptive:** Doesn't overwrite existing project files
3. **Portable:** Can be copied between projects
4. **Clear separation:** Agent system vs. project code is obvious

### Folder Purposes

| Folder | Purpose | Example Contents |
|--------|---------|------------------|
| `agents/` | Agent definitions | `researcher.md`, `transformer.md` |
| `tools/` | Scripts created by agents | `compress_audio.sh`, `resize_image.py` |
| `source/` | Raw inputs from user | Notes, stubs, requests, reference materials |
| `output-drafts/` | First processing stage | Drafts, initial transforms, rough outputs |
| `output-refined/` | Intermediate stage | Reviewed, refined, or transformed outputs |
| `output-final/` | Final deliverables | Publication-ready materials |

### Domain-Specific Naming

Rename output folders to match your domain:

**Video Production:**
```
output-scripts/
output-production/
output-final/
```

**Research Project:**
```
output-notes/
output-analysis/
output-papers/
```

**Content Creation:**
```
output-drafts/
output-reviewed/
output-published/
```

---

## 4. Agent File Anatomy

### What Makes an Agent File

An agent file is a markdown document in `open-agents/agents/` that defines:
- What the agent does
- When it should be activated
- How it should behave
- What output it produces
- Where output goes

### Required Sections

Every agent file should contain these sections:

```markdown
# [Agent Name]

[1-2 sentence description of what this agent does]

---

## Purpose

[Expanded description: what problem does this agent solve?
What is its role in the system? What makes it valuable?]

---

## When to Use This Agent

Use this agent when the user:
- [Trigger phrase or condition]
- [Another trigger]
- [Another trigger]

---

## Core Behaviors

### 1. [First Behavior]
[Description of what the agent does]

### 2. [Second Behavior]
[Description]

### 3. [Third Behavior]
[Description]

---

## Output Format

[Define the structure of what the agent produces.
Use code blocks to show templates if helpful.]

---

## Output Location

Save outputs to: `open-agents/[folder]/[filename_pattern]`

Examples:
- `open-agents/output-drafts/example_filename.ext`
- `open-agents/output-final/another_example.ext`

---

## Examples

[Optional but recommended: show example inputs and outputs]

> Example prompt: "[user request]"
> Example output: [what the agent would produce]
```

### Agent Design Principles

**1. Single Responsibility**
Each agent should do one thing well. If an agent does too much, split it.

**2. Clear Triggers**
Make it obvious when this agent should be used vs. another. The "When to Use" section is critical for routing.

**3. Explicit Output Location**
Always tell the agent where to save its work. Ambiguity causes confusion.

**4. Behavioral, Not Technical**
Describe what the agent should *do*, not how it should *implement*. Let the AI figure out implementation.

**5. Include Examples**
Examples are the most effective way to communicate expectations. Include at least one.

**6. Consider Tool Creation**
Agents may benefit from writing their own scripts/tools for repeatable operations. See [Agent-Created Tools](#agent-created-tools) below.

### Example Agent File (Condensed)

```markdown
# History Researcher

Researches historical topics and produces rich markdown articles with images and links.

---

## Purpose

This agent creates comprehensive, engaging articles about historical topics.
It can originate content from a topic name or expand existing stub files.

---

## When to Use This Agent

Use this agent when the user:
- Asks to "research" a historical topic
- Asks to "expand" or "deepen" an existing article
- Asks to "write about" a historical subject
- Provides a stub file and wants it filled in

---

## Core Behaviors

### 1. Research Thoroughly
Use web search to gather dates, events, figures, and context.
Prioritize interesting details over dry facts.

### 2. Write Engagingly
Produce narrative prose, not encyclopedia entries.
Multi-paragraph depth for each major section.

### 3. Include Visuals
Add markdown image references throughout:
`![Description](suggested-search-term)`

---

## Output Format

```markdown
# [Topic Title]

> [One-sentence hook]

## Introduction
[2-3 paragraphs setting the stage]

## [First Major Era]
[Multiple paragraphs with images]

## [Continue as needed...]

## Legacy and Impact
[Why this matters today]

## Further Reading
- [Links to sources]
```

---

## Output Location

Save to: `open-agents/output-articles/`
Filename: `topic_name.md` (lowercase, underscores)

---

## Examples

> "Research the history of Disney animation"

Creates `open-agents/output-articles/disney_animation.md` with a 2,000-4,000 word
article covering Disney's founding through present day.
```

### Agent-Created Tools

Agents can create their own scripts and tools to handle repeatable operations more efficiently. Instead of regenerating the same logic via the LLM every time, an agent can write a script once and reuse it.

#### When to Create Tools

Consider tool creation when an agent:
- Performs the same file manipulation repeatedly (resize images, compress audio, convert formats)
- Executes complex shell commands that are error-prone to generate each time
- Needs precise, deterministic behavior (not probabilistic LLM output)
- Would benefit from faster execution (scripts run faster than LLM reasoning)

#### Tool Location

Store agent tools in a `tools/` subfolder within `open-agents/`:

```
open-agents/
├── INSTRUCTIONS.md
├── agents/
│   ├── audio_processor.md
│   └── image_optimizer.md
└── tools/
    ├── compress_audio.sh
    ├── resize_image.py
    └── convert_format.js
```

#### Referencing Tools in Agent Files

When an agent has associated tools, document them:

```markdown
## Available Tools

This agent has access to the following scripts:

### `open-agents/tools/compress_audio.sh`
Compresses audio files to a target bitrate.
Usage: `./open-agents/tools/compress_audio.sh <input> <output> <bitrate>`

### `open-agents/tools/normalize_volume.sh`
Normalizes audio volume to -14 LUFS.
Usage: `./open-agents/tools/normalize_volume.sh <input> <output>`

When performing these operations, use the scripts rather than
constructing the ffmpeg commands manually each time.
```

#### Self-Authoring Tools

An agent can be designed to create its own tools when needed. Include this capability in the agent definition:

```markdown
## Tool Creation

If you find yourself repeating the same operation multiple times,
consider writing a reusable script:

1. Create the script in `open-agents/tools/`
2. Make it executable: `chmod +x open-agents/tools/script_name.sh`
3. Document it in this agent file under "Available Tools"
4. Use it for future operations

This improves reliability (deterministic behavior) and speed
(no LLM reasoning required for repeated operations).
```

---

## 5. The Command System

### What Commands Are

Commands provide **predictable invocation** of agents. Instead of hoping the AI recognizes a trigger phrase, you can explicitly call:

```
/history research Disney animation
/history html disney_animation.md
/history extract disney_animation.md
```

### Two Parallel Command Structures

Open Agent Systems maintain commands for multiple tools:

```
.claude/commands/           # Claude Code commands
└── {domain}/
    ├── {command1}.md
    └── {command2}.md

.gemini/commands/           # Gemini CLI commands
└── {domain}/
    └── (same structure)
```

Commands are organized by domain (e.g., `history/`, `video/`, `research/`).

### Command File Structure

Commands are simple—they instruct the AI to use an agent:

```markdown
[Brief description of what this command does]

Follow the instructions in `open-agents/agents/{name}.md` to complete this task.

$ARGUMENTS
```

The `$ARGUMENTS` placeholder passes any user input after the command name.

### Example Command

`.claude/commands/history/research.md`:
```markdown
Research a historical topic and create a comprehensive article.

Follow the instructions in `open-agents/agents/researcher.md`.

$ARGUMENTS
```

The same file should exist at `.gemini/commands/history/research.md`.

### Why Both Claude and Gemini Commands?

**Tool Agnosticism:** Users should be able to use their preferred tool. Maintaining both command structures ensures the system works regardless of which AI assistant is used.

**Identical Content:** The command files are usually identical between `.claude/` and `.gemini/`. When you create or update a command, update both locations.

### Command Naming Conventions

**Structure:** `.claude/commands/{domain}/{action}.md`
- `{domain}` = the subject area (history, video, research, etc.)
- `{action}` = what the command does (research, transform, publish)

**Examples:**
- `/history research` → `.claude/commands/history/research.md`
- `/video critique` → `.claude/commands/video/critique.md`

### Note on System Management

System operations (adding, editing, removing agents) are documented directly in `INSTRUCTIONS.md` rather than as separate commands. This keeps the system simpler and ensures the guidance is always available without additional command files. See [Operations Guide](#7-operations-guide) for details.

---

## 6. The INSTRUCTIONS.md File

### The Heart of the System

`INSTRUCTIONS.md` is the most important file in an Open Agent System. It:
- Describes the system's purpose
- Lists all available agents
- Defines routing logic
- Documents workflow
- Sets behavioral rules (like git commit protocol)

### Required Sections

```markdown
# [System Name]

[Brief description of what this system does]

---

## How This System Works

[Explain the pointer pattern, progressive disclosure]

---

## Project Structure

[Document the folder structure with descriptions]

---

## Available Agents

### 1. [Agent Name] (`agents/file.md`)

**Purpose:** [What it does]

**When to use:**
- [Trigger conditions]

**Output:** [Where results go]

**To use this agent:** Read `open-agents/agents/file.md`

### 2. [Next Agent]
...

---

## Routing Logic

| User says... | Agent to use |
|--------------|--------------|
| "[trigger phrase]" | [Agent name] |
| "[another phrase]" | [Agent name] |

---

## Git Commit Protocol

[Define when and how to commit]

---

## File Naming Conventions

[Define naming patterns]

---

## Quick Start

[Brief getting-started guide]
```

### Agent Descriptions in INSTRUCTIONS.md

Each agent entry should be brief but complete enough for routing:

```markdown
### 1. The Researcher (`agents/researcher.md`)

**Purpose:** Research historical topics and produce rich markdown articles.

**When to use:**
- User asks to "research" a topic
- User asks to "expand" or "deepen" an article
- User asks to "write about" something
- User provides a stub file

**Output:** Markdown files in `open-agents/output-articles/`

**To use this agent:** Read `open-agents/agents/researcher.md`
```

### The Routing Table

The routing table helps the AI decide which agent to invoke:

```markdown
## Routing Logic

| User says... | Agent to use |
|--------------|--------------|
| "Research the history of X" | Researcher |
| "Expand this article" | Researcher |
| "Create an HTML page from this" | HTML Generator |
| "Extract the data into JSON" | Data Extractor |
| "Create all outputs for this" | Researcher → HTML → Extractor (chain) |
```

### Workflow Documentation

If agents can be chained, document the workflow:

```markdown
## Workflow

A common flow through this system:

1. **Research:** User provides a topic → Researcher creates article
2. **Transform:** Article → HTML Generator creates webpage
3. **Extract:** Article → Data Extractor creates JSON

Agents can be used independently or in sequence.
```

---

## 7. Operations Guide

### Creating a New Open Agent System

Follow these steps to create a system from scratch:

#### Step 1: Create Folder Structure

```bash
mkdir -p open-agents/{agents,tools,source,output-drafts,output-refined,output-final}
mkdir -p .claude/commands/{domain}
mkdir -p .gemini/commands/{domain}
```

#### Step 2: Create the README.md

Create `open-agents/README.md`:
```markdown
# Open Agent System

This folder contains an **Open Agent System**—a collection of markdown-defined agents that transform AI coding assistants into specialized tools for [your domain].

## What's Here

- `INSTRUCTIONS.md` — Full documentation, agent index, and routing logic
- `agents/` — Individual agent definitions
- `source/` — Input materials
- `output-*/` — Processing stages

## Quick Start

Read `INSTRUCTIONS.md` for available agents and how to use them.
```

#### Step 3: Create INSTRUCTIONS.md

Create `open-agents/INSTRUCTIONS.md` with:
- System description
- Project structure documentation
- Agent index (initially empty or with planned agents)
- Routing logic
- Git commit protocol

#### Step 4: Create Agent Files

For each agent, create `open-agents/agents/{name}.md` with:
- Purpose
- When to use
- Core behaviors
- Output format
- Output location

#### Step 5: Create Command Files

For each agent, create commands in both:
- `.claude/commands/{domain}/{command}.md`
- `.gemini/commands/{domain}/{command}.md`

#### Step 6: Document System Operations in INSTRUCTIONS.md

Include guidance for managing the system directly in `INSTRUCTIONS.md`:

```markdown
## Managing This System

### Adding a New Agent
1. Create `open-agents/agents/{name}.md` with purpose, triggers, behaviors, output format
2. Create commands in `.claude/commands/{domain}/` and `.gemini/commands/{domain}/`
3. Add agent entry to "Available Agents" section above
4. Add routing entries to the routing table

### Editing an Agent
1. Modify `open-agents/agents/{name}.md`
2. Update commands if invocation changes
3. Update routing table if triggers change

### Removing an Agent
1. Delete the agent file and command files
2. Remove from "Available Agents" and routing table
```

---

### Adding an Agent to an Existing System

#### Step 1: Create the Agent File

Create `open-agents/agents/{name}.md` following the agent anatomy template.

#### Step 2: Create Command Files

Create `.claude/commands/{domain}/{command}.md`:
```markdown
[Brief description]

Follow the instructions in `open-agents/agents/{name}.md`.

$ARGUMENTS
```

Create identical file in `.gemini/commands/{domain}/`.

#### Step 3: Update INSTRUCTIONS.md

Add an entry to the "Available Agents" section:
```markdown
### [N]. [Agent Name] (`agents/{name}.md`)

**Purpose:** [Description]

**When to use:**
- [Triggers]

**Output:** [Location]
```

Add routing entries to the routing table.

#### Step 4: Commit

```bash
git add open-agents/agents/{name}.md
git add .claude/commands/{domain}/{command}.md
git add .gemini/commands/{domain}/{command}.md
git add open-agents/INSTRUCTIONS.md
git commit -m "Add {agent name} agent"
```

---

### Editing an Existing Agent

#### Step 1: Locate Files

Find both components:
- Definition: `open-agents/agents/{name}.md`
- Commands: `.claude/commands/{domain}/{command}.md` and `.gemini/commands/{domain}/{command}.md`

#### Step 2: Understand Current Behavior

Read the files. Understand:
- What the agent currently does
- What triggers it
- Where output goes

#### Step 3: Make Changes

Edit the agent file to modify behavior. Common changes:
- Adding new behaviors
- Changing output format
- Adjusting triggers
- Updating examples

#### Step 4: Update Routing (if needed)

If triggers changed, update `open-agents/INSTRUCTIONS.md`:
- Agent description in "Available Agents"
- Routing table entries

#### Step 5: Commit

```bash
git add -A
git commit -m "Update {agent name}: {what changed}"
```

---

### Removing an Agent

#### Step 1: Delete Files

```bash
rm open-agents/agents/{name}.md
rm .claude/commands/{domain}/{command}.md
rm .gemini/commands/{domain}/{command}.md
```

#### Step 2: Update INSTRUCTIONS.md

Remove:
- Entry from "Available Agents"
- Rows from routing table

#### Step 3: Commit

```bash
git add -A
git commit -m "Remove {agent name} agent"
```

---

### Redefining the System

To completely change the system's purpose:

#### Step 1: Plan the New Configuration

Decide:
- What agents are needed?
- What folder structure makes sense?
- What workflow should outputs follow?

#### Step 2: Update Folder Structure

Rename output folders to match the new domain:
```bash
mv open-agents/output-drafts open-agents/output-scripts
```

#### Step 3: Replace Agents

Either modify existing agents or delete and create new ones.

#### Step 4: Update All Documentation

- `open-agents/INSTRUCTIONS.md`: Complete rewrite
- `open-agents/README.md`: Update for new purpose
- Entry point files: Update the Open Agent section

#### Step 5: Clean Up

Remove old content from source and output folders.

---

## 8. Adding to an Existing Project

Open Agent Systems are designed to **augment** existing projects without disrupting them. This section explains how to add an agent system to a project that already has `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md` files.

### The Augmentation Approach

Instead of replacing existing entry point files, **append** a section that points to the Open Agent System:

```markdown
---

## Open Agents

This project includes an **Open Agent System** for [brief description of what the agents do].

**To use the agent system:** Read `open-agents/INSTRUCTIONS.md`

### Quick Reference

| Agent | Trigger | Output |
|-------|---------|--------|
| [Agent 1] | "[trigger phrase]" | `open-agents/output-*/` |
| [Agent 2] | "[trigger phrase]" | `open-agents/output-*/` |
```

### Step-by-Step Integration

#### Step 1: Create the open-agents/ folder

```bash
mkdir -p open-agents/{agents,tools,source,output-drafts,output-refined,output-final}
```

#### Step 2: Create open-agents/README.md

This provides human-readable context for anyone browsing the folder:

```markdown
# Open Agent System

This folder contains an **Open Agent System**—a structure of markdown files that transform AI coding assistants (Claude Code, Gemini CLI, Codex) into specialized agents.

## What Is This?

Instead of writing code, these agents:
- Manage files and content
- Perform research
- Transform documents between formats
- Execute domain-specific workflows

The agents are defined in markdown. No code required.

## Getting Started

Read `INSTRUCTIONS.md` for:
- Available agents and what they do
- How to invoke each agent
- Routing logic (which agent handles which requests)

## Folder Structure

- `agents/` — Agent definition files
- `tools/` — Scripts created by agents for repeatable operations
- `source/` — Input materials (your raw content goes here)
- `output-*/` — Processing stages (drafts → refined → final)
```

#### Step 3: Create open-agents/INSTRUCTIONS.md

Create the full instructions file following the template in [Section 6](#6-the-instructionsmd-file).

#### Step 4: Create agent files

Add agents to `open-agents/agents/` following the template in [Section 4](#4-agent-file-anatomy).

#### Step 5: Create slash commands

Add commands to `.claude/commands/{domain}/` and `.gemini/commands/{domain}/`.

#### Step 6: Create or update entry point files

Create these files if they don't exist, or add the directive to the top if they do:

**CLAUDE.md, AGENTS.md, GEMINI.md:**
```markdown
**CRITICAL: Read `open-agents/INSTRUCTIONS.md` immediately.**
```

That's the minimum requirement. Optionally add a quick reference table below for convenience.

### What NOT to Do

- **Don't replace** existing `CLAUDE.md` content—append to it
- **Don't put agent files** at project root—keep them in `open-agents/`
- **Don't modify** the project's existing folder structure
- **Don't add** numbered prefixes to existing project folders

### Verifying the Integration

After integration, confirm:

1. `open-agents/README.md` exists and is human-readable
2. `open-agents/INSTRUCTIONS.md` lists all agents
3. Entry point files (`CLAUDE.md`, etc.) have the Open Agents section
4. Slash commands exist in `.claude/commands/` and `.gemini/commands/`
5. Running `/your-domain command` invokes the correct agent

---

## 9. Complete Example

### History Research System

A working Open Agent System for researching historical topics, added to an existing project:

#### Folder Structure

```
my-existing-project/
├── src/                         # Existing project code
├── package.json                 # Existing project files
├── CLAUDE.md                    # Augmented with Open Agents section
├── AGENTS.md                    # Augmented with Open Agents section
├── GEMINI.md                    # Augmented with Open Agents section
│
├── .claude/commands/
│   └── history/
│       ├── research.md
│       ├── html.md
│       └── extract.md
│
├── .gemini/commands/
│   └── history/
│       └── (same structure)
│
└── open-agents/
    ├── README.md
    ├── INSTRUCTIONS.md
    │
    ├── agents/
    │   ├── researcher.md
    │   ├── html_generator.md
    │   └── data_extractor.md
    │
    ├── source/
    │   ├── disney_animation.md      # Stub file
    │   ├── video_games.md           # Stub file
    │   └── manga_origins.md         # Stub file
    │
    ├── output-articles/
    ├── output-html/
    └── output-data/
```

#### Entry Point File (CLAUDE.md)

```markdown
**CRITICAL: Read `open-agents/INSTRUCTIONS.md` immediately.**

[... any existing project instructions ...]

### Quick Reference

| Agent | Trigger | Output |
|-------|---------|--------|
| Researcher | "research [topic]" | `open-agents/output-articles/` |
| HTML Generator | "create HTML from [file]" | `open-agents/output-html/` |
| Data Extractor | "extract data from [file]" | `open-agents/output-data/` |

### Available Commands

- `/history research [topic]` — Research and create article
- `/history html [file]` — Generate HTML from article
- `/history extract [file]` — Extract structured JSON
```

#### open-agents/README.md

```markdown
# Open Agent System: History Research

This folder contains an Open Agent System for researching historical topics and transforming them into multiple output formats.

## Agents

- **Researcher** — Creates comprehensive markdown articles
- **HTML Generator** — Transforms articles into themed webpages
- **Data Extractor** — Extracts structured JSON from articles

## Getting Started

1. Add a stub file to `source/` with your topic
2. Ask the Researcher to expand it: "Research the history of [topic]"
3. Transform to HTML: "Create HTML from [filename]"
4. Extract data: "Extract data from [filename]"

Full documentation: `INSTRUCTIONS.md`
```

#### open-agents/INSTRUCTIONS.md

```markdown
# History Research System

An open agent system for researching historical topics.

---

## How This System Works

1. **Entry points** (CLAUDE.md/AGENTS.md/GEMINI.md) point here
2. **This file** is the index—it describes available agents
3. **Agent files** load on demand when triggered

---

## Available Agents

### 1. The Researcher (`agents/researcher.md`)

**Purpose:** Research historical topics and produce rich markdown articles.

**When to use:**
- User asks to "research" a topic
- User asks to "expand" an existing article
- User provides a stub file

**Output:** Markdown files in `open-agents/output-articles/`

### 2. The HTML Generator (`agents/html_generator.md`)

**Purpose:** Transform markdown articles into themed HTML pages.

**When to use:**
- User asks to "create HTML"
- User asks to "make a webpage"

**Output:** HTML files in `open-agents/output-html/`

### 3. The Data Extractor (`agents/data_extractor.md`)

**Purpose:** Extract structured JSON from articles.

**When to use:**
- User asks to "extract data"
- User asks to "create JSON"

**Output:** JSON files in `open-agents/output-data/`

---

## Routing Logic

| User says... | Agent |
|--------------|-------|
| "Research the history of X" | Researcher |
| "Expand this article" | Researcher |
| "Create HTML from this" | HTML Generator |
| "Extract data into JSON" | Data Extractor |
| "Create all outputs" | Researcher → HTML → Extractor |
```

#### Command File (.claude/commands/history/research.md)

```markdown
Research a historical topic and create a comprehensive markdown article.

Follow the instructions in `open-agents/agents/researcher.md`.

$ARGUMENTS
```

#### Stub File (open-agents/source/disney_animation.md)

```markdown
# The History of Disney Animation

> From a small studio in Los Angeles to the most influential animation
> company in the world.

<!-- Stub file. Ask the Researcher to expand this. -->
```

---

## Summary

An Open Agent System consists of:

1. **A container folder** (`open-agents/`) that isolates the system
2. **A README.md** for human-readable orientation
3. **An INSTRUCTIONS.md** that catalogs agents and routes requests
4. **Agent definitions** (`agents/*.md`) that define specialized behaviors
5. **Commands** (`.claude/commands/`, `.gemini/commands/`) for explicit invocation
6. **Structured folders** (`source/`, `output-*/`) for organized workflow
7. **Entry point files** (CLAUDE.md, AGENTS.md, GEMINI.md) with the read directive

**Critical:** Entry points must contain `**CRITICAL: Read `open-agents/INSTRUCTIONS.md` immediately.**` at the top. Create these files if they don't exist.

The pattern enables:
- **Tool agnosticism:** Works with Claude Code, Gemini CLI, Codex
- **Progressive disclosure:** Only loads what's needed
- **Domain flexibility:** Reconfigurable for any file-based workflow
- **Non-disruptive integration:** Adds to existing projects without conflict
- **Self-modification:** Can add, edit, and remove agents

To create a new system: `open-agents/` folder → README → INSTRUCTIONS → agents → commands → augment entry points with mandatory read directive.

To add to existing project: create `open-agents/`, add mandatory read directive to `CLAUDE.md`/`AGENTS.md`/`GEMINI.md`.

---

*This definition document describes the Open Agent System specification.*
