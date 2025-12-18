### 006-drafter-apiSeedBehavior

**Agent:** ✍️ Section Drafter (Jordan)  
**Phase:** 1 (Quick Win)  
**Estimated Time:** 20 minutes  
**Dependencies:** None  
**Output Location:** `latex/sections/09_variation_determinism.tex` (§9.3), API table if applicable

#### Task Brief

Clarify whether providing a `seed` value automatically enables variation mode.

Tutor A noted: "In Appendix C, Listing C.11 uses `seed: 42`. Does passing seed automatically imply `variation: true`?"

#### Decision Already Made - Implementation Evidence

**✅ APPROACH B IS THE ACTUAL IMPLEMENTATION**

**Evidence:** See `.paper/data/output-refined/research/technical-documentation-consolidated.md` §1.4

From PRD.md §7.2:
> "Deterministic or undetermined variation:
>   - Provide a seed → variation is repeatable.
>   - Omit seed → implementation may pick a default fixed seed, or use entropy for 'shuffle session' semantics."

From README.md API:
```
variation: VariationConfig
  - enabled: Bool (default: false)
  - dimensions: VariationDimensions
  - strength: VariationStrength
  - seed: UInt64 (deterministic seed)
```

**Implementation Behavior:**
```
variation.enabled = true + seed → deterministic variation
variation.enabled = true + no seed → implementation-defined (default or entropy)
variation.enabled = false → deterministic base journey (seed ignored)
```

**Critical:** Seed alone does NOT enable variation. Explicit flag required.

#### Content to Add

**Add to §9.3 (after discussing default seed):**

```latex
\begin{designdecision}
Variation mode requires \emph{explicit enablement} via the 
\texttt{variation.enabled} flag. The \texttt{seed} parameter is only 
consulted when \texttt{variation.enabled = true}. This three-state 
behavior clarifies intent:

\begin{itemize}
\item \texttt{variation: false} — Deterministic base journey (seed ignored)
\item \texttt{variation: true, seed: 42} — Deterministic variation (reproducible)
\item \texttt{variation: true, seed: null} — Implementation-defined (may use default seed or entropy)
\end{itemize}

This explicit design prevents accidental variation when only 
reproducibility is intended, while supporting both deterministic 
and non-deterministic variation modes.
\end{designdecision}
```

**Rationale:** Implementation uses Approach B (explicit flag). Paper must document actual behavior.

**Update API table (if exists in §10.2):**
- Add note about seed → variation behavior
- Clarify which parameters are required vs optional

**Update Appendix C examples** (if needed):
- Ensure code examples align with documented behavior
- Add comment explaining the implicit behavior

#### Success Criteria

- [ ] Clear statement of seed → variation behavior added
- [ ] Design decision box explaining rationale
- [ ] API table updated (if applicable)
- [ ] Code examples consistent with documentation
- [ ] No contradictions between sections
