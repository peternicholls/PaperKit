---
name: problem-analysis
description: Systematically analyze problems to identify root causes, constraints, and solution paths. Use when stuck, debugging issues, or facing complex challenges.
metadata:
  author: specialist-team
  version: "1.0.0"
---

# Problem Analysis

## Your Task

When analyzing a problem, systematically:

1. **Define** the problem clearly and precisely
2. **Decompose** into manageable sub-problems
3. **Identify** root causes, not symptoms
4. **Map** constraints and dependencies
5. **Generate** solution approaches
6. **Recommend** actionable next steps

---

## Problem Analysis Framework

### Step 1: Problem Definition

Before solving, ensure you understand the problem.

**Problem Statement Template**:
```markdown
## Problem Statement

**What's happening**: [Observable behavior/symptom]
**What should happen**: [Expected/desired behavior]
**Impact**: [Why this matters, who's affected]
**Context**: [When it happens, what triggers it]
**Constraints**: [What limits solutions]
```

**Clarity Checklist**:
- [ ] Can someone unfamiliar understand the problem?
- [ ] Is the scope clear (what's in/out)?
- [ ] Are success criteria defined?
- [ ] Are assumptions stated?

### Step 2: Problem Decomposition

Break complex problems into smaller parts.

**Decomposition Techniques**:

#### Hierarchical Decomposition
```
[Main Problem]
├── [Sub-problem 1]
│   ├── [Component 1a]
│   └── [Component 1b]
├── [Sub-problem 2]
│   ├── [Component 2a]
│   └── [Component 2b]
└── [Sub-problem 3]
```

#### MECE Analysis
Mutually Exclusive, Collectively Exhaustive:
- Categories don't overlap
- Categories cover everything

#### Process Decomposition
For process problems:
```
Input → Step 1 → Step 2 → Step 3 → Output
         ↓         ↓         ↓
      [Issue?]  [Issue?]  [Issue?]
```

---

### Step 3: Root Cause Analysis

Identify underlying causes, not surface symptoms.

#### 5 Whys Technique

Keep asking "Why?" until you reach the root:

```markdown
**Problem**: Paper deadline missed

1. Why? → Draft wasn't finished
2. Why? → Research took longer than expected
3. Why? → Scope wasn't well-defined
4. Why? → No initial planning phase
5. Why? → Rushed to start writing immediately

**Root Cause**: Skipped planning phase
**Solution**: Implement mandatory planning before drafting
```

#### Fishbone Diagram (Ishikawa)

Categorize potential causes:

```
              Methods    Materials
                  \        /
                   \      /
                    ↘    ↙
            [PROBLEM]←————
                    ↗    ↖
                   /      \
                  /        \
              People    Tools
```

**Common Categories**:
- Methods (processes, procedures)
- Materials (inputs, resources)
- People (skills, training)
- Tools (equipment, technology)
- Environment (context, conditions)
- Measurement (how we assess)

#### Fault Tree Analysis

Work backward from failure:

```
            [Failure]
           /    |    \
        [A]    [B]   [C]    ← Immediate causes
       /  \     |
    [A1] [A2]  [B1]         ← Contributing factors
```

---

### Step 4: Constraint Mapping

Understand what limits your solution space.

**Constraint Categories**:

| Type | Examples |
|------|----------|
| Time | Deadlines, schedules |
| Resources | Budget, people, tools |
| Technical | Platform limitations, dependencies |
| Policy | Rules, standards, compliance |
| Knowledge | Skills gaps, information needs |

**Constraint Analysis Template**:
```markdown
| Constraint | Type | Severity | Negotiable? | Workaround |
|------------|------|----------|-------------|------------|
| Deadline: Friday | Time | High | No | Reduce scope |
| No external tools | Technical | Medium | Maybe | Check with lead |
```

---

### Step 5: Solution Generation

Generate multiple approaches before choosing.

**Solution Generation Prompts**:
- What's the obvious solution?
- What's the opposite approach?
- What if we had unlimited resources?
- What if we had to solve this today?
- What would an expert do?
- What would a beginner try?
- What if we removed the biggest constraint?

**Solution Evaluation Matrix**:
```markdown
| Solution | Addresses Root Cause | Fits Constraints | Effort | Risk |
|----------|---------------------|------------------|--------|------|
| A        | Yes                 | Partial          | High   | Low  |
| B        | Partial             | Yes              | Medium | Med  |
| C        | Yes                 | Yes              | Low    | High |
```

---

### Step 6: Action Planning

Convert analysis into actionable steps.

**Action Plan Template**:
```markdown
## Recommended Solution: [Name]

### Rationale
[Why this solution addresses the root cause]

### Implementation Steps
1. [ ] [Immediate action - today]
2. [ ] [Short-term - this week]
3. [ ] [Medium-term - next week]

### Dependencies
- [What needs to happen first]
- [Who needs to be involved]

### Risks and Mitigations
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| ... | ... | ... |

### Success Criteria
- [ ] [How we know it's working]
```

---

## Problem Types and Approaches

### Debugging/Technical Problems

**Systematic Approach**:
1. Reproduce the problem reliably
2. Isolate the failure point
3. Form hypotheses
4. Test hypotheses systematically
5. Verify the fix doesn't introduce new issues

**Debugging Questions**:
- What changed recently?
- When did it last work?
- What's different between working and broken cases?
- What assumptions am I making?

### Process/Workflow Problems

**Process Analysis**:
1. Map current process end-to-end
2. Identify bottlenecks and pain points
3. Measure time/effort at each step
4. Find the critical path
5. Optimize highest-impact areas

### People/Communication Problems

**Communication Analysis**:
- Who needs what information when?
- Where are the communication gaps?
- What's the feedback loop?
- Are expectations aligned?

### Decision Problems

**Decision Framework**:
1. What decision needs to be made?
2. What are the options?
3. What criteria matter?
4. What information is missing?
5. What's the reversibility of each option?

---

## Common Problem-Solving Mistakes

| Mistake | Better Approach |
|---------|-----------------|
| Jumping to solutions | Define problem first |
| Treating symptoms | Find root causes |
| Single solution focus | Generate alternatives |
| Ignoring constraints | Map constraints early |
| Analysis paralysis | Set decision deadline |
| Not testing | Verify with small experiments |

---

## Documentation Template

```markdown
# Problem Analysis: [Title]

**Date**: YYYY-MM-DD
**Analyst**: [Name]

## Problem Definition
[Clear statement of the problem]

## Decomposition
[Problem broken into sub-problems]

## Root Cause Analysis
[5 Whys or Fishbone results]

## Constraints
[What limits solutions]

## Solution Options
| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| ... | ... | ... | ... |

## Recommended Action
[What to do and why]

## Next Steps
- [ ] Immediate action
- [ ] Follow-up items
```

---

## For Academic Writing Problems

### Common Paper Problems

| Problem | Analysis Approach |
|---------|-------------------|
| Writer's block | Decompose → write smallest piece |
| Unclear argument | 5 Whys → find core claim |
| Weak structure | Process decomposition → map flow |
| Missing evidence | Constraint mapping → identify gaps |
| Feedback overwhelm | MECE → categorize feedback types |

### Stuck on a Section

Ask:
1. What is this section supposed to accomplish?
2. What's the one key message?
3. What does the reader need to know first?
4. What evidence supports the message?
5. What's the connection to adjacent sections?

---

## Quick Reference

| Need | Technique |
|------|-----------|
| Find root cause | 5 Whys |
| Categorize causes | Fishbone diagram |
| Understand failure | Fault tree |
| List all options | MECE analysis |
| Evaluate solutions | Decision matrix |
| Handle complexity | Decomposition |
