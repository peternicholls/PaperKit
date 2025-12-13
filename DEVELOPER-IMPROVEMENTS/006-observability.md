# Specification: Observability, Telemetry, and UX Telemetry

**Spec ID:** 006-observability  
**Date:** 2024-12-13  
**Status:** Draft  
**Priority:** Medium  
**Category:** Operations & Monitoring

---

## Problem Statement

There is no visible design for logging agent runs, errors, or usage metrics. Without observability, debugging agent orchestration is hard and understanding system usage patterns is impossible.

### Current State

- No structured logging for agent executions
- No run IDs or correlation between workflow steps
- No metrics collection (usage, errors, timing)
- No artifact diffing for user review
- No analytics on agent usage patterns
- Manual debugging required for issues

### Impact

- Difficult to diagnose workflow failures
- No visibility into agent performance
- Cannot identify frequently used agents
- No way to track error rates or patterns
- User experience issues go undetected

---

## Proposed Solution

### Overview

Implement comprehensive observability with structured logging, run correlation, artifact tracking, and usage analytics.

### Technical Requirements

#### 1. Structured Logging System

```yaml
# .paper/_cfg/observability/logging-config.yaml
loggingConfig:
  version: "1.0.0"
  
  defaults:
    level: "info"
    format: "json"
    outputDir: ".paper/logs"
    retentionDays: 30
    maxFileSize: "10MB"
    maxFiles: 10
  
  loggers:
    agent:
      level: "info"
      output: "logs/agent.log"
      includeFields:
        - timestamp
        - runId
        - agentId
        - action
        - duration
        - status
        - inputSummary
        - outputSummary
        
    workflow:
      level: "info"
      output: "logs/workflow.log"
      includeFields:
        - timestamp
        - workflowId
        - workflowName
        - step
        - status
        - duration
        
    tool:
      level: "info"
      output: "logs/tool.log"
      includeFields:
        - timestamp
        - toolId
        - executionTime
        - exitCode
        - filesModified
        
    error:
      level: "error"
      output: "logs/error.log"
      includeFields:
        - timestamp
        - source
        - errorType
        - message
        - stackTrace
        - context
        
    audit:
      level: "info"
      output: "logs/audit.log"
      includeFields:
        - timestamp
        - userId
        - action
        - resource
        - result
```

#### 2. Run Correlation Schema

```yaml
# Schema for run correlation
runContext:
  runId: "run-{uuid}"
  startedAt: "2024-12-13T10:00:00Z"
  
  session:
    sessionId: "session-{uuid}"
    userId: "user"
    startedAt: "2024-12-13T09:30:00Z"
    
  workflow:
    workflowId: "wf-{uuid}"
    workflowName: "write-paper"
    version: "1.0.0"
    
  trace:
    traceId: "trace-{uuid}"
    spanId: "span-{uuid}"
    parentSpanId: "parent-span-{uuid}"
    
  context:
    paperTitle: "Color Perception Modeling"
    currentStep: "draft-introduction"
    previousSteps:
      - stepId: "outline"
        runId: "run-{prev-uuid}"
        completedAt: "2024-12-13T09:45:00Z"
```

#### 3. Agent Run Log Entry

```yaml
# Log entry for agent execution
agentRun:
  runId: "run-abc123"
  timestamp: "2024-12-13T10:00:00Z"
  
  agent:
    id: "section-drafter"
    version: "1.0.0"
    
  execution:
    status: "success"  # success | failure | partial | timeout
    duration: 45.2  # seconds
    tokenUsage:
      input: 2500
      output: 1800
      total: 4300
    
  input:
    summary: "Draft introduction section"
    size: 2500  # characters
    files: ["output-drafts/outlines/paper-outline.md"]
    
  output:
    summary: "Introduction drafted with 3 citations"
    size: 8500  # characters
    files: ["output-drafts/sections/01_introduction.tex"]
    artifacts:
      - type: "section_draft"
        path: "output-drafts/sections/01_introduction.tex"
        hash: "sha256:abc123"
        
  quality:
    citationCount: 3
    wordCount: 1250
    completeness: 0.85
    uncertainAreas: ["paragraph 3 needs verification"]
    
  context:
    workflowId: "wf-123"
    stepId: "draft-introduction"
    previousRunId: "run-xyz789"
```

#### 4. Artifact Diff Tracking

```yaml
# Schema for artifact diff tracking
artifactDiff:
  id: "diff-{uuid}"
  timestamp: "2024-12-13T10:00:00Z"
  
  runId: "run-abc123"
  agentId: "section-drafter"
  
  artifact:
    path: "output-drafts/sections/01_introduction.tex"
    type: "section_draft"
    
  changes:
    previousHash: "sha256:old123"
    currentHash: "sha256:new456"
    previousVersion: "output-drafts/sections/01_introduction.tex.v1"
    currentVersion: "output-drafts/sections/01_introduction.tex.v2"
    
  diff:
    summary: "+250 lines, -30 lines"
    addedLines: 250
    removedLines: 30
    changedSections: ["Introduction", "Background context"]
    
  review:
    status: "pending"  # pending | approved | rejected
    reviewedBy: null
    reviewedAt: null
    comments: []
```

#### 5. Analytics and Metrics

