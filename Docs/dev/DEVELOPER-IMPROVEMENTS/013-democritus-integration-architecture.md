# Democritus-Inspired Agent Architecture Integration

**Specification ID:** 013  
**Date:** 2025-12-27  
**Status:** Draft  
**Priority:** High  
**Category:** Core Architecture  
**Estimated Effort:** 80h  

---

## 1. Problem Statement

### 1.1 Current State

PaperKit's research agents (Librarian and Research Consolidator) follow a **linear research progression**:

```
Question → Search → Answer → Iterate
```

This approach, while functional, has limitations:
- **No structural understanding** of how research findings relate to each other
- **Equal exploration** of all topics, regardless of utility or relevance
- **No contradiction detection** when sources present conflicting findings
- **No visualization** of the research landscape
- **Linear budget consumption** without optimization

### 1.2 DEMOCRITUS Insights

The DEMOCRITUS research paper ([dev-docs/Democritus-agent-improvements/2512.07796.pdf](../Democritus-agent-improvements/2512.07796.pdf)) introduces revolutionary approaches to building Large Causal Models (LCMs) from LLM-generated content. Key innovations include:

> "LLMs are increasingly capable of producing rich causal narratives... However, using an LLM alone leaves us with a *laundry list* of disconnected fragments. Democritus aims to turn these fragments into structured *large causal models*."
> — Section 1, Introduction (p. 1)

Key technical components:
1. **Causal Triple Extraction** - Converting text into (subject, relation, object) triples
2. **Geometric Transformer (GT)** - Producing manifold embeddings that capture structural relationships
3. **Active Research Planning** - Using utility scores to prioritize exploration
4. **Multi-Scale Visualization** - Local neighborhoods + global manifold views

### 1.3 Integration Opportunity

The enhancement ideas document ([dev-docs/Democritus-agent-improvements/Democritus-insight-alignment-first-ideas.md](../Democritus-agent-improvements/Democritus-insight-alignment-first-ideas.md)) outlines specific integration patterns that align DEMOCRITUS capabilities with PaperKit's research workflow.

---

## 2. Proposed Architecture

### 2.1 Overview

Transform PaperKit's research agents from linear processors to **causal graph builders** with active research planning:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ENHANCED RESEARCH ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                    LIBRARIAN (Ellis) - Enhanced                  │ │
│  │                                                                   │ │
│  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐         │ │
│  │  │   Source     │──▶│   Causal     │──▶│  Research    │         │ │
│  │  │   Finding    │   │   Triple     │   │   Frontier   │         │ │
│  │  │              │   │   Extraction │   │   Planning   │         │ │
│  │  └──────────────┘   └──────────────┘   └──────────────┘         │ │
│  │                                                                   │ │
│  │  NEW CAPABILITIES:                                                │ │
│  │  • Extract causal relationships from sources                     │ │
│  │  • Compute research utility scores                               │ │
│  │  • Prioritize high-value exploration directions                  │ │
│  │  • Detect gaps via graph structure analysis                      │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                   │                                   │
│                                   ▼                                   │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │              RESEARCH CONSOLIDATOR (Alex) - Enhanced             │ │
│  │                                                                   │ │
│  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐         │ │
│  │  │   Causal     │──▶│Contradiction │──▶│  Coherent    │         │ │
│  │  │   Graph      │   │  Detection & │   │  Narrative   │         │ │
│  │  │  Building    │   │  Resolution  │   │  Synthesis   │         │ │
│  │  └──────────────┘   └──────────────┘   └──────────────┘         │ │
│  │                                                                   │ │
│  │  NEW CAPABILITIES:                                                │ │
│  │  • Build causal knowledge graphs during synthesis                │ │
│  │  • Detect and characterize contradicting claims                  │ │
│  │  • Generate multi-scale research visualizations                  │ │
│  │  • Identify research triangles (coherent mechanisms)             │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Core Components

#### 2.2.1 Causal Research Graph

