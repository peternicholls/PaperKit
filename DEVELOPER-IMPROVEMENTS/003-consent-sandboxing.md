# Specification: Consent and Sandboxing for Tool Execution

**Spec ID:** 003-consent-sandboxing  
**Date:** 2024-12-13  
**Status:** Draft  
**Priority:** High  
**Category:** Security & Safety

---

## Problem Statement

The `requiresConsent` flags in tool-manifest.yaml indicate awareness of consent needs, but there is no standardized, auditable consent flow or sandboxing/permission enforcement for scripts that execute (LaTeX build, linters). Users cannot easily review what tools do before execution.

### Current State

- `tool-manifest.yaml` includes `requiresConsent` field (boolean)
- Individual tool YAML files in `.paper/_cfg/tools/` define capabilities and constraints
- All current tools marked as `requiresConsent: true`
- No UI or programmatic consent mechanism implemented
- No sandboxing or capability restrictions on tool execution
- No audit logging of tool executions
- Tools execute with full user permissions

### Impact

- Users cannot review tool actions before execution
- No audit trail for tool runs
- Malicious or buggy tools could cause damage
- No isolation between tool executions
- Compliance requirements may not be met

---

## Proposed Solution

### Overview

Implement a comprehensive consent and sandboxing system with explicit user approval workflows, capability-limited execution, and full audit logging.

### Technical Requirements

#### 1. Consent Flow System

```yaml
# .paper/_cfg/consent-config.yaml
consentSystem:
  version: "1.0.0"
  
  defaultPolicy: require_explicit
  
  consentLevels:
    none:
      description: "Tool runs without any consent"
      allowedTools: []
      
    implicit:
      description: "Tool runs with notification only"
      allowedTools:
        - validate-structure  # read-only validation
      notification: true
      
    explicit:
      description: "Requires user confirmation before each run"
      allowedTools:
        - lint-latex
        - format-references
      confirmationRequired: true
      showPreview: true
      
    strict:
      description: "Requires confirmation and shows detailed impact preview"
      allowedTools:
        - build-latex  # writes files, runs external processes
      confirmationRequired: true
      showPreview: true
      showImpactAnalysis: true
      recordReason: true
  
  userPreferences:
    rememberChoices: true
    rememberDuration: session  # session | permanent | 1hour | 1day
    allowBatchApproval: false
```

#### 2. Consent UI/UX Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  🔧 Tool Execution Request                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Tool: build-latex                                              │
│  Description: Compile LaTeX document to PDF                     │
│                                                                  │
│  📁 Files to be Read:                                           │
│     • latex/main.tex                                            │
│     • latex/sections/*.tex (7 files)                            │
│     • latex/references/references.bib                           │
│                                                                  │
│  📝 Files to be Written/Modified:                               │
│     • output-final/pdf/main.pdf                                 │
│     • latex/*.aux, *.log, *.bbl (build artifacts)              │
│                                                                  │
│  ⚙️ External Commands:                                          │
│     • pdflatex main.tex                                         │
│     • bibtex main                                               │
│                                                                  │
│  ⏱️ Estimated Duration: 30-60 seconds                           │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Approve    │  │    Deny      │  │   Details    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  □ Remember my choice for this session                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 3. Tool Capability Manifest

```yaml
# tools/build-latex.yaml
tool:
  name: build-latex
  displayName: Build LaTeX
  description: Compile LaTeX document to PDF
  version: "1.0.0"
  
  capabilities:
    fileRead:
      - pattern: "latex/**/*.tex"
        purpose: "Read LaTeX source files"
      - pattern: "latex/**/*.bib"
        purpose: "Read bibliography"
      - pattern: "latex/**/*.sty"
        purpose: "Read style files"
    
    fileWrite:
      - pattern: "output-final/pdf/*.pdf"
        purpose: "Write compiled PDF"
      - pattern: "latex/*.aux"
        purpose: "LaTeX auxiliary files"
      - pattern: "latex/*.log"
        purpose: "Build log"
    
    processExecution:
      - command: "pdflatex"
        arguments: ["main.tex"]
        purpose: "LaTeX compilation"
      - command: "bibtex"
        arguments: ["main"]
        purpose: "Bibliography processing"
    
    networkAccess: false
    
    environmentVariables:
      read: ["PATH", "HOME", "TEXINPUTS"]
      write: []
  
  riskLevel: medium
  
  sandboxRequirements:
    isolateFileSystem: true
    restrictNetwork: true
    limitCPU: "60s"
    limitMemory: "512MB"
    allowedPaths:
      - "latex/"
      - "output-final/"
  
  consentLevel: strict
  
  auditConfig:
    logLevel: detailed
    retainLogs: "30d"
    includeInReport: true
