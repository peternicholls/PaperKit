# Agent Development Workflow
**For AI Agents Working on PaperKit Development (Specs 001-013)**

---

## 🤖 CRITICAL: If You Are an AI Agent

This document applies to **AI assistants working on PaperKit system improvements** (GitHub Copilot, Claude, GPT, etc.), NOT to the paper-writing agents that are part of PaperKit.

## Mandatory Tracking Workflow

### BEFORE Starting ANY Work

```bash
# 1. Read the tracking file FIRST
cat dev-docs/DEVELOPER-IMPROVEMENTS/tracking.yaml

# 2. Check current context
grep -A 20 "current_context:" dev-docs/DEVELOPER-IMPROVEMENTS/tracking.yaml
```

**What to look for:**
- `last_work_date` - When was work last done?
- `current_focus` - What was being worked on?
- `next_steps` - What should be done next?
- `decisions_needed` - What needs human input?
- Spec status under `specifications.<spec-id>.status`

### WHEN Starting Work on a Spec

**Example: Starting work on spec 002**

```yaml
# Update these fields in tracking.yaml:
specifications:
  "002-workflow-agent-contract":
    status: IN_PROGRESS  # Change from DRAFT
    actual_hours: 0      # Initialize if not present

current_context:
  last_work_date: "2025-12-28"  # Update to today
  current_focus: "Implementing spec 002 workflow-agent contract validation"
  
  next_steps:
    immediate:
      - "Design contract schema structure"
      - "Review workflow YAML files for agent references"
```

### DURING Implementation

**Update tracking.yaml incrementally as you work:**

```yaml
specifications:
  "002-workflow-agent-contract":
    actual_hours: 3  # Increment as you work
    progress:
      tasks:
        - status: COMPLETE  # Change from NOT_STARTED when done
          description: "Define workflow-agent contract schema"
        - status: IN_PROGRESS  # Change from NOT_STARTED when working
          description: "Implement contract validation tool"
        - status: NOT_STARTED
          description: "Add contract checks to CI"
      
      notes:
        - "Schema based on existing workflow YAML structure"
        - "Validation logic similar to agent validation"
```

**Add decisions for human review:**

```yaml
current_context:
  decisions_needed:
    - "Should contract validation be strict or permissive for undefined agents?"
    - "How to handle workflow versions vs agent versions?"
```

**Record blockers immediately:**

```yaml
specifications:
  "002-workflow-agent-contract":
    progress:
      blockers:
        - issue: "Agent schema doesn't include version compatibility field"
          impact: "Cannot validate agent version requirements"
          suggested_fix: "Add 'supportedVersions' field to agent schema"
```

### WHEN Completing Work

```yaml
specifications:
  "002-workflow-agent-contract":
    status: COMPLETE  # Change from IN_PROGRESS
    completion_date: "2025-12-28"
    actual_hours: 12  # Final count
    
    progress:
      deliverables:
        - ".paperkit/_cfg/schemas/contract-schema.json"
        - "open-agents/tools/validate-contracts.py"
        - ".github/workflows/validate-contracts.yml"
      
      impact:
        unblocks: ["005-testing-ci"]
        enables: ["Workflow contract tests", "Agent compatibility checks"]

current_context:
  recent_accomplishments:
    - "Completed spec 002 contract validation system"
    
  next_steps:
    immediate:
      - "Begin spec 005 (testing framework)"
      - "Document contract validation usage"
```

### WHEN Taking a Break

**Always leave context for resumption:**

```yaml
current_context:
  last_work_date: "2025-12-28"
  current_focus: "Spec 002 - implementing validation logic (70% complete)"
  
  next_steps:
    immediate:
      - "Finish validate_contract_references() function"
      - "Add error messages for common validation failures"
      - "Write unit tests for validation logic"
  
  technical_debt:
    - "Contract schema needs documentation"
    - "Test coverage only at 60%"
```

## File Locations

