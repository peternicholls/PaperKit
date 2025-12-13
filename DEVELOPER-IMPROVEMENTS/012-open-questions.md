# Open Questions

**Document ID:** 012-open-questions  
**Date:** 2024-12-13  
**Status:** Tracking  
**Category:** Planning

---

## Overview

This document consolidates open questions from all specification documents that require stakeholder input or further discussion before implementation can proceed.

---

## Agent Metadata (001)

### Q1.1: Agent Definition Format
**Question:** Should agents be defined in individual YAML files or a single manifest file?

**Options:**
- A) Single `agent-manifest.yaml` with all agents
- B) Individual files per agent (e.g., `agents/section-drafter.yaml`)
- C) Hybrid: manifest for discovery, individual files for full definitions

**Considerations:**
- Single file easier to discover and validate
- Individual files easier to maintain and review changes
- Hybrid provides both benefits

**Decision Needed By:** Before implementing 001

---

### Q1.2: Validation Strictness
**Question:** What validation strictness level is appropriate for v1?

**Options:**
- A) Strict: All fields required, fail on any error
- B) Lenient: Warnings for missing optional fields
- C) Progressive: Start lenient, tighten over time

**Recommendation:** Option C - Progressive

---

### Q1.3: JSON Support
**Question:** Should we support JSON alongside YAML for tooling compatibility?

**Options:**
- A) YAML only (simpler)
- B) Both YAML and JSON (flexible)
- C) YAML with JSON Schema validation

**Recommendation:** Option C

---

## Workflow Contracts (002)

### Q2.1: Validation Strictness
**Question:** How strict should input validation be (fail-fast vs lenient)?

**Context:** Strict validation catches errors early but may block valid edge cases.

**Options:**
- A) Fail-fast: Reject invalid inputs immediately
- B) Lenient: Transform/normalize when possible, warn on issues
- C) Configurable per workflow

---

### Q2.2: Contract Versioning
**Question:** Should contracts be versioned independently of agents?

**Context:** Agent version 1.2.0 might use contract version 1.0.0.

**Options:**
- A) Tied: Contract version = Agent version
- B) Independent: Separate versioning
- C) Contract interfaces versioned, implementations tied to agents

---

### Q2.3: Dynamic Workflows
**Question:** How to handle dynamic workflows where steps are determined at runtime?

**Context:** Some workflows may branch based on agent output.

**Options:**
- A) Pre-define all possible paths
- B) Allow runtime step generation with validation
- C) Support both static and dynamic workflows

---

### Q2.4: Contract Inheritance
**Question:** Should we support contract inheritance for common patterns?

**Context:** Many agents share common input patterns (e.g., "takes outline as input").

**Options:**
- A) No inheritance (explicit is better)
- B) Support mixins/traits
- C) Support full inheritance

---

## Consent and Sandboxing (003)

### Q3.1: Sandbox Technology
**Question:** Which sandboxing technology to use?

**Options:**
- A) Firejail (Linux, lightweight)
- B) Docker (cross-platform, heavier)
- C) Bubblewrap (Linux, minimal)
- D) Multiple backends with abstraction layer

**Considerations:**
- macOS support varies
- Docker has broader adoption
- Firejail/bubblewrap are more lightweight

---

### Q3.2: Consent Granularity
**Question:** Should consent be per-tool or per-capability?

**Options:**
- A) Per-tool: "Allow build-latex.sh"
- B) Per-capability: "Allow file write to output-final/"
- C) Both: Tool-level with capability details shown

---

### Q3.3: Network Access Handling
**Question:** How to handle tools that require network access (citation validation)?

**Options:**
- A) Allow network for specific tools
- B) Separate "network tools" category with extra consent
- C) Proxy all network through controlled service

---

### Q3.4: Admin Override
**Question:** Should there be an admin override for trusted environments?

**Options:**
- A) No override (security first)
- B) Allow override with explicit configuration
- C) Allow override for specific tools only

---

## Security (004)

### Q4.1: Injection Detection Sensitivity
**Question:** What level of prompt injection detection sensitivity is appropriate?

**Context:** Too sensitive = false positives; too lenient = missed attacks.

**Options:**
- A) Conservative (more false positives)
- B) Balanced (tuned thresholds)
- C) Configurable per environment

---

### Q4.2: Provenance Tracking
**Question:** Should provenance tracking be opt-in or mandatory?

**Options:**
- A) Mandatory for all sources
- B) Opt-in (user choice)
- C) Required for external sources, optional for user-created

---

### Q4.3: Unverifiable Sources
**Question:** How to handle external sources that can't be verified (e.g., personal notes)?

**Options:**
- A) Mark as "unverified" and proceed
- B) Require manual attestation
- C) Different trust level for unverified sources

---

### Q4.4: Compliance Frameworks
**Question:** What compliance frameworks should be considered (GDPR, etc.)?

**Options:**
- A) GDPR only (most common)
- B) GDPR + academic ethics guidelines
- C) Configurable compliance profiles

---

## Testing and CI (005)

### Q5.1: LLM Output Variance
**Question:** How to handle LLM output variance in regression tests?

**Options:**
- A) Test structure only (headings, sections)
- B) Semantic similarity scoring
- C) Golden outputs with fuzzy matching
- D) Mock LLM responses for determinism

---

### Q5.2: E2E Test Environment
**Question:** Should E2E tests use real LLM or mock responses?

**Options:**
- A) Real LLM (realistic but slow/expensive)
- B) Mocked responses (fast but less realistic)
- C) Both: Mocks for CI, real for release testing

---

### Q5.3: CI Duration
**Question:** What's acceptable CI pipeline duration target?

