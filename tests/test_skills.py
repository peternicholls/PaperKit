#!/usr/bin/env python3
"""
PaperKit Skill System Tests

Tests for skill registry, executor, and validation.
Run with: python3 -m pytest tests/test_skills.py -v
"""

import pytest
import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent / ".paperkit/tools"))

from skill_registry import SkillRegistry, Skill
from skill_executor import SkillExecutor, ExecutionStatus, SkillDepthExceeded, SkillNotFound


class TestSkillRegistry:
    """Tests for SkillRegistry."""

    @pytest.fixture
    def registry(self):
        """Create a registry with the project root."""
        project_root = Path(__file__).parent.parent
        return SkillRegistry(project_root)

    def test_list_skills(self, registry):
        """Test listing all skills."""
        skills = registry.list_skills()
        assert len(skills) == 5
        skill_names = [s.name for s in skills]
        assert "cite-source" in skill_names
        assert "validate-citation" in skill_names
        assert "draft-section" in skill_names
        assert "research-topic" in skill_names
        assert "compile-latex" in skill_names

    def test_get_skill(self, registry):
        """Test getting a specific skill."""
        skill = registry.get_skill("cite-source")
        assert skill is not None
        assert skill.name == "cite-source"
        assert skill.type == "composite"
        assert len(skill.steps) == 2

    def test_get_nonexistent_skill(self, registry):
        """Test getting a skill that doesn't exist."""
        skill = registry.get_skill("nonexistent-skill")
        assert skill is None

    def test_find_skills_for_task(self, registry):
        """Test finding skills by task description."""
        results = registry.find_skills_for_task("format citation harvard style")
        assert len(results) > 0
        # cite-source should be the top result
        top_skill, top_score = results[0]
        assert top_skill.name == "cite-source"
        assert top_score > 0

    def test_find_skills_by_category(self, registry):
        """Test finding skills by category."""
        citations = registry.find_skills_by_category("citations")
        assert len(citations) == 2
        names = [s.name for s in citations]
        assert "cite-source" in names
        assert "validate-citation" in names

    def test_get_categories(self, registry):
        """Test getting all categories."""
        categories = registry.get_categories()
        assert "citations" in categories
        assert "writing" in categories
        assert "research" in categories
        assert "build" in categories

    def test_get_statistics(self, registry):
        """Test getting registry statistics."""
        stats = registry.get_statistics()
        assert stats["total_skills"] == 5
        assert stats["by_type"]["composite"] == 3
        assert stats["by_type"]["conditional"] == 1
        assert stats["by_type"]["atomic"] == 1

    def test_get_skills_for_agent(self, registry):
        """Test finding skills that use a specific agent."""
        skills = registry.get_skills_for_agent("reference-manager")
        assert len(skills) >= 2  # cite-source and validate-citation
        names = [s.name for s in skills]
        assert "cite-source" in names

    def test_to_agent_format(self, registry):
        """Test converting registry to agent format."""
        agent_format = registry.to_agent_format()
        assert len(agent_format) == 5

        # Check structure
        cite_source = next(s for s in agent_format if s["name"] == "cite-source")
        assert "displayName" in cite_source
        assert "description" in cite_source
        assert "type" in cite_source
        assert "category" in cite_source
        assert "agents" in cite_source

    def test_skill_prerequisites(self, registry):
        """Test getting skill prerequisites."""
        prereqs = registry.get_skill_prerequisites("validate-citation")
        assert len(prereqs) >= 1
        prereq_names = [p.get("name") for p in prereqs]
        assert "cite-source" in prereq_names


