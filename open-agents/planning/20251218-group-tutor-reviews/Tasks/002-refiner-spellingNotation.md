### 002-refiner-spellingNotation

**Agent:** 💎 Quality Refiner (Riley)  
**Phase:** 1 (Quick Win)  
**Estimated Time:** 45-60 minutes  
**Dependencies:** None  
**Output Location:** All `latex/sections/*.tex` files

#### Task Brief

Standardize spelling and mathematical notation throughout all LaTeX section files to achieve internal consistency.

#### Spelling Standardization

**Decision:** Use US English throughout (matches API naming and code examples)

**Find & Replace patterns:**
```
Colour     → Color
colour     → color
colours    → colors
neighbouring → neighboring
neighbour  → neighbor
favourite  → favorite
behaviour  → behavior
```

**Note:** Preserve proper nouns and quoted text unchanged.

#### Notation Standardization

**Decision:** Use ∆E consistently (OKLab implied by context)

**Actions:**
1. Replace all `∆E_OK` with `∆E`
2. Replace all `\Delta E_{OK}` with `\Delta E`
3. Add clarification footnote to §1.1 or first occurrence:
   > "All ∆E measurements in this specification refer to color difference in OKLab perceptual space."

**Section citation format:**
- Standardize on `§3.3` format (not "Section 3.3" or "section 3.3")
- Use `\autoref{sec:name}` for cross-references where available

#### Files to Process

- [ ] `latex/sections/01_introduction.tex`
- [ ] `latex/sections/02_perceptual_foundations.tex`
- [ ] `latex/sections/03_journey_construction.tex`
- [ ] `latex/sections/04_perceptual_constraints.tex`
- [ ] `latex/sections/05_style_controls.tex`
- [ ] `latex/sections/06_modes_of_operation.tex`
- [ ] `latex/sections/07_loop_strategies.tex`
- [ ] `latex/sections/08_gamut_management.tex`
- [ ] `latex/sections/09_variation_determinism.tex`
- [ ] `latex/sections/10_api_design.tex`
- [ ] `latex/sections/11_caller_responsibilities.tex`
- [ ] `latex/sections/12_conclusion.tex`
- [ ] `latex/appendices/A_presets.tex`
- [ ] `latex/appendices/B_notation.tex`
- [ ] `latex/appendices/C_examples.tex`
- [ ] `latex/appendices/D_quick_reference.tex`

#### Success Criteria

- [ ] All spelling uses US English consistently
- [ ] All ∆E notation is consistent
- [ ] Section citations use § format
- [ ] Footnote added clarifying OKLab context
- [ ] No LaTeX compilation errors introduced
- [ ] Revision summary document created
