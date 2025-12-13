# Specification: Testing, CI, and Reproducibility

**Spec ID:** 005-testing-ci  
**Date:** 2024-12-13  
**Status:** Draft  
**Priority:** High  
**Category:** Quality Assurance

---

## Problem Statement

Build/lint scripts exist, but there are no CI/workflow definitions (e.g., GitHub Actions) to automatically test agent behaviors or LaTeX builds. This limits confidence in changes and makes reproducibility difficult.

### Current State

- Shell scripts exist: `build-latex.sh`, `lint-latex.sh`
- Python tools exist: `validate-structure.py`, `format-references.py`
- No GitHub Actions workflows
- No unit tests for transformation functions
- No end-to-end workflow tests
- No reproducible build environment (Dockerfile)
- No regression tests for prompts

### Impact

- Changes may break existing functionality undetected
- No confidence in pull request quality
- Difficult to reproduce builds across environments
- No validation that agents produce expected outputs
- Manual testing burden on maintainers

---

## Proposed Solution

### Overview

Implement comprehensive CI/CD pipeline with unit tests, end-to-end workflow tests, reproducible builds via Docker, and regression tests for agent outputs.

### Technical Requirements

#### 1. GitHub Actions Workflow Structure

```yaml
# .github/workflows/ci.yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    name: Lint and Validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
        
      - name: Lint Python
        run: |
          ruff check .
          mypy tools/
          
      - name: Lint Shell scripts
        run: shellcheck tools/*.sh
        
      - name: Lint YAML
        run: yamllint .paper/_cfg/
        
      - name: Validate manifests
        run: python tools/validate-manifests.py
        
      - name: Validate agent schemas
        run: python tools/validate-agent-schema.py
        
      - name: Validate workflow contracts
        run: python tools/validate-workflow-contracts.py

  unit-tests:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
        
      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=tools/ --cov-report=xml
        
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  e2e-tests:
    name: End-to-End Tests
    runs-on: ubuntu-latest
    needs: [lint, unit-tests]
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker image
        run: docker build -t paperkit:test -f docker/Dockerfile.test .
        
      - name: Run E2E tests
        run: |
          docker run --rm paperkit:test pytest tests/e2e/ -v

  latex-build:
    name: LaTeX Build Test
    runs-on: ubuntu-latest
    needs: [lint]
    container:
      image: texlive/texlive:latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Lint LaTeX
        run: ./tools/lint-latex.sh
        
      - name: Build LaTeX document
        run: ./tools/build-latex.sh
        
      - name: Validate PDF output
        run: |
          test -f output-final/pdf/main.pdf
          pdfinfo output-final/pdf/main.pdf
          
      - name: Upload PDF artifact
        uses: actions/upload-artifact@v3
        with:
          name: paper-pdf
          path: output-final/pdf/main.pdf

  regression-tests:
    name: Regression Tests
    runs-on: ubuntu-latest
    needs: [lint, unit-tests]
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
        
      - name: Run regression tests
        run: pytest tests/regression/ -v
        
      - name: Compare golden outputs
        run: python tools/compare-golden-outputs.py
```

#### 2. Unit Test Structure

```python
# tests/unit/test_validate_structure.py
import pytest
from tools.validate_structure import (
    validate_section_files,
    validate_metadata,
    check_completeness
)

class TestValidateStructure:
    def test_validates_existing_sections(self, sample_latex_dir):
        """Test that existing section files are detected."""
        result = validate_section_files(sample_latex_dir)
        assert result.is_valid
        assert len(result.found_sections) == 7
        
    def test_reports_missing_sections(self, sample_latex_dir_incomplete):
        """Test that missing sections are reported."""
        result = validate_section_files(sample_latex_dir_incomplete)
        assert not result.is_valid
        assert "03_methodology.tex" in result.missing
        
    def test_validates_metadata_fields(self, sample_metadata):
        """Test metadata validation."""
        result = validate_metadata(sample_metadata)
        assert result.is_valid
        assert result.has_title
        assert result.has_author
        
    def test_calculates_completeness(self, sample_section_status):
        """Test completeness percentage calculation."""
        result = check_completeness(sample_section_status)
        assert result.percentage == pytest.approx(71.4, rel=0.1)


# tests/unit/test_format_references.py
import pytest
from tools.format_references import (
    parse_bibtex,
    validate_harvard_format,
    check_required_fields
)

class TestFormatReferences:
    def test_parses_valid_bibtex(self, sample_bib_content):
        """Test BibTeX parsing."""
        entries = parse_bibtex(sample_bib_content)
        assert len(entries) == 5
        assert entries[0].entry_type == "article"
        
    def test_detects_missing_fields(self, sample_bib_incomplete):
        """Test detection of missing required fields."""
        issues = check_required_fields(sample_bib_incomplete)
        assert len(issues) > 0
        assert any("author" in issue.field for issue in issues)
```

