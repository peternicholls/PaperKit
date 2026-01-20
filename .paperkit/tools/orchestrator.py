#!/usr/bin/env python3

"""
PaperKit Orchestrator Runtime

Implements intelligent multi-step task routing with:
- Intent classification from user requests (FR-018)
- Confidence scoring for agent routing (FR-020)
- Top-3 fallback when confidence < 0.7 (FR-021)
- Tie-break rules for equal scores (FR-022)
- Multi-step workflow generation (FR-019)
- Workflow state management (FR-024, FR-025)

Usage:
    from orchestrator import Orchestrator
    
    orch = Orchestrator()
    decision = orch.route("Draft my introduction section")
    
    # For multi-step workflows
    workflow = orch.generate_workflow("Research topic X and draft a section")
"""

import sys
import re
import json
import yaml
import time
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
import hashlib


# =============================================================================
# Data Models
# =============================================================================

@dataclass
class Intent:
    """Represents a parsed user intent."""
    raw_text: str
    tokens: List[str]
    action_verbs: List[str]
    entities: List[str]
    is_multi_intent: bool = False
    sub_intents: List['Intent'] = field(default_factory=list)


@dataclass
class AgentMatch:
    """Represents an agent match with confidence score."""
    agent_name: str
    confidence: float
    keyword_matches: List[str]
    when_to_use_matches: List[str]
    exclusion_matches: List[str]
    missing_inputs: List[str]
    reasoning: str


@dataclass
class RoutingDecision:
    """The final routing decision."""
    decision: str  # "route", "ask_clarifying_question", "present_options"
    agent: Optional[str]
    confidence: float
    reason: str
    missing_inputs: List[str]
    suggested_next_prompt: str
    alternatives: List[AgentMatch] = field(default_factory=list)


@dataclass
class WorkflowStep:
    """A step in a generated workflow."""
    step_id: str
    agent: str
    action: str
    inputs: List[str]
    outputs: List[str]
    depends_on: List[str]
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[Any] = None  # Output from completed step (FR-026)


@dataclass
class GeneratedWorkflow:
    """A dynamically generated workflow."""
    workflow_id: str
    user_request: str
    steps: List[WorkflowStep]
    current_step: int = 0
    state: Dict[str, Any] = field(default_factory=dict)
    step_outputs: Dict[str, Any] = field(default_factory=dict)  # Map step_id -> output (FR-026)
    created_at: str = ""
    updated_at: str = ""
    approved: bool = False  # User approval flag (FR-023)


@dataclass
class WorkflowPresentation:
    """
    Presentation format for workflow user approval.
    Implements FR-023: System MUST present generated workflows to users for review before execution.
    """
    workflow_id: str
    summary: str
    steps_preview: List[Dict[str, str]]
    estimated_agents: List[str]
    requires_approval: bool = True
    approval_prompt: str = "Do you want to execute this workflow? (yes/no/modify)"


# =============================================================================
# Intent Parser (FR-018)
# =============================================================================

