# Data Model: Agent System Upgrade

**Feature**: 001-agent-system-upgrade  
**Date**: 2026-01-20  
**Status**: Complete

## Entity Relationship Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AGENT SYSTEM DATA MODEL                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐    invokes    ┌──────────┐    requires    ┌──────────┐       │
│  │  Agent   │──────────────▶│  Skill   │───────────────▶│  Tool    │       │
│  └──────────┘               └──────────┘                └──────────┘       │
│       │                          │                           │              │
│       │ routes via               │ composed of               │ requires     │
│       ▼                          ▼                           ▼              │
│  ┌──────────┐               ┌──────────┐               ┌──────────┐        │
│  │ Routing  │               │  Skill   │               │ Consent  │        │
│  │ Registry │               │  Step    │               │ Record   │        │
│  └──────────┘               └──────────┘               └──────────┘        │
│       │                                                      │              │
│       │ classifies                                           │ logged to    │
│       ▼                                                      ▼              │
│  ┌──────────┐    generates    ┌──────────┐    tracked    ┌──────────┐      │
│  │  Intent  │────────────────▶│ Workflow │──────────────▶│  Metric  │      │
│  └──────────┘                 └──────────┘               └──────────┘      │
│                                    │                                        │
│                                    │ saves state to                         │
│                                    ▼                                        │
│                               ┌──────────┐                                  │
│                               │Checkpoint│                                  │
│                               └──────────┘                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Agent

**Definition**: A specialized AI persona with specific capabilities, constraints, and behavioral instructions.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Machine identifier (kebab-case) |
| `displayName` | string | ✅ | Human persona name |
| `title` | string | ✅ | Functional title |
| `icon` | string | ✅ | Emoji representation |
| `version` | semver | ❌ | Semantic version (default: 1.0.0) |
| `module` | enum | ✅ | `core` or `specialist` |
| `identity` | object | ✅ | Role, description, communication style |
| `capabilities` | string[] | ❌ | What the agent can do |
| `constraints` | string[] | ❌ | What the agent cannot do |
| `principles` | string[] | ❌ | Guiding behavioral principles |
| `inputSchema` | JSONSchema | ❌ | Expected input format |
| `outputSchema` | JSONSchema | ❌ | Expected output format |
| `path` | string | ✅ | Path to MD instruction file |

**Relationships**:
- **Routes via** Routing Registry (1:1)
- **Invokes** Skills (1:N)
- **Tracked by** Metrics (1:N)

**Validation**: `agent-schema.json`

**Storage**: `.paperkit/_cfg/agents/{name}.yaml`

---

## 2. Skill

**Definition**: Reusable capability composed of one or more actions that agents can invoke.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Machine identifier (kebab-case) |
| `displayName` | string | ✅ | Human-readable name |
| `description` | string | ✅ | What the skill does |
| `version` | semver | ✅ | Semantic version |
| `type` | enum | ✅ | `atomic`, `composite`, `conditional` |
| `prerequisites` | array | ❌ | Required skills/tools before execution |
| `steps` | SkillStep[] | ✅ | Ordered execution steps |
| `inputSchema` | JSONSchema | ✅ | Required inputs |
| `outputSchema` | JSONSchema | ✅ | Guaranteed outputs |
| `timeout` | integer | ❌ | Max execution time (ms) |
| `retryPolicy` | object | ❌ | Retry behavior on failure |

**Skill Types**:
- **Atomic**: Single agent, single action (e.g., `extract-metadata`)
- **Composite**: Multi-step sequence (e.g., `cite-source` = extract → format)
- **Conditional**: Branching logic based on inputs (e.g., `validate-citation` with type-specific paths)

**Relationships**:
- **Invoked by** Agents (N:1)
- **Composed of** Skill Steps (1:N)
- **Requires** Tools (N:M)
- **Depends on** other Skills (N:M)

**Validation**: `skill-schema.json`

**Storage**: `.paperkit/_cfg/skills/{name}.yaml`

---

## 3. Skill Step

**Definition**: Single action within a skill execution.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | string | ✅ | Step identifier |
| `agent` | string | ✅ | Agent to execute this step |
| `inputs` | string[] | ✅ | Input variable names |
| `outputs` | string[] | ✅ | Output variable names |
| `condition` | string | ❌ | Conditional expression (for conditional skills) |
| `onError` | enum | ❌ | `fail`, `skip`, `retry` |

**Relationships**:
- **Belongs to** Skill (N:1)
- **Executed by** Agent (N:1)

**Storage**: Embedded in parent Skill YAML

---

## 4. Tool

**Definition**: External executable that agents invoke to perform concrete actions.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Machine identifier |
| `displayName` | string | ✅ | Human-readable name |
| `description` | string | ✅ | What the tool does |
| `version` | semver | ✅ | Semantic version |
| `command` | string | ✅ | Shell command to execute |
| `inputSchema` | JSONSchema | ✅ | Required inputs |
| `outputSchema` | JSONSchema | ✅ | Expected outputs |
| `requiresConsent` | boolean | ✅ | Whether user approval needed |
| `consentLevel` | enum | ❌ | `none`, `session`, `persistent` |
| `timeout` | integer | ❌ | Max execution time (ms) |
| `category` | string | ❌ | Tool category for grouping |