#### 3. End-to-End Test Structure

```python
# tests/e2e/test_workflow_consolidate_to_build.py
import pytest
import subprocess
from pathlib import Path

class TestConsolidateToBuildWorkflow:
    """
    Test the complete workflow from research consolidation to PDF build.
    """
    
    @pytest.fixture
    def test_workspace(self, tmp_path):
        """Create isolated test workspace."""
        workspace = tmp_path / "paperkit-test"
        workspace.mkdir()
        # Copy template files
        return workspace
    
    def test_consolidate_research(self, test_workspace, sample_research_notes):
        """Test research consolidation produces expected output."""
        # Arrange
        (test_workspace / "source/research-notes").mkdir(parents=True)
        for note in sample_research_notes:
            (test_workspace / f"source/research-notes/{note.name}").write_text(note.content)
        
        # Act - simulate agent behavior
        result = run_consolidation_workflow(test_workspace)
        
        # Assert
        assert result.success
        assert (test_workspace / "output-refined/research/consolidated.md").exists()
        
    def test_outline_creation(self, test_workspace, consolidated_research):
        """Test outline creation from research."""
        # Act
        result = run_outline_workflow(test_workspace, consolidated_research)
        
        # Assert
        assert result.success
        assert (test_workspace / "output-drafts/outlines/paper-outline.md").exists()
        outline = (test_workspace / "output-drafts/outlines/paper-outline.md").read_text()
        assert "Introduction" in outline
        assert "Methodology" in outline
        
    def test_section_drafting(self, test_workspace, outline):
        """Test section drafting produces valid LaTeX."""
        # Act
        result = run_draft_workflow(test_workspace, "introduction", outline)
        
        # Assert
        assert result.success
        draft_path = test_workspace / "output-drafts/sections/01_introduction.tex"
        assert draft_path.exists()
        content = draft_path.read_text()
        assert "\\section{Introduction}" in content
        
    def test_full_build(self, test_workspace, complete_sections):
        """Test full LaTeX build produces PDF."""
        # Arrange - set up all sections
        for section in complete_sections:
            (test_workspace / f"latex/sections/{section.name}").write_text(section.content)
        
        # Act
        result = subprocess.run(
            ["./tools/build-latex.sh"],
            cwd=test_workspace,
            capture_output=True
        )
        
        # Assert
        assert result.returncode == 0
        assert (test_workspace / "output-final/pdf/main.pdf").exists()
```

#### 4. Regression Test Structure

```python
# tests/regression/test_golden_outputs.py
import pytest
from pathlib import Path
import hashlib
import difflib

class TestGoldenOutputs:
    """
    Compare agent outputs against known-good golden examples.
    """
    
    GOLDEN_DIR = Path("tests/golden")
    
    def test_consolidation_output_format(self):
        """Test research consolidation produces expected format."""
        input_file = self.GOLDEN_DIR / "inputs/research-notes-sample.md"
        expected_file = self.GOLDEN_DIR / "outputs/consolidated-sample.md"
        
        # Run consolidation
        actual_output = run_consolidation(input_file.read_text())
        
        # Compare structure (not exact content due to LLM variance)
        assert_similar_structure(actual_output, expected_file.read_text())
        
    def test_outline_contains_required_sections(self):
        """Test outlines contain all required academic sections."""
        input_file = self.GOLDEN_DIR / "inputs/paper-scope-sample.yaml"
        
        outline = run_outline_generation(input_file.read_text())
        
        required_sections = [
            "Introduction",
            "Background",
            "Methodology",
            "Results",
            "Discussion",
            "Conclusion"
        ]
        for section in required_sections:
            assert section.lower() in outline.lower(), f"Missing section: {section}"
            
    def test_latex_output_compiles(self):
        """Test that generated LaTeX compiles without errors."""
        golden_latex = self.GOLDEN_DIR / "outputs/sample-section.tex"
        
        # Compile in isolated environment
        result = compile_latex(golden_latex.read_text())
        
        assert result.success
        assert result.errors == []
```

