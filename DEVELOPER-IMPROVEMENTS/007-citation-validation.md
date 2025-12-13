# Specification: Citation, Reference, and Data Validation

**Spec ID:** 007-citation-validation  
**Date:** 2024-12-13  
**Status:** Draft  
**Priority:** Medium  
**Category:** Academic Quality

---

## Problem Statement

There is a workflow to "validate citations" and a reference-manager agent, but stronger automation is needed for academic correctness. Manual validation of citations is error-prone and time-consuming.

### Current State

- Reference Manager agent handles citation formatting
- `format-references.py` validates BibTeX format
- No automatic DOI validation
- No CrossRef/Unpaywall/ORCID integration
- No automatic BibTeX fetching
- Limited in-text citation consistency checking
- Only Harvard style supported

### Impact

- Invalid or incomplete citations may reach final document
- Manual effort required to verify sources
- Missing metadata in bibliography entries
- Inconsistent citation formatting
- Difficult to update citations when sources change

---

## Proposed Solution

### Overview

Implement comprehensive citation validation and enrichment system with external API integration, automatic metadata fetching, consistency checking, and multi-style support.

### Technical Requirements

#### 1. Citation Validation Pipeline

```yaml
# .paper/_cfg/citation/validation-pipeline.yaml
citationValidation:
  version: "1.0.0"
  
  pipeline:
    - stage: parse
      description: "Parse BibTeX entries"
      tool: "bibtexparser"
      
    - stage: validate_format
      description: "Check BibTeX syntax and required fields"
      rules:
        article:
          required: [author, title, journal, year]
          optional: [volume, number, pages, doi, url]
        book:
          required: [author, title, publisher, year]
          optional: [edition, isbn, doi]
        inproceedings:
          required: [author, title, booktitle, year]
          optional: [pages, doi, url]
          
    - stage: validate_doi
      description: "Verify DOIs against CrossRef"
      enabled: true
      service: "crossref"
      timeout: 5s
      
    - stage: enrich_metadata
      description: "Fetch missing metadata from external sources"
      enabled: true
      sources:
        - service: "crossref"
          priority: 1
        - service: "semantic_scholar"
          priority: 2
        - service: "unpaywall"
          priority: 3
          
    - stage: validate_orcid
      description: "Validate ORCID identifiers"
      enabled: false
      
    - stage: check_consistency
      description: "Check citation consistency across document"
      checks:
        - cited_but_not_in_bib
        - in_bib_but_not_cited
        - duplicate_entries
        - inconsistent_author_names
        
    - stage: format_output
      description: "Format to target citation style"
      style: "harvard"
```

#### 2. External API Integration

```python
# tools/citation/external_apis.py
from dataclasses import dataclass
from typing import Optional, List
import httpx

@dataclass
class CitationMetadata:
    title: str
    authors: List[str]
    year: int
    journal: Optional[str] = None
    volume: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    abstract: Optional[str] = None
    
class CrossRefClient:
    """Client for CrossRef API."""
    
    BASE_URL = "https://api.crossref.org"
    
    def __init__(self, mailto: Optional[str] = None):
        self.mailto = mailto  # Polite pool access
        
    async def lookup_doi(self, doi: str) -> Optional[CitationMetadata]:
        """Lookup citation metadata by DOI."""
        url = f"{self.BASE_URL}/works/{doi}"
        headers = {}
        if self.mailto:
            headers["mailto"] = self.mailto
            
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                return self._parse_response(response.json())
        return None
        
    async def search(self, query: str, limit: int = 5) -> List[CitationMetadata]:
        """Search for citations by title/author."""
        pass
        
    def _parse_response(self, data: dict) -> CitationMetadata:
        """Parse CrossRef response to CitationMetadata."""
        pass

class SemanticScholarClient:
    """Client for Semantic Scholar API."""
    
    BASE_URL = "https://api.semanticscholar.org/v1"
    
    async def lookup_paper(self, paper_id: str) -> Optional[CitationMetadata]:
        """Lookup paper by Semantic Scholar ID or DOI."""
        pass
        
    async def search(self, query: str) -> List[CitationMetadata]:
        """Search for papers."""
        pass

class UnpaywallClient:
    """Client for Unpaywall API (open access detection)."""
    
    BASE_URL = "https://api.unpaywall.org/v2"
    
    async def get_open_access_url(self, doi: str) -> Optional[str]:
        """Get open access URL for DOI if available."""
        pass

class ORCIDClient:
    """Client for ORCID API."""
    
    BASE_URL = "https://pub.orcid.org/v3.0"
    
    async def validate_orcid(self, orcid: str) -> bool:
        """Validate ORCID identifier exists."""
        pass
        
    async def get_works(self, orcid: str) -> List[CitationMetadata]:
        """Get works for ORCID."""
        pass
```

