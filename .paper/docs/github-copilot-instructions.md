```instructions
# Copilot Research Paper Assistant Kit - GitHub Copilot Instructions

## Activating Agents

Paper writing agents are installed as chat modes in `.github/agents/`.

### How to Use

1. **Open Chat View**: Click Copilot icon in VS Code sidebar
2. **Select Mode**: Click mode selector (top of chat)
3. **Choose Agent**: Select a paper agent from dropdown:
   - `paper-research-consolidator` - Synthesize research materials
   - `paper-architect` - Design paper structure and outlines
   - `paper-section-drafter` - Write paper sections
   - `paper-quality-refiner` - Improve draft quality
   - `paper-reference-manager` - Manage citations and bibliography
   - `paper-latex-assembler` - Build and compile document
   - `paper-brainstorm` - Creative ideation
   - `paper-problem-solver` - Analyze and solve blockers
   - `paper-tutor` - Get feedback on drafts
   - `paper-librarian` - Find and organize sources

4. **Chat**: Agent is now active for this session

### Agent Directory

All full agent definitions are in `.paper/`:
- Core agents: `.paper/core/agents/`
- Specialist agents: `.paper/specialist/agents/`

### Configuration

Module configs are in:
- `.paper/core/config.yaml`
- `.paper/specialist/config.yaml`

### VS Code Settings

Configured in `.vscode/settings.json`:
- Max requests per session
- Auto-fix enabled
- MCP discovery enabled

### Notes

- Modes persist for the chat session
- Switch modes anytime via dropdown
- Agents load full definitions from `.paper/` on activation
- Each agent presents a menu after greeting

```