#### 5. Docker Build Environment

```dockerfile
# docker/Dockerfile
FROM texlive/texlive:latest as latex-base

# Install Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    shellcheck \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /paperkit

# Copy requirements first for caching
COPY requirements.txt requirements-dev.txt ./
RUN pip3 install --no-cache-dir -r requirements-dev.txt

# Copy application
COPY . .

# Set up paths
ENV PATH="/paperkit/tools:${PATH}"
ENV PYTHONPATH="/paperkit:${PYTHONPATH}"

# Default command
CMD ["bash"]

---
# docker/Dockerfile.test
FROM texlive/texlive:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /paperkit

COPY requirements.txt requirements-dev.txt ./
RUN pip3 install --no-cache-dir -r requirements-dev.txt

COPY . .

# Run tests by default
CMD ["pytest", "tests/", "-v"]
```

#### 6. Test Fixtures and Helpers

```python
# tests/conftest.py
import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def sample_latex_dir(tmp_path):
    """Create sample LaTeX directory structure."""
    latex_dir = tmp_path / "latex"
    latex_dir.mkdir()
    
    sections = [
        "01_introduction.tex",
        "02_background.tex",
        "03_methodology.tex",
        "04_results.tex",
        "05_prior_work.tex",
        "06_implications.tex",
        "07_conclusion.tex"
    ]
    
    sections_dir = latex_dir / "sections"
    sections_dir.mkdir()
    
    for section in sections:
        (sections_dir / section).write_text(f"% {section}\n\\section{{{section}}}\nContent here.")
    
    return latex_dir

@pytest.fixture
def sample_bib_content():
    """Sample BibTeX content."""
    return """
    @article{smith2024example,
        author = {Smith, John and Doe, Jane},
        title = {An Example Paper},
        journal = {Example Journal},
        year = {2024},
        volume = {1},
        pages = {1--10}
    }
    
    @book{jones2023book,
        author = {Jones, Alice},
        title = {Example Book},
        publisher = {Example Press},
        year = {2023}
    }
    """

@pytest.fixture
def golden_test_dir():
    """Path to golden test files."""
    return Path(__file__).parent / "golden"
```

---

## Implementation Steps

| Step | Description | Estimated Effort |
|------|-------------|------------------|
| 1 | Set up pytest infrastructure | 2 hours |
| 2 | Create unit tests for existing tools | 8 hours |
| 3 | Create E2E test framework | 6 hours |
| 4 | Write E2E workflow tests | 8 hours |
| 5 | Create golden output fixtures | 4 hours |
| 6 | Write regression tests | 6 hours |
| 7 | Create Dockerfile | 4 hours |
| 8 | Set up GitHub Actions workflows | 6 hours |
| 9 | Add code coverage reporting | 2 hours |
| 10 | Documentation | 2 hours |

**Total Estimated Effort:** 48 hours

---

## Success Criteria

- [ ] CI runs on every PR and push to main
- [ ] Unit tests cover >80% of tool code
- [ ] E2E tests validate complete workflows
- [ ] LaTeX builds successfully in CI
- [ ] Docker image produces reproducible builds
- [ ] Regression tests detect prompt output drift
- [ ] All tests pass before merge

---

## Dependencies

- [001-agent-metadata.md](001-agent-metadata.md) - Schema validation tests depend on schema
- [002-workflow-agent-contract.md](002-workflow-agent-contract.md) - Contract validation in CI

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Flaky E2E tests | Medium | Isolate tests; use deterministic fixtures |
| LLM output variance breaks regression | High | Test structure not content; fuzzy matching |
| Slow CI pipeline | Medium | Parallelize jobs; cache dependencies |
| Docker image size | Low | Multi-stage builds; slim base images |

---

## Related Specifications

- [006-observability.md](006-observability.md) - Test observability
- [010-agent-governance.md](010-agent-governance.md) - Versioned testing

---

## Open Questions

1. How to handle LLM output variance in regression tests?
2. Should E2E tests use real LLM or mock responses?
3. What's acceptable CI pipeline duration target?
4. Should we test on multiple Python versions?

---

## References

- GitHub Actions: https://docs.github.com/en/actions
- pytest: https://docs.pytest.org/
- TeXLive Docker: https://hub.docker.com/r/texlive/texlive
