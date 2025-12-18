### 011-refiner-thresholdRephrasing

**Agent:** 💎 Quality Refiner (Riley)  
**Phase:** 2 (Core)  
**Estimated Time:** 60 minutes  
**Dependencies:** 008-drafter-limitationsSection  
**Output Location:** All relevant `latex/sections/*.tex` files

#### Task Brief

Systematically rephrase all perceptual threshold presentations to include "(design choice)" qualifier, making explicit that these are engineering heuristics rather than empirically-derived constants.

#### Pattern

**Before:**
> "The ∆_min ≈ 2.0 threshold ensures perceptual distinctness"

**After:**
> "The ∆_min ≈ 2.0 threshold (design choice; see §1.6) ensures perceptual distinctness"

#### Sections to Audit

1. **§2.2** — OKLab JND statements
   - Find: References to ∆E ≈ 1.0 as JND
   - Add: "design target" qualifier

2. **§4.1** — ∆E definition and thresholds
   - Find: "practical JND" of ∆E ≈ 2.0
   - Add: "(design choice)" and reference to §1.6

3. **§4.3** — ∆_min and ∆_max definitions
   - Find: Threshold values stated as facts
   - Add: Qualification language

4. **§6.3** — Velocity weight constants
   - Find: w_h ≈ 1.5–2.0 statements
   - Add: "design heuristic derived from practical experimentation"

5. **§8.1-8.4** — Gamut management thresholds
   - Find: Any numeric thresholds
   - Add: Qualification if presenting as established fact

#### Rephrasing Templates

| Original Pattern | Revised Pattern |
|-----------------|-----------------|
| "∆_min ≈ 2.0 ensures..." | "∆_min ≈ 2.0 (design choice; see §1.6) ensures..." |
| "The threshold of X..." | "The threshold of X (design heuristic)..." |
| "Based on perceptual research, Y..." | "Informed by perceptual research, Y (see §1.6 for validation status)..." |
| "The constant Z is..." | "The constant Z is a recommended engineering parameter..." |

#### Document Changes

Create revision summary:
```markdown
## Threshold Rephrasing Summary

### §2.2 Changes
- Line X: Added "design target" to JND reference

### §4.1 Changes
- Line Y: Added "(design choice; see §1.6)" to ∆_min

[etc.]
```

#### Success Criteria

- [ ] All threshold statements audited
- [ ] "(design choice)" or equivalent added where appropriate
- [ ] Cross-references to §1.6 (Limitations) included
- [ ] Tone remains confident, not apologetic
- [ ] No LaTeX compilation errors
- [ ] Revision summary document created
