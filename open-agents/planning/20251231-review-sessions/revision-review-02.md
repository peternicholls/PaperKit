# Feedback on Chapter 2 Revision Approach

Yep, that “tab” write up is exactly the right kind of move: it turns Chapter 2’s opening from “Kong as the de facto textbook” into a properly triangulated foundation, with Kong kept for what it’s genuinely strong at (temporal / dynamic lighting). 

What to watch for:

## 1. The new source allocation is academically healthier

The mapping in your extraction (Byrne & Hilbert for foundations, Gao for CAT/von Kries maths, Hong for discrimination thresholds, Sekulovski for smoothness vs flicker, Kong for temporal non-uniformity) is coherent and defendable.

It also fixes a common examiner irritation: a thesis being used as the backbone for “basic field intro” when there are standard references available.

## 2. Two credibility “edges” to manage

A. Hong “2024” might actually be 2025 (check your bib metadata) | ✅ CHECKED

~~Your extracted PDF header reads like a reviewed preprint with Nov 2025 dating. If your bib says 2024, you risk looking sloppy even if the science is right. Make the bib match what you actually have in hand (year + venue + DOI + version if it’s a preprint). This is the kind of thing supervisors mark down fast.~~

B. Nölle / H2SI as a ResearchGate preprint

Using it is fine, but treat it as preprint evidence, not a settled “proof that ends the argument.” In prose: “Nölle et al. (preprint) propose…” rather than “Nölle et al. prove…” unless you can anchor the claim in something peer reviewed, or you’ve checked whether there’s a later journal version.

## 3. What to change in the Chapter 2 opening, conceptually

Your opening should do three jobs, in this order:

1.	Physics → perception gap
Use Byrne & Hilbert for the clean “$SPD \times SSR$ is not enough” motivation (and to define SPD/SSR without Kong).

2.	Why we need perceptual spaces (and what they can and cannot claim)
Bring in Hong for local discrimination structure (threshold ellipses / metric tensor framing), but immediately constrain it to the local regime.

3.	A deliberate caveat about global distance
Use Bujack to explicitly say “suprathreshold dissimilarity can violate additivity,” and then state your paper’s stance: you’re designing bounded step transitions, not claiming a globally correct geometry of perceived dissimilarity.

That makes your later choices feel “careful and honest,” not “sweeping and brittle.”

## 4. A couple of wording traps to avoid (even if technically defensible)
- Avoid “strong evidence that perceptual colour space is Riemannian.”
    Prefer “can be well modelled locally as Riemannian (near threshold)” with an explicit scope boundary.

- Avoid implying the $720^\circ$ / Möbius idea is “settled.”
    Frame it as “motivated by…” and “consistent with…” unless you’ve got multiple independent sources converging.

## 5. Practical bib and citation hygiene (so this doesn’t regress later)
- Use a consistent key scheme: byrne_hilbert2020, gao2020_vonkries, hong2025_wppm, sekulovski2007_smoothness, kong2021_temporal, bujack2022_nonriemannian.

- For anything that’s a preprint: include note = {preprint} and a stable URL/DOI if available.

- If you quote, keep it rare and purposeful. Most of Chapter 2 should be paraphrase + citation, otherwise it reads like an annotated bibliography.

## 6. What I’d ask you to double check next (fast wins)
- Confirm the exact numeric basis for the “$10:1$” claim (your own extraction even flags it as potentially coming from a figure or a different source). Don’t let a single spicy ratio sit there unsupported.

- Confirm Hong’s publication status/year so you don’t accidentally cite it as a 2024 journal paper when it’s a 2025 reviewed preprint.

---

# Partial Revision Review

I’ve gone through the compiled main.pdf you shared and focused on Chapter 2 plus any knock on effects elsewhere.

What’s now in good shape
- Chapter 2 reads cleanly and coherently overall, and the “principles → implications” structure is working.  ￼
- The hue weight range note is now present and justified (and importantly, framed as tunable and pending validation).  ￼
- Figure 2.2 is in place and matches the narrative ($wL=10$, $wC=1$, $wH=1.75$  shown as illustrative).  ￼
- The $720^\circ$ / “super importance of hue” mathematics checks out against the H2SI source: they explicitly give
$\frac{s_2(S=1)}{s_1}=4\sqrt{10}=12.65 \approx 4\pi = 720^\circ$
which is exactly the key claim you’re leaning on.  ￼