| File | Purpose |
|------|---------|
| `dev-docs/DEVELOPER-IMPROVEMENTS/tracking.yaml` | **Main tracking file - UPDATE THIS** |
| `dev-docs/DEVELOPER-IMPROVEMENTS/README.md` | Overview and instructions |
| `dev-docs/DEVELOPER-IMPROVEMENTS/001-*.md` | Individual spec documents |
| `dev-docs/DEVELOPER-IMPROVEMENTS/001-IMPLEMENTATION-COMPLETE.md` | Example of completed spec |

## YAML Update Pattern

### Minimal Update (Quick Progress Note)

```yaml
specifications:
  "002-workflow-agent-contract":
    actual_hours: 5  # Just increment hours
    progress:
      tasks:
        - status: COMPLETE  # Update one task status
          description: "Define workflow-agent contract schema"
```

### Comprehensive Update (Milestone or Completion)

```yaml
specifications:
  "002-workflow-agent-contract":
    status: COMPLETE
    completion_date: "2025-12-28"
    actual_hours: 40
    progress:
      original_scope:
        - status: COMPLETE
          description: "Contract schema definition"
        - status: COMPLETE
          description: "Validation tool implementation"
      
      beyond_scope:
        - status: COMPLETE
          description: "Auto-fix for common contract errors"
      
      deliverables:
        - "Path to files created"
      
      impact:
        unblocks: ["Other spec IDs"]
        enables: ["New capabilities"]

current_context:
  last_work_date: "2025-12-28"
  recent_accomplishments:
    - "What you just completed"
  next_steps:
    immediate:
      - "What to do next"
```

## Common Scenarios

### Scenario 1: Human Returns After 2 Weeks

**Agent should:**
1. Read `tracking.yaml` completely
2. Summarize: "You were working on X, last touched 14 days ago"
3. Highlight: decisions_needed, blockers, next_steps
4. Ask: "Would you like to continue with X or switch focus?"

### Scenario 2: Scope Expands Beyond Spec

**Agent should:**
1. Update `beyond_scope` section in spec's progress
2. Track additional hours accurately
3. Document why expansion was valuable
4. Update `impact` section with new capabilities

### Scenario 3: Blocked by Missing Dependency

**Agent should:**
1. Add to spec's `progress.blockers`
2. Add to `current_context.blockers`
3. Suggest workaround or alternative approach
4. Update `decisions_needed` if human input required

### Scenario 4: Discovering Technical Debt

**Agent should:**
1. Add to `current_context.technical_debt`
2. Assess priority (critical/high/medium/low)
3. Estimate effort to address
4. Document in spec notes

## Validation Checklist

Before ending your session, verify:

- [ ] `tracking.yaml` updated with current status
- [ ] `last_work_date` is today's date
- [ ] `actual_hours` reflects time spent
- [ ] Task statuses updated
- [ ] Decisions documented if any
- [ ] Blockers recorded if any
- [ ] Next steps clear for resumption
- [ ] Recent accomplishments listed if milestone reached

## Examples from Spec 001

See `tracking.yaml` for Spec 001 as a reference:
- Status: COMPLETE
- Beyond scope work documented
- All deliverables listed
- Impact on other specs noted
- Learnings recorded for future specs

## Anti-Patterns (DO NOT DO THIS)

❌ **Starting work without reading tracking.yaml**
❌ **Forgetting to update status from DRAFT → IN_PROGRESS**
❌ **Not recording actual hours**
❌ **Leaving stale next_steps when work changes direction**
❌ **Not documenting decisions for human review**
❌ **Batch updating tracking.yaml at the end (update continuously)**
❌ **Using vague task descriptions ("fixed stuff")**
❌ **Not recording context when taking breaks**

## Questions?

- Check `dev-docs/DEVELOPER-IMPROVEMENTS/README.md`
- Check `dev-docs/DEVELOPER-IMPROVEMENTS/012-open-questions.md`
- Ask the human for clarification
- Document the question in `decisions_needed`

---

**Remember: tracking.yaml is the single source of truth for development progress. Keep it current!**
