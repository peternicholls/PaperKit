# PaperKit Guides

This folder contains reference documentation for agents and workflows.

## Available Guides

### harvard-citation-guide.md

Comprehensive Harvard citation style guide (Cite Them Right standard) including:

- **Core Principles** - Author-date format, reference list requirements
- **In-Text Citations** - Format for 1-4+ authors, quotes, page numbers
- **Reference List Formats** - Books, articles, websites, reports, conferences, theses
- **Special Cases** - Multiple works by same author, corporate authors, no date
- **Common Errors** - What to avoid and best practices
- **BibTeX Integration** - Entry types, required fields, examples
- **Agent Guidelines** - How the reference-manager agent uses this guide

## Usage

Agents automatically load relevant guides during activation. The reference-manager agent (Harper) loads:

- `harvard-citation-guide.md` - Style rules and formatting templates
- `../resources/citation-rules.yaml` - Validation rules and field specifications

## Contributing

When updating guides:

1. Maintain consistent formatting
2. Include clear examples for each rule
3. Update the agent instructions if rules change
4. Test with the reference-manager agent

## Related Files

- [.paperkit/_cfg/resources/citation-rules.yaml](../resources/citation-rules.yaml) - Validation rules
- [.paperkit/_cfg/agents/reference-manager.yaml](../agents/reference-manager.yaml) - Agent definition
- [.paperkit/core/agents/reference-manager.md](../../core/agents/reference-manager.md) - Agent persona

---

**Version:** 2.0.0  
**Last Updated:** December 2025