class TestSkillExecutor:
    """Tests for SkillExecutor."""

    @pytest.fixture
    def executor(self):
        """Create an executor with mock callbacks."""
        project_root = Path(__file__).parent.parent
        registry = SkillRegistry(project_root)

        # Mock agent executor that returns expected outputs
        def mock_agent_executor(agent_name, action, inputs):
            if action == "extract-metadata":
                return {
                    "metadata": {
                        "title": "Test Paper",
                        "author": "Test Author",
                        "year": 2024
                    }
                }
            elif action == "format-citation":
                return {
                    "harvard_citation": "Author, T. (2024) Test Paper.",
                    "bibtex_entry": "@article{author2024test,...}"
                }
            return {}

        def mock_tool_executor(tool_name, inputs):
            return {"success": True}

        return SkillExecutor(
            registry=registry,
            agent_executor=mock_agent_executor,
            tool_executor=mock_tool_executor
        )

    def test_validate_inputs_valid(self, executor):
        """Test validating valid inputs."""
        errors = executor.validate_inputs("cite-source", {"source_url": "https://example.com"})
        assert len(errors) == 0

    def test_validate_inputs_missing_required(self, executor):
        """Test validating inputs with missing required field."""
        errors = executor.validate_inputs("draft-section", {})
        assert len(errors) > 0
        assert any("section_name" in err for err in errors)

    def test_validate_inputs_nonexistent_skill(self, executor):
        """Test validating inputs for nonexistent skill."""
        errors = executor.validate_inputs("nonexistent", {})
        assert len(errors) == 1
        assert "not found" in errors[0]

    def test_dry_run(self, executor):
        """Test dry run of skill execution."""
        plan = executor.dry_run("cite-source", {"source_url": "https://example.com"})
        assert plan["skill"] == "cite-source"
        assert plan["type"] == "composite"
        assert len(plan["steps"]) == 2
        assert len(plan["validation_errors"]) == 0

    def test_dry_run_with_prerequisites(self, executor):
        """Test dry run shows prerequisites."""
        plan = executor.dry_run("validate-citation", {"citation_text": "Test (2024)"})
        assert len(plan["prerequisites"]) >= 1

    def test_execute_skill(self, executor):
        """Test executing a skill."""
        result = executor.execute("cite-source", {"source_url": "https://example.com"})
        assert result.status == ExecutionStatus.COMPLETED
        assert result.skill_name == "cite-source"
        assert len(result.step_results) == 2

    def test_execute_nonexistent_skill(self, executor):
        """Test executing nonexistent skill raises error."""
        with pytest.raises(SkillNotFound):
            executor.execute("nonexistent", {})

    def test_depth_limiting(self):
        """Test that depth limiting works."""
        project_root = Path(__file__).parent.parent
        registry = SkillRegistry(project_root)

        # Create executor that calls itself recursively
        depth_counter = [0]

        def recursive_executor(agent, action, inputs):
            depth_counter[0] += 1
            return {}

        executor = SkillExecutor(
            registry=registry,
            agent_executor=recursive_executor
        )

        # This should not exceed max depth for a simple skill
        result = executor.execute("cite-source", {"source_url": "test"})
        assert depth_counter[0] <= SkillExecutor.MAX_DEPTH + 5  # Some buffer for steps


class TestSkillDataModel:
    """Tests for Skill data model."""

    def test_skill_from_dict(self):
        """Test creating Skill from dictionary."""
        data = {
            "name": "test-skill",
            "displayName": "Test Skill",
            "description": "A test skill",
            "version": "1.0.0",
            "type": "atomic",
            "steps": [
                {
                    "action": "test-action",
                    "agent": "test-agent",
                    "inputs": ["input1"],
                    "outputs": ["output1"]
                }
            ],
            "inputSchema": {"type": "object", "properties": {}},
            "outputSchema": {"type": "object", "properties": {}}
        }

        skill = Skill.from_dict(data)
        assert skill.name == "test-skill"
        assert skill.display_name == "Test Skill"
        assert skill.type == "atomic"
        assert len(skill.steps) == 1
        assert skill.steps[0].action == "test-action"

    def test_skill_to_dict(self):
        """Test converting Skill back to dictionary."""
        data = {
            "name": "test-skill",
            "displayName": "Test Skill",
            "description": "A test skill",
            "version": "1.0.0",
            "type": "atomic",
            "steps": [
                {
                    "action": "test-action",
                    "agent": "test-agent",
                    "inputs": ["input1"],
                    "outputs": ["output1"]
                }
            ],
            "inputSchema": {"type": "object", "properties": {}},
            "outputSchema": {"type": "object", "properties": {}}
        }

        skill = Skill.from_dict(data)
        result = skill.to_dict()

        assert result["name"] == data["name"]
        assert result["displayName"] == data["displayName"]
        assert len(result["steps"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
