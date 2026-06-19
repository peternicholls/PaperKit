#!/usr/bin/env python3
"""
PaperKit Agent Skills Registry

Implements the agentskills.io standard for Agent Skills discovery.
This is separate from compositional workflows (YAML orchestration).

Agent Skills:
- SKILL.md files with YAML frontmatter + markdown instructions
- HOW to do something (instructions)
- Per agentskills.io specification

Usage:
    from skill_registry import AgentSkillRegistry

    registry = AgentSkillRegistry()
    registry.load_all()  # Returns load time in ms (target: <50ms)

    # Get all skills (metadata only)
    skills = registry.list_skills()

    # Find skills matching a query
    matches = registry.find_skills("citation harvard reference")

    # Get full skill content (progressive disclosure)
    content = registry.load_skill_content("harvard-citations")
"""

import sys
import time
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict


# =============================================================================
# AGENT SKILLS (agentskills.io standard - SKILL.md files)
# =============================================================================

@dataclass
class AgentSkillMetadata:
    """Metadata extracted from SKILL.md frontmatter (~100 tokens)."""
    name: str
    description: str
    path: Path
    license: Optional[str] = None
    compatibility: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "path": str(self.path),
            "license": self.license,
            "compatibility": self.compatibility,
            "metadata": self.metadata,
        }


@dataclass
class AgentSkillMatch:
    """A skill matching a search query with relevance score."""
    skill: AgentSkillMetadata
    score: float
    matched_terms: list


