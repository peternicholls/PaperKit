# Specification: Security, Prompt-Safety, and Data Governance

**Spec ID:** 004-security-governance  
**Date:** 2025-12-13  
**Status:** Draft  
**Priority:** High  
**Category:** Security & Safety

---

## Problem Statement

Agentic systems that fetch sources and execute tools need explicit mitigations for prompt injection, data exfiltration, and accidental leakage of sensitive data (e.g., private PDFs, API keys). Currently, no formal security model exists for the PaperKit system.

### Current State

- No input sanitization for user-provided content
- No provenance tracking for external sources
- No trust model for agent network access
- No secrets handling policy
- No documented data retention policy
- No prompt injection detection or mitigation

### Impact

- Potential for prompt injection attacks via user content
- Untracked external sources could introduce malicious content
- API keys or sensitive data could leak through prompts or logs
- No compliance with data governance requirements
- Difficult to audit data flow through the system

---

## Proposed Solution

### Overview

Implement comprehensive security layers including input sanitization, provenance tracking, trust models, secrets management, and explicit data governance policies.

### Technical Requirements

#### 1. Input Sanitization Layer

```yaml
# .paper/_cfg/security/input-sanitization.yaml
inputSanitization:
  version: "1.0.0"
  
  rules:
    # Detect and neutralize prompt injection patterns
    promptInjection:
      enabled: true
      patterns:
        - "ignore previous instructions"
        - "disregard all prior"
        - "system prompt:"
        - "you are now"
        - "new instructions:"
      action: flag_and_sanitize
      
    # Detect potential secrets in input
    # Note: Patterns are configurable and loaded from external file
    # to allow updates without code changes
    secretsDetection:
      enabled: true
      patternsFile: ".paper/_cfg/security/secret-patterns.yaml"  # External config
      builtinPatterns:  # Fallback if external file not found
        - regex: "(?i)(api[_-]?key|apikey)[\\s]*[=:][\\s]*['\"]?[a-zA-Z0-9]{20,}"
        - regex: "(?i)(secret|password|token)[\\s]*[=:][\\s]*['\"]?[^\\s'\"]{8,}"
        - regex: "(?i)aws[_-]?(access[_-]?key|secret)"
        - regex: "sk-[a-zA-Z0-9]{48}"  # OpenAI API key pattern (update as format changes)
      customPatterns: []  # User-defined patterns loaded at runtime
      action: block_and_alert
      
    # Detect URLs and external references
    externalReferences:
      enabled: true
      logAllUrls: true
      blockPatterns:
        - "file://"
        - "localhost"
        - "127.0.0.1"
        - "internal."
      requireValidation:
        - "http://"
        - "https://"
  
  # Processing pipeline
  pipeline:
    - stage: normalize
      description: "Normalize whitespace, encoding"
    - stage: detect_patterns
      description: "Run all detection patterns"
    - stage: sanitize
      description: "Apply sanitization rules"
    - stage: log
      description: "Log sanitization actions"
    - stage: validate
      description: "Final validation before processing"
```

#### 2. Provenance Tracking System

```yaml
# Schema for source provenance
provenanceRecord:
  id: "prov-{uuid}"
  
  source:
    type: "academic_paper"  # or: url, file, user_input, generated
    
    # For DOI-identified sources
    doi: "10.1000/example.doi"
    crossref:
      title: "Example Paper Title"
      authors: ["Author One", "Author Two"]
      publicationDate: "2025-01-15"
      journal: "Example Journal"
      validated: true
      validationTimestamp: "2025-12-13T10:00:00Z"
    
    # For URL sources
    url: "https://example.com/paper.pdf"
    urlMetadata:
      fetchTimestamp: "2025-12-13T10:00:00Z"
      httpStatus: 200
      contentType: "application/pdf"
      contentHash: "sha256:abc123..."
      contentLength: 1234567
      
    # For file sources
    file:
      path: "source/reference-materials/paper.pdf"
      hash: "sha256:def456..."
      uploadTimestamp: "2025-12-12T09:00:00Z"
      uploadedBy: "user"
  
  # Chain of custody
  custody:
    - action: "uploaded"
      timestamp: "2025-12-12T09:00:00Z"
      agent: "user"
    - action: "processed"
      timestamp: "2025-12-13T10:00:00Z"
      agent: "research-consolidator"
      outputArtifact: "output-refined/research/consolidated.md"
    - action: "cited"
      timestamp: "2025-12-13T11:00:00Z"
      agent: "section-drafter"
      location: "latex/sections/02_background.tex:45"
  
  # Trust assessment
  trust:
    level: "verified"  # unverified | self_reported | verified | trusted
    verificationMethod: "crossref_lookup"
    verificationTimestamp: "2025-12-13T10:00:00Z"
    flags: []
```

