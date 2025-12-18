# Technical Documentation Research: Color Journey Implementation Evidence

**Created:** 18 December 2025  
**Consolidated By:** Alex (Research Consolidator)  
**Purpose:** Synthesized reference for paper improvement tasks (003-017)  
**Sources:** Color Journey codebase technical documentation  
**Base Path:** `./open-agents/source/reference-materials/tech-docs-from-exisiting-software-repo/`

---

## Executive Summary

This consolidated research document synthesizes evidence from the Color Journey implementation documentation to support paper revision tasks. The implementation provides concrete validation for performance claims, API behavior, perceptual constraints, and system limitations. Key findings include verified performance metrics (5.2M colors/s), explicit variation semantics, documented precision trade-offs, and comprehensive limitation cataloging.

**Critical Insight:** Several paper claims require clarification—Möbius loop appears theoretical-only, perceptual velocity is curve-parameterized (not arc-length), and seed behavior requires explicit variation enablement.

---

## 1. Implementation Evidence by Paper Task

### 1.1 Task 003: Möbius Loop Verification

**Status:** NOT IMPLEMENTED

**Evidence:**
- PRD.md §6 documents three loop modes: Open, Closed Loop, Ping-Pong
- Möbius loop NOT mentioned in any implementation documentation
- Paper §7.4 appears to be theoretical extension

**Sources:**
- `DevDocs/PRD.md` §6 (Loop Modes)

**Recommendation:** Clarify in paper as "proposed extension" or verify if implemented but undocumented.

---

### 1.2 Task 004: Perceptual Velocity Parameterization

**Finding:** Implementation uses **curve parameter** t, not arc-length s.

**Evidence:**

From PRD.md §3.3:
> "The route can be expressed as: A continuous function t ∈ [0, 1] → OKLab"

From Architecture.md:
> "Journey sampling: No allocations, pure computation. Waypoint interpolation in LCh space. Shortest-path hue wrapping. Smoothstep easing (cubic polynomial, not transcendental)"

**Key Technical Details:**
- Parameter domain: t ∈ [0, 1] (curve parameter)
- Easing function: smoothstep (cubic polynomial)
- Interpolation space: LCh (cylindrical OKLab)
- Hue handling: shortest-path wrapping

**Sources:**
- `DevDocs/PRD.md` §3.3, §4
- `DevDocs/standards/ARCHITECTURE.md` (Journey Sampling)

**Paper Implication:** Derivatives ∂L/∂t, ∂C/∂t, ∂h/∂t are with respect to curve parameter, not perceptual arc-length. Perceptual velocity varies with Bézier control point placement. Add clarification note.

**Implementation Status:** See §2 for concrete algorithm in `004-incremental-creation/` - first implementation showing feasibility.

---

### 1.3 Task 005: Performance Metrics

**Verified Metrics:**

| Metric | Value | Configuration |
|--------|-------|---------------|
| Per-color generation time | ~180 ns | Single invocation |
| Throughput (single-threaded) | 5.2M colors/s | M1 Max, Clang 15, -O3 |
| Range operation (100 colors) | ~0.019 ms | C core, gcc -O2 |
| Range operation (1000 colors) | ~0.191 ms | C core, gcc -O2 |
| Working set memory | < 64 KB | 3 anchors, defaults |
| Memory per call | ~24 bytes | Stack-only allocation |
| Scaling factor | Linear | Per additional anchor |
| Multi-threaded performance | 117K ops/s | 100 threads |

**Hardware Context:**
- Platform: Apple M1/M1 Max
- Compiler: Clang 15 (primary) / gcc -O2
- Optimization: -O3 for production
- Execution: Single-threaded baseline
- Architecture: 64-bit ARM

**Sources:**
- `performance-analysis-reports/baseline-performance-report.md`
- `performance-analysis-reports/chunk-size-benchmark-report.md`
- `performance-analysis-reports/thread-safety-review.md`
- `README.md` (Performance Claims)

