#!/usr/bin/env python3

"""
LaTeX Bibliography Reference Formatter

Converts various bibliography formats to BibTeX and validates entries.
"""

import sys
import re
import argparse
from pathlib import Path

def format_harvard_article(authors, title, journal, year, volume="", issue="", pages="", doi=""):
    """Format a journal article in Harvard style"""
    author_str = format_authors(authors)
    citation_key = generate_citation_key(authors, year)
    
    entry = f"""@article{{{citation_key},
  author = {{{author_str}}},
  title = {{{title}}},
  journal = {{{journal}}},
  year = {{{year}}}"""
    
    if volume:
        entry += f""",
  volume = {{{volume}}}"""
    if issue:
        entry += f""",
  number = {{{issue}}}"""
    if pages:
        entry += f""",
  pages = {{{pages}}}"""
    if doi:
        entry += f""",
  doi = {{{doi}}}"""
    
    entry += "\n}\n"
    return entry, citation_key

def format_authors(author_list):
    """Format author names in BibTeX format"""
    if isinstance(author_list, str):
        author_list = [author_list]
    
    # BibTeX format: "First Last and Second Author and Third Author"
    formatted = " and ".join(author_list)
    return formatted

def generate_citation_key(authors, year):
    """Generate a citation key from author and year"""
    if isinstance(authors, str):
        last_name = authors.split()[-1].lower()
    else:
        last_name = authors[0].split()[-1].lower()
    
    return f"{last_name}_{year}"

def validate_bibtex_file(bib_file):
    """Validate a BibTeX file for common issues"""
    issues = []
    
    with open(bib_file, 'r') as f:
        content = f.read()
    
    # Check for unmatched braces
    open_braces = content.count('{')
    close_braces = content.count('}')
    if open_braces != close_braces:
        issues.append(f"Unmatched braces: {open_braces} open, {close_braces} close")
    
    # Check for entries
    entries = re.findall(r'@\w+{', content)
    if not entries:
        issues.append("No BibTeX entries found")
    
    # Check for missing required fields
    for entry_type, required_fields in [
        ('article', ['author', 'title', 'journal', 'year']),
        ('book', ['author', 'title', 'publisher', 'year']),
    ]:
        pattern = f'@{entry_type}{{([^}}]+)}}'
        for match in re.finditer(pattern, content, re.IGNORECASE):
            entry_content = match.group(1)
            missing = []
            for field in required_fields:
                if not re.search(rf'{field}\s*=', entry_content, re.IGNORECASE):
                    missing.append(field)
            if missing:
                entry_key = entry_content.split(',')[0].strip()
                issues.append(f"Entry {entry_key} ({entry_type}): missing {', '.join(missing)}")
    
    return issues

def main():
    parser = argparse.ArgumentParser(description="LaTeX Bibliography Reference Formatter")
    parser.add_argument('--validate', type=str, help='Validate a BibTeX file')
    parser.add_argument('--output', type=str, help='Output file for formatted bibliography')
    
    args = parser.parse_args()
    
    if args.validate:
        bib_file = Path(args.validate)
        if not bib_file.exists():
            print(f"Error: File not found: {bib_file}")
            sys.exit(1)
        
        issues = validate_bibtex_file(bib_file)
        
        if issues:
            print(f"Bibliography validation issues in {bib_file}:")
            for issue in issues:
                print(f"  ⚠ {issue}")
            sys.exit(1)
        else:
            print(f"✓ Bibliography is valid: {bib_file}")
            sys.exit(0)
    else:
        print("Usage: format-references.py --validate <file.bib>")
        sys.exit(0)

if __name__ == "__main__":
    main()
