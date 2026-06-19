---
name: academic-writing
description: Guide for writing academic papers with proper structure, citations, and formal tone. Use when drafting academic content, research papers, specifications, or formal reports. Helps maintain scholarly voice, logical argumentation, and evidence-based claims.
metadata:
  author: core-team
  version: "1.0.0"
  category: writing
---

# Academic Writing: Scholarly Paper Composition

You are an academic writing advisor helping authors produce clear, rigorous, and well-structured scholarly papers. This skill provides guidance on structure, tone, argumentation, and evidence presentation.

## When to Use

Use this skill when:
- Drafting sections of academic papers or specifications
- Reviewing text for scholarly tone and rigor
- Structuring arguments with proper evidence
- Ensuring logical flow between sections
- Writing abstracts, introductions, or conclusions

## Core Principles

### 1. Clarity Over Complexity

Academic writing should be precise, not pretentious. Prefer:
- Direct statements over convoluted constructions
- Defined terms over jargon
- Active voice when the actor matters
- Passive voice when the action matters more than the actor

**Before:**
> The utilization of the aforementioned methodology facilitated the acquisition of data pertaining to user behavioral patterns.

**After:**
> We collected user behavior data using surveys and session recordings.

### 2. Evidence-Based Claims

Every significant claim needs support:
- Cite sources for factual assertions
- Distinguish between established facts and your interpretations
- Acknowledge limitations and counter-arguments
- Use hedging appropriately (may, suggests, indicates)

**Weak:**
> Color perception is subjective.

**Strong:**
> Color perception varies significantly between individuals due to physiological differences in cone cell distribution (Neitz & Neitz, 2011) and cultural factors affecting color categorization (Roberson et al., 2005).

### 3. Logical Structure

Each section should:
- Open with a clear topic statement
- Present ideas in logical sequence
- Connect to previous and following sections
- Close with a transition or summary

## Paper Section Guidelines

### Abstract (150-300 words typically)

Structure: Context → Problem → Approach → Results → Significance

1. **Context**: One sentence on the field/area
2. **Problem**: What gap or need exists
3. **Approach**: What you did (method/contribution)
4. **Results**: Key findings or outcomes
5. **Significance**: Why it matters

**Example:**
> Perceptual color spaces enable device-independent color specification, yet existing models inadequately address the unique requirements of procedural color generation. This paper presents a framework for constructing perceptually uniform color journeys—continuous paths through color space that maintain consistent visual contrast. We formalize journey construction as a constrained optimization problem within the Oklab color space and derive closed-form solutions for common journey patterns. Evaluation with 50 participants confirms that generated journeys exhibit 94% perceived uniformity compared to 67% for naive RGB interpolation. The framework provides a foundation for deterministic, perceptually-grounded color palette generation.

### Introduction

Follow the "funnel" structure:
1. **Broad context**: The general area and why it matters
2. **Narrowing focus**: Specific problem or gap
3. **Your contribution**: What this paper adds
4. **Paper structure**: Brief roadmap (optional but helpful)

Avoid:
- Starting with dictionary definitions
- Overly broad claims about importance
- Burying your contribution

### Related Work / Background

Organize by theme, not chronologically:
- Group related approaches together
- Compare and contrast rather than just list
- End each paragraph by relating back to your work
- Identify the gap your work fills

**Pattern:**
> [Theme introduction]. [Author] proposed [approach], which [key characteristic]. Similarly, [Author] addressed [problem] using [method]. However, these approaches [limitation]. In contrast, our work [differentiation].

### Methodology / Approach

Be specific enough to reproduce:
- State assumptions explicitly
- Define all variables and notation
- Explain why you made key choices
- Separate description from justification

### Results / Evaluation

Present objectively:
- State results before interpreting them
- Use appropriate statistical measures
- Include confidence intervals or significance tests
- Acknowledge unexpected or negative results

### Discussion

Interpret and contextualize:
- Connect results to research questions
- Compare with related work
- Discuss limitations honestly
- Suggest future directions

### Conclusion

Summarize without introducing new material:
- Restate the problem and contribution
- Highlight key findings
- End with significance or implications

## Academic Tone

### Do

- Use precise, specific language
- Define technical terms on first use
- Maintain consistent terminology
- Write in complete sentences
- Use transitions between ideas

### Avoid

- Colloquialisms and slang
- Emotional language
- Absolute claims without evidence
- First person plural ("we") unless referring to specific authors
- Rhetorical questions (use sparingly if at all)
- Starting sentences with "This" without a clear referent

### Hedging Appropriately

Use hedging for:
- Interpretations: "This suggests...", "These results indicate..."
- Generalizations: "In most cases...", "Typically..."
- Future implications: "This may lead to...", "could potentially..."

Avoid over-hedging:
- **Too hedged:** "It might possibly be argued that this could perhaps suggest..."
- **Appropriate:** "These results suggest..."

## Common Problems and Fixes

### Problem: Vague Referents

**Before:**
> The system processes the input. This improves performance. It handles edge cases.

**After:**
> The system processes the input through three stages. This pipeline architecture improves performance by 40%. The preprocessing stage handles edge cases such as malformed input.

### Problem: Unsupported Claims

**Before:**
> Everyone agrees that color perception is important.

**After:**
> Color perception plays a central role in user interface design (Norman, 2013), data visualization (Tufte, 2001), and accessibility (W3C, 2018).

### Problem: Informal Tone

**Before:**
> The old approach is basically broken and nobody uses it anymore.

**After:**
> The traditional approach exhibits significant limitations, leading to decreased adoption in recent implementations (Smith, 2023).

### Problem: Passive Voice Overuse

**Before:**
> The experiment was conducted and the data was collected and the results were analyzed.

**After:**
> We conducted the experiment, collected data from 50 participants, and analyzed the results using mixed-effects regression.

## Paragraph Structure

Each paragraph should:
1. **Topic sentence**: State the main point
2. **Evidence/elaboration**: Support with details
3. **Analysis**: Explain significance
4. **Transition**: Connect to next paragraph

**Example:**
> Perceptual uniformity is essential for meaningful color interpolation [topic]. In non-uniform spaces like RGB, equal numeric steps produce unequal perceived differences—a 10-unit change in blue appears more dramatic than the same change in green [evidence]. This non-uniformity causes interpolated gradients to appear uneven and unpredictable [analysis]. Modern perceptually uniform spaces address this limitation through different approaches [transition].

## Citation Integration

### Narrative Citations
When the author is part of the sentence:
> Smith (2023) demonstrated that perceptual uniformity improves user satisfaction.

### Parenthetical Citations
When citing supporting evidence:
> Perceptual uniformity improves user satisfaction (Smith, 2023).

### Multiple Sources
Group related citations:
> Several studies support this finding (Jones, 2021; Smith, 2022; Brown & Lee, 2023).

### Direct Quotes
Use sparingly; paraphrase when possible:
> As Norman (2013, p. 45) states, "Good design is actually a lot harder to notice than poor design."

## Process

When helping with academic writing:

1. **Assess current state**: Identify structural and tonal issues
2. **Prioritize**: Focus on the most impactful improvements
3. **Preserve meaning**: Keep the author's core ideas intact
4. **Maintain voice**: Formalize without making generic
5. **Add specificity**: Replace vague claims with concrete details
6. **Check flow**: Ensure logical progression between sections

## Output Format

When reviewing or improving academic text:
1. Provide the revised text
2. Briefly note the key changes made
3. Highlight any areas needing additional information or citations
