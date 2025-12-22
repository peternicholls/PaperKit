# Contributing to PaperKit

Thanks for your interest in contributing to PaperKit! This guide outlines a standard GitHub-driven flow: discuss → issue → backlog → fork → branch → PR → review → merge.

## Contribution Workflow

1. **Discuss**
   - Use [Discussions](https://github.com/peternicholls/PaperKit/discussions) for questions, ideas, and design proposals.

2. **Open an Issue**
   - Use templates for Bug Reports or Feature Requests.
   - Provide clear context, steps to reproduce (for bugs), and desired outcomes.

3. **Backlog & Triage**
   - Issues are labeled (e.g., `bug`, `enhancement`, `docs`, `good first issue`) and, when relevant, assigned to a milestone.
   - If your issue is accepted, it becomes part of the public backlog.

4. **Fork & Clone**
   ```bash
   git fork https://github.com/peternicholls/PaperKit.git
   git clone https://github.com/<your-username>/PaperKit.git
   cd PaperKit
   ```

5. **Create a Branch**
   - Use concise, descriptive names:
     - `feature/latex-audit-tools`
     - `fix/lint-latex-error`
     - `docs/quickstart-refactor`
   ```bash
   git checkout -b feature/your-branch-name
   ```

6. **Set Up Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   # If tools need dependencies, add them to requirements and document it
   ```

7. **Implement Changes**
   - Edit the canonical sources in `.paperkit/` (agents, tools, manifests), then regenerate IDE files:
   ```bash
   ./paperkit generate
   ```
   - Keep changes focused (one issue/feature per branch).

8. **Run Checks**
   - LaTeX lint & build:
   ```bash
   ./.paperkit/tools/lint-latex.sh
   ./.paperkit/tools/build-latex.sh
   ```
   - Validate structure & schemas:
   ```bash
   python3 ./.paperkit/tools/validate-structure.py
   ./paperkit validate
   ```

9. **Commit Cleanly**
   - Write descriptive messages explaining what and why:
   ```bash
   git commit -m "Docs: clarify Quick Start install/regenerate flow"
   git commit -m "Tools: add citation completeness check"
   ```

10. **Push & Open a PR**
   ```bash
   git push origin <branch>
   ```
   - In the PR, include:
     - Motivation and summary
     - Linked issues (`Fixes #123`)
     - Testing/validation notes
     - Breaking changes (if any)

11. **Review & Merge**
   - Maintainers review for clarity, scope, and correctness.
   - Address feedback; keep the PR focused.
   - Once approved, it will be merged.

## Guidelines

### Code & Docs Style
- **Python**: PEP 8, clear names, small functions.
- **Bash**: Validate with `shellcheck`; keep output readable.
- **Markdown**: GitHub Flavored Markdown; concise, actionable.
- **YAML**: 2-space indentation; document fields.

### Agents & Tools
- Edit agent, workflow, and tool definitions in `.paperkit/`.
- Regenerate IDE files after changes: `./paperkit generate`.
- Prefer small, reviewable changes that preserve structure.

### Commit Hygiene
- One logical change per commit (or a short series).
- Reference issues in the commit/PR.
- Keep the history clean and easy to follow.

## Testing Locally

### LaTeX & Structure
```bash
./.paperkit/tools/lint-latex.sh
./.paperkit/tools/build-latex.sh
python3 ./.paperkit/tools/validate-structure.py
./paperkit validate
```

### Agents (IDE)
- In VS Code, use Copilot Chat and the generated `.github/agents/` files.
- For Codex, use `.codex/prompts/` (generated from `.paperkit/`).

## PR Checklist
- [ ] Linked issue(s) and clear motivation
- [ ] Focused scope (one feature/fix)
- [ ] Code/docs follow style guidelines
- [ ] Local checks pass (lint, build, validate)
- [ ] Updated docs where relevant

## Reporting Issues
- Use the **Bug Report** and **Feature Request** templates.
- Provide clear repro steps (for bugs) and concrete outcomes (for features).
- Add logs/screenshots where helpful.

## Versioning & Releases

### Version Numbers
- Semantic versioning is used (MAJOR.MINOR.PATCH).
- Pre-release tags like `alpha-*` / `beta-*` may appear during development.
- See [VERSION](.paperkit/_cfg/version.yaml) for current version.

### Release Authorization

**PaperKit uses two-layer authorization for releases:**

1. **Local checks** in `./paperkit-dev` script (developer convenience)
2. **Service-side enforcement** via GitHub Actions (security)

**For Contributors:**
- You can propose version bumps in PRs
- Only authorized maintainers can create releases
- All releases require approval via GitHub's protected environments

**For Maintainers:**
- See [dev-docs/service-side-authorization.md](dev-docs/service-side-authorization.md) for setup
- See [dev-docs/setup-authorization.md](dev-docs/setup-authorization.md) for quick reference
- Use `./paperkit-dev` for local version management
- Releases require approval on GitHub (cannot be bypassed)

## Community Norms
- Be respectful and constructive.
- Assume good intent; welcome diverse perspectives.
- Share context and learnings.

## Questions?
- Start with the README and docs in `.paperkit/docs/`.
- Ask in [Discussions](https://github.com/peternicholls/PaperKit/discussions).
- Open an issue if you’re blocked.

## License
By contributing to PaperKit, you agree that your contributions are licensed under MIT.

**Thank you for helping improve academic paper workflows! 🎓✨**