**Paper Recommendation:** Replace "5.6 million colors per second" claim with contextualized table showing hardware, compiler, and configuration details. Include note about linear scaling.

---

### 1.4 Task 006: API Seed Behavior

**Finding:** Seed does NOT implicitly enable variation. Variation must be explicitly enabled.

**Implementation Behavior:**

```
variation.enabled = true + seed → deterministic variation
variation.enabled = true + no seed → implementation-defined (default seed or entropy)
variation.enabled = false → deterministic base journey (seed ignored)
```

**API Structure (from README.md):**
```
variation: VariationConfig
  - enabled: Bool (default: false)
  - dimensions: VariationDimensions (which axes to vary)
  - strength: VariationStrength
  - seed: UInt64 (deterministic seed)
```

**From PRD.md §7.2:**
> "Deterministic or undetermined variation:
>   - Provide a seed → variation is repeatable.
>   - Omit seed → implementation may pick a default fixed seed, or use entropy for 'shuffle session' semantics."

**Determinism Guarantee (Architecture.md):**
> "Seeded variation is reproducible. Given identical config and seed, output is byte-identical across platforms. No floating-point nondeterminism (no fma, no IEEE rounding issues). Variation is fully seeded (no true randomness)."

**Sources:**
- `DevDocs/PRD.md` §7.2
- `DevDocs/standards/ARCHITECTURE.md` (Determinism)
- `README.md` (API Reference)

**Paper Implication:** Approach B (explicit variation flag) is correct. Current paper text may imply seed alone enables variation—clarify three-state behavior.

---

### 1.5 Task 008: Limitations Section

**Documented Limitations (from RELEASENOTES.md):**

| ID | Limitation | Impact | Mitigation |
|----|------------|--------|------------|
| L-001 | Delta enforcement overhead (~6×) | Performance | OKLab conversions required |
| L-002 | O(n) individual index access | Scalability | Batch operations preferred |
| L-003 | Fixed delta parameters (0.02-0.05) | Flexibility | Values chosen for perceptual validity |
| L-004 | Maximum ΔE best-effort at boundaries | Quality | Up to 5% may exceed threshold |
| L-005 | Binary search monotonicity assumption | Robustness | Edge cases in complex journeys |
| L-008 | High index precision degradation (>1M) | Scale | Float precision limits |
| L-010 | Iterator not thread-safe | Concurrency | Per-iterator, journey is thread-safe |

**Index Precision Guarantees (from spec.md):**

| Range | Status | Perceptual Error |
|-------|--------|------------------|
| 0 to 1M | Full precision guaranteed | <0.02 ΔE |
| 1M to 10M | Warning range | 0.02-0.10 ΔE |
| Beyond 10M | Not recommended | Undefined |

**Additional Context Limitations:**

1. **OKLab Recency:** Color space developed 2020 (Ottosson blog post), lacks 45+ years validation history of CIELAB (1976)
2. **Perceptual Thresholds:** Δ_min ≈ 0.02, Δ_max ≈ 0.05 are engineering heuristics, not peer-reviewed standards
3. **Fast Cube Root Trade-off:** ~1% error for 3-5× speed (documented in Part 2.1)
4. **Context Independence:** No special handling for brand colors, memory colors, or accessibility modes

**Sources:**
- `RELEASENOTES.md` (Known Issues & Limitations)
- `DevelopmentSpecSprints/004-incremental-creation/spec.md` (Precision Guarantees)
- `README.md` (OKLab Context)

**Paper Recommendation:** Use for §1.6 and §12. Frame as honest engineering trade-offs with documented rationale.

---

### 1.6 Task 009: OKLab Recency Acknowledgment

**OKLab Context:**

**Origin:**
- Developed: 2020 by Björn Ottosson
- Publication: Blog post, not peer-reviewed journal
- Purpose: Graphics and image processing applications
- Validation: Industry adoption, not academic longevity