class AgentSkillRegistry:
    """
    Registry for discovering and loading Agent Skills (agentskills.io standard).

    Implements progressive disclosure per FR-2A-04:
    1. load_all() - Load metadata for ALL skills (~100 tokens each, <50ms)
    2. find_skills() - Search by description/name
    3. load_skill_content() - Load full instructions on demand (<5000 tokens)
    """

    def __init__(self, skills_dir: Optional[Path] = None):
        """
        Initialize the registry.

        Args:
            skills_dir: Path to skills directory. If None, auto-detects from project root.
        """
        self._skills: Dict[str, AgentSkillMetadata] = {}
        self._skills_dir = skills_dir or self._find_skills_dir()
        self._loaded = False
        self._load_time_ms: float = 0

    def _find_skills_dir(self) -> Path:
        """Find the skills directory from project root."""
        current = Path.cwd()
        while current != current.parent:
            skills_path = current / '.paperkit' / '_cfg' / 'skills'
            if skills_path.is_dir():
                return skills_path
            current = current.parent
        # Fallback
        return Path('.paperkit/_cfg/skills')

    def _extract_frontmatter(self, skill_md: Path) -> Optional[dict]:
        """Extract YAML frontmatter from SKILL.md file."""
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.startswith('---'):
                return None

            lines = content.split('\n')
            end_index = None
            for i, line in enumerate(lines[1:], start=1):
                if line.strip() == '---':
                    end_index = i
                    break

            if end_index is None:
                return None

            frontmatter_text = '\n'.join(lines[1:end_index])
            return yaml.safe_load(frontmatter_text)
        except Exception:
            return None

    def load_all(self) -> float:
        """
        Load metadata for all skills (progressive disclosure step 1).

        Returns:
            Load time in milliseconds.
        """
        start_time = time.perf_counter()
        self._skills.clear()

        if not self._skills_dir.exists():
            self._loaded = True
            self._load_time_ms = 0
            return 0

        for skill_dir in self._skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith('.'):
                continue

            skill_md = skill_dir / 'SKILL.md'
            if not skill_md.exists():
                continue

            frontmatter = self._extract_frontmatter(skill_md)
            if not frontmatter:
                continue

            name = frontmatter.get('name', skill_dir.name)
            self._skills[name] = AgentSkillMetadata(
                name=name,
                description=frontmatter.get('description', ''),
                path=skill_md,
                license=frontmatter.get('license'),
                compatibility=frontmatter.get('compatibility'),
                metadata=frontmatter.get('metadata', {}),
            )

        self._loaded = True
        self._load_time_ms = (time.perf_counter() - start_time) * 1000
        return self._load_time_ms

    def list_skills(self) -> List[AgentSkillMetadata]:
        """
        Get all registered skills.

        Returns:
            List of skill metadata.
        """
        if not self._loaded:
            self.load_all()
        return list(self._skills.values())

    def get_skill(self, name: str) -> Optional[AgentSkillMetadata]:
        """
        Get metadata for a specific skill by name.

        Args:
            name: Skill name (e.g., "humanizer", "harvard-citations")

        Returns:
            Skill metadata or None if not found.
        """
        if not self._loaded:
            self.load_all()
        return self._skills.get(name)

    def find_skills(self, query: str, threshold: float = 0.1) -> List[AgentSkillMatch]:
        """
        Find skills matching a search query.

        Searches skill names and descriptions for matching terms.

        Args:
            query: Search query (space-separated terms)
            threshold: Minimum score to include (0-1)

        Returns:
            List of matching skills sorted by relevance.
        """
        if not self._loaded:
            self.load_all()

        # Tokenize query
        query_terms = set(query.lower().split())
        if not query_terms:
            return []

        matches = []
        for skill in self._skills.values():
            # Build searchable text
            searchable = f"{skill.name} {skill.description}".lower()

            # Find matching terms
            matched = []
            for term in query_terms:
                if term in searchable:
                    matched.append(term)

            if matched:
                # Calculate score based on match ratio
                score = len(matched) / len(query_terms)

                # Boost if name matches exactly
                if skill.name.lower() in query.lower():
                    score = min(1.0, score + 0.3)

                if score >= threshold:
                    matches.append(AgentSkillMatch(
                        skill=skill,
                        score=score,
                        matched_terms=matched,
                    ))

        # Sort by score descending
        matches.sort(key=lambda m: m.score, reverse=True)
        return matches

    def load_skill_content(self, name: str) -> Optional[str]:
        """
        Load full skill content (progressive disclosure step 2).

        This loads the complete SKILL.md body for use in agent context.

        Args:
            name: Skill name

        Returns:
            Full SKILL.md content (frontmatter + body) or None if not found.
        """
        skill = self.get_skill(name)
        if not skill:
            return None

        try:
            with open(skill.path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None

    def load_skill_instructions(self, name: str) -> Optional[str]:
        """
        Load only the instruction body (without frontmatter).

        Args:
            name: Skill name

        Returns:
            SKILL.md body content only, or None if not found.
        """
        content = self.load_skill_content(name)
        if not content:
            return None

        # Strip frontmatter
        if not content.startswith('---'):
            return content

        lines = content.split('\n')
        end_index = 0
        found_start = False
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if found_start:
                    end_index = i + 1
                    break
                found_start = True

        return '\n'.join(lines[end_index:]).strip()

    @property
    def load_time_ms(self) -> float:
        """Time taken to load all skill metadata in milliseconds."""
        return self._load_time_ms

    @property
    def skill_count(self) -> int:
        """Number of registered skills."""
        if not self._loaded:
            self.load_all()
        return len(self._skills)

    def to_agent_format(self) -> List[Dict]:
        """
        Convert skill registry to format suitable for agent prompts.

        Returns:
            List of skill summaries for orchestrator consumption.
        """
        if not self._loaded:
            self.load_all()

        return [
            {
                'name': skill.name,
                'description': skill.description,
                'version': skill.metadata.get('version', 'unknown'),
            }
            for skill in self._skills.values()
        ]


# =============================================================================
# LEGACY: Compositional Workflows (YAML files) - kept for backwards compatibility
# =============================================================================

@dataclass
class WorkflowStep:
    """Represents a single step within a workflow execution."""
    action: str
    agent: str
    inputs: List[str]
    outputs: List[str]
    condition: Optional[str] = None
    on_error: str = "fail"
    tool: Optional[str] = None


@dataclass
class Workflow:
    """Represents a loaded workflow definition (YAML)."""
    name: str
    display_name: str
    description: str
    version: str
    type: str  # atomic, composite, conditional
    steps: List[WorkflowStep]
    input_schema: Dict
    output_schema: Dict
    prerequisites: List[Dict] = field(default_factory=list)
    timeout: int = 60000
    retry_policy: Dict = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Workflow':
        """Create Workflow from dictionary (loaded from YAML)."""
        steps = [
            WorkflowStep(
                action=s['action'],
                agent=s['agent'],
                inputs=s.get('inputs', []),
                outputs=s.get('outputs', []),
                condition=s.get('condition'),
                on_error=s.get('onError', 'fail'),
                tool=s.get('tool')
            )
            for s in data.get('steps', [])
        ]

        return cls(
            name=data['name'],
            display_name=data['displayName'],
            description=data['description'],
            version=data['version'],
            type=data['type'],
            steps=steps,
            input_schema=data.get('inputSchema', {}),
            output_schema=data.get('outputSchema', {}),
            prerequisites=data.get('prerequisites', []),
            timeout=data.get('timeout', 60000),
            retry_policy=data.get('retryPolicy', {}),
            metadata=data.get('metadata', {})
        )

    def to_dict(self) -> Dict:
        """Convert Workflow back to dictionary format."""
        return {
            'name': self.name,
            'displayName': self.display_name,
            'description': self.description,
            'version': self.version,
            'type': self.type,
            'steps': [
                {
                    'action': s.action,
                    'agent': s.agent,
                    'inputs': s.inputs,
                    'outputs': s.outputs,
                    **(({'condition': s.condition} if s.condition else {})),
                    'onError': s.on_error,
                    **(({'tool': s.tool} if s.tool else {}))
                }
                for s in self.steps
            ],
            'inputSchema': self.input_schema,
            'outputSchema': self.output_schema,
            'prerequisites': self.prerequisites,
            'timeout': self.timeout,
            'retryPolicy': self.retry_policy,
            'metadata': self.metadata
        }


# Backwards compatibility aliases
SkillStep = WorkflowStep
Skill = Workflow


class WorkflowRegistry:
    """
    Registry for discovering and loading PaperKit compositional workflows (YAML).

    NOTE: This is for YAML workflow orchestration, NOT Agent Skills (SKILL.md).
    For Agent Skills, use AgentSkillRegistry.

    Provides:
    - Workflow discovery and loading
    - Keyword-based workflow matching
    - Category filtering
    - Prerequisite resolution
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the workflow registry.

        Args:
            project_root: Path to project root. Auto-detected if not provided.
        """
        self.project_root = project_root or self._find_project_root()
        self._workflows: Dict[str, Workflow] = {}
        self._keywords_index: Dict[str, Set[str]] = defaultdict(set)
        self._category_index: Dict[str, Set[str]] = defaultdict(set)
        self._loaded = False

    def _find_project_root(self) -> Optional[Path]:
        """Find the project root by looking for .paperkit/ directory."""
        current = Path.cwd()
        for path in [current] + list(current.parents):
            if (path / ".paperkit").is_dir():
                return path
        return None

    def _load_workflows(self) -> None:
        """Load all workflows from the workflows directory."""
        if self._loaded:
            return

        if not self.project_root:
            raise RuntimeError("Could not find PaperKit project root")

        workflows_dir = self.project_root / ".paperkit/_cfg/workflows"

        if not workflows_dir.exists():
            self._loaded = True
            return

        for yaml_file in workflows_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)

                if data and 'name' in data:
                    workflow = Workflow.from_dict(data)
                    self._workflows[workflow.name] = workflow

                    # Index by keywords from metadata tags
                    tags = workflow.metadata.get('tags', [])
                    for tag in tags:
                        self._keywords_index[tag.lower()].add(workflow.name)

                    # Index by words in description
                    desc_words = workflow.description.lower().split()
                    for word in desc_words:
                        if len(word) > 3:  # Skip short words
                            self._keywords_index[word].add(workflow.name)

                    # Index by category
                    category = workflow.metadata.get('category', 'uncategorized')
                    self._category_index[category].add(workflow.name)

            except Exception as e:
                print(f"Warning: Failed to load workflow {yaml_file.name}: {e}", file=sys.stderr)

        self._loaded = True

    def get_workflow(self, name: str) -> Optional[Workflow]:
        """
        Get a workflow by name.

        Args:
            name: Workflow name (e.g., "cite-source")

        Returns:
            Workflow object or None if not found
        """
        self._load_workflows()
        return self._workflows.get(name)

    def list_workflows(self) -> List[Workflow]:
        """
        List all available workflows.

        Returns:
            List of all loaded workflows
        """
        self._load_workflows()
        return list(self._workflows.values())

    def list_workflow_names(self) -> List[str]:
        """
        List all workflow names.

        Returns:
            List of workflow names
        """
        self._load_workflows()
        return list(self._workflows.keys())

    def find_workflows_by_category(self, category: str) -> List[Workflow]:
        """
        Find workflows by category.

        Args:
            category: Category name (e.g., "citations", "writing")

        Returns:
            List of workflows in that category
        """
        self._load_workflows()
        workflow_names = self._category_index.get(category, set())
        return [self._workflows[name] for name in workflow_names if name in self._workflows]

    def find_workflows_for_task(self, task_description: str, limit: int = 5) -> List[tuple]:
        """
        Find workflows that match a task description.

        Uses keyword matching to find relevant workflows.

        Args:
            task_description: Natural language task description
            limit: Maximum number of results

        Returns:
            List of (workflow, score) tuples, sorted by relevance
        """
        self._load_workflows()

        # Tokenize task description
        words = task_description.lower().split()

        # Score each workflow
        scores: Dict[str, float] = defaultdict(float)

        for word in words:
            if len(word) <= 3:
                continue

            # Exact keyword match
            if word in self._keywords_index:
                for workflow_name in self._keywords_index[word]:
                    scores[workflow_name] += 1.0

            # Partial match (word starts with keyword)
            for keyword in self._keywords_index:
                if keyword.startswith(word) or word.startswith(keyword):
                    for workflow_name in self._keywords_index[keyword]:
                        scores[workflow_name] += 0.5

        # Sort by score and return top results
        sorted_workflows = sorted(
            [(self._workflows[name], score) for name, score in scores.items() if name in self._workflows],
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_workflows[:limit]

    def get_workflow_prerequisites(self, workflow_name: str) -> List[Dict]:
        """
        Get all prerequisites for a workflow (recursive).

        Args:
            workflow_name: Name of the workflow

        Returns:
            List of prerequisite dictionaries with type and name
        """
        self._load_workflows()

        workflow = self._workflows.get(workflow_name)
        if not workflow:
            return []

        all_prereqs = []
        visited = set()

        def collect_prereqs(w_name: str):
            if w_name in visited:
                return
            visited.add(w_name)

            w = self._workflows.get(w_name)
            if not w:
                return

            for prereq in w.prerequisites:
                all_prereqs.append(prereq)
                if prereq.get('type') == 'workflow':
                    collect_prereqs(prereq.get('name', ''))

        collect_prereqs(workflow_name)
        return all_prereqs

    def get_workflows_for_agent(self, agent_name: str) -> List[Workflow]:
        """
        Get all workflows that use a specific agent.

        Args:
            agent_name: Name of the agent

        Returns:
            List of workflows that have steps using this agent
        """
        self._load_workflows()

        matching_workflows = []
        for workflow in self._workflows.values():
            for step in workflow.steps:
                if step.agent == agent_name:
                    matching_workflows.append(workflow)
                    break

        return matching_workflows

    def get_categories(self) -> List[str]:
        """
        Get all workflow categories.

        Returns:
            List of category names
        """
        self._load_workflows()
        return list(self._category_index.keys())

    def get_statistics(self) -> Dict:
        """
        Get workflow registry statistics.

        Returns:
            Dictionary with counts and categorizations
        """
        self._load_workflows()

        type_counts = defaultdict(int)
        for workflow in self._workflows.values():
            type_counts[workflow.type] += 1

        return {
            'total_workflows': len(self._workflows),
            'by_type': dict(type_counts),
            'by_category': {cat: len(workflows) for cat, workflows in self._category_index.items()},
            'categories': list(self._category_index.keys())
        }

    def to_agent_format(self) -> List[Dict]:
        """
        Convert workflow registry to format suitable for agent routing.

        Returns:
            List of workflow summaries for orchestrator consumption
        """
        self._load_workflows()

        return [
            {
                'name': workflow.name,
                'displayName': workflow.display_name,
                'description': workflow.description,
                'type': workflow.type,
                'category': workflow.metadata.get('category', 'uncategorized'),
                'tags': workflow.metadata.get('tags', []),
                'requiredInputs': [
                    k for k, v in workflow.input_schema.get('properties', {}).items()
                    if k in workflow.input_schema.get('required', [])
                ],
                'agents': list(set(step.agent for step in workflow.steps))
            }
            for workflow in self._workflows.values()
        ]


SKILL_WORKFLOW_NAMES = (
    "cite-source",
    "validate-citation",
    "draft-section",
    "research-topic",
    "compile-latex",
)


class SkillRegistry(WorkflowRegistry):
    """
    Registry for the executable skill workflows introduced by the skill system.

    WorkflowRegistry intentionally exposes every PaperKit workflow. This wrapper
    keeps the older SkillRegistry API focused on the five workflow-backed skills
    used by SkillExecutor and the generated skill-system contract.
    """

    def _load_workflows(self) -> None:
        """Load only workflow definitions that are modeled as executable skills."""
        if self._loaded:
            return

        super()._load_workflows()

        self._workflows = {
            name: self._workflows[name]
            for name in SKILL_WORKFLOW_NAMES
            if name in self._workflows
        }

        self._keywords_index.clear()
        self._category_index.clear()

        for workflow in self._workflows.values():
            tags = workflow.metadata.get('tags', [])
            for tag in tags:
                self._keywords_index[tag.lower()].add(workflow.name)

            for word in workflow.description.lower().split():
                if len(word) > 3:
                    self._keywords_index[word].add(workflow.name)

            category = workflow.metadata.get('category', 'uncategorized')
            self._category_index[category].add(workflow.name)

    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a skill workflow by name."""
        return self.get_workflow(name)

    def list_skills(self) -> List[Skill]:
        """List all skill workflows in manifest order."""
        self._load_workflows()
        return [
            self._workflows[name]
            for name in SKILL_WORKFLOW_NAMES
            if name in self._workflows
        ]

    def find_skills_by_category(self, category: str) -> List[Skill]:
        """Find skill workflows by category."""
        return self.find_workflows_by_category(category)

    def find_skills_for_task(self, task_description: str, limit: int = 5) -> List[tuple]:
        """Find skill workflows that match a task description."""
        return self.find_workflows_for_task(task_description, limit=limit)

    def get_skill_prerequisites(self, skill_name: str) -> List[Dict]:
        """Get all prerequisites for a skill workflow."""
        return self.get_workflow_prerequisites(skill_name)

    def get_skills_for_agent(self, agent_name: str) -> List[Skill]:
        """Get all skill workflows that use a specific agent."""
        return self.get_workflows_for_agent(agent_name)

    def get_statistics(self) -> Dict:
        """Get skill registry statistics."""
        stats = super().get_statistics()
        return {
            'total_skills': stats['total_workflows'],
            'total_workflows': stats['total_workflows'],
            'by_type': stats['by_type'],
            'by_category': stats['by_category'],
            'categories': stats['categories'],
        }


def main():
    """CLI interface for skill and workflow registries."""
    import argparse

    parser = argparse.ArgumentParser(
        description="PaperKit Agent Skills & Workflow Registry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Agent Skills (agentskills.io SKILL.md format)
  python skill_registry.py skills --list
  python skill_registry.py skills --find "citation harvard"
  python skill_registry.py skills --get harvard-citations
  python skill_registry.py skills --benchmark

  # Compositional Workflows (YAML format)
  python skill_registry.py workflows --list
  python skill_registry.py workflows --find "compile latex"
  python skill_registry.py workflows --stats
        """
    )

    subparsers = parser.add_subparsers(dest='registry', help='Registry type')

    # Agent Skills subparser
    skills_parser = subparsers.add_parser('skills', help='Agent Skills (SKILL.md)')
    skills_parser.add_argument('--list', action='store_true', help='List all skills')
    skills_parser.add_argument('--find', type=str, help='Search for skills matching query')
    skills_parser.add_argument('--get', type=str, help='Get metadata for a specific skill')
    skills_parser.add_argument('--content', type=str, help='Load full content for a skill')
    skills_parser.add_argument('--benchmark', action='store_true', help='Benchmark load time')
    skills_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # Workflows subparser
    workflows_parser = subparsers.add_parser('workflows', help='Compositional Workflows (YAML)')
    workflows_parser.add_argument('--list', action='store_true', help='List all workflows')
    workflows_parser.add_argument('--find', type=str, help='Search query for find command')
    workflows_parser.add_argument('--get', type=str, help='Workflow name for get command')
    workflows_parser.add_argument('--category', '-c', help='Filter by category')
    workflows_parser.add_argument('--stats', action='store_true', help='Show statistics')
    workflows_parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if args.registry == 'skills':
        registry = AgentSkillRegistry()

        if args.benchmark:
            # Run multiple times for accurate measurement
            times = []
            for _ in range(10):
                registry._loaded = False
                registry._skills.clear()
                times.append(registry.load_all())

            avg_time = sum(times) / len(times)
            print(f"Load time (avg of 10): {avg_time:.2f}ms")
            print(f"Skills loaded: {registry.skill_count}")
            print(f"Target: <50ms - {'✓ PASS' if avg_time < 50 else '✗ FAIL'}")
            return

        if args.list:
            registry.load_all()
            print(f"Loaded {registry.skill_count} skills in {registry.load_time_ms:.2f}ms\n")
            for skill in registry.list_skills():
                if args.json:
                    print(json.dumps(skill.to_dict()))
                else:
                    print(f"  {skill.name}")
                    print(f"    {skill.description[:80]}...")
                    print()
            return

        if args.find:
            matches = registry.find_skills(args.find)
            print(f"Found {len(matches)} matches for '{args.find}':\n")
            for match in matches:
                if args.json:
                    print(json.dumps({
                        'skill': match.skill.to_dict(),
                        'score': match.score,
                        'matched_terms': match.matched_terms
                    }))
                else:
                    print(f"  {match.skill.name} (score: {match.score:.2f})")
                    print(f"    Matched: {', '.join(match.matched_terms)}")
                    print()
            return

        if args.get:
            skill = registry.get_skill(args.get)
            if skill:
                if args.json:
                    print(json.dumps(skill.to_dict(), indent=2))
                else:
                    print(f"Name: {skill.name}")
                    print(f"Description: {skill.description}")
                    print(f"Path: {skill.path}")
                    if skill.metadata:
                        print(f"Metadata: {skill.metadata}")
            else:
                print(f"Skill not found: {args.get}", file=sys.stderr)
                sys.exit(1)
            return

        if args.content:
            content = registry.load_skill_content(args.content)
            if content:
                print(content)
            else:
                print(f"Skill not found: {args.content}", file=sys.stderr)
                sys.exit(1)
            return

        skills_parser.print_help()

    elif args.registry == 'workflows':
        registry = WorkflowRegistry()

        if args.list:
            if args.category:
                workflows = registry.find_workflows_by_category(args.category)
            else:
                workflows = registry.list_workflows()

            if args.json:
                print(json.dumps([w.to_dict() for w in workflows], indent=2))
            else:
                for workflow in workflows:
                    print(f"  {workflow.name} ({workflow.type}): {workflow.description}")
            return

        if args.get:
            workflow = registry.get_workflow(args.get)
            if workflow:
                if args.json:
                    print(json.dumps(workflow.to_dict(), indent=2))
                else:
                    print(f"Name: {workflow.name}")
                    print(f"Display Name: {workflow.display_name}")
                    print(f"Description: {workflow.description}")
                    print(f"Version: {workflow.version}")
                    print(f"Type: {workflow.type}")
                    print(f"Steps: {len(workflow.steps)}")
                    print(f"Prerequisites: {len(workflow.prerequisites)}")
            else:
                print(f"Workflow not found: {args.get}", file=sys.stderr)
                sys.exit(1)
            return

        if args.find:
            results = registry.find_workflows_for_task(args.find)
            if args.json:
                print(json.dumps([{'workflow': w.name, 'score': score} for w, score in results], indent=2))
            else:
                for workflow, score in results:
                    print(f"  {workflow.name} (score: {score:.1f}): {workflow.description}")
            return

        if args.stats:
            stats = registry.get_statistics()
            if args.json:
                print(json.dumps(stats, indent=2))
            else:
                print(f"Total Workflows: {stats['total_workflows']}")
                print("By Type:")
                for t, c in stats['by_type'].items():
                    print(f"  {t}: {c}")
                print("By Category:")
                for cat, c in stats['by_category'].items():
                    print(f"  {cat}: {c}")
            return

        workflows_parser.print_help()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
