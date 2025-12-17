# Working Reference (live session handoff)

Purpose: keep a concise, always-current handoff so any agent can resume work after interruptions.

---

## Current Paper Goal

**Internal technical reference** for the engineering team developing the C-core Color Journey Engine. Documents design rationale, mathematical foundations, and architectural decisions to enable "literally on the same page" team alignment.

## Audience

Engineering team (internal). Not a generic specification for external implementers.

## Format/Standards

- Harvard citations
- LaTeX output
- 8,000–12,000 words
- Open sources only (team must access all citations)
- Strategic citations (foundational: 5-8, comparative: 3-5, validating: 2-3)

## Key Constraints

- Focus on "why" over "how" (technical docs exist for implementation)
- Structure for random-access reference (section titles as conversational references)
- Performance context: 5.6M colors/sec, microsecond-range

---

## Latest Decisions (2024-12-17)

1. **Tutor session reframed paper** as internal working reference
2. **Prior art scan completed** — all 7 research areas documented
3. **Research index updated** with 13 external citations (Harvard style)
4. **Synthesis document created** at `.paper/data/output-refined/research/prior-art-synthesis.md`

## Research Gaps Status

| Gap | Status |
|-----|--------|
| OKLab adoption evidence | ✅ Complete (Adobe, CSS, plugins documented) |
| Gamut mapping standards | ✅ Complete (CSS §12, ICC, Color.js) |
| JND/perceptual spacing | ✅ Complete (Ottosson, Wikipedia, Color.js) |
| Arc-length parameterization | ✅ Complete (Kamermans, Levien) |
| Determinism/PRNG | ✅ Complete (xoshiro, standard practice) |
| Color harmony theory | ✅ Complete (IxDF, traditional rules) |
| Performance benchmarking | ⚠️ Internal only — need to document method |

## Novelty Claim

**Combination is novel**, not individual components:
- Continuous Bézier path + discrete constrained sampling + mood expansion + arc-length parameterization

No prior art found for single-anchor mood expansion using lightness direction.

---

## Next Actions

1. **For Peter**: Document C-core benchmark method (hardware, test code) for performance claims
2. **For drafting**: Use synthesis document when writing §1.4 (Positioning)
3. **Phase 2 (tutor recommendations)**: Add Appendix D quick reference, decision boxes, enhanced section titles

---

## Key Files

| File | Purpose |
|------|---------|
| `open-agents/planning/0000-Project-Overview/prior-art-scan.md` | Detailed source checklist |
| `open-agents/memory/research-index.yaml` | All citations (Harvard format) |
| `.paper/data/output-refined/research/prior-art-synthesis.md` | Consolidated positioning guide |
| `open-agents/planning/20241217-tutor-session/tutor-handoff-foundation-updates.md` | Tutor recommendations |

---

*Last updated: 2024-12-17*
