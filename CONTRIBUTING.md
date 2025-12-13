# Contributing to Paper Kit

Thank you for your interest in contributing to **Paper Kit** — the Agentic Academic Style Paper Writing System! We welcome contributions from the community to help improve and expand this system.

## How to Contribute

There are many ways to contribute to Paper Kit:

- **Ask questions** — Help others and learn from the community in [Discussions](https://github.com/peternicholls/PaperKit/discussions)
- **Report bugs** — Help us identify and fix issues
- **Suggest features** — Propose improvements or new capabilities
- **Improve documentation** — Enhance guides, examples, or clarifications
- **Develop new agents** — Create specialized agents for specific writing tasks
- **Build tools** — Add validation scripts, build utilities, or integrations
- **Share workflows** — Document and share your paper-writing workflows
- **Test and feedback** — Test the system and provide constructive feedback

## Getting Started

### Prerequisites

- macOS (or Linux with bash support)
- VS Code with GitHub Copilot extension
- Python 3.8+
- LaTeX installation (for document compilation)
- Git

### Set Up Your Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/PaperKit.git
   cd PaperKit
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Set up Python environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r open-agents/tools/requirements.txt
   ```

## Development Guidelines

### Code Style

- **Python**: Follow PEP 8; use meaningful variable names
- **Bash**: Use shellcheck for validation; add comments for complex logic
- **Markdown**: Follow standard GitHub Flavored Markdown conventions
- **YAML**: Use 2-space indentation; keep configurations clear and documented

### Agent Development

When creating or modifying agents:

1. **Define agent role clearly** in `.copilot/agents/` YAML configuration
2. **Specify triggers** — how users invoke the agent
3. **Document inputs and outputs** — what the agent expects and produces
4. **Test with Copilot** — ensure the agent works in GitHub Copilot
5. **Register in manifest** — add to `.copilot/agents.yaml`
6. **Write documentation** — explain capabilities and usage

### Command Development

When adding commands:

1. **Create command YAML** in `.copilot/commands/paper/`
2. **Map to agent** — specify which agent(s) the command routes to
3. **Define inputs** — clearly specify user inputs needed
4. **Document output** — explain what the command produces
5. **Register in manifest** — add to `.copilot/commands.yaml`
6. **Test routing** — verify the command invokes correctly

### Tool Development

When building scripts/tools:

1. **Place in `open-agents/tools/`**
2. **Add error handling** — handle edge cases gracefully
3. **Provide logging** — make output clear and debuggable
4. **Document usage** — include docstrings and help text
5. **Test before submitting** — verify correctness

### Documentation

- Write clear, concise documentation
- Use present tense ("this system is", not "was built")
- Include examples where appropriate
- Keep README files current and accurate
- Document any new commands or agents in relevant files

## Making Changes

### Commit Messages

Use descriptive commit messages that explain *what* and *why*:

```bash
# Good
git commit -m "Add Brainstorm agent for creative ideation"
git commit -m "Improve Quality Refiner clarity evaluation criteria"

# Less helpful
git commit -m "Update file"
git commit -m "Fix bug"
```

### Organization

- Keep changes focused — one feature or fix per branch
- Test changes before committing
- Update documentation alongside code changes
- Reference related issues in commit messages

## Testing Your Changes

### Test Agents Locally

1. **In GitHub Copilot Chat**:
   - Load the agent configuration
   - Test with sample queries
   - Verify outputs match expectations

2. **Test LaTeX Building**:
   ```bash
   ./open-agents/tools/lint-latex.sh
   ./open-agents/tools/build-latex.sh
   ```

3. **Validate Structure**:
   ```bash
   python3 ./open-agents/tools/validate-structure.py
   ```

### Test Commands

- Manually invoke commands in Copilot
- Verify proper routing to agents
- Confirm correct output locations
- Check for error handling

## Submitting Changes

### Before Submitting

- [ ] Changes follow code style guidelines
- [ ] Documentation is updated
- [ ] No unnecessary files are included
- [ ] Commit history is clean
- [ ] Changes have been tested locally

### Pull Request Process

1. **Create a descriptive PR title**:
   - "Add [Feature]: Brief description"
   - "Fix [Issue]: Brief description"
   - "Docs: Brief description"

2. **Write a clear PR description**:
   - What does this change do?
   - Why is it needed?
   - How was it tested?
   - Are there any breaking changes?

3. **Link related issues**:
   ```markdown
   Fixes #123
   Related to #456
   ```

4. **Request review** from maintainers

## Reporting Issues

### Bug Reports

Use the **Bug Report** template when reporting issues:

- **Title**: Clear, concise description of the bug
- **Environment**: OS, software versions, relevant configs
- **Steps to reproduce**: Specific steps that trigger the bug
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happened
- **Logs/output**: Any relevant error messages or logs
- **Attachments**: Screenshots, sample files, etc.

### Feature Requests

Use the **Feature Request** template for new ideas:

- **Title**: Clear description of the feature
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternative approaches**: Other ways to solve the problem
- **Context**: Any relevant background or examples

## Code Review Process

All contributions go through code review:

- Maintainers will review your changes
- Feedback will be constructive and specific
- You may be asked to make revisions
- Once approved, changes will be merged

## Areas for Contribution

### High Priority

- [ ] Expand LaTeX template features
- [ ] Add more specialized agents
- [ ] Improve documentation clarity
- [ ] Build additional validation tools
- [ ] Create user workflow examples

### Medium Priority

- [ ] Add support for other citation styles
- [ ] Improve error messages
- [ ] Create video tutorials
- [ ] Build integration examples
- [ ] Develop templates for specific paper types

### Nice to Have

- [ ] Theme variations
- [ ] Alternative output formats
- [ ] Extended language support
- [ ] Community showcase
- [ ] Performance optimizations

## Version Management

The project follows semantic versioning. Check [VERSION](VERSION) for the current release version.

Release candidates and previews are tagged with labels like `alpha-*` or `beta-*`. Version bumps are handled by the release process and should be coordinated with maintainers.

## Community Guidelines

### Be Respectful

- Treat all contributors with respect
- Assume good intentions
- Provide constructive feedback
- Welcome diverse perspectives

### Be Helpful

- Help answer questions
- Share knowledge and experience
- Mentor newer contributors
- Celebrate contributions

### Be Honest

- Give accurate, truthful feedback
- Acknowledge limitations
- Share what you've learned
- Admit mistakes

## Questions?

If you have questions about contributing:

- **Check existing documentation** — start with README.md and CONTRIBUTING.md
- **Search discussions** — your question may already be answered in [GitHub Discussions](https://github.com/peternicholls/PaperKit/discussions)
- **Ask in discussions** — post in the [Help & Support](https://github.com/peternicholls/PaperKit/discussions/categories/help-support) category
- **Open an issue** — open a discussion or issue if stuck
- **Reach out** — contact maintainers if needed

## Recognition

Contributors will be recognized in:

- Pull request comments
- Release notes
- Contributors section in README
- Community showcases

Thank you for contributing to making academic paper writing easier!

---

## License

By contributing to Paper Kit, you agree that your contributions will be licensed under the MIT License.

---

**Happy contributing! 🎓✨**