**Advantages Over CIELAB:**
- Consistent brightness across hue wheel
- Reliable chroma behavior
- Predictable contrast
- No "muddy midpoints"
- Better hue linearity
- Simpler computation

**Implementation Details (Architecture.md):**
> "OKLab Math: 3-stage pipeline (RGB → LMS → LMS' → OKLab). Fully inlined, no function call overhead. Precomputed matrices (constants)."

**Precision (spec.md):**
> "Double precision OKLab conversions: All internal color space conversions use IEEE 754 double precision (64-bit). Standard library cbrt(): Cube root calculations use cbrt() from C standard library."

**Industry Adoption Evidence:**
- CSS Color 4 specification mentions
- Design software integration
- Modern gamut support (DCI-P3, Rec. 2020)
- Growing developer ecosystem

**Sources:**
- `README.md` (OKLab Color Space)
- `DevDocs/PRD.md` (Industry Context)
- `DevDocs/standards/ARCHITECTURE.md` (Implementation)
- `DevelopmentSpecSprints/004-incremental-creation/spec.md` (Precision)

**Paper Recommendation:** Section §2.2.1 should acknowledge:
1. OKLab's recency (2020 vs CIELAB 1976)
2. Chosen for practical software performance and demonstrated uniformity
3. Specification formalism is color-space agnostic (could port to future spaces)
4. Trade-off: modern performance vs long-term validation

---

### 1.7 Task 010: Gamut Management Context Nuance

**Current Implementation Priority (delta-algorithm.md):**

> "Resolution Strategy (Priority Order):
> 1. Prefer Minimum ΔE ≥ 0.02 over maximum ΔE ≤ 0.05
> - Rationale: Perceptual distinctness > avoidance of perceptual jumps"

**Gamut Fallback (delta-algorithm.md):**
> "Gamut Mapping Fallback: If constraint still unsatisfied, apply perceptual-preserving gamut mapping. Desaturate color toward sRGB boundary while maintaining hue and lightness."

**Hierarchy:** Hue > Lightness > Chroma (when resolving conflicts)

**Global Constraints (PRD.md §4.6):**
> "Avoid unreadable dark-on-dark or light-on-light combinations in typical UI contexts. Avoid ultra-bright spikes unless explicitly configured. Respect contrast levels derived from OKLab distance."

**Context NOT Addressed:**
- Brand color preservation (no pre-validation guidance)
- Memory colors (skin, sky, grass) special handling
- Accessibility modes (colorblind variants)
- Cultural color associations
- Domain-specific gamut priorities

**Sources:**
- `DevelopmentSpecSprints/004-incremental-creation/delta-algorithm.md`
- `DevDocs/PRD.md` §4.6

**Paper Recommendation:** Add nuance to §8.4:
1. Hierarchy is for general-purpose UI design
2. Brand colors may require zero modification (pre-validate anchors)
3. Memory colors may need different hierarchy
4. Future work: Context-aware gamut mapping

---

### 1.8 Task 013: Novelty Positioning

**What Color Journey Implements:**

**Core Features (PRD.md):**
1. Single-anchor mood-based expansion (lightness-weighted directional)
2. Multi-anchor interpolation in OKLab
3. Five perceptual dynamics (lightness, chroma, contrast, vibrancy, temperature)
4. Three loop modes (open, closed, ping-pong)
5. Deterministic variation layer
6. Waypoint-based journey design with smoothstep easing

**Unique Formalization (Architecture.md):**
1. Designed waypoints with non-uniform hue distribution
2. Easing curves (smoothstep) for natural pacing
3. Chroma envelopes following parametric curves
4. Lightness waves for visual interest
5. Mid-journey boosts controlled by vibrancy parameter
6. Shortest-path hue wrapping

**NOT Novel (Standard Techniques):**
- Color palette generation from single anchor
- OKLab color space usage
- Perceptual contrast enforcement
- Bézier curve interpolation