The two issues I’d fix immediately (they’re small but credibility critical)

## 1. Kong over reliance is still present (as a quoted block)

Your concern is valid: in §2.5 you still include a direct quote from Kong (2021) to summarise Sekulovski’s result.  ￼

Minimal fix (no restructuring needed):
- Keep Sekulovski et al. (2007) as the only quoted authority here.
- Convert the Kong quote into a non quoted supporting sentence or footnote, e.g. “Kong (2021, p.3) summarises Sekulovski’s finding as …”, without block quoting it. This keeps Kong as secondary commentary, not load bearing evidence.

## 2. Internal inconsistency: Appendix B.9 contradicts Chapter 2’s weights

In Chapter 2, you define the temporal weighting as $wL = 10.0$, $wC = 1.0$, $wH \approx 1.5–2.0$, with Figure 2.2 reinforcing that.  
￼
But in Appendix B.9, the “Typical Value” column says $wL = 1.0$, $wC \sim 1.2$, and $wh \sim 1.5–2.0$ (note also the inconsistent symbol $wh$ vs $wH$).  ￼

This is exactly the kind of thing a reviewer will spot and then doubt everything else.

Minimal fix:
- In Appendix B.9, change those “Typical Value” entries to match Chapter 2:
- $wL = 10.0$
- $wC = 1.0$
- $wH \approx 1.5–2.0$
- Rename $wh$ → $wH$ to match your main text notation.

## 3. One bibliographic red flag

Your references list includes “Kong, Xieyuan (2021)”.  ￼

Unless this is genuinely a different Kong than the one you mean, that looks like a BibTeX metadata error (author given name swapped/wrong). If you keep Kong at all, fix that entry because it’s an easy credibility hit.

## 4. One wording risk (not wrong, but likely to attract “overclaim” pushback)

In §2.1 and §2.2.1 you state, fairly strongly, that perceptual colour difference is “well modeled as a Riemannian manifold” / “strong evidence”.  
￼
Given your earlier discussion about non Riemannian findings, I’d expect reviewers to poke this. Minimal softening that keeps your argument intact is to consistently say “locally well approximated” (small step regime), which you already gesture toward later.  ￼

Next steps
- Please address the above four issues.
- Once done, recompile and share the updated main.pdf for a final review pass.
- After that, we can proceed to lock Chapter 2 for conceptual edits and create the snapshot.

You’ve anchored the 10:1 claim to the specific interpretation you’re willing to defend, and you’ve now added enough local context that it doesn’t read like a magic constant.

Given that, the only “trust” risk left isn’t the ratio itself — it’s consistency and provenance:

1) Consistency across the document (this is the one that bites)

Even if the 10:1 is correct and well explained in Chapter 2, you must ensure every other place that mentions the weights matches it.

From the PDF build you shared earlier, Appendix B.9 still looked inconsistent with Chapter 2 (it listed different “typical values”). That’s not a scientific disagreement — it’s just a doc bug that undermines confidence fast.

Action: make Appendix B.9 match Chapter 2’s settled values and notation (w_L = 10, w_C = 1, w_H ≈ 1.5–2.0, and w_H not wh).

2) Provenance statement (make the reader feel safe)

Where you state the ratio, one extra clause is usually enough:
	•	“We adopt 10:1 as a working engineering default in this paper, reflecting the reported threshold separation under the tested conditions; we treat it as calibratable for other displays, field sizes, and viewing contexts.”

That reassures readers you’re not overgeneralising.

3) Citation hygiene (primary vs secondary)

If your chapter currently uses Kong to summarise the 10:1 finding, that’s fine, but make sure the primary citation is always Sekulovski (and Kong becomes “as discussed by…”).

That way, even a reviewer who dislikes Kong can’t pull the rug out from under your key parameter.

If you paste the exact paragraph where you “settled” the 10:1 ratio (the final revised wording), I’ll do a very tight check for: (a) whether the claim is scoped correctly, and (b) whether the citations support exactly what the sentence says — without changing your structure.