Reference: [Democritus-insight-alignment-first-ideas.md, Section 1](../Democritus-agent-improvements/Democritus-insight-alignment-first-ideas.md#1-from-linear-research-to-causal-graph-construction)

```python
class CausalResearchGraph:
    """
    Build a causal knowledge graph during research.
    
    Based on DEMOCRITUS Module 4-style triple extraction.
    Reference: 2512.07796.pdf, Section describing Module 4
    """
    
    def __init__(self):
        self.causal_triples = []  # List of (subject, relation, object)
        self.topic_graph = nx.DiGraph()  # NetworkX graph
        self.research_frontier = PriorityQueue()  # Prioritized exploration
        self.source_mapping = {}  # Triple -> Source citation mapping
    
    def extract_causal_claims(self, paper_content: str, citation: str) -> List[Tuple]:
        """
        Extract causal relationships as triples from paper content.
        
        Relationship types align with DEMOCRITUS taxonomy:
        - causes, prevents, increases, decreases
        - influences, leads_to, moderates, correlates_with
        
        Args:
            paper_content: Text content from source
            citation: Harvard-style citation for attribution
            
        Returns:
            List of (subject, relation, object, citation) tuples
        """
        pass
    
    def compute_research_utility(self, topic: str) -> float:
        """
        Compute utility score for exploring a topic.
        
        Based on DEMOCRITUS Section 11: Active manifold building.
        Reference: Democritus-insight-alignment-first-ideas.md, Section 2
        
        Factors:
        - Centrality score (0.3): How connected is this topic?
        - Gap score (0.3): How much unknown territory?
        - Controversy score (0.2): Are there conflicting claims?
        - Recency score (0.2): Recent developments?
        """
        return (
            0.3 * self.centrality_score(topic) +
            0.3 * self.gap_score(topic) +
            0.2 * self.controversy_score(topic) +
            0.2 * self.recency_score(topic)
        )
```

#### 2.2.2 Active Research Planner

Reference: [Democritus-insight-alignment-first-ideas.md, Section 2](../Democritus-agent-improvements/Democritus-insight-alignment-first-ideas.md#2-active-research-frontier-the-big-win)

```python
class ActiveResearchPlanner:
    """
    Decides WHERE to spend research budget using utility scoring.
    
    Key insight from DEMOCRITUS: "Don't explore everything equally—use 
    utility scores." This contrasts with naive implementations that 
    "expand every topic to a fixed depth."
    Reference: 2512.07796.pdf, Introduction
    """
    
    def prioritize_next_query(
        self, 
        current_graph: CausalResearchGraph, 
        user_goal: str, 
        budget_remaining: int
    ) -> List[Tuple[float, str]]:
        """
        Select highest-utility research directions.
        
        Returns:
            List of (utility_score, query) tuples, sorted by utility
        """
        candidates = []
        
        for direction in self.get_frontier_questions(current_graph):
            utility = self.compute_utility(
                direction,
                current_graph=current_graph,
                user_goal=user_goal
            )
            candidates.append((utility, direction))
        
        return sorted(candidates, reverse=True)[:budget_remaining]
    
    def compute_utility(
        self, 
        question: str, 
        current_graph: CausalResearchGraph, 
        user_goal: str
    ) -> float:
        """
        Multi-factor utility scoring for research direction.
        
        Based on Democritus-insight-alignment-first-ideas.md:
        - Factor 1: Relevance to user's goal (0.30)
        - Factor 2: Information gain / novelty (0.25)
        - Factor 3: Structural importance - bridges clusters (0.20)
        - Factor 4: Citation impact (0.15)
        - Factor 5: Recency (0.10)
        """
        relevance = self.semantic_similarity(question, user_goal)
        novelty = self.novelty_in_embedding_space(
            question, 
            current_graph.get_embeddings()
        )
        bridge_score = self.bridges_clusters(question, current_graph)
        impact = self.get_citation_metrics(question)
        recency = self.temporal_relevance(question)
        
        return (
            0.30 * relevance +
            0.25 * novelty +
            0.20 * bridge_score +
            0.15 * impact +
            0.10 * recency
        )
```

#### 2.2.3 Contradiction Analyzer

Reference: [Democritus-insight-alignment-first-ideas.md, Section 4](../Democritus-agent-improvements/Democritus-insight-alignment-first-ideas.md#4-contradiction-detection--resolution)

```python
class ContradictionAnalyzer:
    """
    Find and characterize conflicting research findings.
    
    DEMOCRITUS strength: Handles conflicting claims gracefully.
    This is critical for academic synthesis where contradictions
    often indicate important research frontiers.
    """
    
    OPPOSING_RELATIONS = {
        'causes': ['prevents'],
        'increases': ['decreases'],
        'supports': ['contradicts'],
        'confirms': ['refutes']
    }
    
    def detect_contradictions(
        self, 
        causal_graph: CausalResearchGraph
    ) -> List[Dict]:
        """
        Find opposing causal claims in the research graph.
        
        Examples:
        - (A, increases, B) vs (A, decreases, B)
        - (A, causes, B) vs (A, prevents, B)
        
        Returns:
            List of contradiction dictionaries with:
            - subject, object, claim_1, claim_2, supporting_papers
        """
        contradictions = []
        
        for (subj, rel1, obj) in causal_graph.edges:
            opposing_rels = self.OPPOSING_RELATIONS.get(rel1, [])
            
            for rel2 in opposing_rels:
                if causal_graph.has_edge(subj, rel2, obj):
                    contradictions.append({
                        'subject': subj,
                        'object': obj,
                        'claim_1': {
                            'relation': rel1,
                            'papers': causal_graph.get_supporting_papers(subj, rel1, obj)
                        },
                        'claim_2': {
                            'relation': rel2,
                            'papers': causal_graph.get_supporting_papers(subj, rel2, obj)
                        }
                    })
        
        return contradictions
    
    def resolve_contradiction(self, contradiction: Dict) -> Dict:
        """
        Analyze WHY a contradiction exists.
        
        Resolution factors (per Democritus-insight-alignment-first-ideas.md):
        - Different experimental conditions?
        - Different populations studied?
        - Temporal effects (early vs late)?
        - Dosage/magnitude effects?
        - Methodological differences?
        
        Returns:
            Analysis dict with resolution insights
        """
        papers_1 = contradiction['claim_1']['papers']
        papers_2 = contradiction['claim_2']['papers']
        
        return {
            'temporal_difference': self.check_year_gap(papers_1, papers_2),
            'methodological_difference': self.compare_methods(papers_1, papers_2),
            'context_difference': self.extract_conditions(papers_1, papers_2),
            'citation_trajectory': self.analyze_citation_evolution(papers_1, papers_2),
            'consensus_direction': self.identify_consensus(papers_1, papers_2)
        }
```

#### 2.2.4 Multi-Scale Research View

Reference: [Democritus-insight-alignment-first-ideas.md, Section 3](../Democritus-agent-improvements/Democritus-insight-alignment-first-ideas.md#3-multi-scale-research-architecture)

```python
class MultiScaleResearchView:
    """
    Navigate research at different granularities.
    
    DEMOCRITUS lesson: Local neighborhoods + global manifold.
    Reference: 2512.07796.pdf
    
    The paper demonstrates multi-scale visualization through several figures:
    - Figure 1: Local causal neighborhood example (Indus River drought model)
    - Figure 2: Global LCM as 2D UMAP manifold (Indus Valley civilization)
    - Figure 4: Additional global manifold example showing research landscape
    - Figures 7-8: Additional local neighborhood examples in other domains
    """
    
    def get_local_view(self, concept: str, hop_distance: int = 2) -> Dict:
        """
        Get local causal neighborhood around a concept.
        
        Implements local neighborhood visualization as shown in DEMOCRITUS
        Figure 1 (Indus River example) and Figures 7-8 (domain-specific examples).
        
        Example for "transformer architecture":
        - 1-hop: attention mechanism, self-attention, positional encoding
        - 2-hop: BERT, GPT, multi-head attention, layer normalization
        
        Args:
            concept: Central concept to explore
            hop_distance: How many hops from central concept
            
        Returns:
            Dict with local graph and supporting papers
        """
        local_graph = self.causal_graph.ego_graph(concept, hop_distance)
        return {
            'graph': local_graph,
            'papers': self.get_papers_for_subgraph(local_graph),
            'key_relationships': self.identify_key_relationships(local_graph),
            'gaps': self.identify_local_gaps(local_graph)
        }
    
    def get_global_view(self) -> Dict:
        """
        Get entire research landscape as 2D/3D manifold.
        
        Implements global manifold visualization as shown in DEMOCRITUS
        Figure 2 (Indus Valley UMAP) and Figure 4 (research landscape overview).
        Uses UMAP projection of embeddings.
        
        Returns:
            Dict with coordinates, clusters, bridges, gaps
        """
        embeddings = self.compute_geometric_embeddings()
        manifold_2d = self.umap_projection(embeddings)
        
        return {
            'coordinates': manifold_2d,
            'clusters': self.identify_research_clusters(),
            'bridges': self.find_interdisciplinary_connections(),
            'gaps': self.identify_unexplored_regions()
        }
```

---

## 3. Agent Enhancement Specifications

### 3.1 Librarian Agent (Ellis) Enhancements

**File:** `.paperkit/specialist/agents/librarian.md`

#### 3.1.1 New Capabilities

| Capability | Description | DEMOCRITUS Reference |
|------------|-------------|---------------------|
| Causal Triple Extraction | Extract (subject, relation, object) from sources | Module 4, 2512.07796.pdf |
| Research Utility Scoring | Compute utility for exploration directions | Section 11 - Active manifold |
| Gap Detection | Identify structural gaps in knowledge graph | Democritus-insights, Section 1 |
| Frontier Prioritization | Rank next research directions by utility | Democritus-insights, Section 2 |

#### 3.1.2 Enhanced Menu Items

```xml
<menu>
  <!-- Existing items -->
  <item cmd="*search" workflow="...">[S] Search for Sources on Topic</item>
  <item cmd="*evaluate" workflow="...">[E] Evaluate Source Quality</item>
  <item cmd="*gaps" workflow="...">[G] Identify Research Gaps</item>
  <item cmd="*track" workflow="...">[T] Track Sources Status</item>
  
  <!-- NEW: DEMOCRITUS-inspired items -->
  <item cmd="*causal" workflow=".../causal-extract.yaml">[C] Extract Causal Claims from Source</item>
  <item cmd="*frontier" workflow=".../research-frontier.yaml">[F] Show Research Frontier (Prioritized)</item>
  <item cmd="*utility" workflow=".../utility-score.yaml">[U] Compute Research Utility Score</item>
  <item cmd="*visualize" workflow=".../visualize-local.yaml">[V] Visualize Local Research Neighborhood</item>
  
  <item cmd="*dismiss">[D] Dismiss Agent</item>
</menu>
```

#### 3.1.3 Enhanced Principles

Add to `.paperkit/_cfg/agents/librarian.yaml`:

```yaml
principles:
  # Existing principles...
  - Academic integrity is crucial - always prioritize reputable sources
  - Understand actual research need first
  
  # NEW: DEMOCRITUS-inspired principles
  - Extract causal relationships when analyzing sources, not just facts
  - Prioritize research directions by utility score, not arbitrary sequence
  - Identify structural gaps in knowledge graph, not just topic coverage
  - Flag contradictions between sources for Research Consolidator resolution
  - Build research frontier incrementally with each source analyzed
```

#### 3.1.4 New Output Schema

Add to outputSchema in `librarian.yaml`:

```yaml
outputSchema:
  type: object
  properties:
    # Existing properties...
    recommendations:
      type: array
    organization:
      type: object
    gaps:
      type: array
    
    # NEW: DEMOCRITUS-inspired outputs
    causalTriples:
      type: array
      description: Extracted causal relationships with citations
      items:
        type: object
        properties:
          subject:
            type: string
          relation:
            type: string
            enum: [causes, prevents, increases, decreases, influences, leads_to, moderates]
          object:
            type: string
          citation:
            type: string
          confidence:
            type: string
            enum: [high, medium, low]
    
    researchFrontier:
      type: array
      description: Prioritized research directions by utility
      items:
        type: object
        properties:
          direction:
            type: string
          utilityScore:
            type: number
          factors:
            type: object
            properties:
              relevance:
                type: number
              novelty:
                type: number
              bridgeScore:
                type: number
              impact:
                type: number
              recency:
                type: number
    
    structuralGaps:
      type: array
      description: Knowledge graph structural gaps
      items:
        type: object
        properties:
          type:
            type: string
            enum: [disconnected, contradiction, unexplored]
          details:
            type: string
          priority:
            type: string
            enum: [high, medium, low]
```

### 3.2 Research Consolidator Agent (Alex) Enhancements

**File:** `.paperkit/core/agents/research-consolidator.md`

#### 3.2.1 New Capabilities

| Capability | Description | DEMOCRITUS Reference |
|------------|-------------|---------------------|
| Causal Graph Building | Build knowledge graph during synthesis | Module 4-5, 2512.07796.pdf |
| Contradiction Detection | Find and characterize conflicting claims | Democritus-insights, Section 4 |
| Triangle Detection | Find coherent research regimes | Table 2, 2512.07796.pdf |
| Multi-Scale Visualization | Generate local + global research views | Figures 1-4, 2512.07796.pdf |
| Controversy Synthesis | Present balanced view of conflicts | Democritus-insights, Section 4 |

#### 3.2.2 Enhanced Menu Items

```xml
<menu>
  <!-- Existing items -->
  <item cmd="*research" workflow="...">[R] Consolidate Research on Topic</item>
  <item cmd="*sources" workflow="...">[S] Add New Sources</item>
  <item cmd="*gaps" workflow="...">[G] Identify Research Gaps</item>
  <item cmd="*index" workflow="...">[I] Update Research Index</item>
  
  <!-- NEW: DEMOCRITUS-inspired items -->
  <item cmd="*graph" workflow=".../build-causal-graph.yaml">[K] Build Causal Knowledge Graph</item>
  <item cmd="*contradictions" workflow=".../detect-contradictions.yaml">[O] Detect & Resolve Contradictions</item>
  <item cmd="*triangles" workflow=".../find-triangles.yaml">[T] Find Research Triangles (Coherent Mechanisms)</item>
  <item cmd="*global" workflow=".../global-view.yaml">[L] Generate Global Research Manifold View</item>
  <item cmd="*local" workflow=".../local-view.yaml">[N] Generate Local Neighborhood View</item>
  
  <item cmd="*dismiss">[D] Dismiss Agent</item>
</menu>
```

#### 3.2.3 Enhanced Principles

Add to `.paperkit/_cfg/agents/research-consolidator.yaml`:

```yaml
principles:
  # Existing principles...
  - Academic integrity is paramount in all research synthesis
  - Synthesize information into coherent narrative, not lists of facts
  
  # NEW: DEMOCRITUS-inspired principles
  - Build causal knowledge graph incrementally during synthesis
  - Detect contradictions between sources and characterize their nature
  - Identify research triangles that indicate coherent causal mechanisms
  - Present controversies with balanced evidence from both sides
  - Generate multi-scale views: local neighborhoods + global manifold
  - Weight claims by evidence strength and citation patterns
  - Flag speculative vs well-supported causal claims
```

#### 3.2.4 Enhanced Report Structure

```markdown
# [Research Topic Title]

## Overview
[Scope, relevance to paper goal, what this covers]

## Causal Model
[Visual representation or textual description of key causal relationships]

### Key Causal Relationships
| Subject | Relation | Object | Confidence | Sources |
|---------|----------|--------|------------|---------|
| X | causes | Y | High | (Smith 2020; Jones 2021) |

## [Major Topic 1]
[Content with proper citations]

## [Major Topic 2]
[Content with proper citations]

## Key Insights and Synthesis
[Connecting themes, relationships between sources]

### Research Triangles Identified
[Coherent causal mechanisms found]
1. **Triangle 1:** A → B → C → A (positive feedback)
   - Evidence: ...
   - Implications: ...

## Controversies and Contradictions
[Balanced presentation of conflicting findings]

### Controversy 1: [Topic]
- **Claim A:** [Description] - Supported by: (Source 1; Source 2)
- **Claim B:** [Opposing view] - Supported by: (Source 3; Source 4)
- **Analysis:** [Why they differ - methods, populations, time periods]
- **Consensus Direction:** [Which view is gaining support]

## Gaps and Future Research
[What remains unknown, where more research needed]

### Structural Gaps
| Gap Type | Description | Priority | Suggested Action |
|----------|-------------|----------|------------------|
| Disconnected | Clusters X and Y not linked | High | Explore bridging topics |
| Unexplored | Concept Z mentioned but not studied | Medium | Targeted search |

## Research Frontier (Prioritized)
| Direction | Utility Score | Rationale |
|-----------|---------------|-----------|
| Topic A | 0.85 | High relevance, bridges clusters |
| Topic B | 0.72 | Resolves contradiction |

## Bibliography
[Harvard-formatted complete bibliography]
```

---

## 4. Implementation Plan

### 4.1 Phase 1: Foundation (Weeks 1-3, ~30h)

**Goal:** Implement core causal graph infrastructure

| Task | Effort | Output |
|------|--------|--------|
| Create CausalResearchGraph class | 8h | Python module |
| Implement triple extraction prompts | 6h | Prompt templates |
| Add graph storage to research-index.yaml | 4h | Schema update |
| Update Librarian with extraction capability | 8h | Agent update |
| Basic gap detection (disconnected, unexplored) | 4h | Gap detection |

**Files Modified:**
- `.paperkit/_cfg/agents/librarian.yaml` - New schema
- `.paperkit/specialist/agents/librarian.md` - New capabilities
- `.paperkit/data/schemas/causal-graph-schema.json` - New schema
- `open-agents/memory/research-index.yaml` - Structure update

### 4.2 Phase 2: Active Planning (Weeks 4-5, ~20h)

**Goal:** Implement utility-based research prioritization

| Task | Effort | Output |
|------|--------|--------|
| Implement utility scoring function | 8h | Scoring logic |
| Create ActiveResearchPlanner | 6h | Planning module |
| Update Librarian with frontier menu | 4h | Agent update |
| Integration testing | 2h | Test suite |

**Files Modified:**
- `.paperkit/specialist/agents/librarian.md` - Frontier menu
- New workflow: `.paperkit/specialist/workflows/librarian/research-frontier.yaml`

### 4.3 Phase 3: Contradiction Handling (Weeks 6-7, ~15h)

**Goal:** Implement contradiction detection and resolution

| Task | Effort | Output |
|------|--------|--------|
| Implement ContradictionAnalyzer | 6h | Analyzer module |
| Create resolution characterization | 4h | Resolution logic |
| Update Research Consolidator | 3h | Agent update |
| Add controversies section to reports | 2h | Template update |

**Files Modified:**
- `.paperkit/_cfg/agents/research-consolidator.yaml` - New schema
- `.paperkit/core/agents/research-consolidator.md` - New capabilities
- New workflow: `.paperkit/core/workflows/research/detect-contradictions.yaml`

### 4.4 Phase 4: Visualization (Weeks 8-10, ~15h)

**Goal:** Implement multi-scale research visualization

| Task | Effort | Output |
|------|--------|--------|
| Implement local neighborhood view | 5h | View generator |
| Implement global manifold view (text-based) | 5h | View generator |
| Create visualization workflows | 3h | Workflow files |
| Integration testing | 2h | Test suite |

**Files Modified:**
- New workflows for visualization
- Output templates for views

---

## 5. Success Criteria

### 5.1 Functional Requirements

- [ ] Librarian can extract causal triples from any source with Harvard citations
- [ ] Research directions are prioritized by computed utility score
- [ ] Structural gaps (disconnected, contradictions, unexplored) are detected
- [ ] Research Consolidator detects contradictions between sources
- [ ] Contradictions are characterized with resolution analysis
- [ ] Reports include controversies section with balanced evidence
- [ ] Local neighborhood views show 2-hop causal relationships
- [ ] Research frontier is prioritized and actionable

### 5.2 Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Causal triple extraction accuracy | >80% | Manual validation |
| Gap detection recall | >70% | Comparison with expert review |
| Contradiction detection precision | >85% | Manual validation |
| Utility score correlation with value | >0.6 | User feedback |

### 5.3 Academic Integrity

- [ ] All extracted triples include source citations
- [ ] Contradictions cite both opposing viewpoints
- [ ] No fabricated relationships or claims
- [ ] Page numbers included for direct quotes
- [ ] Harvard citation style maintained throughout

---

## 6. Dependencies

### 6.1 Internal Dependencies

| Dependency | Description | Status |
|------------|-------------|--------|
| [001-agent-metadata](001-agent-metadata.md) | Agent schema foundation | Complete |
| [002-workflow-agent-contract](002-workflow-agent-contract.md) | Workflow linking | In Progress |
| [007-citation-validation](007-citation-validation.md) | Citation infrastructure | Draft |

### 6.2 External Dependencies

| Dependency | Description | Required |
|------------|-------------|----------|
| NetworkX | Graph operations | Yes |
| UMAP (optional) | Manifold visualization | No |
| Sentence Transformers (optional) | Embedding similarity | No |

---

## 7. Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| LLM inconsistency in triple extraction | Medium | High | Structured prompts, validation |
| Over-complexity for users | High | Medium | Progressive disclosure, simple defaults |
| Performance with large graphs | Medium | Low | Lazy loading, caching |
| Citation accuracy in extractions | High | Medium | Require source verification |

---

## 8. References

### 8.1 Primary Sources

1. **DEMOCRITUS Research Paper**
   - Location: `dev-docs/Democritus-agent-improvements/2512.07796.pdf`
   - Key sections: Introduction, Module 4-6, Section 11 (Active manifold)
   - Figures: 1-4, 7-8 (local/global views)
   - Table 2: GT performance on triangle detection

2. **DEMOCRITUS Integration Ideas**
   - Location: `dev-docs/Democritus-agent-improvements/Democritus-insight-alignment-first-ideas.md`
   - Key sections: 1-8 (all enhancement proposals)
   - Code examples: CausalResearchGraph, ActiveResearchPlanner, ContradictionAnalyzer

### 8.2 PaperKit Architecture

3. **System Architecture**
   - Location: `dev-docs/ARCHITECTURE.md`
   - Agent routing map
   - Data flow architecture

4. **Current Agent Definitions**
   - Librarian: `.paperkit/_cfg/agents/librarian.yaml`, `.paperkit/specialist/agents/librarian.md`
   - Research Consolidator: `.paperkit/_cfg/agents/research-consolidator.yaml`, `.paperkit/core/agents/research-consolidator.md`

### 8.3 Related Specifications

5. **Developer Improvements**
   - Location: `dev-docs/DEVELOPER-IMPROVEMENTS/`
   - Related: 001 (metadata), 002 (contracts), 007 (citations)

---

## 9. Open Questions

1. **Embedding Choice:** Should we use sentence transformers for semantic similarity, or rely on LLM-based similarity?

2. **Graph Persistence:** Should the causal graph be persisted as a separate file or integrated into research-index.yaml?

3. **Visualization Format:** Text-based ASCII graphs vs generated images vs interactive HTML?

4. **Complexity Disclosure:** How much of the causal analysis should be exposed to users by default?

5. **Cross-Paper Integration:** Should causal graphs from multiple research sessions be merged?

---

## 10. Appendix: Key Quotes from DEMOCRITUS Paper

### 10.1 On the Core Problem

> "Using an LLM alone leaves us with a *laundry list* of disconnected fragments. Democritus aims to turn these fragments into structured *large causal models*."
> — Section 1, Introduction

### 10.2 On Active Exploration

> "A naive implementation expands every topic to a fixed depth, asks the LLM for causal questions and statements at every node, and only then builds the manifold. This works, but the LLM cost dominates and the result is unfocused."
> — Section 1, Introduction

### 10.3 On Local vs Global Views

> "Figure 1 illustrates a local causal model learned by DEMOCRITUS, whereas Figure 2 shows the entire global LCM, projected onto 2D using the UMAP data visualization method."
> — Section 1, describing Indus Valley example

### 10.4 On Causal Triple Extraction

> "DEMOCRITUS then assembles the results of querying an LLM into 'causal triples', such as (tropical Pacific warming, reduces, monsoon rainfall)"
> — Section 1, describing Module 4

---

*Last Updated: 2025-12-27*