**Sources:**
- `DevDocs/PRD.md` (Feature Set)
- `DevDocs/standards/ARCHITECTURE.md` (Design Details)

**Paper Recommendation:** Position novelty as:
- ✗ "First palette generator" or "first to use OKLab"
- ✓ "Formalizing lightness-weighted directional expansion in perceptual space"
- ✓ "Systematic journey metaphor with explicit mood dynamics"
- ✓ "Rigorous mathematical specification of informal design tool features"
- ✓ "Novel combination: continuous Bézier path + discrete sampling + perceptual constraints + mood expansion"

---

## 2. Incremental Creation Implementation

**Sprint:** 004-incremental-creation  
**Status:** ✅ Implemented & Merged (December 9, 2025)  
**Source Code:** `SourceCode/CColorJourney/ColorJourney.c` (lines 621-721)

This is the **core reference implementation** of the single journey with incremental steps referenced in the paper.

**Important Context:**
- This is a **first implementation** - a concrete working prototype
- Demonstrates what is possible and establishes baseline requirements
- Needs refinement and improvement based on usage and evaluation
- Source code provides illuminating reference for algorithm development
- Not claimed as the definitive or perfect algorithm
- Validates feasibility and informs paper specification

**Value for Paper:**
- Proves the delta range algorithm (0.02-0.05 ΔE) is implementable
- Provides concrete performance characteristics (O(n) index access)
- Shows real trade-offs (distinctness vs smoothness priority)
- Documents fallback strategies for edge cases
- Serves as validation that specification is grounded in working code

### 2.1 API Design

**C API:**
```c
// Get single color by index
CJ_RGB cj_journey_discrete_at(CJ_Journey journey, int index);

// Get range of colors (batch operations)
void cj_journey_discrete_range(CJ_Journey journey, int start, int count, CJ_RGB* out_colors);

// Fixed spacing constant
#define CJ_DISCRETE_DEFAULT_SPACING 0.05f
```

**Swift API:**
```swift
// Index access
func discrete(at index: Int) -> ColorJourneyRGB

// Range access
func discrete(range: Range<Int>) -> [ColorJourneyRGB]

// Subscript convenience
subscript(index: Int) -> ColorJourneyRGB { get }

// Lazy sequence for streaming
var discreteColors: AnySequence<ColorJourneyRGB>
```

### 2.2 Position Calculation Algorithm

**Deterministic Index Mapping:**
```c
static float discrete_position_from_index(int index) {
    if (index < 0) return 0.0f;
    float t = fmodf((float)index * CJ_DISCRETE_DEFAULT_SPACING, 1.0f);
    return t;
}
```

**Key Properties:**
- Fixed position spacing: 0.05 → ~20 colors per full journey cycle
- Modulo wrapping: creates infinite cyclic sequence
- Deterministic: same index always maps to same position
- Closed loop topology only (no open/ping-pong/Möbius in this feature)

### 2.3 Delta Range Enforcement Algorithm

This is the **concrete implementation** of perceptual constraints in the paper.

**Constraints:**
- **Minimum ΔE:** 0.02 (ensures sufficient perceptual distinctness)
- **Maximum ΔE:** 0.05 (prevents excessive perceptual jumps)
- **Color Space:** All measurements in OKLab
- **Measurement:** Euclidean distance in OKLab: `sqrt((L2-L1)² + (a2-a1)² + (b2-b1)²)`

**Algorithm Steps:**

1. **Compute base color** at position `t = (index × 0.05) % 1.0` in OKLab space
2. **Calculate ΔE(base, previous)** where previous = color at index−1
3. **If ΔE < 0.02 (too similar):**  
   → Adjust position forward (increase t) until ΔE ≥ 0.02
4. **If ΔE > 0.05 (too different):**  
   → Adjust position backward (decrease t) until ΔE ≤ 0.05
