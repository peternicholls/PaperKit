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