**Relationships**:
- **Invoked by** Skills (N:M)
- **Requires** Consent Records (1:N)
- **Logged to** Metrics (1:N)

**Validation**: `tool-schema.json` (existing)

**Storage**: `.paperkit/_cfg/tools/*.yaml` (existing)

---

## 5. Routing Registry

**Definition**: Centralized rules mapping user intents to appropriate agents.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schemaVersion` | semver | ✅ | Registry schema version |
| `lastUpdated` | date | ✅ | Last modification date |
| `agents` | AgentRoute[] | ✅ | Per-agent routing rules |
| `abTests` | ABTest[] | ❌ | Active A/B tests |
| `defaultAgent` | string | ❌ | Fallback when no match |
| `confidenceThreshold` | float | ❌ | Minimum score for auto-routing (default: 0.7) |

**Agent Route Entry**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Agent name reference |
| `whenToUse` | string[] | ✅ | Use case descriptions |
| `keywords` | string[] | ✅ | Trigger keywords |
| `requiredInputs` | string[] | ❌ | Mandatory inputs for this agent |
| `hardExclusions` | string[] | ❌ | Requests to never route here |
| `priority` | integer | ❌ | Tie-break priority (higher = preferred) |

**Relationships**:
- **Routes to** Agents (1:N)
- **Classifies** Intents (1:N)

**Storage**: `.paperkit/_cfg/routing.registry.yaml`

---

## 6. Intent

**Definition**: Parsed user goal extracted from natural language request.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | uuid | ✅ | Unique identifier |
| `rawRequest` | string | ✅ | Original user input |
| `parsedIntents` | string[] | ✅ | Identified goals (can be multiple) |
| `matchedKeywords` | string[] | ✅ | Keywords that triggered match |
| `confidenceScores` | map | ✅ | Agent → score mapping |
| `selectedAgent` | string | ❌ | Final routing decision |
| `userOverride` | boolean | ✅ | Whether user changed selection |
| `timestamp` | datetime | ✅ | When intent was created |

**Relationships**:
- **Classified by** Routing Registry (N:1)
- **Generates** Workflow (1:1)
- **Tracked by** Metrics (1:N)

**Storage**: In-memory during session; logged to metrics DB

---

## 7. Workflow

**Definition**: Multi-step orchestration generated dynamically or defined statically.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | uuid | ✅ | Unique identifier |
| `name` | string | ✅ | Workflow name |
| `intent` | Intent | ✅ | Source intent |
| `steps` | WorkflowStep[] | ✅ | Ordered execution steps |
| `status` | enum | ✅ | `pending`, `approved`, `running`, `completed`, `failed` |
| `createdAt` | datetime | ✅ | Creation timestamp |
| `startedAt` | datetime | ❌ | Execution start |
| `completedAt` | datetime | ❌ | Execution end |
| `userApproved` | boolean | ✅ | Whether user approved workflow |

**Workflow Step**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order` | integer | ✅ | Execution order |
| `agent` | string | ✅ | Agent to execute |
| `skill` | string | ❌ | Skill to invoke (optional) |
| `inputs` | map | ✅ | Input parameters |
| `outputs` | map | ❌ | Captured outputs |
| `status` | enum | ✅ | `pending`, `running`, `completed`, `failed`, `skipped` |
| `dependsOn` | integer[] | ❌ | Steps that must complete first |

**Relationships**:
- **Generated from** Intent (1:1)
- **Saves state to** Checkpoints (1:N)
- **Tracked by** Metrics (1:N)

**Storage**: In-memory during execution; checkpoints to `.paperkit/data/checkpoints/`

---

## 8. Checkpoint

**Definition**: Workflow execution state snapshot enabling resumption.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | uuid | ✅ | Unique identifier |
| `workflowId` | uuid | ✅ | Parent workflow |
| `stepIndex` | integer | ✅ | Last completed step |
| `state` | map | ✅ | Accumulated outputs |
| `context` | map | ❌ | Execution context |
| `createdAt` | datetime | ✅ | Checkpoint timestamp |
| `expiresAt` | datetime | ✅ | Auto-cleanup time (24h default) |

**Relationships**:
- **Belongs to** Workflow (N:1)

**Storage**: `.paperkit/data/checkpoints/{workflow_id}.json`

---

## 9. Consent Record

**Definition**: User consent for tool execution.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `toolName` | string | ✅ | Tool identifier |
| `scope` | enum | ✅ | `session`, `persistent` |
| `grantedAt` | datetime | ✅ | When consent was given |
| `expiresAt` | datetime | ❌ | When consent expires (null = never for persistent) |
| `grantedBy` | string | ❌ | User identifier |