5. **If constraints conflict:**  
   → Prefer minimum ΔE ≥ 0.02 over maximum ≤ 0.05  
   → Rationale: Perceptual distinctness > smoothness
6. **Apply standard contrast enforcement** (FR-002) after delta adjustment
7. **Return** final adjusted position and computed color

**Exhaustion and Fallback Strategy:**

When local OKLab region is saturated:

1. **Search Bounds:** Limit adjustment to ±0.10 in t space (~2 position steps)
2. **Modulo Wrapping:** If adjustment exceeds [0.0, 1.0], wrap via `fmod(t, 1.0)`
3. **Soft Chroma Reduction:** Reduce chroma by 10-20%, preserve hue/lightness, retry
4. **Gamut Fallback:** Apply full gamut mapping (desaturate to sRGB boundary)
5. **Guaranteed Termination:** After 3 iterations, accept best-effort (ΔE ≥ 0.01, relaxed)

**Relationship to Contrast (FR-002):**
- FR-002: Minimum contrast enforcement (user-configured: LOW/MEDIUM/HIGH)
- FR-007: Delta Range Enforcement (fixed 0.02–0.05 ΔE)
- When both apply: enforce intersection (tighter bounds)
- Example: MEDIUM contrast [0.04–0.10] ∩ delta range [0.02–0.05] = [0.04–0.05]

**Paper Implication:** This algorithm directly implements the perceptual constraints discussed in §4 and §6. The priority (distinctness > smoothness) validates paper claims as feasible and demonstrates one working approach.

**Note on Algorithm Evolution:** This represents Sprint 004's approach. Future refinements may adjust thresholds (0.02-0.05), search strategies, or fallback priorities based on production usage patterns and perceptual evaluation.

### 2.4 Performance Characteristics

| Operation | Complexity | Implementation |
|-----------|------------|----------------|
| `discrete_at(index)` | O(n) where n = index | Must compute contrast chain |
| `discrete_range(start, count)` | O(start + count) | More efficient for batches |
| Memory per call | ~24 bytes | Stack-only, no heap allocations |
| Cycle length | ~20 colors | Before wrapping to position 0.0 |

**Key Trade-off:** O(n) index access for O(1) memory usage.

**Sources:**
- `DevelopmentSpecSprints/004-incremental-creation/spec.md`
- `DevelopmentSpecSprints/004-incremental-creation/README.md`
- `DevelopmentSpecSprints/004-incremental-creation/SourceCode/CColorJourney/ColorJourney.c`

### 2.5 What the Source Code Illuminates

The 004-incremental-creation source code provides concrete evidence for several paper claims:

**For §4 (Perceptual Constraints):**
- Shows actual OKLab distance calculations in code
- Demonstrates binary search for constraint satisfaction
- Reveals edge cases (exhaustion, wrapping, fallback)
- Validates that 0.02-0.05 ΔE range is computationally tractable

**For §6 (Mood Dynamics):**
- Position calculation shows how t-parameter maps to journey
- Demonstrates interaction between fixed spacing and perceptual constraints
- Shows contrast chain dependency (why index access is O(n))

**For §8 (Gamut Management):**
- Implements concrete fallback strategy: search → wrap → desaturate → accept
- Shows how priority enforcement works in practice
- Demonstrates guaranteed termination (3 iterations + best-effort)

**For §10 (API Design):**
- Validates subscript/index access pattern is implementable
- Shows range access optimization strategy
- Demonstrates lazy sequence integration (Swift)

**For §12 (Limitations):**
- Proves O(n) complexity is inherent (must compute contrast chain)
- Shows where precision issues may arise (float accumulation)
- Documents performance trade-offs (memory vs computation)

**Broader Project Insights:**
- Working C implementation demonstrates specification is achievable
- Test suite (56 tests) validates determinism guarantees
- Performance benchmarks establish realistic expectations
- Error handling patterns show "return black" strategy in practice
- Swift wrapper demonstrates cross-language integration patterns

