# Related Work Addendum: DEMOCRITUS and Implications for CMS “Deepen”

**Document:** Related Work Addendum (DEMOCRITUS)  
**Applies to:** Continuity Memory System (CMS) / PaperKit middleware  
**Date:** 2025-12-23  
**Status:** Draft (drop-in + spec deltas)

---

## 1) What DEMOCRITUS contributes (high-signal)
DEMOCRITUS presents a multi-module system for building structured causal models from unstructured text. The key relevance to CMS is not “causal graphs”, but the **systems pattern**:
- break the work into staged modules
- accept that LLM calls dominate cost
- use explicit utility / active exploration to decide what to expand next
- treat outputs as structured hypotheses with governance and validation requirements

This supports CMS’s design stance that memory is **active structure**, not passive storage.

---

## 2) Directly reusable insights for CMS

### 2.1 Modular pipeline beats “one prompt”
DEMOCRITUS frames value as the composition of multiple bounded modules (expansion → generation → extraction → refinement → storage), rather than relying on a single LLM step.

**CMS mapping**
- Capture pipeline: extract typed thoughts from runs/events
- Consolidation (“dreaming”): merge, supersede, prune
- Retrieval: compose + rerank + invariants
- Deepen: bounded iterative research loop (GAM-style), now with explicit selection logic

### 2.2 Cost dominance of LLM calls → budget Deepen aggressively
DEMOCRITUS reports that LLM-heavy modules dominate latency/cost compared to downstream graph work.

**CMS mapping**
- Make Deepen a budgeted escalation path:
  - `max_iterations`
  - `max_evidence_pages`
  - `max_total_tokens`
  - `max_wall_time` (optional)
- Invest in cheap prefilters (typed retrieval, operator gates, supersession invariants) because they save LLM calls.

### 2.3 Active exploration with a utility function
DEMOCRITUS argues naive traversal wastes budget and proposes selecting expansions via a utility score U(t) combining novelty, depth penalty, centrality, and task conditioning.

**CMS mapping**
Introduce a **Deepen Planner** that selects what to re-read/expand next using an explicit utility score over candidate targets:
- episodes (recent vs relevant)
- evidence refs (citations, tool outputs)
- entities (concept hubs)
- open threads (active objectives)

This is a principled alternative to “retrieve top-k similar pages and hope”.

### 2.4 Hub–fringe robustness heuristic
They observe graphs often produce hubs + many low-degree nodes and hypothesise this structure can contain noise (hallucinations stay peripheral).

**CMS mapping**
A similar robustness signal exists in CMS:
- high support count / multi-episode reinforcement → “hub-like” memories
- one-off unverified claims → “fringe”
Use this to:
- calibrate confidence
- drive pruning
- prioritise what to reconfirm

### 2.5 Governance warning: coherent structure can still be wrong
DEMOCRITUS explicitly notes hallucinations can produce coherent but incorrect structure.

**CMS mapping**
Reinforces:
- evidence pointers in precision mode
- epistemic gating (“know vs verify”)
- explicit hypothesis tagging

---

## 3) Drop-in paragraph (Related Work)
> **Active structure building under budgets (DEMOCRITUS).** DEMOCRITUS demonstrates a multi-module pipeline that converts unstructured text into structured representations via staged generation, extraction, refinement, and storage. While its target is causal graphs, the transferable insight for CMS is architectural: LLM calls dominate cost, so systems should be modular, budget-aware, and use explicit selection logic to allocate expensive expansions. DEMOCRITUS proposes active exploration using a utility score to prioritize what to expand next, and emphasises that coherent structure does not guarantee truth, motivating governance mechanisms and evidence-based validation. This supports CMS’s design of a bounded “Deepen” mode and suggests adding a Deepen Planner that selects episodes/evidence to revisit via an explicit utility function rather than naive top-k similarity.

---

## 4) Spec Delta: Add a Deepen Planner (utility-scored selection)

### 4.1 New component
**Deepen Planner**: chooses next deepening targets (episodes/evidence/entities/threads) under a budget.

### 4.2 Candidate target types
- `episode`: episodic memory slice; has recency, entities, evidence pointers
- `evidence_ref`: a citation / tool output / file locator
- `entity`: canonical slug; has degree and support counts
- `thread`: open thread ID; has urgency, last_touched, owner

### 4.3 Utility score (default)
Let candidates be c ∈ C. Define:

U(c) = w_recency * R(c)  
     + w_task * T(c)  
     + w_risk * K(c)  
     + w_novelty * N(c)  
     + w_support * S(c)  
     - w_cost * Cost(c)

Where:
- R(c): recency (decays by age; high for recent episodes)
- T(c): task alignment (mentions current entities, open_thread_ids, constraints)
- K(c): risk/volatility (time_sensitive/high_risk boosts; precision mode boosts)
- N(c): novelty (low local density in embedding space or “not seen before”)
- S(c): support (multi-episode reinforcement; optionally inverted to prioritise weakly supported claims needing reconfirmation)
- Cost(c): estimated token cost (page size, tool latency, model cost)

### 4.4 Selection rule
- Pick top-M candidates by U(c) each iteration (M small; eg 1–3).
- Enforce diversity: at least one from evidence/page-store when precision mode is active.
- Stop when:
  - completeness heuristic passes OR
  - max_iterations reached OR
  - budget exhausted.

### 4.5 Outputs
Each iteration appends to the audit trail:
- selected candidates + U(c) breakdown
- pages fetched / evidence refs resolved
- updated Context Bundle with citations and rationale

---

## 5) Suggested evaluation fixtures for Deepen Planner
- **DP-01**: precision query with time-sensitive claim → planner selects evidence first
- **DP-02**: multiple entities mentioned → planner selects one per iteration (diversity)
- **DP-03**: conflict present (contradicts edge) → planner prioritises reconfirmation
- **DP-04**: very long page-store pages → planner avoids high-cost pages unless required

---

## Reference
- *DEMOCRITUS* (arXiv:2512.07796v1).
