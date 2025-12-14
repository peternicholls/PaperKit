# Specification: State Management and Mode Persistence Risks

**Spec ID:** 009-state-management  
**Date:** 2024-12-13  
**Status:** Draft  
**Priority:** Medium  
**Category:** Core Architecture

---

## Problem Statement

Modes persist for a chat session. Persistent context is powerful but can cause stale state or cross-session leakage. Users cannot easily see what state is loaded, and there's no mechanism for checkpoints or rollbacks.

### Current State

- Agent mode persists within a chat session
- Session state is implicit (not visible to user)
- No way to view loaded context
- No checkpoint/restore capability
- State can become stale during long sessions
- No versioning of context objects
- Cross-session state leakage possible

### Impact

- Users confused about what context is active
- Stale state leads to incorrect agent responses
- No recovery from bad states
- Long sessions accumulate irrelevant context
- Difficult to reproduce specific states for debugging

---

## Proposed Solution

### Overview

Implement explicit state management with visibility, checkpoints, versioning, and controlled context lifecycle.

### Technical Requirements

#### 1. Session State Schema

```yaml
# Schema for session state
sessionState:
  sessionId: "session-{uuid}"
  createdAt: "2024-12-13T10:00:00Z"
  lastActivityAt: "2024-12-13T11:30:00Z"
  expiresAt: "2024-12-13T14:00:00Z"  # Auto-expire after inactivity
  
  user:
    id: "user"
    preferences:
      autoSave: true
      contextExpiry: "4h"
      
  activeAgent:
    id: "section-drafter"
    activatedAt: "2024-12-13T11:00:00Z"
    
  context:
    version: 3
    createdAt: "2024-12-13T10:30:00Z"
    updatedAt: "2024-12-13T11:25:00Z"
    
    paper:
      title: "Color Perception Modeling"
      scope: "Mathematical approaches to color perception"
      targetLength: 10000
      
    loadedDocuments:
      - id: "doc-1"
        path: "output-drafts/outlines/paper-outline.md"
        loadedAt: "2024-12-13T10:30:00Z"
        hash: "sha256:abc123"
        stale: false
        
      - id: "doc-2"
        path: "output-refined/research/consolidated.md"
        loadedAt: "2024-12-13T10:35:00Z"
        hash: "sha256:def456"
        stale: true  # File changed since load
        
    currentTask:
      type: "draft_section"
      section: "introduction"
      startedAt: "2024-12-13T11:00:00Z"
      
    conversationSummary:
      turns: 15
      topics: ["outline review", "introduction drafting"]
      decisions:
        - "Focus on practical applications"
        - "Include 3 case studies"
        
  checkpoints:
    - id: "cp-1"
      createdAt: "2024-12-13T10:45:00Z"
      description: "After outline completion"
      contextVersion: 1
      
    - id: "cp-2"
      createdAt: "2024-12-13T11:15:00Z"
      description: "Mid-introduction draft"
      contextVersion: 2
```

#### 2. State Visibility UI

```yaml
# State display for user
stateDisplay:
  format: "compact"  # compact | detailed | json
  
  compact:
    template: |
      📋 Session: {sessionId} | Active: {activeAgent}
      📄 Context: {paperTitle} ({loadedDocCount} docs)
      ⏰ Last checkpoint: {lastCheckpoint}
      ⚠️ Stale docs: {staleDocCount}
      
  detailed:
    sections:
      - header: "Active Session"
        fields:
          - "Session ID: {sessionId}"
          - "Started: {createdAt}"
          - "Expires: {expiresAt}"
          
      - header: "Current Context"
        fields:
          - "Paper: {paperTitle}"
          - "Active Agent: {activeAgent}"
          - "Context Version: {contextVersion}"
          
      - header: "Loaded Documents"
        list: loadedDocuments
        format: "• {path} ({status})"
        
      - header: "Checkpoints"
        list: checkpoints
        format: "• {id}: {description} ({createdAt})"
```