#### 3. Agent Trust Model

```yaml
# .paper/_cfg/security/trust-model.yaml
trustModel:
  version: "1.0.0"
  
  agentCapabilities:
    research-consolidator:
      networkAccess: true
      networkScope:
        allowed:
          - "api.crossref.org"
          - "api.unpaywall.org"
          - "api.semanticscholar.org"
          - "doi.org"
        blocked: ["*"]
      fileAccess:
        read: ["source/**", "output-refined/research/**"]
        write: ["output-refined/research/**", "memory/**"]
      sensitiveDataAccess: false
      
    paper-architect:
      networkAccess: false
      fileAccess:
        read: ["output-refined/**", "memory/**"]
        write: ["output-drafts/outlines/**", "memory/**"]
      sensitiveDataAccess: false
      
    section-drafter:
      networkAccess: false
      fileAccess:
        read: ["output-refined/**", "output-drafts/outlines/**", "memory/**"]
        write: ["output-drafts/sections/**", "memory/**"]
      sensitiveDataAccess: false
      
    quality-refiner:
      networkAccess: false
      fileAccess:
        read: ["output-drafts/**", "memory/**"]
        write: ["output-refined/sections/**", "memory/**"]
      sensitiveDataAccess: false
      
    reference-manager:
      networkAccess: true
      networkScope:
        allowed:
          - "api.crossref.org"
          - "doi.org"
        blocked: ["*"]
      fileAccess:
        read: ["output-refined/**", "latex/references/**"]
        write: ["latex/references/**", "memory/**"]
      sensitiveDataAccess: false
      
    latex-assembler:
      networkAccess: false
      fileAccess:
        read: ["latex/**", "output-refined/**"]
        write: ["latex/**", "output-final/**"]
      sensitiveDataAccess: false
  
  escalationPolicy:
    networkAccessDenied:
      notify: true
      logLevel: "warning"
      action: "block"
    fileAccessDenied:
      notify: true
      logLevel: "error"
      action: "block"
```

#### 4. Secrets Management Policy

```yaml
# .paper/_cfg/security/secrets-policy.yaml
secretsPolicy:
  version: "1.0.0"
  
  # Where secrets can be stored
  storage:
    allowed:
      - type: "environment_variable"
        prefix: "PAPERKIT_"
        description: "System credentials stored as env vars"
      - type: "keychain"
        description: "OS keychain/credential manager"
    forbidden:
      - type: "file"
        patterns: ["*.yaml", "*.json", "*.md", "*.tex"]
      - type: "git"
        description: "Never commit secrets to git"
  
  # Supported credentials
  credentials:
    crossref_api:
      name: "CrossRef API Mailto"
      type: "email"
      envVar: "PAPERKIT_CROSSREF_EMAIL"
      required: false
      usedBy: ["research-consolidator", "reference-manager"]
      
    semantic_scholar_api:
      name: "Semantic Scholar API Key"
      type: "api_key"
      envVar: "PAPERKIT_SEMANTIC_SCHOLAR_KEY"
      required: false
      usedBy: ["research-consolidator"]
  
  # Leakage prevention
  leakagePrevention:
    scanLogs: true
    scanOutputs: true
    redactionPattern: "[REDACTED]"
    alertOnDetection: true
  
  # Audit
  audit:
    logSecretAccess: true
    logLevel: "info"
    retentionDays: 90
```

#### 5. Data Governance Policy

