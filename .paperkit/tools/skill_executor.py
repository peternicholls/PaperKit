#!/usr/bin/env python3
"""
PaperKit Skill Executor

Executes skills by orchestrating agent steps and managing state.
Handles prerequisites, conditional execution, and error recovery.

Usage:
    from skill_executor import SkillExecutor

    executor = SkillExecutor()
    result = executor.execute("cite-source", {"source_url": "https://doi.org/..."})
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

try:
    from skill_registry import SkillRegistry, Skill, SkillStep
except ImportError:
    # Allow running from different directories
    sys.path.insert(0, str(Path(__file__).parent))
    from skill_registry import SkillRegistry, Skill, SkillStep


class ExecutionStatus(Enum):
    """Status of a skill execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StepResult:
    """Result of a single step execution."""
    step_index: int
    action: str
    status: ExecutionStatus
    outputs: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration_ms: int = 0
    skipped_reason: Optional[str] = None


@dataclass
class ExecutionResult:
    """Result of a complete skill execution."""
    skill_name: str
    status: ExecutionStatus
    outputs: Dict[str, Any] = field(default_factory=dict)
    step_results: List[StepResult] = field(default_factory=list)
    total_duration_ms: int = 0
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class SkillDepthExceeded(Exception):
    """Raised when skill composition depth exceeds maximum."""
    pass


class SkillNotFound(Exception):
    """Raised when a skill is not found in registry."""
    pass


class PrerequisiteError(Exception):
    """Raised when a prerequisite fails."""
    pass