```
┌─────────────────────────────────────────────────────────────────┐
│  📊 Session State                                    [Refresh]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🔹 Session: session-abc123                                     │
│  🔹 Active Agent: Section Drafter (Jordan)                      │
│  🔹 Started: 10:00 AM | Expires: 2:00 PM                        │
│                                                                  │
│  📄 Context: "Color Perception Modeling"                         │
│  └─ Version 3 (updated 5 min ago)                               │
│                                                                  │
│  📚 Loaded Documents (2):                                        │
│  ├─ ✓ paper-outline.md (current)                                │
│  └─ ⚠️ consolidated.md (stale - file changed)                   │
│                                                                  │
│  📍 Checkpoints (2):                                             │
│  ├─ cp-1: After outline (10:45 AM)                              │
│  └─ cp-2: Mid-intro draft (11:15 AM)                            │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Refresh  │  │ Checkpoint│  │ Restore  │  │  Clear   │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 3. Checkpoint System

```python
# tools/state/checkpoint_manager.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import json
import hashlib

@dataclass
class Checkpoint:
    id: str
    session_id: str
    created_at: datetime
    description: str
    context_version: int
    state_snapshot: dict
    artifact_hashes: dict

class CheckpointManager:
    """Manage session checkpoints for state recovery."""
    
    def __init__(self, storage_path: str = ".paper/state/checkpoints"):
        self.storage_path = storage_path
        
    def create_checkpoint(
        self, 
        session: SessionState, 
        description: str
    ) -> Checkpoint:
        """
        Create a checkpoint of current session state.
        
        Args:
            session: Current session state
            description: Human-readable checkpoint description
            
        Returns:
            Created checkpoint
        """
        checkpoint = Checkpoint(
            id=f"cp-{generate_uuid()}",
            session_id=session.session_id,
            created_at=datetime.utcnow(),
            description=description,
            context_version=session.context.version,
            state_snapshot=session.to_dict(),
            artifact_hashes=self._hash_artifacts(session.context.loaded_documents)
        )
        self._save_checkpoint(checkpoint)
        return checkpoint
        
    def restore_checkpoint(self, checkpoint_id: str) -> SessionState:
        """
        Restore session state from checkpoint.
        
        Args:
            checkpoint_id: ID of checkpoint to restore
            
        Returns:
            Restored session state
        """
        checkpoint = self._load_checkpoint(checkpoint_id)
        session = SessionState.from_dict(checkpoint.state_snapshot)
        
        # Check for artifact drift
        current_hashes = self._hash_artifacts(session.context.loaded_documents)
        drifted = []
        for path, expected_hash in checkpoint.artifact_hashes.items():
            if current_hashes.get(path) != expected_hash:
                drifted.append(path)
                
        if drifted:
            session.warnings.append(f"Artifacts changed since checkpoint: {drifted}")
            
        return session
        
    def list_checkpoints(self, session_id: str) -> List[Checkpoint]:
        """List all checkpoints for a session."""
        pass
        
    def delete_checkpoint(self, checkpoint_id: str) -> None:
        """Delete a checkpoint."""
        pass
        
    def auto_checkpoint(self, session: SessionState, trigger: str) -> Optional[Checkpoint]:
        """
        Create automatic checkpoint based on triggers.
        
        Triggers: agent_switch, task_complete, time_interval
        """
        pass
```

#### 4. Context Lifecycle Management

```yaml
# .paper/_cfg/state/lifecycle-config.yaml
contextLifecycle:
  version: "1.0.0"
  
  expiry:
    default: "4h"
    maxDuration: "24h"
    inactivityTimeout: "2h"
    
  staleDetection:
    enabled: true
    checkInterval: "5m"
    onStaleDocument:
      action: "warn"  # warn | auto_reload | prompt
      
  autoCheckpoint:
    enabled: true
    triggers:
      - event: "agent_switch"
        description: "When switching to different agent"
      - event: "task_complete"
        description: "When a major task completes"
      - event: "time_interval"
        interval: "30m"
        description: "Every 30 minutes of activity"
    maxCheckpoints: 10
    prunePolicy: "keep_recent"
    
  cleanup:
    orphanedStates: "7d"
    oldCheckpoints: "30d"
    expiredSessions: "24h"
