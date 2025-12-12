# Open Agent System

An experiment in repurposing AI coding assistants as general-purpose agent hosts.

---

> **For AI Agents:**
>
> The file you're looking for is [`OpenAgentDefinition.md`](./OpenAgentDefinition.md).
> Read that document to understand and implement this system.

---

## What Is This?

This project explores a simple observation: tools like **Claude Code**, **Gemini CLI**, and **Codex** aren't really "coding assistants." They're general-purpose agent frameworks that happen to be configured for coding by default.

Their core capabilities -- reading files, writing files, following instructions, using tools, managing context -- work for *any* file-based workflow. So what if we redirected them?

An **Open Agent System** is a folder structure and set of markdown files that reconfigures these tools to perform specialized, non-coding tasks. No code required. The AI reads your instructions and becomes that agent.

## The Idea

Instead of building custom agent infrastructure (APIs, deployments, UIs, databases), you define agent behavior in markdown files and run them in existing agentic environments.

```
+-------------------------------------+
|  Claude Code / Gemini CLI / Codex   |  <-- Existing tools with strong agentic loops
|  (Your "agent host")                |
+------------------+------------------+
                   |
                   v
+-------------------------------------+
|  open-agents/INSTRUCTIONS.md        |  <-- Your agent definitions in markdown
|  open-agents/agents/*.md            |
+-------------------------------------+
                   |
                   v
+-------------------------------------+
|  Research, transform, publish...    |  <-- The agents do real work
|  (Whatever you define)              |
+-------------------------------------+
```

The same system works across different tools because they all understand the same pattern: read instructions, follow them, produce outputs.

## What's Interesting About This

**No code required.** Agent behavior is defined entirely in markdown. You describe what the agent should do, when it should activate, and where outputs go.

**Tool agnostic.** Write once, run in Claude Code, Gemini CLI, or Codex. The pointer files (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) all reference the same instructions.

**Progressive disclosure.** Only the agent catalog loads at start. Full agent definitions load on-demand, keeping context small.

**Self-modifying.** Agents can add, edit, or remove other agents. The system can evolve itself.

**Embeddable.** Drop the `open-agents/` folder into any existing project without disrupting its structure.

## What This Is Not

This is **not** a production-ready framework or a definitive solution to building agents. It's an exploration of a pattern -- using the agentic loops already built into popular tools as hosts for custom agents.

Think of it as a proof of concept for a different way of thinking about agent development: instead of building agent infrastructure, borrow it from tools that already have it.

## Getting Started

1. Read [`OpenAgentDefinition.md`](./OpenAgentDefinition.md) for the complete specification
2. Create an `open-agents/` folder in your project
3. Define your agents in markdown
4. Point your tool's instruction file to `open-agents/INSTRUCTIONS.md`

The definition document includes complete examples, folder structure templates, and step-by-step guides.

## Example Use Cases

- **Research systems** -- Agents that research topics, produce articles, transform to HTML
- **Content pipelines** -- Ingest raw notes, process through multiple stages, output polished content
- **Data processing** -- Extract, transform, validate data across file formats
- **Media workflows** -- Organize, process, and publish audio/video projects

If it involves files and can be described in natural language, it can probably be an Open Agent.

## License

MIT License. See [LICENSE](./LICENSE) for details.

---

*This is an experiment. Fork it, break it, improve it.*
