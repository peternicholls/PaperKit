# Tool Registry API Contract

**Feature**: 001-agent-system-upgrade
**Version**: 1.0.0
**Date**: 2026-01-20

## Overview

API for tool discovery, consent management, and invocation. Enables agents to programmatically discover and invoke tools with appropriate user consent.

---

## Data Types

### ToolDefinition
```python
@dataclass
class ToolDefinition:
    name: str
    display_name: str
    description: str
    version: str
    command: str
    input_schema: dict  # JSON Schema
    output_schema: dict  # JSON Schema
    requires_consent: bool
    consent_level: ConsentLevel
    timeout_ms: int
    category: Optional[str] = None
```

### ConsentLevel (Enum)
```python
class ConsentLevel(Enum):
    NONE = "none"        # No consent required
    SESSION = "session"  # Consent valid for current session
    PERSISTENT = "persistent"  # Consent persists across sessions
```

### ConsentRecord
```python
@dataclass
class ConsentRecord:
    tool_name: str
    scope: ConsentLevel
    granted_at: datetime
    expires_at: Optional[datetime] = None
```

### ToolResult
```python
@dataclass
class ToolResult:
    success: bool
    output: Optional[dict] = None
    error: Optional[str] = None
    error_type: Optional[str] = None
    duration_ms: int = 0
    stdout: Optional[str] = None
    stderr: Optional[str] = None
```

### InvocationContext
```python
@dataclass
class InvocationContext:
    agent_name: str
    skill_name: Optional[str] = None
    workflow_id: Optional[str] = None
    request_id: Optional[str] = None
```

---

## API Methods

### `discover_tools(category: Optional[str] = None) -> List[ToolDefinition]`

List all available tools, optionally filtered by category.

**Parameters**:
- `category`: Optional category filter (e.g., "build", "validation", "references")

**Returns**: List of ToolDefinition

**Example**:
```python
from paperkit.tools import ToolRegistry

registry = ToolRegistry()
build_tools = registry.discover_tools(category="build")
for tool in build_tools:
    print(f"{tool.name}: {tool.description}")
```

---

### `get_tool(name: str) -> Optional[ToolDefinition]`

Get a specific tool definition by name.

**Parameters**:
- `name`: Tool name

**Returns**: ToolDefinition or None if not found

**Example**:
```python
tool = registry.get_tool("build-latex")
if tool:
    print(f"Inputs: {tool.input_schema}")
    print(f"Requires consent: {tool.requires_consent}")
```

---

### `check_consent(tool_name: str) -> ConsentStatus`

Check if user has granted consent for a tool.

**ConsentStatus**:
```python
@dataclass
class ConsentStatus:
    has_consent: bool
    consent_type: Optional[ConsentLevel] = None
    expires_at: Optional[datetime] = None
    needs_prompt: bool = True
```

**Example**:
```python
status = registry.check_consent("build-latex")
if status.has_consent:
    # Proceed with invocation
    pass
elif status.needs_prompt:
    # Prompt user for consent
    pass
```

---

### `request_consent(tool_name: str, scope: ConsentLevel = ConsentLevel.SESSION) -> ConsentResult`

Request user consent for a tool.

**ConsentResult**:
```python
@dataclass
class ConsentResult:
    granted: bool
    scope: ConsentLevel
    reason: Optional[str] = None  # If denied, why
```

**Behavior**:
1. Display consent prompt to user with tool description
2. Wait for user response (approve/deny)
3. If approved, store consent record
4. Return result

**Consent Prompt Format**:
```
┌─────────────────────────────────────────────────────────────┐
│ Tool Consent Required                                        │
├─────────────────────────────────────────────────────────────┤
│ Tool: build-latex                                            │
│ Description: Compile LaTeX document to PDF                   │
│ Command: pdflatex -interaction=nonstopmode main.tex          │
│                                                              │
│ This tool will execute a shell command.                      │
│                                                              │
│ [A]pprove for this session                                   │
│ [P]ersistent approval (remember choice)                      │
│ [D]eny                                                       │
└─────────────────────────────────────────────────────────────┘
```

**Example**:
```python
result = registry.request_consent("build-latex", ConsentLevel.SESSION)
if result.granted:
    print(f"Consent granted ({result.scope.value})")
else:
    print(f"Consent denied: {result.reason}")
```

---

