---
name: bibtex-management
description: Manage BibTeX databases including parsing, validation, formatting, and fixing common issues. Use when working with references.bib files, validating citations, or resolving bibliography errors.
metadata:
  author: core-team
  version: "1.0.0"
---

# BibTeX Management

## Your Task

When working with BibTeX files, ensure:

1. **Valid syntax** - All entries parse correctly
2. **Complete fields** - Required fields present for each type
3. **Consistent formatting** - Uniform style throughout
4. **Accurate data** - No typos in fields
5. **Proper citation keys** - Follow naming convention

---

## BibTeX Entry Types

### Common Entry Types and Required Fields

| Type | Required Fields | Optional Fields |
|------|-----------------|-----------------|
| `@article` | author, title, journal, year | volume, number, pages, month, doi |
| `@book` | author/editor, title, publisher, year | edition, address, isbn |
| `@inproceedings` | author, title, booktitle, year | editor, pages, organization, publisher |
| `@incollection` | author, title, booktitle, publisher, year | editor, chapter, pages |
| `@techreport` | author, title, institution, year | type, number, address |
| `@phdthesis` | author, title, school, year | type, address |
| `@mastersthesis` | author, title, school, year | type, address |
| `@misc` | author, title, year | howpublished, note, url |
| `@online` | author, title, url, year | urldate, accessed |

---

## Citation Key Convention

### Standard Format

```
AuthorYear[Suffix]
```

**Examples**:
- `Smith2023` - Single author
- `SmithJones2023` - Two authors
- `SmithEtAl2023` - Three+ authors
- `Smith2023a`, `Smith2023b` - Multiple works by same author/year

### Rules

1. Use first author's surname (capitalized)
2. For two authors: both surnames
3. For three+ authors: first surname + "EtAl"
4. Four-digit year
5. Lowercase letter suffix if needed for disambiguation
6. No spaces, hyphens, or special characters

---

## Entry Formatting

### Standard Format

```bibtex
@article{SmithJones2023,
  author    = {Smith, John A. and Jones, Mary B.},
  title     = {A Study of Color Perception in Digital Interfaces},
  journal   = {Journal of Human-Computer Interaction},
  year      = {2023},
  volume    = {45},
  number    = {3},
  pages     = {123--145},
  doi       = {10.1000/example.2023.123},
}
```

### Formatting Rules

1. **Opening brace** on same line as `@type{key,`
2. **Fields** indented with 2 spaces
3. **Field names** lowercase, aligned
4. **Values** in braces `{...}` (not quotes)
5. **Each field** on its own line
6. **Trailing comma** after last field
7. **Closing brace** on its own line

---

## Field-Specific Rules

### Author Names

**Format**: `{Surname, First Name and Surname, First Name}`

```bibtex
author = {Smith, John A. and Jones, Mary B. and Brown, Robert},
```

**Multiple names**: Separate with ` and ` (not commas)

**Corporate authors**: Wrap in extra braces
```bibtex
author = {{World Health Organization}},
```

### Titles

**Preserve capitalization** with braces:
```bibtex
title = {A Study of {RGB} Color Spaces in {HCI}},
```

**Book titles**: Capitalize normally
**Article titles**: Only first word and proper nouns capitalized (BibTeX style handles this)

### Page Numbers

Use double dash for ranges:
```bibtex
pages = {123--145},
```

### DOIs

Include without `https://doi.org/` prefix:
```bibtex
doi = {10.1000/example.2023.123},
```

### URLs

```bibtex
url = {https://example.com/paper},
urldate = {2023-12-15},
```

---

## Validation Checklist

### Required Field Validation

For each entry, verify:

- [ ] Citation key follows convention
- [ ] All required fields present
- [ ] No duplicate citation keys
- [ ] Author names properly formatted
- [ ] Year is four digits
- [ ] Page numbers use double dash

### Common Issues to Check

| Issue | Fix |
|-------|-----|
| Missing required field | Add the field |
| Duplicate citation key | Add suffix (a, b, c) |
| Single dash in pages | Replace with `--` |
| Unprotected capitals | Wrap in `{}` |
| `and` missing between authors | Add ` and ` |
| Stray commas in values | Remove or escape |
| Mismatched braces | Balance `{` and `}` |
| URL encoding issues | Escape special chars |

---

## Fixing Common Problems

### Problem: Missing Author