**Options:**
- A) < 5 minutes (fast feedback)
- B) < 15 minutes (thorough)
- C) < 30 minutes (comprehensive)

**Recommendation:** < 15 minutes for PR checks, < 30 for nightly

---

### Q5.4: Python Versions
**Question:** Should we test on multiple Python versions?

**Options:**
- A) Single version (3.11)
- B) Two versions (3.10, 3.11)
- C) Three versions (3.9, 3.10, 3.11)

---

## Observability (006)

### Q6.1: External Tools
**Question:** Should we use external observability tools (OpenTelemetry, etc.)?

**Options:**
- A) Build custom (simpler deployment)
- B) OpenTelemetry (industry standard)
- C) Both: Custom with OTel export option

---

### Q6.2: Metrics Granularity
**Question:** What granularity of metrics is appropriate?

**Options:**
- A) High-level only (runs, errors)
- B) Detailed (per-step timing, token usage)
- C) Configurable levels

---

### Q6.3: Artifact Retention
**Question:** How long should artifact versions be retained?

**Options:**
- A) 7 days
- B) 30 days
- C) Project duration
- D) Configurable

---

### Q6.4: Data Export
**Question:** Should observability data be exportable?

**Options:**
- A) No (local only)
- B) Yes, standard formats (JSON, CSV)
- C) Yes, with privacy filtering

---

## Citation Validation (007)

### Q7.1: DOI Validation
**Question:** Should DOI validation be mandatory or optional?

**Options:**
- A) Mandatory (quality assurance)
- B) Optional (flexibility)
- C) Required for final build, optional for drafts

---

### Q7.2: Sources Without DOIs
**Question:** How to handle sources without DOIs (books, websites)?

**Options:**
- A) Require alternative identifiers (ISBN, URL)
- B) Manual verification attestation
- C) Lower trust level, flag for review

---

### Q7.3: PDF Bibliography
**Question:** Should we support automatic bibliography generation from PDFs?

**Options:**
- A) No (scope creep)
- B) Yes, basic extraction
- C) Future enhancement

---

### Q7.4: Caching Strategy
**Question:** What's the appropriate caching strategy for API responses?

**Options:**
- A) No caching (always fresh)
- B) 24-hour cache
- C) Indefinite for DOI lookups (immutable)
- D) Configurable TTL

---

## Onboarding (008)

### Q8.1: Video Tutorials
**Question:** Should we create video tutorials?

**Options:**
- A) No (maintenance burden)
- B) Yes, basic walkthrough
- C) Yes, comprehensive series

---

### Q8.2: Example Detail Level
**Question:** What's the right level of detail for examples?

**Options:**
- A) Minimal (prompts only)
- B) Moderate (prompts + expected output)
- C) Comprehensive (full workflow with explanations)

---

### Q8.3: Doc Versioning
**Question:** Should docs be versioned with releases?

**Options:**
- A) No (always latest)
- B) Yes, version-specific docs
- C) Hybrid: stable + latest

---

### Q8.4: Multi-IDE Documentation
**Question:** How to handle multiple IDE documentation?

**Options:**
- A) Single unified doc with sections
- B) Separate docs per IDE
- C) Core docs + IDE-specific supplements

---

## State Management (009)

### Q9.1: Conversation History
**Question:** Should checkpoints include conversation history?

**Options:**
- A) No (privacy, size)
- B) Yes, full history
- C) Summary only

---

### Q9.2: Large Artifacts
**Question:** How to handle large artifacts in state snapshots?

**Options:**
- A) Store hashes only, reference files
- B) Compress and include
- C) Configurable threshold

---

### Q9.3: State Export
**Question:** Should users be able to share/export states?

**Options:**
- A) No (complexity)
- B) Yes, portable format
- C) Export to specific formats (JSON)

---

### Q9.4: Auto vs Manual Checkpoints
**Question:** What's the right balance of auto vs manual checkpoints?

**Options:**
- A) Auto only (user-friendly)
- B) Manual only (user control)
- C) Both with configurable auto triggers

---

## Agent Governance (010)

### Q10.1: Release Frequency
**Question:** How frequently should we release agent updates?

**Options:**
- A) Weekly
- B) Bi-weekly
- C) Monthly
- D) As needed

---

### Q10.2: Multi-Version Support
**Question:** Should we support multiple agent versions simultaneously?

**Options:**
- A) No (simplicity)
- B) Yes, n-1 versions
- C) Yes, all stable versions

---

### Q10.3: Emergency Fixes
**Question:** How to handle emergency fixes vs planned releases?

**Options:**
- A) Same process (consistency)
- B) Fast-track for critical fixes
- C) Hotfix branch with expedited review

---

### Q10.4: Auto-Generated Changelog
**Question:** Should changelog be auto-generated from commits?

**Options:**
- A) No (manual control)
- B) Yes, from conventional commits
- C) Auto-draft with manual review

---

## Priority Matrix

| Question ID | Impact | Urgency | Blocks |
|-------------|--------|---------|--------|
| Q3.1 | High | High | 003 implementation |
| Q1.1 | High | Medium | 001 implementation |
| Q5.1 | High | Medium | 005 E2E tests |
| Q7.1 | Medium | Low | 007 features |
| Q8.1 | Low | Low | None |

---

## Next Steps

1. Review with stakeholders
2. Prioritize based on implementation timeline
3. Make decisions for blocking questions
4. Document decisions in respective specs
5. Update this document with resolutions

---

## Decision Log

| Question | Decision | Date | Rationale |
|----------|----------|------|-----------|
| (pending) | | | |