```

#### 5. State Versioning

```python
# tools/state/version_manager.py
@dataclass
class ContextVersion:
    version: int
    created_at: datetime
    changes: List[str]
    parent_version: Optional[int]

class ContextVersionManager:
    """Track and manage context versions."""
    
    def increment_version(
        self, 
        context: ContextState, 
        changes: List[str]
    ) -> ContextVersion:
        """
        Create new context version with changes.
        
        Args:
            context: Current context
            changes: List of changes made
            
        Returns:
            New version record
        """
        new_version = ContextVersion(
            version=context.version + 1,
            created_at=datetime.utcnow(),
            changes=changes,
            parent_version=context.version
        )
        context.version = new_version.version
        context.version_history.append(new_version)
        return new_version
        
    def get_version_diff(
        self, 
        version_a: int, 
        version_b: int
    ) -> List[str]:
        """Get changes between two versions."""
        pass
        
    def rollback_to_version(
        self, 
        context: ContextState, 
        target_version: int
    ) -> ContextState:
        """Rollback context to specific version."""
        pass
```

#### 6. Cross-Session Isolation

```yaml
# Session isolation configuration
sessionIsolation:
  enabled: true
  
  isolation:
    contextSharing: false
    artifactSharing: true  # Artifacts on disk are shared
    preferenceSharing: true
    
  boundaries:
    # What's isolated per session
    perSession:
      - context
      - conversationHistory
      - checkpoints
      - activeAgent
      
    # What persists across sessions
    persistent:
      - userPreferences
      - paperMetadata
      - artifacts
      - bibliography
      
  cleanup:
    onSessionEnd:
      - clearContext: true
      - saveCheckpoint: "optional"
      - archiveConversation: true
```

#### 7. State Commands

```yaml
# User commands for state management
stateCommands:
  show_state:
    trigger: "/state"
    description: "Show current session state"
    output: "stateDisplay.detailed"
    
  create_checkpoint:
    trigger: "/checkpoint [description]"
    description: "Create checkpoint with description"
    example: "/checkpoint After completing introduction"
    
  list_checkpoints:
    trigger: "/checkpoints"
    description: "List available checkpoints"
    
  restore_checkpoint:
    trigger: "/restore [checkpoint-id]"
    description: "Restore state from checkpoint"
    example: "/restore cp-1"
    
  clear_context:
    trigger: "/clear"
    description: "Clear current context (with confirmation)"
    confirmation: true
    
  refresh_documents:
    trigger: "/refresh"
    description: "Reload stale documents"
```

---

## Implementation Steps

| Step | Description | Estimated Effort |
|------|-------------|------------------|
| 1 | Define session state schema | 4 hours |
| 2 | Implement state storage layer | 6 hours |
| 3 | Build checkpoint manager | 8 hours |
| 4 | Implement context versioning | 6 hours |
| 5 | Add stale document detection | 4 hours |
| 6 | Create state visibility UI | 6 hours |
| 7 | Implement state commands | 4 hours |
| 8 | Add session isolation | 4 hours |
| 9 | Implement auto-checkpoint | 4 hours |
| 10 | Testing and documentation | 4 hours |

**Total Estimated Effort:** 50 hours

---

## Success Criteria

- [ ] Session state visible to user
- [ ] Checkpoints can be created and restored
- [ ] Stale documents detected and flagged
- [ ] Context versioning tracks all changes
- [ ] Sessions properly isolated
- [ ] Auto-checkpoints created on triggers
- [ ] State commands working

---

## Dependencies

- [006-observability.md](006-observability.md) - State logging integration

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| State storage overhead | Medium | Pruning policies; compression |
| Checkpoint restore fails | High | Validation before restore; backup |
| Performance impact | Low | Lazy loading; caching |
| User confusion | Medium | Clear UI; documentation |

---

## Related Specifications

- [002-workflow-agent-contract.md](002-workflow-agent-contract.md) - Workflow state
- [006-observability.md](006-observability.md) - State logging

---

## Open Questions

1. Should checkpoints include conversation history?
2. How to handle large artifacts in state snapshots?
3. Should users be able to share/export states?
4. What's the right balance of auto vs manual checkpoints?

---

## References

- Event sourcing patterns
- Git-like versioning for state