### `invoke_tool(name: str, inputs: dict, context: InvocationContext) -> ToolResult`

Invoke a tool with given inputs.

**Parameters**:
- `name`: Tool name
- `inputs`: Input parameters (validated against input_schema)
- `context`: Invocation context for audit logging

**Returns**: ToolResult

**Behavior**:
1. Validate inputs against tool's input_schema
2. Check consent (request if needed)
3. If consent denied, return error result
4. Execute tool command with timeout
5. Validate output against output_schema
6. Log invocation to audit trail and metrics
7. Return result

**Error Handling**:
- `ToolNotFoundError`: Tool doesn't exist
- `InputValidationError`: Inputs don't match schema
- `ConsentDeniedError`: User denied consent
- `TimeoutError`: Tool execution exceeded timeout
- `OutputValidationError`: Output doesn't match schema
- `ExecutionError`: Command failed

**Example**:
```python
result = registry.invoke_tool(
    name="build-latex",
    inputs={"input_file": "main.tex", "output_dir": "build/"},
    context=InvocationContext(
        agent_name="latex-assembler",
        skill_name="compile-latex"
    )
)

if result.success:
    pdf_path = result.output["pdf_path"]
    print(f"Built: {pdf_path}")
else:
    print(f"Error: {result.error}")
    if result.stderr:
        print(f"Details: {result.stderr}")
```

---

### `revoke_consent(tool_name: str) -> bool`

Revoke persistent consent for a tool.

**Parameters**:
- `tool_name`: Tool to revoke consent for

**Returns**: True if consent was revoked, False if no consent existed

**Example**:
```python
if registry.revoke_consent("build-latex"):
    print("Consent revoked")
```

---

### `list_consents() -> List[ConsentRecord]`

List all current consent records (session and persistent).

**Returns**: List of ConsentRecord

---

### `get_audit_log(tool_name: Optional[str] = None, limit: int = 100) -> List[AuditEntry]`

Get tool invocation audit log.

**AuditEntry**:
```python
@dataclass
class AuditEntry:
    timestamp: datetime
    tool_name: str
    agent_name: str
    skill_name: Optional[str]
    inputs_hash: str  # SHA256 of inputs (not full inputs for privacy)
    success: bool
    duration_ms: int
    error_type: Optional[str] = None
```

**Example**:
```python
audit = registry.get_audit_log(tool_name="build-latex", limit=10)
for entry in audit:
    status = "✓" if entry.success else "✗"
    print(f"{entry.timestamp} {status} {entry.agent_name} ({entry.duration_ms}ms)")
```

---

## Storage

### Consent Registry
**Location**: `.paperkit/_cfg/consent.registry.yaml`

```yaml
# Persistent consent records
schemaVersion: 1.0.0
consents:
  - tool: build-latex
    scope: persistent
    grantedAt: 2026-01-20T10:30:00Z
  - tool: lint-latex
    scope: persistent
    grantedAt: 2026-01-20T10:30:05Z
```

### Session Consent
**Storage**: In-memory (cleared on process exit)

### Audit Log
**Storage**: `.paperkit/data/metrics.db` (via Metrics API)

---

## Fallback Strategies

When tool execution fails, the registry supports configurable fallback:

```python
@dataclass
class FallbackConfig:
    strategy: str  # "retry", "alternate", "skip", "fail"
    retry_count: int = 3
    retry_delay_ms: int = 1000
    alternate_tool: Optional[str] = None
```

### Fallback Strategies

| Strategy | Behavior |
|----------|----------|
| `retry` | Retry up to N times with backoff |
| `alternate` | Try alternate tool if available |
| `skip` | Return partial success, continue workflow |
| `fail` | Fail immediately (default) |

---

## Thread Safety

- Tool discovery: Thread-safe (read-only)
- Consent check: Thread-safe (read-only)
- Consent request: NOT thread-safe (interactive prompt)
- Tool invocation: Thread-safe (concurrent invocations allowed)
- Audit logging: Thread-safe (via Metrics API)

---

## Performance Characteristics

| Operation | Expected Latency |
|-----------|------------------|
| `discover_tools` | <10ms |
| `get_tool` | <5ms |
| `check_consent` | <5ms |
| `request_consent` | User-dependent (interactive) |
| `invoke_tool` | Tool-dependent + overhead (<50ms) |
| `revoke_consent` | <20ms |
| `get_audit_log` | <50ms |
