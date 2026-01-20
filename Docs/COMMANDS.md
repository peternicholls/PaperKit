# PaperKit CLI Commands

Run the CLI commands in the terminal:

## Initialization

Initialize a new PaperKit paper project. Sets up directory structure, LaTeX templates, and configuration.

```bash
./paperkit init                        # Initialize new paper project
./paperkit init --help                 # Show initialization options
```

## Get Help

Display available commands, options, and examples.

```bash
./paperkit help
```

## Generate IDE Files

Generate IDE-specific agent files (GitHub Copilot, OpenAI Codex) from the canonical `.paperkit/` definitions. Use `--check` to verify if regeneration is needed.

```bash
./paperkit generate
./paperkit generate --target=copilot
./paperkit generate --target=codex
./paperkit generate --target=all
./paperkit generate --check
```

## Validate

Validate agent definitions, workflow schemas, and tool configurations. Checks YAML structure, required fields, and manifest consistency.

```bash
./paperkit validate
```

## Version Information

View current version and detailed version metadata. Version management commands (modify/bump) require `paperkit-dev`.

```bash
./paperkit version                     # Show current version
./paperkit version --info              # Show full version info (JSON)
./paperkit version --help              # Show version help
```

For version modification commands, see [Developer Commands](developer-commands.md).

## LaTeX

Compile academic papers, check LaTeX syntax, and preview PDF output. Build runs multiple passes for bibliography and cross-references.

```bash
./paperkit latex build                  # Compile PDF (3-pass with BibTeX)
./paperkit latex lint                   # Check LaTeX syntax
./paperkit latex open                   # Open compiled PDF
```

For a comprehensive guide on how the LaTeX document is assembled from modular components, see [LATEX-ASSEMBLY.md](LATEX-ASSEMBLY.md).

## Evidence Extraction

Extract text evidence from PDF files based on search terms. Useful for forensic audits and citation verification.

```bash
./paperkit evidence --dir <pdf_dir> --output <output_md> [--terms "term1" "term2" ...]
./paperkit evidence --help             # Show evidence extraction help
```

## Agent Skills & Workflows

PaperKit uses a dual architecture: **Agent Skills** (SKILL.md instructions) and **Compositional Workflows** (YAML orchestration). See [docs/dev/SKILLS.md](dev/SKILLS.md) for details.

### Agent Skills (SKILL.md)

Agent Skills teach agents HOW to perform tasks. They follow the [agentskills.io](https://agentskills.io) specification.

```bash
# List all Agent Skills
python .paperkit/tools/skill_registry.py skills --list

# Search for skills
python .paperkit/tools/skill_registry.py skills --find "citation"

# Get skill metadata
python .paperkit/tools/skill_registry.py skills --get harvard-citations

# View full skill content
python .paperkit/tools/skill_registry.py skills --content humanizer

# Benchmark skill registry load time (target: <50ms)
python .paperkit/tools/skill_registry.py skills --benchmark

# Validate all SKILL.md files
python .paperkit/tools/validate-skill-frontmatter.py --all
python .paperkit/tools/validate-skill-frontmatter.py --all --ci    # CI mode
```

### Compositional Workflows (YAML)

Workflows define WHAT steps to execute and orchestrate multiple agents.

```bash
# List all workflows
python .paperkit/tools/skill_registry.py workflows --list

# Search for workflows
python .paperkit/tools/skill_registry.py workflows --find "citation"

# Get workflow details
python .paperkit/tools/skill_registry.py workflows --get cite-source

# View statistics
python .paperkit/tools/skill_registry.py workflows --stats
```

### Available Skills

| Skill | Description |
|-------|-------------|
| `humanizer` | Remove AI writing patterns from text |
| `academic-writing` | Academic paper composition guidelines |
| `harvard-citations` | Harvard citation style (Cite Them Right) |
| `latex-best-practices` | LaTeX document best practices |

### Available Workflows

| Workflow | Description |
|----------|-------------|
| `cite-source` | Extract metadata and format citation |
| `validate-citation` | Validate citation format and verify source |
| `draft-section` | Draft paper section with outline |
| `research-topic` | Research and consolidate findings |
| `compile-latex` | Compile LaTeX to PDF |