#### 3. BibTeX Auto-Fetching

```yaml
# Configuration for automatic BibTeX fetching
autoFetch:
  enabled: true
  
  triggers:
    - event: "doi_detected"
      action: "fetch_and_suggest"
    - event: "citation_added"
      action: "validate_and_enrich"
      
  sources:
    doi:
      service: "crossref"
      format: "bibtex"
      autoUpdate: true
      
    arxiv:
      service: "arxiv"
      format: "bibtex"
      pattern: "arxiv:\\d+\\.\\d+"
      
    isbn:
      service: "openlibrary"
      format: "bibtex"
      
  output:
    suggestionFile: "latex/references/suggested.bib"
    mergeStrategy: "manual_review"
```

```python
# tools/citation/auto_fetch.py
class BibTeXAutoFetcher:
    """Automatically fetch and update BibTeX entries."""
    
    def __init__(self, config: dict):
        self.crossref = CrossRefClient()
        self.config = config
        
    async def fetch_by_doi(self, doi: str) -> str:
        """Fetch BibTeX entry for DOI."""
        metadata = await self.crossref.lookup_doi(doi)
        if metadata:
            return self._to_bibtex(metadata)
        raise ValueError(f"DOI not found: {doi}")
        
    async def update_entry(self, entry: BibTeXEntry) -> BibTeXEntry:
        """Update entry with latest metadata from external source."""
        if entry.doi:
            latest = await self.crossref.lookup_doi(entry.doi)
            return self._merge_entry(entry, latest)
        return entry
        
    async def batch_validate(self, bib_file: str) -> ValidationReport:
        """Validate all entries in BibTeX file."""
        entries = parse_bibtex(bib_file)
        results = []
        for entry in entries:
            result = await self._validate_entry(entry)
            results.append(result)
        return ValidationReport(results)
```

#### 4. In-Text Citation Consistency Checker

```python
# tools/citation/consistency_checker.py
import re
from pathlib import Path
from typing import List, Set, Tuple

class CitationConsistencyChecker:
    """Check consistency between in-text citations and bibliography."""
    
    # LaTeX citation commands
    CITE_PATTERNS = [
        r"\\cite\{([^}]+)\}",
        r"\\citep\{([^}]+)\}",
        r"\\citet\{([^}]+)\}",
        r"\\citealp\{([^}]+)\}",
        r"\\citeauthor\{([^}]+)\}",
        r"\\citeyear\{([^}]+)\}",
    ]
    
    def extract_citations(self, tex_content: str) -> Set[str]:
        """Extract all citation keys from LaTeX content."""
        citations = set()
        for pattern in self.CITE_PATTERNS:
            matches = re.findall(pattern, tex_content)
            for match in matches:
                # Handle multiple citations in single command
                keys = [k.strip() for k in match.split(",")]
                citations.update(keys)
        return citations
        
    def extract_bib_keys(self, bib_content: str) -> Set[str]:
        """Extract all keys from BibTeX file."""
        pattern = r"@\w+\{([^,]+),"
        return set(re.findall(pattern, bib_content))
        
    def check_consistency(
        self, 
        tex_files: List[Path], 
        bib_file: Path
    ) -> ConsistencyReport:
        """Check citation consistency across document."""
        
        # Collect all citations from tex files
        all_citations = set()
        for tex_file in tex_files:
            content = tex_file.read_text()
            all_citations.update(self.extract_citations(content))
            
        # Get bibliography keys
        bib_keys = self.extract_bib_keys(bib_file.read_text())
        
        # Find inconsistencies
        cited_not_in_bib = all_citations - bib_keys
        in_bib_not_cited = bib_keys - all_citations
        
        return ConsistencyReport(
            cited_not_in_bib=cited_not_in_bib,
            in_bib_not_cited=in_bib_not_cited,
            valid_citations=all_citations & bib_keys
        )
```

#### 5. Multi-Style Support