**Relationships**:
- **Belongs to** Tool (N:1)

**Storage**: `.paperkit/_cfg/consent.registry.yaml`
- Session consents: In-memory (cleared on exit)
- Persistent consents: Appended to consent.registry.yaml

---

## 10. Metric

**Definition**: Performance measurement collected during system operation.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | integer | ✅ | Auto-increment ID |
| `timestamp` | datetime | ✅ | When metric was recorded |
| `category` | enum | ✅ | `agent`, `skill`, `tool`, `workflow`, `routing` |
| `entityName` | string | ✅ | Name of measured entity |
| `action` | string | ✅ | Action performed |
| `success` | boolean | ✅ | Whether action succeeded |
| `durationMs` | integer | ❌ | Execution time |
| `confidenceScore` | float | ❌ | Routing confidence (for routing metrics) |
| `userModified` | boolean | ❌ | Whether user changed agent/workflow |
| `errorType` | string | ❌ | Error category if failed |
| `metadata` | json | ❌ | Additional context |

**Relationships**:
- **Tracks** Agents, Skills, Tools, Workflows (N:1)

**Storage**: `.paperkit/data/metrics.db` (SQLite, 90-day retention)

---

## 11. A/B Test

**Definition**: Experiment comparing two agent versions.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Test identifier |
| `control` | string | ✅ | Control agent name |
| `treatment` | string | ✅ | Treatment agent name |
| `splitRatio` | float | ✅ | Traffic to treatment (0.0-1.0) |
| `minimumSampleSize` | integer | ✅ | Min invocations per variant |
| `startDate` | date | ✅ | Test start |
| `endDate` | date | ✅ | Test end |
| `status` | enum | ✅ | `active`, `completed`, `cancelled` |
| `metrics` | string[] | ✅ | Metrics to compare |
| `results` | object | ❌ | Statistical analysis results |

**Relationships**:
- **Defined in** Routing Registry (N:1)
- **Tracked by** Metrics (1:N)

**Storage**: `.paperkit/_cfg/routing.registry.yaml` (definition), metrics.db (results)

---

## State Transitions

### Workflow Status

```
┌─────────┐   user approves   ┌──────────┐   execution    ┌─────────┐
│ pending │──────────────────▶│ approved │───────────────▶│ running │
└─────────┘                   └──────────┘                └─────────┘
     │                                                         │
     │ user rejects                                            │
     ▼                                              ┌──────────┴──────────┐
┌──────────┐                                        ▼                     ▼
│ rejected │                                  ┌───────────┐        ┌────────┐
└──────────┘                                  │ completed │        │ failed │
                                              └───────────┘        └────────┘
```

### Consent Scope

```
┌───────────────┐
│ Tool Invoked  │
└───────┬───────┘
        │
        ▼
┌───────────────────┐
│ requiresConsent?  │
└───────┬───────────┘
        │
   ┌────┴────┐
   │         │
  yes        no
   │         │
   ▼         ▼
┌──────────┐  ┌────────────┐
│ Check    │  │ Execute    │
│ Registry │  │ Directly   │
└────┬─────┘  └────────────┘
     │
     ▼
┌──────────────────┐
│ Consent exists?  │
└───────┬──────────┘
        │
   ┌────┴────┐
   │         │
  yes        no
   │         │
   ▼         ▼
┌──────────┐  ┌────────────┐
│ Execute  │  │ Prompt     │
│ Tool     │  │ User       │
└──────────┘  └─────┬──────┘
                    │
               ┌────┴────┐
               │         │
            approve    deny
               │         │
               ▼         ▼
          ┌────────┐  ┌────────┐
          │ Store  │  │ Return │
          │ & Exec │  │ Denied │
          └────────┘  └────────┘
```

---

## Validation Rules

### Cross-Entity Validation

1. **Agent-Skill**: Skills can only reference agents that exist in `agent-manifest.yaml`
2. **Skill-Tool**: Skills can only require tools that exist in `tool-manifest.yaml`
3. **Skill-Skill**: Skill prerequisites must not create circular dependencies
4. **Skill Depth**: Skill composition chain cannot exceed 5 levels
5. **Routing-Agent**: Routing registry can only reference existing agents
6. **Workflow-Agent**: Workflow steps can only use agents from routing registry

### Schema Files

| Entity | Schema File | Location |
|--------|-------------|----------|
| Agent | `agent-schema.json` | `.paperkit/_cfg/schemas/` |
| Skill | `skill-schema.json` | `.paperkit/_cfg/schemas/` |
| Tool | `tool-schema.json` | `.paperkit/_cfg/schemas/` |
| Workflow | `workflow-schema.json` | `.paperkit/_cfg/schemas/` |
| Routing | `routing-schema.json` | `.paperkit/_cfg/schemas/` |
| Metrics | `metrics-schema.json` | `.paperkit/_cfg/schemas/` |
