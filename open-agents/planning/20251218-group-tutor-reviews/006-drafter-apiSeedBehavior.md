### 006-drafter-apiSeedBehavior

**Agent:** ✍️ Section Drafter (Jordan)  
**Phase:** 1 (Quick Win)  
**Estimated Time:** 20 minutes  
**Dependencies:** None  
**Output Location:** `latex/sections/09_variation_determinism.tex` (§9.3), API table if applicable

#### Task Brief

Clarify whether providing a `seed` value automatically enables variation mode.

Tutor A noted: "In Appendix C, Listing C.11 uses `seed: 42`. Does passing seed automatically imply `variation: true`?"

#### Decision to Make

**Choose one approach:**

**Approach A (Implicit — cleaner API):**
```
If seed is provided → variation is automatically enabled
If seed is null/omitted → deterministic mode (no variation)
```

**Approach B (Explicit — clearer):**
```
variation: true/false controls mode
seed is only used when variation: true
```

#### Content to Add

**Add to §9.3 (after discussing default seed):**

```latex
\begin{designdecision}
If a \texttt{seed} value is provided, variation mode is automatically 
enabled. If \texttt{seed} is omitted or null, the engine generates 
deterministic palettes based solely on anchor configuration. This 
implicit behavior reduces API surface while maintaining explicit 
control for callers who need reproducible variation.
\end{designdecision}
```

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