**Refinement Opportunities Identified:**
- Search radius (±0.10 in t space) may need tuning
- Chroma reduction percentage (10-20%) is heuristic
- Best-effort threshold (0.01 ΔE relaxed) needs perceptual validation
- Iteration limit (3) may be too conservative or too lenient

---

## 3. Algorithm Precision Trade-offs

**Fast Cube Root Optimization:**

From README.md:
> "Fast Cube Root: Uses bit manipulation + Newton-Raphson for ~1% error, 3-5x speedup"

From Architecture.md:
> "Perceptually invisible error. Consistent across platforms. Performance vs Accuracy: ~1% error for 3-5x speed gain. Trade-off acceptable because error is invisible to perception."

**C vs WASM Implementation Differences (ALGORITHM_COMPARISON_ANALYSIS.md):**

| Aspect | C Core | WASM (Reference) |
|--------|--------|------------------|
| Cube Root | `float` fast_cbrt (~1% error) | `double` cbrt (IEEE 754) |
| Precision | 32-bit float (~7 digits) | 64-bit double (~15 digits) |
| Chroma Boost | `1 + v * (1 - 4*(t-0.5)²)` | `1 + v * 0.6 * max(0, 1 - |t-0.5|/0.35)` |
| Periodic Pulse | None | `1 + 0.1 * cos(i * π/5)` for 20+ colors |
| Discrete Spacing | Fixed 0.05 per index | Adaptive (count-based) |
| Contrast Loop | Single-pass | Iterative (up to 5 passes) |

**Paper Implication:** Error compounds through color pipeline. Fast cube root is acceptable per documented rationale, but §12 limitations should mention precision trade-offs.

**Sources:**
- `README.md` (Performance Features)
- `DevDocs/standards/ARCHITECTURE.md` (Optimization Details)
- `DevDocs/archived/ALGORITHM_COMPARISON_ANALYSIS.md`

---

## 4. Perceptual Quality Validation

**Achieved Contrast Thresholds (perceptual-quality-evaluation.md):**

| Contrast Level | Required Min ΔE | Achieved Min ΔE | Success Rate |
|----------------|-----------------|-----------------|--------------|
| LOW | ≥0.02 | 0.021 | 98.6% |
| MEDIUM | ≥0.10 | 0.101 | 98.6% |
| HIGH | ≥0.15 | 0.151 | 98.6% |

**Quality Metrics:**
- 27.4% improvement in perceived distinctness
- 98.6% of adjacent colors rated "clearly distinct"
- 0% "colors too similar" issues (eliminated)
- 8.2/10 simulated user satisfaction score

**Distinctness Classification:**

| ΔE Range | Classification | Description |
|----------|----------------|-------------|
| < 0.01 | Imperceptible | Cannot distinguish |
| 0.01-0.02 | Barely Noticeable | Just noticeable difference (JND) |
| 0.02-0.05 | Noticeable | Clearly different |
| 0.05-0.10 | Obvious | Distinctly different |
| > 0.10 | Very Obvious | Strongly contrasting |

**Sources:**
- `DevelopmentSpecSprints/004-incremental-creation/perceptual-quality-evaluation.md`

**Paper Implication:** Threshold Δ_min ≈ 0.02 has concrete implementation validation. Use this for "engineering heuristic" justification in §4. Note: Simulated evaluation, not formal user study.

---

## 5. Determinism Guarantees

**Platform Independence (Architecture.md):**
> "Given identical config and seed, output is byte-identical across platforms. No floating-point nondeterminism (no fma, no IEEE rounding issues). Variation is fully seeded (no true randomness)."

**Per-Call Determinism (spec.md):**
> "Deterministic: same index always returns same color across calls. IEEE 754 floating-point guarantees."

