# PaperKit Tools

This directory contains the **canonical tool implementations** for PaperKit.

## Available Tools

| Tool | Description | Usage |
|------|-------------|-------|
| `build-latex.sh` | Compile LaTeX document with BibTeX handling | `./build-latex.sh [--clean] [--final]` |
| `lint-latex.sh` | Validate LaTeX syntax before compilation | `./lint-latex.sh` |
| `extract-evidence.sh` | Batch PDF evidence extraction with context | `./extract-evidence.sh <pdf_dir> <output_md> [terms...]` |
| `format-references.py` | Validate BibTeX bibliography files | `python3 format-references.py --validate <file.bib>` |
| `validate-structure.py` | Validate paper structure and section files | `python3 validate-structure.py` |
| `check-dependencies.sh` | Verify all required dependencies | `./check-dependencies.sh` |

## Tool Definitions

Tool metadata is defined in YAML files at `.paper/_cfg/tools/`:

```
.paper/_cfg/tools/
├── build-latex.yaml
├── extract-evidence.yaml
├── format-references.yaml
├── lint-latex.yaml
└── validate-structure.yaml
```

## Dependencies

Python tools require packages listed in `requirements.txt`:

```bash
pip install -r .paperkit/tools/requirements.txt
```

System dependencies:
- **pdflatex** — LaTeX compilation
- **bibtex** — Bibliography generation
- **pdftotext** — PDF text extraction (from poppler-utils)
- **Python 3.7+** — Script execution

Run `./check-dependencies.sh` to verify your environment.

## Running from Project Root

All tools are designed to run from the project root:

```bash
# From project root
./.paperkit/tools/build-latex.sh
./.paperkit/tools/lint-latex.sh

# Or add to PATH
export PATH="$PATH:$(pwd)/.paper/tools"
```

## Legacy Location

The tools were previously located at `open-agents/tools/`. That directory now contains a deprecation notice pointing here.

---

*Part of PaperKit - `.paper/` is the source of truth*