```yaml
# Metrics collection schema
metrics:
  collection:
    interval: "1h"
    retentionDays: 90
    
  counters:
    agent_runs_total:
      labels: [agent_id, status]
      description: "Total agent executions"
      
    workflow_completions_total:
      labels: [workflow_name, status]
      description: "Total workflow completions"
      
    tool_executions_total:
      labels: [tool_id, exit_code]
      description: "Total tool executions"
      
    errors_total:
      labels: [error_type, source]
      description: "Total errors"
  
  gauges:
    active_sessions:
      description: "Currently active sessions"
      
    pending_artifacts:
      labels: [type]
      description: "Artifacts pending review"
  
  histograms:
    agent_duration_seconds:
      labels: [agent_id]
      buckets: [1, 5, 15, 30, 60, 120, 300]
      description: "Agent execution duration"
      
    workflow_duration_seconds:
      labels: [workflow_name]
      buckets: [60, 300, 600, 1800, 3600]
      description: "Workflow duration"
      
    token_usage:
      labels: [agent_id]
      buckets: [100, 500, 1000, 2000, 4000, 8000]
      description: "Token usage per run"
```

#### 6. Dashboard and Reporting

```python
# tools/observability/dashboard.py
class ObservabilityDashboard:
    """
    Generate observability reports and dashboards.
    """
    
    def generate_summary_report(self, time_range: str = "24h") -> Report:
        """
        Generate summary report for time range.
        
        Returns:
            Report with:
            - Total runs by agent
            - Success/failure rates
            - Average durations
            - Top errors
            - Most used workflows
        """
        
    def get_agent_stats(self, agent_id: str) -> AgentStats:
        """
        Get statistics for specific agent.
        """
        
    def get_workflow_trace(self, workflow_id: str) -> WorkflowTrace:
        """
        Get complete trace for workflow execution.
        """
        
    def list_recent_errors(self, limit: int = 10) -> List[ErrorEntry]:
        """
        List recent errors with context.
        """
        
    def get_artifact_history(self, path: str) -> List[ArtifactDiff]:
        """
        Get version history and diffs for artifact.
        """
```

```yaml
# Dashboard output example
dailySummary:
  date: "2024-12-13"
  
  overview:
    totalRuns: 45
    successRate: 0.93
    averageDuration: 32.5
    activeWorkflows: 3
    
  byAgent:
    - agent: "section-drafter"
      runs: 15
      successRate: 0.93
      avgDuration: 45.2
    - agent: "quality-refiner"
      runs: 12
      successRate: 0.92
      avgDuration: 38.1
    - agent: "paper-architect"
      runs: 5
      successRate: 1.0
      avgDuration: 22.3
      
  errors:
    total: 3
    byType:
      - type: "validation_error"
        count: 2
      - type: "timeout"
        count: 1
        
  artifacts:
    created: 28
    pendingReview: 5
    approved: 20
    rejected: 3
```

#### 7. User-Facing Observability

```yaml
# User-visible run status
userRunStatus:
  currentRun:
    id: "run-abc123"
    agent: "Section Drafter"
    startedAt: "10:00:00"
    status: "in_progress"
    progress: 0.65
    
  recentActivity:
    - time: "10:00:00"
      agent: "Section Drafter"
      action: "Drafting introduction"
      status: "in_progress"
    - time: "09:45:00"
      agent: "Paper Architect"
      action: "Created outline"
      status: "completed"
      artifact: "output-drafts/outlines/paper-outline.md"
      
  pendingReview:
    - artifact: "output-drafts/sections/01_introduction.tex"
      agent: "Section Drafter"
      changedAt: "09:50:00"
      diff: "+250 lines"
      
  notifications:
    - type: "warning"
      message: "Draft has 2 uncertain areas flagged"
    - type: "info"
      message: "3 new citations added to bibliography"
```

---

## Implementation Steps

| Step | Description | Estimated Effort |
|------|-------------|------------------|
| 1 | Define logging schema and config | 4 hours |
| 2 | Implement structured logger | 6 hours |
| 3 | Add run correlation/tracing | 6 hours |
| 4 | Implement artifact diff tracking | 6 hours |
| 5 | Add metrics collection | 6 hours |
| 6 | Build dashboard/report generator | 8 hours |
| 7 | Add user-facing status display | 4 hours |
| 8 | Integrate with existing tools | 4 hours |
| 9 | Documentation | 2 hours |

**Total Estimated Effort:** 46 hours

---

## Success Criteria

- [ ] All agent runs logged with correlation IDs
- [ ] Workflow traces available for debugging
- [ ] Artifact diffs generated and stored
- [ ] Metrics collected for key operations
- [ ] Dashboard shows usage and error patterns
- [ ] Users can review artifact changes before acceptance
- [ ] Log retention and rotation working

---

## Dependencies

- [003-consent-sandboxing.md](003-consent-sandboxing.md) - Audit logging integration
- [004-security-governance.md](004-security-governance.md) - Security event logging

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Log volume too high | Medium | Configurable log levels; sampling |
| Performance impact | Low | Async logging; buffering |
| Storage costs | Medium | Retention policies; compression |
| Sensitive data in logs | High | Sanitization; log filtering |

---

## Related Specifications

- [003-consent-sandboxing.md](003-consent-sandboxing.md) - Audit logging
- [005-testing-ci.md](005-testing-ci.md) - Test observability
- [009-state-management.md](009-state-management.md) - State tracking

---

## Open Questions

1. Should we use external observability tools (OpenTelemetry, etc.)?
2. What granularity of metrics is appropriate?
3. How long should artifact versions be retained?
4. Should observability data be exportable?

---

## References

- OpenTelemetry: https://opentelemetry.io/
- Structured Logging: https://www.structlog.org/
- Prometheus metrics: https://prometheus.io/docs/