**Implications:**
- Reproducible builds across macOS, Linux, Windows
- No hardware-specific behavior (SIMD disabled for determinism)
- Unit tests verify byte-identical output
- Variation uses seeded PRNG (not OS entropy)

**Sources:**
- `DevDocs/standards/ARCHITECTURE.md` (Determinism)
- `DevelopmentSpecSprints/004-incremental-creation/spec.md`

---

## 6. Thread Safety Model

**Concurrent Access (thread-safety-review.md):**
> "Conclusion: The incremental API is SAFE for concurrent reads from multiple threads."

**Safe Operations:**
- Concurrent calls to `discrete(at:)` with same or different indices
- Concurrent calls to `discrete(range:)` with distinct output buffers
- Creating multiple independent lazy sequence iterators

**Constraints:**
- Journey handle must remain valid during concurrent access
- Iterators themselves are NOT thread-safe (per-iterator state)
- No write operations during concurrent reads

**Performance:** 117K ops/second with 100 threads

**Sources:**
- `performance-analysis-reports/thread-safety-review.md`

---

## 7. Memory Model

**Architecture (Architecture.md):**
> "Memory: O(1) for continuous sampling, ~2KB for discrete palette. Stack-only allocation: ~24 bytes per call."

**Stateless Design (spec.md):**
> "No persistent state - Each call is independent. Contrast chain built on-demand - Recomputed for each index access."

**Memory Characteristics:**
- No heap allocations during sampling
- Working set < 64 KB (3 anchors, default config)
- Linear scaling per additional anchor
- Cache-friendly sequential access

**Trade-off:** O(n) index access (recompute contrast chain) for O(1) memory.

**Sources:**
- `DevDocs/standards/ARCHITECTURE.md` (Memory)
- `DevelopmentSpecSprints/004-incremental-creation/spec.md`

---

## 8. Evidence Summary by Paper Section