```yaml
# .paper/_cfg/citation/styles.yaml
citationStyles:
  available:
    - name: "harvard"
      description: "Harvard Referencing Style"
      package: "natbib"
      style: "agsm"
      default: true
      
    - name: "apa"
      description: "APA 7th Edition"
      package: "biblatex"
      style: "apa"
      options: ["backend=biber"]
      
    - name: "ieee"
      description: "IEEE Citation Style"
      package: "biblatex"
      style: "ieee"
      options: ["backend=biber"]
      
    - name: "chicago"
      description: "Chicago Manual of Style"
      package: "biblatex"
      style: "chicago-authordate"
      
    - name: "vancouver"
      description: "Vancouver (Medical)"
      package: "natbib"
      style: "vancouver"
      
  conversion:
    enabled: true
    preserveKeys: true
    logChanges: true
```

```python
# tools/citation/style_converter.py
class CitationStyleConverter:
    """Convert between citation styles."""
    
    def convert(
        self, 
        bib_content: str, 
        from_style: str, 
        to_style: str
    ) -> str:
        """Convert BibTeX entries between styles."""
        pass
        
    def update_latex_preamble(
        self, 
        tex_content: str, 
        target_style: str
    ) -> str:
        """Update LaTeX preamble for new citation style."""
        pass
```

#### 6. Validation Report Format

```yaml
# Citation validation report schema
validationReport:
  timestamp: "2024-12-13T10:00:00Z"
  bibFile: "latex/references/references.bib"
  texFiles:
    - "latex/sections/01_introduction.tex"
    - "latex/sections/02_background.tex"
    
  summary:
    totalEntries: 25
    validEntries: 22
    entriesWithIssues: 3
    citedInDocument: 20
    uncitedEntries: 5
    missingFromBib: 2
    
  issues:
    critical:
      - key: "smith2024"
        type: "cited_but_missing"
        location: "01_introduction.tex:45"
        message: "Citation key 'smith2024' used but not in bibliography"
        
    warnings:
      - key: "jones2023book"
        type: "missing_doi"
        message: "Entry missing DOI - consider adding for verification"
        
      - key: "doe2022article"
        type: "incomplete_metadata"
        missingFields: ["pages", "volume"]
        
    info:
      - key: "brown2021"
        type: "uncited"
        message: "Entry in bibliography but not cited in document"
        
  enrichment:
    updated:
      - key: "williams2023"
        fields: ["doi", "url"]
        source: "crossref"
        
    suggested:
      - key: "new_citation"
        bibtex: "@article{new_citation, ...}"
        source: "detected DOI in text"
        
  doiValidation:
    validated: 18
    valid: 17
    invalid: 1
    notFound:
      - key: "invalid_doi_entry"
        doi: "10.xxxx/invalid"
```

---

## Implementation Steps

| Step | Description | Estimated Effort |
|------|-------------|------------------|
| 1 | Define validation pipeline schema | 4 hours |
| 2 | Implement CrossRef client | 6 hours |
| 3 | Implement Semantic Scholar client | 4 hours |
| 4 | Implement Unpaywall client | 2 hours |
| 5 | Build BibTeX auto-fetcher | 6 hours |
| 6 | Implement consistency checker | 4 hours |
| 7 | Add multi-style support | 6 hours |
| 8 | Build validation report generator | 4 hours |
| 9 | Integration with Reference Manager agent | 4 hours |
| 10 | Testing and documentation | 4 hours |

**Total Estimated Effort:** 44 hours

---

## Success Criteria

- [ ] DOI validation against CrossRef API working
- [ ] Automatic BibTeX fetching for DOIs
- [ ] In-text citation consistency checking
- [ ] Missing citation detection
- [ ] Multiple citation styles supported
- [ ] Validation report generated with actionable items
- [ ] Integration with existing Reference Manager workflow

---

## Dependencies

- [004-security-governance.md](004-security-governance.md) - API access trust model
- [005-testing-ci.md](005-testing-ci.md) - Citation validation in CI

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| API rate limits | Medium | Caching; respect rate limits; batch requests |
| External API unavailability | Medium | Graceful degradation; offline mode |
| False positives in validation | Low | Configurable strictness; manual override |
| DOI not found for valid sources | Medium | Multiple lookup sources; manual entry option |

---

## Related Specifications

- [004-security-governance.md](004-security-governance.md) - External API trust
- [005-testing-ci.md](005-testing-ci.md) - Automated validation in CI

---

## Open Questions

1. Should DOI validation be mandatory or optional?
2. How to handle sources without DOIs (books, websites)?
3. Should we support automatic bibliography generation from PDFs?
4. What's the appropriate caching strategy for API responses?

---

## References

- CrossRef API: https://api.crossref.org/swagger-ui/index.html
- Semantic Scholar API: https://api.semanticscholar.org/
- Unpaywall API: https://unpaywall.org/products/api
- ORCID API: https://info.orcid.org/documentation/api-tutorials/
