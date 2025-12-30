

# Section 2 Review (Perceptual Foundations)

This is PhD supervisor style feedback on the updated **Section 2** (Perceptual Foundations) as represented in `02_perceptual_foundations.tex`.

## Executive summary
Section 2 is moving in the right direction. The conceptual spine is clearer (perceptual geometry → practical working space → temporal perception → engineering implications), and the Hong + Nölle + temporal-perception integration is a strong backbone.

However, there are a small number of **blocking** issues (including a LaTeX compilation error), and several **high impact** revisions that will significantly improve defensibility for a sceptical technical reader.

---

## Must fix (blocking)

### 1) LaTeX compilation error: broken quote environment
There is an `\end{quote>` (with a `>`). That leaves the environment unclosed and will cause compilation errors.

**Fix:** change `\end{quote>` → `\end{quote}`.

### 2) Quote length and source quality
At points the argument relies on long quotations, including one that is a secondary summary of a primary source and then another quote from the primary source.

**Fix:** keep **one short quote** (ideally a single sentence) and paraphrase the remainder. Prefer citing the **primary** study for core claims.

---

## Major academic issues (conceptual / defensibility)

### 3) Riemannian manifold and metric tensor need the minimal “line element” definition
You invoke “Riemannian manifold” and “metric tensor” and then jump directly to a specific component (e.g., `g_{HH}` / hue circumference reasoning). That is efficient, but it reads as a *hand wave* unless you give the reader the minimal geometric scaffold.

**Add 2–3 lines** in the manifold subsection:

- State the core idea: local discrimination ellipsoids imply a **position-dependent quadratic form**.
- Write the canonical line element:
  - `ds^2 = d\mathbf{x}^\top g(\mathbf{x})\, d\mathbf{x}`
- Then say the hue-circle result is a special case: integrate the relevant component around a closed path at constant parameters.

This small insertion materially increases rigour per sentence.

### 4) “Euclidean impossibility” is currently overstated
The intuition is right: a single global 3D Euclidean coordinate system cannot make perceptual distance uniformly Euclidean everywhere without distortion.

But the wording risks an over-claim: mathematically-trained readers will immediately think about embeddings and will ask “impossible under what constraints?”

**Rephrase** to something like:

- “No single global Euclidean coordinate system in 3D can make perceptual distance everywhere equal to Euclidean distance without distortion.”
- “Therefore practical 3D colour spaces must accept nonuniformity, or treat distance as position-dependent (a metric).”

Keep the “720°” discussion as **intuition / consequence of nonuniformity**, not a literal topological statement.

### 5) Möbius connection needs a stronger caution label
The Möbius analogy is intriguing, but as written it can be attacked as a category slip (metric circumference and perceptual nonuniformity are not the same as orientation reversal).

**Fix:** explicitly label it as **analogy / design intuition**, not a derived theorem. If you intend a formal development later (e.g., `\S\ref{sec:mobius-mathematical}`), say so and keep this section modest.

### 6) OKLab pipeline should acknowledge sign-preserving cube root
Real implementations can see negative LMS values (especially outside gamut or due to transform behaviour). The OKLab reference uses sign-preserving cbrt.

**Fix:** add one sentence: you use the **standard sign-preserving cube root** as per the OKLab reference implementation.

This avoids later internal inconsistency when you discuss gamut and “unbounded” behaviour.

### 7) Performance claim is too specific without evidence
The “50–100 CPU cycles” line is fragile and architecture-dependent. It reads precise but is unlikely to be stable across targets.

**Fix options (choose one):**

- Remove the cycle count; keep an operation-level description (matrix multiplies + cbrt + affine transforms).
- Or move the cycle claim to an appendix with a tiny microbenchmark and caveats (compiler, CPU, flags).

---

## Structure and persuasion improvements (make the reader care)

### 8) Add a closing “therefore” paragraph at the end of Section 2
Section 2 does four big things: curvature, 720°/nonuniformity, OKLab as compromise, temporal sensitivity.

End the section with a short synthesis that makes the engineering consequences explicit:

- **Axioms for the engine:** distance is approximate; OKLab/OKLCh is the working space; perceptual change rate matters.
- **Tunable parameters:** `\Delta_{\min}`, `\Delta_{\max}`, channel weights (`w_L, w_C, w_H`), transition scaling.
- **Calibration plan:** what remains empirical (JND thresholds, temporal weights, domain-specific defaults).

Right now those points exist, but are dispersed.

### 9) Temporal section: add one bridge sentence before numeric weights
You introduce weights like `w_L = 10`, `w_C = 1`, `w_H \approx 1.5–2`. That can be plausible, but it reads chosen rather than motivated.

**Fix:** add one explicit modelling bridge:

- “We model temporal smoothness as a weighted path-length constraint in OKLab/OKLCh, where weights approximate relative JND sensitivity per channel under transition viewing.”

Even if provisional, stating the modelling step makes the choices interpretable.

---

## Minor but worthwhile edits

- In the colour space comparison table (“Excellent / Good / Low”), add a footnote explaining the axis basis (e.g., ΔE correlation, perceptual uniformity evidence, gradient behaviour) so it doesn’t read as subjective.
- Wherever you use saturation `S` vs chroma `C`, define coordinate conventions once and stick to them.
- Be consistent with page numbers when making quantitative claims (e.g., 58%, 10×, 12.65): if it’s precise, cite precisely.

---

## Supervisor verdict
The section is now **credible and close to solid**. Fix the LaTeX error, tighten the Euclidean wording, insert the minimal metric definition, caution the Möbius analogy, and de-risk the performance claim.

Once those are done, Section 2 will read as a defensible perceptual foundations chapter rather than an ambitious but attackable narrative.

---

## Optional: ready-to-paste rewrite snippets

### A) Minimal metric definition (insert near the first “Riemannian / metric tensor” mention)
> In practice, discrimination varies with location in colour space. This can be modelled by a position-dependent metric tensor `g(\mathbf{x})` that defines local perceptual distance via the line element `ds^2 = d\mathbf{x}^\top g(\mathbf{x})\, d\mathbf{x}`. Distances along specific directions (e.g., hue at fixed lightness and chroma) follow from the corresponding components of `g` integrated along a path.

### B) Safer Euclidean wording (replace stronger “impossibility” phrasing)
> There is no single global 3D Euclidean coordinate system that makes perceptual distance everywhere equal to Euclidean distance without distortion. Consequently, practical 3D colour spaces must accept nonuniformity, or treat distance as position-dependent by using a metric. The “720°” observation is best read as an intuition for this nonuniformity rather than a literal topological requirement.

### C) Temporal weights bridge (add immediately before choosing `w_L, w_C, w_H`)
> We treat temporal smoothness as a weighted path-length constraint in OKLab/OKLCh. The channel weights approximate relative JND sensitivity under transition viewing, so that visually dominant changes (notably in lightness) are penalised more strongly than less salient changes.