**Detection**: Entry has no `author` field

**Fix**: Add author or use `key` field for sorting:
```bibtex
@misc{NoAuthor2023,
  title  = {Annual Report},
  year   = {2023},
  key    = {Annual Report},
}
```

### Problem: Special Characters

**Escape these in BibTeX**:

| Character | Escape |
|-----------|--------|
| & | `\&` |
| % | `\%` |
| $ | `\$` |
| # | `\#` |
| _ | `\_` |
| { | `\{` |
| } | `\}` |
| ~ | `\~{}` |
| ^ | `\^{}` |

**Accented characters**:
```bibtex
author = {M{\"u}ller, Hans},  % Müller
author = {Gonz{\'a}lez, Maria},  % González
```

### Problem: Inconsistent Capitalization

**Detection**: Article titles with random capitalization

**Fix**: Use sentence case, protect proper nouns:
```bibtex
% Bad
title = {A Study of RGB Color Spaces},

% Good
title = {A study of {RGB} color spaces},
```

### Problem: Duplicate Keys

**Detection**: Two entries with same key

**Fix**: Add suffix or rename:
```bibtex
@article{Smith2023a,
  ...
}
@article{Smith2023b,
  ...
}
```

---

## BibTeX vs BibLaTeX

### Key Differences

| Feature | BibTeX | BibLaTeX |
|---------|--------|----------|
| New entry types | Limited | `@online`, `@software`, etc. |
| Name handling | Basic | Sophisticated |
| Unicode | Limited | Full support |
| Date formats | year, month | date field |
| URL handling | Manual | Built-in |

### BibLaTeX-Specific Fields

```bibtex
@online{Website2023,
  author  = {Smith, John},
  title   = {Example Website},
  url     = {https://example.com},
  urldate = {2023-12-15},
  date    = {2023},
}
```

---

## Harvard Style Specifics

For Harvard citation style:

### Entry Requirements

| Type | Must Have |
|------|-----------|
| Journal article | author, year, title, journal, volume, issue, pages |
| Book | author, year, title, edition (if not first), place, publisher |
| Website | author/organization, year, title, URL, access date |

### Edition Format

```bibtex
edition = {3rd},
% or
edition = {Revised},
```

### Online Sources

Always include access date:
```bibtex
urldate = {2023-12-15},
note    = {Accessed: 15 December 2023},
```

---

## Entry Templates

### Journal Article

```bibtex
@article{AuthorYear,
  author  = {Surname, First and Surname, First},
  title   = {Article Title in Sentence Case},
  journal = {Journal Name},
  year    = {2023},
  volume  = {10},
  number  = {2},
  pages   = {100--120},
  doi     = {10.xxxx/xxxxx},
}
```

### Book

```bibtex
@book{AuthorYear,
  author    = {Surname, First},
  title     = {Book Title},
  publisher = {Publisher Name},
  year      = {2023},
  address   = {City},
  edition   = {2nd},
  isbn      = {978-0-000-00000-0},
}
```

### Conference Paper

```bibtex
@inproceedings{AuthorYear,
  author    = {Surname, First},
  title     = {Paper Title},
  booktitle = {Proceedings of the Conference Name},
  year      = {2023},
  pages     = {100--110},
  address   = {City, Country},
  publisher = {Publisher},
}
```

### Website

```bibtex
@online{AuthorYear,
  author  = {Surname, First},
  title   = {Page Title},
  url     = {https://example.com/page},
  urldate = {2023-12-15},
  year    = {2023},
}
```

### Software

```bibtex
@software{AuthorYear,
  author  = {Surname, First},
  title   = {Software Name},
  version = {1.0.0},
  url     = {https://github.com/example/repo},
  year    = {2023},
}
```

---

## Validation Script Usage

```bash
# Check BibTeX syntax
biber --tool --validate-datamodel references.bib

# Check for common issues
checkcites --undefined --unused main.aux

# View warnings during LaTeX compilation
biber main  # Check output for warnings
```

---

## Quick Reference

| Task | Action |
|------|--------|
| New entry | Use appropriate type template |
| Multiple authors | Separate with ` and ` |
| Protect capitals | Wrap in `{...}` |
| Page range | Use `--` (double dash) |
| Special chars | Escape with `\` |
| Corporate author | Double braces `{{...}}` |
| Duplicate key | Add letter suffix |
| Missing field | Add required field for type |
