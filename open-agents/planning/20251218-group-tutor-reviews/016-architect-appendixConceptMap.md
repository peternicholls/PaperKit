### 016-architect-appendixConceptMap

**Agent:** 🏗️ Paper Architect (Morgan)  
**Phase:** 3 (Strategic)  
**Estimated Time:** 1 hour  
**Dependencies:** 015-assembler-visualDiagrams (for consistent style)  
**Output Location:** `latex/appendices/D_quick_reference.tex`

#### Task Brief

Complete the missing Concept Map (D.1.1) that is listed in Appendix D but not present.

Tutor B noted: "Appendix D Quick Reference lists Concept Map (D.1.1) but the actual diagram is missing"

#### Content to Create

**D.1.1 Concept Map**

A visual diagram showing relationships between system components:

```
                    ┌─────────────┐
                    │   Config    │
                    │  (Anchors,  │
                    │   Mode,     │
                    │   Params)   │
                    └──────┬──────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Journey Construction │
              │   (§3: Bézier curves)  │
              └────────────┬───────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │Perceptual│    │  Style   │    │  Gamut   │
    │Constraints│   │ Controls │    │Management│
    │   (§4)   │    │   (§5)   │    │   (§8)   │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Discrete Sampling │
              │   (→ Palette)       │
              └─────────────────────┘
```

#### Also Expand

**D.6 Troubleshooting Table**

Tutors noted this is "pure gold for users" and should be expanded:

| Problem | Symptom | Solution |
|---------|---------|----------|
| Grayscale anchor | No color spread | §3.4: Use colored anchor or expand chroma |
| Gamut boundary exceeded | Chroma reduced unexpectedly | §8.4: Check gamut limits, verify anchor is in-gamut |
| Hue shifts with chroma change | Unexpected color cast | §8: Verify gamut mapping hierarchy |
| Velocity feels flat | Boring/uniform palette | §6.3: Adjust velocity weights |
| Reproducibility fails | Different output on re-run | §9: Verify seed value, check config hash |
| Palette too similar | Colors indistinguishable | §4.3: Increase ∆_min threshold |
| Palette too varied | Colors feel disconnected | §4.3: Decrease ∆_max threshold |
| Performance degradation | Slow generation | §10.6: Check anchor count, reduce constraints |

#### Success Criteria

- [ ] Concept map created (TikZ or ASCII art)
- [ ] Relationships between components clear
- [ ] Section references included
- [ ] Troubleshooting table expanded (8+ rows)
- [ ] Solutions reference specific sections
- [ ] LaTeX compiles without errors
