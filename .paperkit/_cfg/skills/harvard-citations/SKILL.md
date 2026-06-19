---
name: harvard-citations
description: Format academic citations in Harvard style (Cite Them Right). Use when creating bibliographies, citing sources, formatting references, or validating citation completeness. Ensures proper author-date format, reference list structure, and BibTeX compatibility.
metadata:
  author: core-team
  version: "1.0.0"
  category: referencing
---

# Harvard Citations: Cite Them Right Style Guide

You are a citation specialist ensuring all references follow Harvard style (Cite Them Right, 11th Edition). This skill provides guidance on in-text citations, reference lists, and BibTeX formatting.

## When to Use

Use this skill when:
- Formatting in-text citations
- Creating or updating reference lists
- Converting citations to BibTeX format
- Validating citation completeness
- Checking citation consistency throughout a document

## Academic Integrity

**CRITICAL:** Every citation requires:
1. The quote text (if directly quoting)
2. Page number(s) for direct quotes
3. Full citation for both in-text use AND bibliography
4. Never fabricate or guess citations - flag uncertainties

## Core Format

### In-Text Citations

**Single author:**
```
(Smith, 2020)
Smith (2020) argues that...
```

**Two authors:**
```
(Jones and Brown, 2019)
```

**Three authors:**
```
(Wilson, Davis and Lee, 2021)
```

**Four or more authors:**
```
(Chen et al., 2022)
```

### Direct Quotes

**Short quotes (under 40 words):**
```
Research shows that "climate change is accelerating" (Green, 2023, p. 45).
```

**Long quotes (40+ words):**
Use indented block format, no quotation marks, include page number.

### Page Numbers

- Single page: `(Baker, 2020, p. 67)`
- Multiple pages: `(Taylor, 2019, pp. 23-27)`

### Multiple Sources

List alphabetically by surname:
```
(Brown, 2018; Jones, 2022; Smith, 2020)
```

## Reference List Format

### Books

**Single author:**
```
Smith, J. (2020) Understanding climate change. 3rd edn. London: Academic Press.
```

**Multiple authors (2-3):**
```
Jones, P., Brown, R. and Wilson, S. (2019) Research methods. Oxford: Oxford University Press.
```

**Four or more authors:**
```
Chen, L. et al. (2021) Advanced statistics. New York: McGraw-Hill.
```

**Chapter in edited book:**
```
Tan, J. (2012) 'Chapter title', in Jones, P. (ed.) Book title. Bristol: Policy Press, pp. 123-145.
```

### Journal Articles

**Print journal:**
```
Kirwan, B. and Leather, C. (2011) 'Article title', Journal Title, 29(1), pp. 33-41.
```

**Online journal with DOI:**
```
Hamer, E.M. (1996) 'Article title', Journal, 12(2), pp. 100-110. Available at: https://doi.org/10.1016/example.
```

**Online journal without DOI:**
```
Thompson, R. (2022) 'Article title', Business Review, 45(3), pp. 78-92. Available at: URL (Accessed: 10 January 2023).
```

### Websites

**Organization:**
```
World Health Organization (2023) Climate change and health. Available at: URL (Accessed: 5 April 2023).
```

**With author:**
```
Roberts, K. (2021) Understanding ML. Available at: URL (Accessed: 20 June 2023).
```

**No date:**
```
Title (n.d.) Available at: URL (Accessed: Date).
```

## BibTeX Format

### Entry Types

| Type | Use Case |
|------|----------|
| `@article` | Journal articles |
| `@book` | Books |
| `@incollection` | Chapter in edited book |
| `@inproceedings` | Conference papers |
| `@techreport` | Technical reports |
| `@phdthesis` | Dissertations |
| `@misc` | Websites, other |

### Citation Key Convention

Use format: `AuthorSurname_Year` or `AuthorSurname_Year_Keyword`

### Examples

```bibtex
@article{Hunt_2005,
  author = {Hunt, R. W. G.},
  title = {The fundamentals of color vision},
  journal = {Color Research \& Application},
  year = {2005},
  volume = {30},
  number = {3},
  pages = {171--179},
  doi = {10.1002/col.20120}
}

@book{Fairchild_2013,
  author = {Fairchild, Mark D.},
  title = {Color appearance models},
  edition = {3rd},
  publisher = {Wiley},
  address = {Chichester},
  year = {2013}
}

@misc{WHO_2023,
  author = {{World Health Organization}},
  title = {Climate change and health},
  year = {2023},
  url = {https://www.who.int/climate-health},
  note = {Accessed: 5 April 2023}
}
```

### Protecting Capitalization

Use braces for proper nouns and acronyms:
```bibtex
title = {Understanding {COVID-19} impacts on {European} economies}
```

## Common Errors

### Wrong

- `[2020]` - Use round brackets: `(2020)`
- `"quote" (Author, 2020)` - Missing page: `(Author, 2020, p. 45)`
- `Understanding Climate Change` - Use sentence case: `Understanding climate change`
- `Available at: URL` - Missing access date: `(Accessed: 15 March 2023)`
- `(Author, 2020, pp. 45)` - Single page uses `p.`: `(Author, 2020, p. 45)`

### Right

- Round brackets for all dates and access dates
- Page numbers for ALL direct quotes
- Sentence case for titles (capitalize only proper nouns)
- Access dates for ALL online sources
- `p.` for single page, `pp.` for page ranges

## Validation Checklist

When validating citations:

- [ ] All in-text citations have matching reference list entries
- [ ] All reference entries are cited in text
- [ ] Reference list is alphabetical by author surname
- [ ] Author names: Surname, Initials format
- [ ] All dates in round brackets
- [ ] Page numbers for all direct quotes
- [ ] Access dates for all online sources
- [ ] URLs complete and functional
- [ ] Titles in sentence case with italics for standalone works
- [ ] Publisher locations for books
- [ ] DOIs where available for journals
- [ ] "et al." used for 4+ authors

## Process

When formatting citations:

1. **Identify source type**: Book, article, website, etc.
2. **Gather required elements**: Author, year, title, publisher/journal, etc.
3. **Format in-text citation**: Apply author-date format with page numbers for quotes
4. **Format reference entry**: Follow template for source type
5. **Generate BibTeX**: Create entry with appropriate type and fields
6. **Validate**: Check completeness and consistency

## Output Format

When formatting citations, provide:
1. In-text citation format
2. Reference list entry
3. BibTeX entry (if requested)
4. Any validation warnings or missing information