```yaml
# .paper/_cfg/security/data-governance.yaml
dataGovernance:
  version: "1.0.0"
  
  # Data classification
  classification:
    levels:
      public:
        description: "Can be shared freely"
        retention: "indefinite"
        examples: ["published papers", "public datasets"]
      internal:
        description: "Internal use only"
        retention: "project_duration"
        examples: ["draft content", "notes"]
      confidential:
        description: "Restricted access"
        retention: "90_days_after_project"
        examples: ["unpublished research", "reviews"]
      sensitive:
        description: "Highly restricted"
        retention: "explicit_deletion"
        examples: ["personal data", "proprietary content"]
  
  # Retention policies
  retention:
    drafts:
      classification: "internal"
      retentionPeriod: "project_duration"
      deletionPolicy: "user_initiated"
    finalOutputs:
      classification: "public"
      retentionPeriod: "indefinite"
      deletionPolicy: "never_auto"
    logs:
      classification: "internal"
      retentionPeriod: "90_days"
      deletionPolicy: "automatic"
    sourceFiles:
      classification: "varies"
      retentionPeriod: "project_duration"
      deletionPolicy: "user_initiated"
  
  # Allowed data types
  allowedDataTypes:
    - type: "text/plain"
      maxSize: "10MB"
    - type: "text/markdown"
      maxSize: "10MB"
    - type: "application/pdf"
      maxSize: "50MB"
      scanRequired: true
    - type: "application/x-bibtex"
      maxSize: "5MB"
    - type: "text/x-latex"
      maxSize: "10MB"
  
  # Prohibited content
  prohibitedContent:
    - pattern: "social_security_number"
      action: "block"
    - pattern: "credit_card_number"
      action: "block"
    - pattern: "personal_health_info"
      action: "warn"
  
  # Export controls
  export:
    requireApproval: false
    allowedFormats: ["pdf", "tex", "bib", "md"]
    auditExports: true
```

#### 6. Prompt Injection Detection

```python
# tools/security/prompt_injection_detector.py
class PromptInjectionDetector:
    """
    Detects and mitigates prompt injection attacks.
    """
    
    patterns = [
        # Direct instruction override
        r"ignore\s+(all\s+)?previous\s+instructions?",
        r"disregard\s+(all\s+)?prior\s+",
        r"forget\s+(everything|all)\s+",
        
        # Role manipulation
        r"you\s+are\s+now\s+",
        r"act\s+as\s+(a|an)\s+",
        r"pretend\s+(to\s+be|you\s+are)",
        
        # System prompt extraction
        r"(show|reveal|output)\s+(your\s+)?(system\s+)?prompt",
        r"what\s+(are|were)\s+your\s+instructions",
        
        # Delimiter injection
        r"```system",
        r"\[system\]",
        r"<\|system\|>",
    ]
    
    def scan(self, text: str) -> ScanResult:
        """Scan text for injection patterns."""
        
    def sanitize(self, text: str) -> str:
        """Remove or neutralize detected patterns."""
        
    def get_risk_score(self, text: str) -> float:
        """Return risk score 0.0-1.0."""
```

---

## Implementation Steps

| Step | Description | Estimated Effort |
|------|-------------|------------------|
| 1 | Define input sanitization rules | 6 hours |
| 2 | Implement prompt injection detector | 8 hours |
| 3 | Define provenance tracking schema | 4 hours |
| 4 | Implement provenance logger | 6 hours |
| 5 | Define agent trust model | 4 hours |
| 6 | Implement trust enforcement | 8 hours |
| 7 | Define secrets management policy | 4 hours |
| 8 | Implement secrets scanner | 6 hours |
| 9 | Define data governance policy | 4 hours |
| 10 | Implement data classification | 6 hours |
| 11 | Integration and testing | 8 hours |
| 12 | Documentation | 4 hours |

**Total Estimated Effort:** 68 hours

---

## Success Criteria

- [ ] Input sanitization detects and neutralizes prompt injection patterns
- [ ] All external sources have provenance records
- [ ] Agent trust model enforced at runtime
- [ ] No secrets stored in repository or logs
- [ ] Data retention policies enforced
- [ ] Security audit passes without critical findings

---

## Dependencies

- [003-consent-sandboxing.md](003-consent-sandboxing.md) - Sandboxing for enforcement
- [006-observability.md](006-observability.md) - Logging infrastructure

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| False positives in injection detection | Medium | Tune patterns; allow user override |
| Performance impact of scanning | Low | Optimize patterns; cache results |
| Over-restrictive trust model | Medium | Start permissive; tighten based on usage |
| Secrets leakage before implementation | High | Immediate scan of existing codebase |

---

## Related Specifications

- [003-consent-sandboxing.md](003-consent-sandboxing.md) - Tool sandboxing
- [006-observability.md](006-observability.md) - Security logging
- [007-citation-validation.md](007-citation-validation.md) - Source verification

---

## Open Questions

1. What level of prompt injection detection sensitivity is appropriate?
2. Should provenance tracking be opt-in or mandatory?
3. How to handle external sources that can't be verified (e.g., personal notes)?
4. What compliance frameworks should be considered (GDPR, etc.)?

---

## References

- OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Prompt Injection attacks: https://simonwillison.net/2022/Sep/12/prompt-injection/
- CrossRef API: https://api.crossref.org/