class IntentParser:
    """
    Parses user requests to identify single or multiple intents.
    Implements FR-018: Orchestrator MUST analyze user requests to identify 
    single or multiple intents.
    """
    
    # Action verbs that indicate distinct intents
    ACTION_VERBS = {
        "research": ["research", "find", "search", "discover", "locate", "investigate"],
        "write": ["write", "draft", "compose", "create", "author"],
        "review": ["review", "check", "validate", "verify", "audit"],
        "refine": ["refine", "polish", "improve", "edit", "rewrite", "tighten"],
        "explain": ["explain", "teach", "clarify", "describe", "help understand"],
        "structure": ["structure", "outline", "organize", "plan", "architect"],
        "compile": ["compile", "build", "generate", "assemble", "format"],
        "cite": ["cite", "reference", "bibliography", "bib"],
        "brainstorm": ["brainstorm", "ideate", "think", "explore"],
        "debug": ["debug", "fix", "solve", "troubleshoot", "diagnose"],
    }
    
    # Conjunctions that may indicate multiple intents
    MULTI_INTENT_MARKERS = ["and then", "then", "after that", "followed by", "next", "also"]
    
    def __init__(self):
        # Build reverse lookup for action verbs
        self._verb_to_action = {}
        for action, verbs in self.ACTION_VERBS.items():
            for verb in verbs:
                self._verb_to_action[verb] = action
    
    def parse(self, text: str) -> Intent:
        """Parse user request into intent(s)."""
        # Normalize text
        text_lower = text.lower().strip()
        
        # Tokenize
        tokens = re.findall(r'\b\w+\b', text_lower)
        
        # Extract action verbs
        action_verbs = []
        for token in tokens:
            if token in self._verb_to_action:
                action_verbs.append(token)
        
        # Extract entities (quoted strings, section names, etc.)
        entities = self._extract_entities(text)
        
        # Check for multi-intent markers
        is_multi = self._is_multi_intent(text_lower)
        
        intent = Intent(
            raw_text=text,
            tokens=tokens,
            action_verbs=action_verbs,
            entities=entities,
            is_multi_intent=is_multi,
        )
        
        # If multi-intent, split into sub-intents
        if is_multi:
            intent.sub_intents = self._split_intents(text)
        
        return intent
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract entities from text (quoted strings, section names)."""
        entities = []
        
        # Quoted strings
        quoted = re.findall(r'"([^"]+)"', text)
        entities.extend(quoted)
        quoted = re.findall(r"'([^']+)'", text)
        entities.extend(quoted)
        
        # Section names
        section_pattern = r'\b(introduction|abstract|methodology|methods|results|discussion|conclusion|related work|literature review|background)\b'
        sections = re.findall(section_pattern, text.lower())
        entities.extend(sections)
        
        return entities
    
    def _is_multi_intent(self, text: str) -> bool:
        """Check if text contains multiple intents."""
        # Check for explicit multi-intent markers (phrases, not just "and")
        for marker in self.MULTI_INTENT_MARKERS:
            # Use word boundaries for matching
            if re.search(rf'\b{re.escape(marker)}\b', text, re.IGNORECASE):
                return True
        
        return False
    
    def _split_intents(self, text: str) -> List[Intent]:
        """Split multi-intent text into separate intents."""
        sub_intents = []
        
        # Split on markers (use explicit markers only)
        pattern = r'\b(?:and then|then|after that|followed by|next|also)\b'
        parts = re.split(pattern, text, flags=re.IGNORECASE)
        
        for part in parts:
            part = part.strip()
            if part and len(part) > 3:  # Skip very short fragments
                # Create a simple intent without recursion
                tokens = re.findall(r'\b\w+\b', part.lower())
                action_verbs = [t for t in tokens if t in self._verb_to_action]
                entities = self._extract_entities(part)
                
                sub_intent = Intent(
                    raw_text=part,
                    tokens=tokens,
                    action_verbs=action_verbs,
                    entities=entities,
                    is_multi_intent=False,  # Prevent recursion
                    sub_intents=[],
                )
                sub_intents.append(sub_intent)
        
        return sub_intents


# =============================================================================
# Confidence Scorer (FR-020)
# =============================================================================

class ConfidenceScorer:
    """
    Calculates confidence scores for agent routing.
    Implements FR-020: Orchestrator MUST calculate confidence scores for 
    agent routing using keyword matching and routing registry rules.
    """
    
    # Weights for different matching types
    KEYWORD_WEIGHT = 0.3
    WHEN_TO_USE_WEIGHT = 0.5
    EXCLUSION_PENALTY = 0.4
    REQUIRED_INPUT_PENALTY = 0.2
    
    # Threshold for automatic routing (FR-021)
    CONFIDENCE_THRESHOLD = 0.7
    
    def __init__(self, routing_registry: Dict):
        self.registry = routing_registry
        self._build_indices()
    
    def _build_indices(self):
        """Build keyword indices for fast matching."""
        self._keyword_to_agents: Dict[str, Set[str]] = defaultdict(set)
        
        for agent in self.registry.get('agents', []):
            agent_name = agent['name']
            for keyword in agent.get('keywords', []):
                self._keyword_to_agents[keyword.lower()].add(agent_name)
    
    def score_agents(self, intent: Intent, available_agents: List[str]) -> List[AgentMatch]:
        """
        Score all available agents for the given intent.
        Returns list sorted by confidence (highest first).
        """
        matches = []
        
        for agent in self.registry.get('agents', []):
            agent_name = agent['name']
            if agent_name not in available_agents:
                continue
            
            match = self._score_agent(intent, agent)
            matches.append(match)
        
        # Sort by confidence descending
        matches.sort(key=lambda m: m.confidence, reverse=True)
        return matches
    
    def _score_agent(self, intent: Intent, agent: Dict) -> AgentMatch:
        """Calculate confidence score for a single agent."""
        agent_name = agent['name']
        keywords = [k.lower() for k in agent.get('keywords', [])]
        when_to_use = agent.get('whenToUse', [])
        hard_exclusions = agent.get('hardExclusions', [])
        required_inputs = agent.get('requiredInputs', [])
        
        score = 0.0
        keyword_matches = []
        when_to_use_matches = []
        exclusion_matches = []
        reasoning_parts = []
        
        # Keyword matching
        intent_text = intent.raw_text.lower()
        for keyword in keywords:
            if keyword in intent_text:
                keyword_matches.append(keyword)
        
        if keyword_matches:
            keyword_score = min(1.0, len(keyword_matches) / max(1, len(keywords) / 2))
            score += keyword_score * self.KEYWORD_WEIGHT
            reasoning_parts.append(f"Keywords matched: {', '.join(keyword_matches)}")
        
        # When to use matching (semantic)
        for use_case in when_to_use:
            use_case_lower = use_case.lower()
            # Check for significant word overlap
            use_words = set(re.findall(r'\b\w+\b', use_case_lower))
            intent_words = set(intent.tokens)
            overlap = use_words & intent_words
            if len(overlap) >= 2:
                when_to_use_matches.append(use_case)
        
        if when_to_use_matches:
            when_score = min(1.0, len(when_to_use_matches) / len(when_to_use))
            score += when_score * self.WHEN_TO_USE_WEIGHT
            reasoning_parts.append(f"Use case matches: {len(when_to_use_matches)}")
        
        # Exclusion checking
        for exclusion in hard_exclusions:
            exclusion_lower = exclusion.lower()
            exclusion_words = set(re.findall(r'\b\w+\b', exclusion_lower))
            intent_words = set(intent.tokens)
            overlap = exclusion_words & intent_words
            if len(overlap) >= 2:
                exclusion_matches.append(exclusion)
        
        if exclusion_matches:
            score -= self.EXCLUSION_PENALTY
            reasoning_parts.append(f"Exclusion hit: {exclusion_matches[0]}")
        
        # Check for missing required inputs
        missing_inputs = []
        for req_input in required_inputs:
            # Simple heuristic: check if the input type is mentioned
            if req_input.lower() not in intent_text:
                missing_inputs.append(req_input)
        
        if missing_inputs:
            score -= self.REQUIRED_INPUT_PENALTY * len(missing_inputs)
            reasoning_parts.append(f"Missing inputs: {', '.join(missing_inputs)}")
        
        # Clamp score to [0, 1]
        score = max(0.0, min(1.0, score))
        
        reasoning = "; ".join(reasoning_parts) if reasoning_parts else "No strong matches"
        
        return AgentMatch(
            agent_name=agent_name,
            confidence=score,
            keyword_matches=keyword_matches,
            when_to_use_matches=when_to_use_matches,
            exclusion_matches=exclusion_matches,
            missing_inputs=missing_inputs,
            reasoning=reasoning,
        )


# =============================================================================
# Tie-Break Rules (FR-022)
# =============================================================================

class TieBreaker:
    """
    Implements tie-break rules when multiple agents have equal confidence.
    Implements FR-022: Orchestrator MUST apply explicit tie-break rules 
    when multiple agents have equal scores.
    """
    
    # Priority order for agents (first = higher priority)
    AGENT_PRIORITY = [
        "reference-manager",      # Most specific tasks
        "latex-assembler",
        "section-drafter",
        "quality-refiner",
        "paper-architect",
        "research-consolidator",
        "librarian",
        "tutor",
        "brainstorm",
        "problem-solver",         # Most general
    ]
    
    def break_tie(self, matches: List[AgentMatch]) -> List[AgentMatch]:
        """
        Apply tie-break rules to sort agents with equal confidence.
        
        Rules (in order):
        1. More keyword matches wins
        2. Fewer exclusion matches wins
        3. Fewer missing inputs wins
        4. Priority order (more specific agents first)
        """
        if len(matches) <= 1:
            return matches
        
        def sort_key(match: AgentMatch):
            priority_idx = (
                self.AGENT_PRIORITY.index(match.agent_name)
                if match.agent_name in self.AGENT_PRIORITY
                else len(self.AGENT_PRIORITY)
            )
            return (
                -match.confidence,           # Higher confidence first
                -len(match.keyword_matches), # More keyword matches first
                len(match.exclusion_matches), # Fewer exclusions first
                len(match.missing_inputs),    # Fewer missing inputs first
                priority_idx,                 # Priority order
            )
        
        return sorted(matches, key=sort_key)


# =============================================================================
# Main Orchestrator Class
# =============================================================================

class Orchestrator:
    """
    Main orchestrator for intelligent task routing.
    
    Combines intent parsing, confidence scoring, and routing decisions
    with support for multi-step workflow generation.
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or self._find_project_root()
        self._routing_registry: Optional[Dict] = None
        self._intent_parser = IntentParser()
        self._tie_breaker = TieBreaker()
        self._scorer: Optional[ConfidenceScorer] = None
        self._available_agents: List[str] = []
        
        # Load resources
        self._load_routing_registry()
        self._discover_agents()
    
    def _find_project_root(self) -> Optional[Path]:
        """Find project root by looking for .paperkit/ directory."""
        current = Path.cwd()
        for path in [current] + list(current.parents):
            if (path / ".paperkit").is_dir():
                return path
        return None
    
    def _load_routing_registry(self):
        """Load the routing registry."""
        if not self.project_root:
            return
        
        registry_path = self.project_root / ".paperkit" / "_cfg" / "routing.registry.yaml"
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                registry_data = yaml.safe_load(f)
            if registry_data:
                self._routing_registry = registry_data
                self._scorer = ConfidenceScorer(registry_data)
    
    def _discover_agents(self):
        """Discover available agents."""
        if not self.project_root:
            return
        
        agents_dir = self.project_root / ".paperkit" / "_cfg" / "agents"
        if agents_dir.exists():
            for yaml_file in agents_dir.glob("*.yaml"):
                try:
                    with open(yaml_file, 'r') as f:
                        data = yaml.safe_load(f)
                    if data and 'name' in data:
                        self._available_agents.append(data['name'])
                except Exception:
                    pass
    
    def route(self, user_request: str) -> RoutingDecision:
        """
        Route a user request to the appropriate agent.
        
        Implements:
        - FR-018: Intent analysis
        - FR-020: Confidence scoring
        - FR-021: Top-3 fallback when confidence < 0.7
        - FR-022: Tie-break rules
        
        Returns:
            RoutingDecision with agent recommendation or clarification request
        """
        start_time = time.perf_counter()
        
        # Parse intent
        intent = self._intent_parser.parse(user_request)
        
        # Score agents
        if not self._scorer or not self._available_agents:
            return RoutingDecision(
                decision="ask_clarifying_question",
                agent=None,
                confidence=0.0,
                reason="No agents available for routing",
                missing_inputs=[],
                suggested_next_prompt="Please configure agents in .paperkit/_cfg/agents/",
            )
        
        matches = self._scorer.score_agents(intent, self._available_agents)
        
        # Apply tie-break rules
        matches = self._tie_breaker.break_tie(matches)
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        # No matches
        if not matches:
            return RoutingDecision(
                decision="ask_clarifying_question",
                agent=None,
                confidence=0.0,
                reason="No matching agents found",
                missing_inputs=[],
                suggested_next_prompt="Could you rephrase your request? I couldn't find a suitable agent.",
            )
        
        top_match = matches[0]
        
        # Check confidence threshold (FR-021)
        if top_match.confidence >= ConfidenceScorer.CONFIDENCE_THRESHOLD:
            # High confidence - auto-route
            if top_match.missing_inputs:
                return RoutingDecision(
                    decision="ask_clarifying_question",
                    agent=top_match.agent_name,
                    confidence=top_match.confidence,
                    reason=f"Agent '{top_match.agent_name}' matched but requires additional inputs",
                    missing_inputs=top_match.missing_inputs,
                    suggested_next_prompt=f"Please provide: {', '.join(top_match.missing_inputs)}",
                )
            
            return RoutingDecision(
                decision="route",
                agent=top_match.agent_name,
                confidence=top_match.confidence,
                reason=top_match.reasoning,
                missing_inputs=[],
                suggested_next_prompt=user_request,
            )
        
        # Low confidence - present top 3 options (FR-021)
        top_3 = matches[:3]
        alternatives = top_3[1:] if len(top_3) > 1 else []
        
        options_text = "\n".join([
            f"  {i+1}. {m.agent_name} (confidence: {m.confidence:.2f})"
            for i, m in enumerate(top_3)
        ])
        
        return RoutingDecision(
            decision="present_options",
            agent=top_match.agent_name,  # Still provide best guess
            confidence=top_match.confidence,
            reason=f"Confidence below threshold ({top_match.confidence:.2f} < 0.70). Top options:\n{options_text}",
            missing_inputs=top_match.missing_inputs,
            suggested_next_prompt="Please select an agent by number or rephrase your request:",
            alternatives=alternatives,
        )
    
    def generate_workflow(self, user_request: str) -> GeneratedWorkflow:
        """
        Generate a multi-step workflow for complex requests.
        
        Implements FR-019: Orchestrator MUST generate multi-step workflows 
        with dependency resolution.
        
        Returns:
            GeneratedWorkflow with steps and dependencies
        """
        # Parse intent
        intent = self._intent_parser.parse(user_request)
        
        # Generate workflow ID
        workflow_id = hashlib.md5(
            f"{user_request}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        steps = []
        
        if intent.is_multi_intent and intent.sub_intents:
            # Multi-intent: create step for each sub-intent
            prev_step_id = None
            for i, sub_intent in enumerate(intent.sub_intents):
                decision = self.route(sub_intent.raw_text)
                
                step_id = f"step_{i+1}"
                step = WorkflowStep(
                    step_id=step_id,
                    agent=decision.agent or "unknown",
                    action=sub_intent.action_verbs[0] if sub_intent.action_verbs else "process",
                    inputs=sub_intent.entities,
                    outputs=[f"output_{step_id}"],
                    depends_on=[prev_step_id] if prev_step_id else [],
                )
                steps.append(step)
                prev_step_id = step_id
        else:
            # Single intent: create single step
            decision = self.route(user_request)
            step = WorkflowStep(
                step_id="step_1",
                agent=decision.agent or "unknown",
                action=intent.action_verbs[0] if intent.action_verbs else "process",
                inputs=intent.entities,
                outputs=["result"],
                depends_on=[],
            )
            steps.append(step)
        
        now = datetime.now().isoformat()
        return GeneratedWorkflow(
            workflow_id=workflow_id,
            user_request=user_request,
            steps=steps,
            created_at=now,
            updated_at=now,
        )
    
    def present_workflow(self, workflow: GeneratedWorkflow) -> WorkflowPresentation:
        """
        Present a workflow to the user for approval.
        
        Implements FR-023: System MUST present generated workflows to users 
        for review before execution.
        
        Args:
            workflow: The generated workflow to present
            
        Returns:
            WorkflowPresentation with human-readable summary
        """
        # Build step previews with clear descriptions
        steps_preview = []
        for step in workflow.steps:
            deps_text = ""
            if step.depends_on:
                deps_text = f" (after: {', '.join(step.depends_on)})"
            
            preview = {
                "step_id": step.step_id,
                "description": f"Use {step.agent} to {step.action}",
                "inputs": ", ".join(step.inputs) if step.inputs else "none",
                "dependencies": deps_text,
            }
            steps_preview.append(preview)
        
        # Collect unique agents
        agents = list(dict.fromkeys(s.agent for s in workflow.steps))
        
        # Build summary
        step_count = len(workflow.steps)
        summary = f"Workflow with {step_count} step{'s' if step_count > 1 else ''} using {', '.join(agents)}"
        
        return WorkflowPresentation(
            workflow_id=workflow.workflow_id,
            summary=summary,
            steps_preview=steps_preview,
            estimated_agents=agents,
            requires_approval=True,
            approval_prompt="Do you want to execute this workflow? (yes/no/modify)",
        )
    
    def approve_workflow(self, workflow: GeneratedWorkflow) -> GeneratedWorkflow:
        """
        Mark a workflow as approved for execution.
        
        Args:
            workflow: The workflow to approve
            
        Returns:
            Updated workflow with approved=True
        """
        workflow.approved = True
        workflow.updated_at = datetime.now().isoformat()
        return workflow
    
    def execute_step(
        self, 
        workflow: GeneratedWorkflow, 
        step_id: str, 
        step_result: Any
    ) -> GeneratedWorkflow:
        """
        Record the output of a completed workflow step.
        
        Implements FR-026: System MUST pass output from completed steps 
        as input to dependent steps.
        
        Args:
            workflow: The workflow being executed
            step_id: ID of the completed step
            step_result: Output from the step execution
            
        Returns:
            Updated workflow with step output stored
        """
        # Find and update the step
        for step in workflow.steps:
            if step.step_id == step_id:
                step.status = "completed"
                step.result = step_result
                break
        
        # Store output for dependent steps
        workflow.step_outputs[step_id] = step_result
        workflow.updated_at = datetime.now().isoformat()
        
        # Advance current_step counter
        completed_count = sum(1 for s in workflow.steps if s.status == "completed")
        workflow.current_step = completed_count
        
        return workflow
    
    def get_step_inputs(self, workflow: GeneratedWorkflow, step_id: str) -> Dict[str, Any]:
        """
        Get inputs for a step including outputs from dependencies.
        
        Implements FR-026: System MUST pass output from completed steps 
        as input to dependent steps.
        
        Args:
            workflow: The workflow being executed
            step_id: ID of the step needing inputs
            
        Returns:
            Dictionary with step's declared inputs plus dependency outputs
        """
        # Find the step
        step = None
        for s in workflow.steps:
            if s.step_id == step_id:
                step = s
                break
        
        if not step:
            return {}
        
        inputs = {
            "declared_inputs": step.inputs,
            "dependency_outputs": {},
        }
        
        # Collect outputs from dependencies
        for dep_id in step.depends_on:
            if dep_id in workflow.step_outputs:
                inputs["dependency_outputs"][dep_id] = workflow.step_outputs[dep_id]
        
        return inputs
    
    def get_next_step(self, workflow: GeneratedWorkflow) -> Optional[WorkflowStep]:
        """
        Get the next step ready for execution.
        
        A step is ready when:
        - Status is 'pending'
        - All dependencies are 'completed'
        
        Returns:
            Next executable step or None if workflow complete/blocked
        """
        for step in workflow.steps:
            if step.status != "pending":
                continue
            
            # Check all dependencies are completed
            deps_complete = all(
                any(s.step_id == dep and s.status == "completed" for s in workflow.steps)
                for dep in step.depends_on
            )
            
            if deps_complete:
                return step
        
        return None
    
    def get_workflow_status(self, workflow: GeneratedWorkflow) -> Dict[str, Any]:
        """
        Get the current status of a workflow.
        
        Returns:
            Status dictionary with progress and step states
        """
        total = len(workflow.steps)
        completed = sum(1 for s in workflow.steps if s.status == "completed")
        failed = sum(1 for s in workflow.steps if s.status == "failed")
        in_progress = sum(1 for s in workflow.steps if s.status == "in_progress")
        pending = sum(1 for s in workflow.steps if s.status == "pending")
        
        # Determine overall status
        if failed > 0:
            status = "failed"
        elif completed == total:
            status = "completed"
        elif in_progress > 0:
            status = "in_progress"
        else:
            status = "pending"
        
        return {
            "workflow_id": workflow.workflow_id,
            "approved": workflow.approved,
            "status": status,
            "progress": f"{completed}/{total}",
            "steps": {
                "total": total,
                "completed": completed,
                "in_progress": in_progress,
                "pending": pending,
                "failed": failed,
            },
            "current_outputs": workflow.step_outputs,
        }
    
    def get_agent_info(self, agent_name: str) -> Optional[Dict]:
        """Get detailed info about an agent."""
        if not self._routing_registry:
            return None
        
        for agent in self._routing_registry.get('agents', []):
            if agent['name'] == agent_name:
                return agent
        return None
    
    # =========================================================================
    # Checkpoint Management (FR-024, FR-025)
    # =========================================================================
    
    def _get_checkpoints_dir(self) -> Path:
        """Get the checkpoints directory, creating if needed."""
        if not self.project_root:
            raise RuntimeError("Project root not found")
        
        checkpoints_dir = self.project_root / ".paperkit" / "data" / "checkpoints"
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        return checkpoints_dir
    
    def save_checkpoint(self, workflow: GeneratedWorkflow) -> str:
        """
        Save workflow state to a checkpoint file.
        
        Implements FR-024: System MUST checkpoint workflow state after each 
        completed step.
        
        Args:
            workflow: The workflow to checkpoint
            
        Returns:
            Path to the checkpoint file
        """
        checkpoints_dir = self._get_checkpoints_dir()
        checkpoint_path = checkpoints_dir / f"{workflow.workflow_id}.checkpoint.json"
        
        # Serialize workflow state
        checkpoint_data = {
            "workflow_id": workflow.workflow_id,
            "user_request": workflow.user_request,
            "current_step": workflow.current_step,
            "state": workflow.state,
            "step_outputs": workflow.step_outputs,
            "created_at": workflow.created_at,
            "updated_at": datetime.now().isoformat(),
            "approved": workflow.approved,
            "steps": [
                {
                    "step_id": s.step_id,
                    "agent": s.agent,
                    "action": s.action,
                    "inputs": s.inputs,
                    "outputs": s.outputs,
                    "depends_on": s.depends_on,
                    "status": s.status,
                    "result": s.result,
                }
                for s in workflow.steps
            ]
        }
        
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
        
        return str(checkpoint_path)
    
    def load_checkpoint(self, workflow_id: str) -> Optional[GeneratedWorkflow]:
        """
        Load workflow state from a checkpoint file.
        
        Implements FR-025: System MUST support workflow resumption from last 
        checkpoint after interruption.
        
        Args:
            workflow_id: The workflow ID to load
            
        Returns:
            Restored GeneratedWorkflow or None if not found
        """
        checkpoints_dir = self._get_checkpoints_dir()
        checkpoint_path = checkpoints_dir / f"{workflow_id}.checkpoint.json"
        
        if not checkpoint_path.exists():
            return None
        
        with open(checkpoint_path, 'r') as f:
            data = json.load(f)
        
        # Reconstruct workflow steps
        steps = [
            WorkflowStep(
                step_id=s["step_id"],
                agent=s["agent"],
                action=s["action"],
                inputs=s["inputs"],
                outputs=s["outputs"],
                depends_on=s["depends_on"],
                status=s["status"],
                result=s.get("result"),
            )
            for s in data["steps"]
        ]
        
        # Reconstruct workflow
        workflow = GeneratedWorkflow(
            workflow_id=data["workflow_id"],
            user_request=data["user_request"],
            steps=steps,
            current_step=data["current_step"],
            state=data.get("state", {}),
            step_outputs=data.get("step_outputs", {}),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            approved=data.get("approved", False),
        )
        
        return workflow
    
    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """
        List all available checkpoints.
        
        Returns:
            List of checkpoint summaries
        """
        checkpoints_dir = self._get_checkpoints_dir()
        checkpoints = []
        
        for checkpoint_file in checkpoints_dir.glob("*.checkpoint.json"):
            try:
                with open(checkpoint_file, 'r') as f:
                    data = json.load(f)
                
                # Calculate progress
                steps = data.get("steps", [])
                completed = sum(1 for s in steps if s["status"] == "completed")
                total = len(steps)
                
                checkpoints.append({
                    "workflow_id": data["workflow_id"],
                    "user_request": data["user_request"],
                    "progress": f"{completed}/{total}",
                    "updated_at": data["updated_at"],
                    "status": "completed" if completed == total else "in_progress",
                })
            except Exception:
                pass
        
        return sorted(checkpoints, key=lambda x: x["updated_at"], reverse=True)
    
    def delete_checkpoint(self, workflow_id: str) -> bool:
        """
        Delete a checkpoint file.
        
        Args:
            workflow_id: The workflow ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        checkpoints_dir = self._get_checkpoints_dir()
        checkpoint_path = checkpoints_dir / f"{workflow_id}.checkpoint.json"
        
        if checkpoint_path.exists():
            checkpoint_path.unlink()
            return True
        return False
    
    def execute_step_with_checkpoint(
        self, 
        workflow: GeneratedWorkflow, 
        step_id: str, 
        step_result: Any
    ) -> GeneratedWorkflow:
        """
        Execute a step and automatically save checkpoint.
        
        Implements FR-024: System MUST checkpoint workflow state after each 
        completed step.
        
        Args:
            workflow: The workflow being executed
            step_id: ID of the completed step
            step_result: Output from the step execution
            
        Returns:
            Updated workflow with checkpoint saved
        """
        # Execute the step
        workflow = self.execute_step(workflow, step_id, step_result)
        
        # Save checkpoint
        self.save_checkpoint(workflow)
        
        return workflow


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    """CLI interface for the orchestrator."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="PaperKit Orchestrator - Intelligent task routing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python orchestrator.py route "Draft my introduction section"
  python orchestrator.py route "Research color theory and then draft a section"
  python orchestrator.py workflow "Research X, then outline, then draft"
  python orchestrator.py benchmark
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Route command
    route_parser = subparsers.add_parser('route', help='Route a user request')
    route_parser.add_argument('request', help='User request to route')
    route_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Workflow command
    workflow_parser = subparsers.add_parser('workflow', help='Generate multi-step workflow')
    workflow_parser.add_argument('request', help='User request for workflow')
    workflow_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Present command (FR-023)
    present_parser = subparsers.add_parser('present', help='Present workflow for user approval')
    present_parser.add_argument('request', help='User request for workflow')
    present_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Benchmark command
    bench_parser = subparsers.add_parser('benchmark', help='Benchmark routing performance')
    bench_parser.add_argument('--iterations', type=int, default=100, help='Number of iterations')
    
    # Simulate command (FR-026 demonstration)
    simulate_parser = subparsers.add_parser('simulate', help='Simulate workflow execution with step outputs')
    simulate_parser.add_argument('request', help='User request for workflow')
    simulate_parser.add_argument('--json', action='store_true', help='Output as JSON')
    simulate_parser.add_argument('--checkpoint', action='store_true', help='Save checkpoints during simulation')
    
    # Checkpoint commands (FR-024, FR-025)
    checkpoint_parser = subparsers.add_parser('checkpoints', help='List saved checkpoints')
    checkpoint_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    resume_parser = subparsers.add_parser('resume', help='Resume workflow from checkpoint')
    resume_parser.add_argument('workflow_id', help='Workflow ID to resume')
    resume_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    orch = Orchestrator()
    
    if args.command == 'route':
        decision = orch.route(args.request)
        
        if args.json:
            print(json.dumps({
                'decision': decision.decision,
                'agent': decision.agent,
                'confidence': decision.confidence,
                'reason': decision.reason,
                'missing_inputs': decision.missing_inputs,
                'suggested_next_prompt': decision.suggested_next_prompt,
                'alternatives': [
                    {'agent': a.agent_name, 'confidence': a.confidence}
                    for a in decision.alternatives
                ]
            }, indent=2))
        else:
            print(f"Decision: {decision.decision}")
            print(f"Agent: {decision.agent}")
            print(f"Confidence: {decision.confidence:.2f}")
            print(f"Reason: {decision.reason}")
            if decision.missing_inputs:
                print(f"Missing Inputs: {', '.join(decision.missing_inputs)}")
            if decision.alternatives:
                print("Alternatives:")
                for alt in decision.alternatives:
                    print(f"  - {alt.agent_name}: {alt.confidence:.2f}")
    
    elif args.command == 'workflow':
        workflow = orch.generate_workflow(args.request)
        
        if args.json:
            print(json.dumps({
                'workflow_id': workflow.workflow_id,
                'user_request': workflow.user_request,
                'steps': [
                    {
                        'step_id': s.step_id,
                        'agent': s.agent,
                        'action': s.action,
                        'inputs': s.inputs,
                        'outputs': s.outputs,
                        'depends_on': s.depends_on,
                    }
                    for s in workflow.steps
                ]
            }, indent=2))
        else:
            print(f"Workflow ID: {workflow.workflow_id}")
            print(f"Request: {workflow.user_request}")
            print(f"Steps ({len(workflow.steps)}):")
            for step in workflow.steps:
                deps = f" (depends on: {', '.join(step.depends_on)})" if step.depends_on else ""
                print(f"  {step.step_id}: {step.agent} -> {step.action}{deps}")
    
    elif args.command == 'present':
        # Present workflow for user approval (FR-023)
        workflow = orch.generate_workflow(args.request)
        presentation = orch.present_workflow(workflow)
        
        if args.json:
            print(json.dumps({
                'workflow_id': presentation.workflow_id,
                'summary': presentation.summary,
                'steps_preview': presentation.steps_preview,
                'estimated_agents': presentation.estimated_agents,
                'requires_approval': presentation.requires_approval,
                'approval_prompt': presentation.approval_prompt,
            }, indent=2))
        else:
            print("=" * 60)
            print("WORKFLOW PREVIEW (FR-023)")
            print("=" * 60)
            print(f"\nWorkflow ID: {presentation.workflow_id}")
            print(f"Summary: {presentation.summary}")
            print(f"\nSteps:")
            for i, step in enumerate(presentation.steps_preview, 1):
                print(f"  {i}. {step['description']}")
                if step['inputs'] != 'none':
                    print(f"     Inputs: {step['inputs']}")
                if step['dependencies']:
                    print(f"     Dependencies: {step['dependencies']}")
            print(f"\nAgents involved: {', '.join(presentation.estimated_agents)}")
            print(f"\n{presentation.approval_prompt}")
    
    elif args.command == 'benchmark':
        # Benchmark routing performance (FR-020: <100ms for single-intent)
        test_requests = [
            "Draft my introduction section",
            "Fix my bibliography",
            "Research color perception",
            "Explain the methodology",
            "Polish this paragraph",
            "Create an outline",
            "Cite this source",
            "Debug my latex compilation",
            "Brainstorm research angles",
            "Verify this citation",
        ]
        
        times = []
        for _ in range(args.iterations):
            for request in test_requests:
                start = time.perf_counter()
                orch.route(request)
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        
        print("Routing Performance Benchmark")
        print("=" * 50)
        print(f"Iterations: {args.iterations}")
        print(f"Requests per iteration: {len(test_requests)}")
        print(f"Total routings: {len(times)}")
        print(f"\nTiming:")
        print(f"  Average: {avg_time:.2f}ms")
        print(f"  Min: {min_time:.2f}ms")
        print(f"  Max: {max_time:.2f}ms")
        print(f"\nFR-020 Target (<100ms): {'✓ PASS' if avg_time < 100 else '✗ FAIL'}")
    
    elif args.command == 'simulate':
        # Simulate workflow execution with step output passing (FR-026)
        workflow = orch.generate_workflow(args.request)
        workflow = orch.approve_workflow(workflow)
        simulation_log = []  # Initialize log
        
        if not args.json:
            print("=" * 60)
            print("WORKFLOW SIMULATION (FR-026: Step Output Passing)")
            print("=" * 60)
            print(f"\nWorkflow ID: {workflow.workflow_id}")
            print(f"Approved: {workflow.approved}")
        
        # Execute each step in order
        while True:
            next_step = orch.get_next_step(workflow)
            if not next_step:
                break
            
            # Get inputs for this step (including dependency outputs)
            step_inputs = orch.get_step_inputs(workflow, next_step.step_id)
            
            # Simulate step execution with mock output
            mock_output = {
                "agent": next_step.agent,
                "action": next_step.action,
                "result": f"Completed {next_step.action} with {next_step.agent}",
                "artifacts": [f"{next_step.step_id}_artifact.md"],
            }
            
            # Record the step completion (with optional checkpoint)
            if hasattr(args, 'checkpoint') and args.checkpoint:
                workflow = orch.execute_step_with_checkpoint(workflow, next_step.step_id, mock_output)
            else:
                workflow = orch.execute_step(workflow, next_step.step_id, mock_output)
            
            if args.json:
                simulation_log.append({
                    "step_id": next_step.step_id,
                    "agent": next_step.agent,
                    "action": next_step.action,
                    "inputs_from_deps": step_inputs["dependency_outputs"],
                    "output": mock_output,
                })
            else:
                print(f"\n--- Step: {next_step.step_id} ---")
                print(f"Agent: {next_step.agent}")
                print(f"Action: {next_step.action}")
                if step_inputs["dependency_outputs"]:
                    print(f"Inputs from dependencies: {json.dumps(step_inputs['dependency_outputs'], indent=2)}")
                print(f"Output: {json.dumps(mock_output, indent=2)}")
        
        # Get final status
        status = orch.get_workflow_status(workflow)
        
        if args.json:
            print(json.dumps({
                "workflow_id": workflow.workflow_id,
                "simulation_steps": simulation_log,
                "final_status": status,
                "step_outputs": workflow.step_outputs,
            }, indent=2))
        else:
            print(f"\n{'=' * 60}")
            print("FINAL STATUS")
            print(f"{'=' * 60}")
            print(f"Status: {status['status']}")
            print(f"Progress: {status['progress']}")
            print(f"\nStep Outputs (available to dependent steps):")
            for step_id, output in workflow.step_outputs.items():
                print(f"  {step_id}: {json.dumps(output, indent=4)}")
            
            if hasattr(args, 'checkpoint') and args.checkpoint:
                print(f"\n✓ Checkpoint saved: {workflow.workflow_id}")
    
    elif args.command == 'checkpoints':
        # List saved checkpoints (FR-024, FR-025)
        checkpoints = orch.list_checkpoints()
        
        if args.json:
            print(json.dumps(checkpoints, indent=2))
        else:
            print("=" * 60)
            print("SAVED CHECKPOINTS (FR-024, FR-025)")
            print("=" * 60)
            
            if not checkpoints:
                print("\nNo checkpoints found.")
            else:
                print(f"\nFound {len(checkpoints)} checkpoint(s):\n")
                for cp in checkpoints:
                    status_icon = "✓" if cp["status"] == "completed" else "⏳"
                    print(f"  {status_icon} {cp['workflow_id']}")
                    print(f"    Request: {cp['user_request'][:50]}...")
                    print(f"    Progress: {cp['progress']}")
                    print(f"    Updated: {cp['updated_at']}")
                    print()
    
    elif args.command == 'resume':
        # Resume workflow from checkpoint (FR-025)
        workflow = orch.load_checkpoint(args.workflow_id)
        
        if not workflow:
            print(f"Error: No checkpoint found for workflow '{args.workflow_id}'")
            sys.exit(1)
        
        if args.json:
            status = orch.get_workflow_status(workflow)
            print(json.dumps({
                "workflow_id": workflow.workflow_id,
                "user_request": workflow.user_request,
                "status": status,
                "next_step": None if status["status"] == "completed" else orch.get_next_step(workflow).__dict__ if orch.get_next_step(workflow) else None,
            }, indent=2))
        else:
            print("=" * 60)
            print("WORKFLOW RESUMED FROM CHECKPOINT (FR-025)")
            print("=" * 60)
            print(f"\nWorkflow ID: {workflow.workflow_id}")
            print(f"Request: {workflow.user_request}")
            print(f"Approved: {workflow.approved}")
            
            status = orch.get_workflow_status(workflow)
            print(f"\nStatus: {status['status']}")
            print(f"Progress: {status['progress']}")
            
            print("\nSteps:")
            for step in workflow.steps:
                status_icon = {"completed": "✓", "in_progress": "⏳", "pending": "○", "failed": "✗"}.get(step.status, "?")
                deps = f" (depends on: {', '.join(step.depends_on)})" if step.depends_on else ""
                print(f"  {status_icon} {step.step_id}: {step.agent} -> {step.action}{deps}")
            
            next_step = orch.get_next_step(workflow)
            if next_step:
                print(f"\nNext step ready: {next_step.step_id} ({next_step.agent})")
            else:
                print("\nWorkflow complete or blocked.")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