```

#### 4. Sandboxing Implementation

```yaml
# Sandbox configuration
# Note: Engine is configurable per platform
# - Linux: firejail, bubblewrap, nsjail, docker
# - macOS: docker (firejail not available)
# - Windows: docker, Windows Sandbox
sandboxConfig:
  engine: "auto"  # auto-detect best available, or specify: firejail, docker, bubblewrap
  fallbackEngine: "docker"  # fallback if preferred not available
  
  profiles:
    latex-build:
      capabilities:
        - cap_setuid: false
        - cap_net_admin: false
        - cap_sys_admin: false
      
      filesystem:
        readOnly:
          - /usr/share/texlive
          - /usr/share/fonts
        readWrite:
          - ${WORKSPACE}/latex
          - ${WORKSPACE}/output-final
        noAccess:
          - /home/*/.ssh
          - /home/*/.aws
          - /etc/passwd
      
      network:
        enabled: false
      
      resources:
        maxCPU: 60
        maxMemory: 512M
        maxProcesses: 50
        maxFileSize: 100M
    
    lint-only:
      capabilities: []
      filesystem:
        readOnly:
          - ${WORKSPACE}/latex
        readWrite: []
        noAccess: ["*"]
      network:
        enabled: false
```

#### 5. Audit Logging System

```yaml
# Audit log entry schema
auditEntry:
  id: "audit-{uuid}"
  timestamp: "2024-12-13T10:30:00Z"
  
  tool:
    name: "build-latex"
    version: "1.0.0"
  
  user:
    id: "user-id"
    consentGiven: true
    consentTimestamp: "2024-12-13T10:29:55Z"
    consentMethod: "explicit_approval"
  
  execution:
    startTime: "2024-12-13T10:30:00Z"
    endTime: "2024-12-13T10:30:45Z"
    status: "success"
    exitCode: 0
  
  impact:
    filesRead:
      - path: "latex/main.tex"
        hash: "sha256:abc123..."
    filesWritten:
      - path: "output-final/pdf/main.pdf"
        hash: "sha256:def456..."
        size: 245678
    filesDeleted: []
    
  sandbox:
    profile: "latex-build"
    violations: []
    resourceUsage:
      cpuTime: "32s"
      memoryPeak: "128MB"
  
  context:
    workflowId: "wf-123"
    sessionId: "session-456"
    triggeredBy: "user_command"
```

#### 6. Consent Verification API

```python
# tools/consent_manager.py
class ConsentManager:
    def request_consent(self, tool_id: str, context: dict) -> ConsentResult:
        """
        Request user consent for tool execution.
        Returns ConsentResult with approved/denied status.
        """
        
    def verify_consent(self, tool_id: str, session_id: str) -> bool:
        """
        Verify if valid consent exists for this tool in current session.
        """
        
    def revoke_consent(self, tool_id: str, session_id: str) -> None:
        """
        Revoke previously granted consent.
        """
        
    def get_consent_history(self, session_id: str) -> List[ConsentRecord]:
        """
        Get consent history for audit purposes.
        """
```

---

## Implementation Steps

| Step | Description | Estimated Effort |
|------|-------------|------------------|
| 1 | Define consent level schema and config | 4 hours |
| 2 | Define tool capability manifest schema | 4 hours |
| 3 | Implement consent request flow | 8 hours |
| 4 | Create consent UI components | 6 hours |
| 5 | Implement sandbox wrapper (firejail/docker) | 12 hours |
| 6 | Implement audit logging system | 6 hours |
| 7 | Update existing tools with capability manifests | 8 hours |
| 8 | Add consent verification to tool runner | 4 hours |
| 9 | Create audit report generator | 4 hours |
| 10 | Documentation and examples | 4 hours |

**Total Estimated Effort:** 60 hours

---

## Success Criteria

- [ ] All tools have capability manifests
- [ ] Consent UI shows impact preview before execution
- [ ] User consent recorded in audit log
- [ ] Tools execute in sandboxed environment
- [ ] Audit logs capture all tool executions
- [ ] Consent can be revoked and re-requested
- [ ] Sandbox violations are detected and logged

---

## Dependencies

- [001-agent-metadata.md](001-agent-metadata.md) - Tool schema format
- Operating system sandbox support (firejail, Docker, or equivalent)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Sandbox breaks tool functionality | High | Test thoroughly; provide escape hatch for trusted tools |
| Performance overhead | Medium | Optimize sandbox startup; cache configurations |
| User fatigue from consent prompts | Medium | Allow "remember choice" per session; batch approvals |
| Platform compatibility | Medium | Support multiple sandbox backends |

---

## Related Specifications

- [004-security-governance.md](004-security-governance.md) - Broader security model
- [006-observability.md](006-observability.md) - Audit logging integration

---

## Open Questions

1. Which sandboxing technology to use (firejail, Docker, bubblewrap)?
2. Should consent be per-tool or per-capability?
3. How to handle tools that require network access (citation validation)?
4. Should there be an admin override for trusted environments?

---

## References

- Current: `.paper/_cfg/tool-manifest.yaml`
- Tool Definitions: `.paper/_cfg/tools/*.yaml`
- Tool Schema: `.paper/_cfg/schemas/tool-schema.json`
- Firejail: https://firejail.wordpress.com/
- Bubblewrap: https://github.com/containers/bubblewrap