class SkillExecutor:
    """
    Executes skills by orchestrating agent steps.

    Features:
    - Prerequisite resolution and execution
    - Conditional step evaluation
    - Error handling with retry support
    - State management between steps
    - Depth limiting to prevent infinite recursion
    """

    MAX_DEPTH = 5

    def __init__(
        self,
        registry: Optional[SkillRegistry] = None,
        agent_executor: Optional[Callable] = None,
        tool_executor: Optional[Callable] = None
    ):
        """
        Initialize the skill executor.

        Args:
            registry: SkillRegistry instance. Created if not provided.
            agent_executor: Callback to execute agent steps.
                           Signature: (agent_name, action, inputs) -> outputs
            tool_executor: Callback to execute tools.
                          Signature: (tool_name, inputs) -> outputs
        """
        self.registry = registry or SkillRegistry()
        self.agent_executor = agent_executor or self._default_agent_executor
        self.tool_executor = tool_executor or self._default_tool_executor
        self._execution_stack: List[str] = []

    def _default_agent_executor(self, agent_name: str, action: str, inputs: Dict) -> Dict:
        """
        Default agent executor (placeholder).

        In production, this would invoke the actual agent via the LLM.
        """
        print(f"[Agent] {agent_name}.{action}({list(inputs.keys())})")
        # Return empty outputs - actual implementation would call the agent
        return {}

    def _default_tool_executor(self, tool_name: str, inputs: Dict) -> Dict:
        """
        Default tool executor (placeholder).

        In production, this would invoke the actual tool.
        """
        print(f"[Tool] {tool_name}({list(inputs.keys())})")
        # Return empty outputs - actual implementation would call the tool
        return {}

    def execute(
        self,
        skill_name: str,
        inputs: Dict[str, Any],
        context: Optional[Dict] = None,
        _depth: int = 0
    ) -> ExecutionResult:
        """
        Execute a skill with the given inputs.

        Args:
            skill_name: Name of the skill to execute
            inputs: Input parameters matching skill's inputSchema
            context: Additional context to pass to agents
            _depth: Internal depth counter (do not set manually)

        Returns:
            ExecutionResult with outputs and status

        Raises:
            SkillDepthExceeded: If max composition depth exceeded
            SkillNotFound: If skill not found in registry
            PrerequisiteError: If a prerequisite fails
        """
        # Check depth limit
        if _depth > self.MAX_DEPTH:
            raise SkillDepthExceeded(
                f"Skill '{skill_name}' exceeded maximum depth of {self.MAX_DEPTH}. "
                f"Execution stack: {' -> '.join(self._execution_stack)}"
            )

        # Get skill from registry
        skill = self.registry.get_skill(skill_name)
        if not skill:
            raise SkillNotFound(f"Skill not found: {skill_name}")

        # Track execution stack
        self._execution_stack.append(skill_name)

        result = ExecutionResult(
            skill_name=skill_name,
            status=ExecutionStatus.PENDING,
            started_at=datetime.now()
        )

        try:
            # Execute prerequisites first
            prereq_outputs = self._execute_prerequisites(skill, inputs, context, _depth)

            # Merge prerequisite outputs into inputs
            merged_inputs = {**inputs, **prereq_outputs}

            # Execute skill steps
            result.status = ExecutionStatus.RUNNING
            state = merged_inputs.copy()

            for i, step in enumerate(skill.steps):
                step_result = self._execute_step(i, step, state, context, skill)
                result.step_results.append(step_result)

                if step_result.status == ExecutionStatus.FAILED:
                    if step.on_error == 'fail':
                        result.status = ExecutionStatus.FAILED
                        result.error = step_result.error
                        break
                    elif step.on_error == 'skip':
                        continue
                    elif step.on_error == 'retry':
                        # Retry logic with backoff
                        retry_result = self._retry_step(i, step, state, context, skill)
                        result.step_results[-1] = retry_result
                        if retry_result.status == ExecutionStatus.FAILED:
                            result.status = ExecutionStatus.FAILED
                            result.error = retry_result.error
                            break
                        state.update(retry_result.outputs)
                elif step_result.status == ExecutionStatus.SKIPPED:
                    continue
                else:
                    # Update state with outputs
                    state.update(step_result.outputs)

            # If we completed all steps successfully
            if result.status == ExecutionStatus.RUNNING:
                result.status = ExecutionStatus.COMPLETED

                # Extract outputs according to outputSchema
                result.outputs = self._extract_outputs(skill, state)

        except Exception as e:
            result.status = ExecutionStatus.FAILED
            result.error = str(e)

        finally:
            self._execution_stack.pop()
            result.completed_at = datetime.now()
            if result.started_at and result.completed_at:
                result.total_duration_ms = int(
                    (result.completed_at - result.started_at).total_seconds() * 1000
                )

        return result

    def _execute_prerequisites(
        self,
        skill: Skill,
        inputs: Dict,
        context: Optional[Dict],
        depth: int
    ) -> Dict:
        """Execute all prerequisites and collect their outputs."""
        outputs = {}

        for prereq in skill.prerequisites:
            prereq_type = prereq.get('type')
            prereq_name = prereq.get('name')

            if prereq_type in ('skill', 'workflow') and prereq_name:
                # Recursively execute prerequisite skill
                prereq_result = self.execute(
                    prereq_name, inputs, context, depth + 1
                )

                if prereq_result.status != ExecutionStatus.COMPLETED:
                    raise PrerequisiteError(
                        f"Prerequisite skill '{prereq_name}' failed: {prereq_result.error}"
                    )

                outputs.update(prereq_result.outputs)

            elif prereq_type == 'tool':
                # Just check tool exists - don't execute
                # Tools are executed as part of steps
                pass

        return outputs

    def _execute_step(
        self,
        index: int,
        step: SkillStep,
        state: Dict,
        context: Optional[Dict],
        skill: Skill
    ) -> StepResult:
        """Execute a single step."""
        start_time = time.time()

        # Check condition
        if step.condition:
            if not self._evaluate_condition(step.condition, state):
                return StepResult(
                    step_index=index,
                    action=step.action,
                    status=ExecutionStatus.SKIPPED,
                    skipped_reason=f"Condition not met: {step.condition}"
                )

        # Gather inputs for this step
        step_inputs = {
            key: state.get(key)
            for key in step.inputs
            if key in state
        }

        # Add context if available
        if context:
            step_inputs['_context'] = context

        try:
            # Execute via tool or agent
            if step.tool:
                outputs = self.tool_executor(step.tool, step_inputs)
            else:
                outputs = self.agent_executor(step.agent, step.action, step_inputs)

            # Map outputs to output variable names
            mapped_outputs = {}
            if isinstance(outputs, dict):
                for output_name in step.outputs:
                    if output_name in outputs:
                        mapped_outputs[output_name] = outputs[output_name]

            duration = int((time.time() - start_time) * 1000)

            return StepResult(
                step_index=index,
                action=step.action,
                status=ExecutionStatus.COMPLETED,
                outputs=mapped_outputs,
                duration_ms=duration
            )

        except Exception as e:
            duration = int((time.time() - start_time) * 1000)

            return StepResult(
                step_index=index,
                action=step.action,
                status=ExecutionStatus.FAILED,
                error=str(e),
                duration_ms=duration
            )

    def _retry_step(
        self,
        index: int,
        step: SkillStep,
        state: Dict,
        context: Optional[Dict],
        skill: Skill
    ) -> StepResult:
        """Retry a failed step with backoff."""
        retry_policy = skill.retry_policy
        max_retries = retry_policy.get('maxRetries', 0)
        backoff_ms = retry_policy.get('backoffMs', 1000)

        for attempt in range(max_retries):
            # Wait with backoff
            time.sleep(backoff_ms / 1000 * (attempt + 1))

            result = self._execute_step(index, step, state, context, skill)

            if result.status == ExecutionStatus.COMPLETED:
                return result

        # All retries failed
        return StepResult(
            step_index=index,
            action=step.action,
            status=ExecutionStatus.FAILED,
            error=f"Step failed after {max_retries} retries"
        )

    def _evaluate_condition(self, condition: str, state: Dict) -> bool:
        """
        Evaluate a condition expression.

        Supports simple expressions like:
        - "citation_type == 'doi'"
        - "'isbn' in parsed_fields"
        """
        try:
            # Create a safe evaluation context with state variables
            eval_context = state.copy()
            return eval(condition, {"__builtins__": {}}, eval_context)
        except Exception:
            # If evaluation fails, condition is false
            return False

    def _extract_outputs(self, skill: Skill, state: Dict) -> Dict:
        """Extract outputs according to skill's outputSchema."""
        output_properties = skill.output_schema.get('properties', {})
        required_outputs = skill.output_schema.get('required', [])

        outputs = {}
        for name in output_properties:
            if name in state:
                outputs[name] = state[name]
            elif name in required_outputs:
                outputs[name] = None  # Required but missing

        return outputs

    def validate_inputs(self, skill_name: str, inputs: Dict) -> List[str]:
        """
        Validate inputs against skill's inputSchema.

        Args:
            skill_name: Name of the skill
            inputs: Input parameters to validate

        Returns:
            List of validation errors (empty if valid)
        """
        skill = self.registry.get_skill(skill_name)
        if not skill:
            return [f"Skill not found: {skill_name}"]

        errors = []

        required = skill.input_schema.get('required', [])
        properties = skill.input_schema.get('properties', {})

        # Check required inputs
        for req in required:
            if req not in inputs:
                errors.append(f"Missing required input: {req}")

        # Check types (basic validation)
        for name, value in inputs.items():
            if name in properties:
                expected_type = properties[name].get('type')
                if expected_type and not self._check_type(value, expected_type):
                    errors.append(f"Invalid type for {name}: expected {expected_type}")

        return errors

    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check if value matches expected JSON Schema type."""
        type_map = {
            'string': str,
            'integer': int,
            'number': (int, float),
            'boolean': bool,
            'array': list,
            'object': dict
        }

        if expected_type not in type_map:
            return True

        return isinstance(value, type_map[expected_type])

    def dry_run(self, skill_name: str, inputs: Dict) -> Dict:
        """
        Perform a dry run of skill execution.

        Shows what would be executed without actually running.

        Args:
            skill_name: Name of the skill
            inputs: Input parameters

        Returns:
            Dictionary describing the execution plan
        """
        skill = self.registry.get_skill(skill_name)
        if not skill:
            return {'error': f"Skill not found: {skill_name}"}

        plan = {
            'skill': skill_name,
            'type': skill.type,
            'prerequisites': [],
            'steps': [],
            'validation_errors': self.validate_inputs(skill_name, inputs)
        }

        # List prerequisites
        for prereq in skill.prerequisites:
            plan['prerequisites'].append({
                'type': prereq.get('type'),
                'name': prereq.get('name')
            })

        # List steps
        for i, step in enumerate(skill.steps):
            plan['steps'].append({
                'index': i,
                'action': step.action,
                'agent': step.agent,
                'tool': step.tool,
                'inputs': step.inputs,
                'outputs': step.outputs,
                'condition': step.condition,
                'on_error': step.on_error
            })

        return plan


def main():
    """CLI interface for skill executor."""
    import argparse

    parser = argparse.ArgumentParser(description="PaperKit Skill Executor")
    parser.add_argument('command', choices=['execute', 'dry-run', 'validate'],
                        help='Command to execute')
    parser.add_argument('skill', help='Skill name')
    parser.add_argument('--inputs', '-i', help='JSON inputs', default='{}')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    executor = SkillExecutor()

    try:
        inputs = json.loads(args.inputs)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON inputs: {args.inputs}", file=sys.stderr)
        sys.exit(1)

    if args.command == 'execute':
        result = executor.execute(args.skill, inputs)

        if args.json:
            print(json.dumps({
                'skill': result.skill_name,
                'status': result.status.value,
                'outputs': result.outputs,
                'error': result.error,
                'duration_ms': result.total_duration_ms
            }, indent=2))
        else:
            print(f"Skill: {result.skill_name}")
            print(f"Status: {result.status.value}")
            print(f"Duration: {result.total_duration_ms}ms")
            if result.error:
                print(f"Error: {result.error}")
            if result.outputs:
                print(f"Outputs: {json.dumps(result.outputs, indent=2)}")

    elif args.command == 'dry-run':
        plan = executor.dry_run(args.skill, inputs)

        if args.json:
            print(json.dumps(plan, indent=2))
        else:
            print(f"Skill: {plan.get('skill')} ({plan.get('type')})")

            if plan.get('validation_errors'):
                print("Validation Errors:")
                for err in plan['validation_errors']:
                    print(f"  - {err}")

            if plan.get('prerequisites'):
                print("Prerequisites:")
                for p in plan['prerequisites']:
                    print(f"  - {p['type']}: {p['name']}")

            print("Steps:")
            for step in plan.get('steps', []):
                cond = f" [if: {step['condition']}]" if step.get('condition') else ""
                tool = f" (tool: {step['tool']})" if step.get('tool') else ""
                print(f"  {step['index']+1}. {step['agent']}.{step['action']}{tool}{cond}")

    elif args.command == 'validate':
        errors = executor.validate_inputs(args.skill, inputs)

        if args.json:
            print(json.dumps({'valid': len(errors) == 0, 'errors': errors}, indent=2))
        else:
            if errors:
                print("Validation failed:")
                for err in errors:
                    print(f"  - {err}")
            else:
                print("Validation passed")


if __name__ == "__main__":
    main()
