# PaperKit Generation System Test Plan

## Test Objective
Verify that all generated files (IDE agents, documentation) can be fully regenerated from `.paperkit/` source of truth.

## Test Scope

### Generated Files to Verify
1. **GitHub Copilot Agents** (`.github/agents/*.agent.md`)
   - 10 agent files (6 core + 4 specialist)
2. **OpenAI Codex Prompts** (`.codex/prompts/*.md`)
   - 10 prompt files
3. **Documentation Files**
   - `AGENTS.md`
   - `COPILOT.md`

### Success Criteria

#### ✅ Pre-Test Validation
- [ ] `.paperkit/` directory exists with complete structure
- [ ] All 10 agent markdown files exist in `.paperkit/{core|specialist}/agents/`
- [ ] `agent-manifest.yaml` contains all 10 agents
- [ ] Generation scripts are executable

#### ✅ Generation Test Criteria
- [ ] All 10 Copilot agent files regenerated correctly
- [ ] All 10 Codex prompt files regenerated correctly
- [ ] `AGENTS.md` regenerated with correct content
- [ ] `COPILOT.md` regenerated with correct content
- [ ] All files reference `.paperkit/` (not `.paper/`)
- [ ] No errors during generation process

#### ✅ Content Validation Criteria
- [ ] Agent triggers match pattern `paper-{name}`
- [ ] All agent personas/display names are correct
- [ ] All icons are present in AGENTS.md
- [ ] Output locations reference `.paperkit/data/`
- [ ] Tool paths reference `.paperkit/tools/`
- [ ] Workflow references point to `.paperkit/_cfg/workflows/`

#### ✅ File Integrity Criteria
- [ ] Generated files have proper markdown formatting
- [ ] Code blocks use correct syntax
- [ ] No placeholder text like `${agent_name}` remaining
- [ ] All links are valid relative paths
- [ ] Auto-generation notices present in all derived files

## Test Procedure

### Phase 1: Setup Test Environment
```bash
# Create test branch
git checkout -b test/regeneration-validation

# Backup current generated files for comparison
mkdir -p /tmp/paperkit-backup
cp -r .github/agents /tmp/paperkit-backup/
cp -r .codex/prompts /tmp/paperkit-backup/
cp AGENTS.md COPILOT.md /tmp/paperkit-backup/
```

### Phase 2: Delete Generated Files
```bash
# Remove all generated IDE files
rm -rf .github/agents/*.agent.md
rm -rf .codex/prompts/*.md

# Remove generated documentation
rm -f AGENTS.md COPILOT.md
```

### Phase 3: Verify Deletion
```bash
# Should show no agent files
ls -la .github/agents/*.agent.md 2>/dev/null || echo "✓ Copilot agents deleted"
ls -la .codex/prompts/*.md 2>/dev/null || echo "✓ Codex prompts deleted"
test ! -f AGENTS.md && echo "✓ AGENTS.md deleted"
test ! -f COPILOT.md && echo "✓ COPILOT.md deleted"
```

### Phase 4: Regenerate Files
```bash
# Run main generation script
./paperkit generate

# Verify generation completed without errors
echo "Exit code: $?"
```

### Phase 5: Validate Generated Files
```bash
# Count generated files
echo "Copilot agents: $(ls -1 .github/agents/*.agent.md 2>/dev/null | wc -l) (expect: 10)"
echo "Codex prompts: $(ls -1 .codex/prompts/*.md 2>/dev/null | wc -l) (expect: 10)"
test -f AGENTS.md && echo "✓ AGENTS.md exists"
test -f COPILOT.md && echo "✓ COPILOT.md exists"

# Check for .paper/ references (should be 0 in generated files)
echo ""
echo "Checking for old .paper/ references:"
grep -r "\.paper/" .github/agents/ 2>/dev/null | grep -v "\.paperkit/" || echo "✓ No .paper/ refs in Copilot agents"
grep -r "\.paper/" .codex/prompts/ 2>/dev/null | grep -v "\.paperkit/" || echo "✓ No .paper/ refs in Codex prompts"
grep "\.paper/" AGENTS.md 2>/dev/null | grep -v "\.paperkit/" || echo "✓ No .paper/ refs in AGENTS.md"
grep "\.paper/" COPILOT.md 2>/dev/null | grep -v "\.paperkit/" || echo "✓ No .paper/ refs in COPILOT.md"
```