| Paper Section | Key Evidence | Source Documents |
|--------------|--------------|------------------|
| §1 Introduction | Limitations catalog, OKLab context | RELEASENOTES.md, spec.md |
| §2 Perceptual Foundations | OKLab implementation, precision | README.md, Architecture.md, spec.md |
| §3 Route Definition | Journey concepts, waypoint design | PRD.md, Architecture.md |
| §4 Perceptual Constraints | **Delta range algorithm (0.02-0.05 ΔE)**, velocity | **004-incremental-creation/spec.md**, PRD.md, Architecture.md, perceptual-quality-evaluation.md |
| §6 Mood Dynamics | Dynamics specification | PRD.md §4, Architecture.md |
| §7 Loop Strategies | Loop modes (Möbius NOT found), closed loop | PRD.md §6, **004-incremental-creation/spec.md** |
| §8 Gamut Management | Priority hierarchy, fallback, exhaustion strategy | delta-algorithm.md, PRD.md §4.6, **004-incremental-creation/spec.md** |
| §9 Variation & Determinism | Seed behavior, byte-identical output | PRD.md §7.2, Architecture.md |
| §10 API Design | Performance metrics, API structure, **incremental API** | baseline-performance-report.md, chunk-size-benchmark-report.md, Architecture.md, **004-incremental-creation/** |
| §12 Limitations & Future | All documented limitations, O(n) index access | RELEASENOTES.md, spec.md, **004-incremental-creation/spec.md** |

---

## 9. Research Gaps

Items referenced in paper but NOT found in implementation documentation:

| Paper Claim | Status | Action Required |
|------------|--------|-----------------|
| §7.4 Möbius Loop | Not implemented | Verify if theoretical or add implementation evidence |
| §6.3 Perceptual Velocity Formula | Not explicit | Derive from smoothstep implementation |
| §4.1 ΔE ≈ 2.0 as JND threshold | No source cited | Add literature reference (Mahy et al., MacAdam) |
| §4.3 ΔE ≈ 5.0 coherence threshold | No source cited | Add literature reference or clarify as heuristic |
| §8.3-8.4 Hierarchy rationale | Not justified | Add design decision documentation |
| 5.6M colors/s claim | Inconsistent | Standardize to 5.2M with context |

---

## 10. Source Document Index

### Primary Technical Specifications
1. **PRD.md** - Product Requirements Document (full system spec)
2. **ARCHITECTURE.md** - Two-layer architecture, design decisions
3. **spec.md** - Incremental creation algorithm specification
4. **delta-algorithm.md** - Perceptual constraint enforcement

### Implementation Source Code
5. **004-incremental-creation/SourceCode/** - Actual C/Swift implementation
6. **ColorJourney.c** - Core C implementation (lines 621-721)
7. **ColorJourneyClass.swift** - Swift wrapper with lazy sequences
8. **004-incremental-creation/README.md** - Implementation overview
9. **004-incremental-creation/quickstart.md** - Usage guide

### Performance & Quality Reports
10. **baseline-performance-report.md** - Core performance metrics
11. **chunk-size-benchmark-report.md** - Batch operation benchmarks
12. **thread-safety-review.md** - Concurrency analysis
13. **perceptual-quality-evaluation.md** - Quality validation metrics
14. **ALGORITHM_COMPARISON_ANALYSIS.md** - C vs WASM comparison

### User Documentation
15. **README.md** - Product overview, features, API reference
16. **RELEASENOTES.md** - Version history, known limitations
17. **OUTPUT_PATTERNS.md** - Usage patterns
18. **QUICK_REFERENCE.md** - API quick reference
19. **EXECUTIVE_SUMMARY.md** - High-level overview

---

## 11. Usage Guide

### For Paper Revision Tasks

**When working on a specific task (003-017):**
1. Consult §1 (Implementation Evidence) for exact quotes and sources
2. See §2 (Incremental Creation) for concrete algorithm implementation
3. Cross-reference §8 (Evidence Summary) for related paper sections
4. Check §9 (Research Gaps) for missing information
5. Use §10 (Source Index) to locate full documents

**When drafting paper sections:**
1. Use §1 evidence with proper attribution
2. Reference §2 for concrete algorithm implementation
3. Integrate cross-cutting details from §3-7
4. Acknowledge gaps from §9 explicitly
5. Add [CITATION NEEDED] for external literature

**Citation Format (Harvard):**
- Internal docs: (Color Journey PRD 2025)
- Architecture: (Color Journey Architecture 2025)
- Performance: (Color Journey Performance Analysis 2025)
- External: (Ottosson 2020), (Fairchild 2013), etc.

---

## Bibliography

### Implementation Documentation

Color Journey Engineering Team (2025). *Product Requirements Document (PRD)*. Internal technical specification.

Color Journey Engineering Team (2025). *Architecture Standards*. Internal design documentation.

Color Journey Engineering Team (2025). *Incremental Creation Specification*. Development sprint documentation.

Color Journey Engineering Team (2025). *Baseline Performance Report*. Performance analysis documentation.

Color Journey Engineering Team (2025). *Perceptual Quality Evaluation*. Quality assurance documentation.

### External References (for paper citations)

Ottosson, B. (2020). *A perceptual color space for image processing*. [Blog post]. https://bottosson.github.io/posts/oklab/

[CITATION NEEDED: CIELAB foundational papers]  
[CITATION NEEDED: JND thresholds (MacAdam, Mahy et al.)]  
[CITATION NEEDED: Perceptual uniformity validation]

---

**Document Status:** Consolidated with Implementation Evidence  
**Quality Level:** Production-ready reference  
**Implementation Context:** Sprint 004 represents first working prototype - validates feasibility, informs refinement  
**Next Action:** Use as evidence base for paper revision tasks 003-017

**Key Insight:** Paper specification is grounded in working code that demonstrates algorithms are implementable, while acknowledging room for optimization and refinement based on production usage.
