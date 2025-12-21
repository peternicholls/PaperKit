# PaperKit CLI Commands

Run the CLI commands in the terminal:

## Setup

Initialize PaperKit in your project directory. Creates the `.paperkit/` structure, agent definitions, and configuration files.

```bash
./paperkit init
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

## Version Management

Manage semantic versioning with optional prerelease tags and build metadata. Supports automatic bumping (major/minor/patch) and testing.

```bash
./paperkit version                     # show current version
./paperkit version --info              # show full JSON info
./paperkit version --set alpha-1.3.0   # set version
./paperkit version --bump patch        # bump patch (major|minor|patch)
./paperkit version --build 45          # add build metadata (+45)
./paperkit version --clear-build       # remove build metadata
./paperkit version --help              # show flags help
./paperkit version --test              # run version system tests
```

Test the version system:
```bash
PATH=".venv/bin:$PATH" ./.paperkit/tools/test-version-system.sh
```

## LaTeX

Compile academic papers, check LaTeX syntax, and preview PDF output. Build runs multiple passes for bibliography and cross-references.

```bash
./paperkit latex build
./paperkit latex lint
./paperkit latex open
```

## Evidence Extraction

Extract text evidence from PDF files based on search terms. Useful for forensic audits and citation verification.

```bash
./paperkit evidence extract <pdf_dir> <output_md> [terms...]
```