### Phase 6: Content Spot Checks
```bash
# Verify key content in AGENTS.md
echo ""
echo "Spot checking AGENTS.md content:"
grep -q "Research Consolidator" AGENTS.md && echo "✓ Research Consolidator found"
grep -q "Paper Architect" AGENTS.md && echo "✓ Paper Architect found"
grep -q "\.paperkit/tools/" AGENTS.md && echo "✓ Tool paths correct"
grep -q "auto-generated" AGENTS.md && echo "✓ Auto-generation notice present"

# Verify key content in COPILOT.md
echo ""
echo "Spot checking COPILOT.md content:"
grep -q "paper-architect" COPILOT.md && echo "✓ Agent trigger found"
grep -q "\.paperkit/" COPILOT.md && echo "✓ Source path correct"
grep -q "auto-generated" COPILOT.md && echo "✓ Auto-generation notice present"

# Verify Copilot agent structure
echo ""
echo "Spot checking .github/agents/paper-architect.agent.md:"
grep -q "chatagent" .github/agents/paper-architect.agent.md && echo "✓ Chatagent block present"
grep -q "\.paperkit/core/agents/" .github/agents/paper-architect.agent.md && echo "✓ Source path correct"
grep -q "agent-activation" .github/agents/paper-architect.agent.md && echo "✓ Activation protocol present"
```

### Phase 7: Compare with Backup (Optional)
```bash
# Visual diff to check what changed
diff -u /tmp/paperkit-backup/AGENTS.md AGENTS.md | head -20
diff -u /tmp/paperkit-backup/.github/agents/paper-architect.agent.md .github/agents/paper-architect.agent.md | head -20
```

### Phase 8: Git Status Check
```bash
# Check what changed
git status
git diff --stat

# Review changes
git diff AGENTS.md | head -50
```

## Test Results Template

```markdown
## Test Execution Results

**Date:** YYYY-MM-DD HH:MM
**Branch:** test/regeneration-validation
**Tester:** [Name]

### Pre-Test Validation
- [ ] Source structure verified
- [ ] Scripts executable
- [ ] Backups created

### Generation Results
- Generated Copilot agents: X/10
- Generated Codex prompts: X/10
- Generated AGENTS.md: Yes/No
- Generated COPILOT.md: Yes/No
- Exit code: N
- Errors: [list any errors]

### Content Validation
- [ ] No `.paper/` references found
- [ ] All `.paperkit/` references correct
- [ ] Agent names/triggers match
- [ ] Icons present
- [ ] Tool paths correct

### File Quality
- [ ] Markdown formatting valid
- [ ] No template placeholders
- [ ] Auto-generation notices present
- [ ] Links functional

### Overall Result
**PASS** / **FAIL**

### Issues Found
[List any issues or deviations from expected results]

### Recommendations
[Any improvements or follow-up actions needed]
```

## Rollback Plan

If tests fail:
```bash
# Restore from backup
cp /tmp/paperkit-backup/AGENTS.md .
cp /tmp/paperkit-backup/COPILOT.md .
cp -r /tmp/paperkit-backup/.github/agents/* .github/agents/
cp -r /tmp/paperkit-backup/.codex/prompts/* .codex/prompts/

# Delete test branch
git checkout master
git branch -D test/regeneration-validation
```

## Merge Criteria

Before creating PR, verify:
- [ ] All tests pass
- [ ] No regressions in functionality
- [ ] Documentation updated
- [ ] No unintended changes to source files
- [ ] Clean git history (squash if needed)

## Post-Merge Actions
- [ ] Tag release if appropriate
- [ ] Update documentation
- [ ] Notify team of changes
