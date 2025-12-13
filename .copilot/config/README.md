# Configuration Files

This directory contains system-wide configuration files that control behavior, defaults, and policies.

## Files

### settings.yaml
System-wide settings and defaults including:
- Path configurations
- Default behaviors (standards flexibility, citation requirements)
- Memory management settings
- UI preferences
- Integration toggles
- Quality standards

### consent.yaml
Consent and permission management including:
- Consent scope definitions (once, session, workspace, always)
- Tool-specific policies
- Logging configuration
- Reset options

## Usage

These files are read by the Paper System Router to configure agent behavior and tool execution policies.

### Modifying Settings

Settings can be adjusted to customize system behavior:

```yaml
# Example: Change from pragmatic to strict standards
defaults:
  standards-flexibility: "strict"
```

### Consent Policies

Tool execution requires user consent for potentially dangerous operations:

```yaml
# Example: Tool consent configuration
tool-policies:
  build-latex:
    requires-consent: true
    default-scope: "once"
```

## Design Principles

1. **Sensible defaults:** System works out-of-the-box
2. **Progressive disclosure:** Advanced options available but not required
3. **User control:** Consent for all non-reversible operations
4. **Transparency:** All policies are explicit and documented
