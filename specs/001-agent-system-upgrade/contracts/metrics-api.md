# Metrics API Contract

**Feature**: 001-agent-system-upgrade
**Version**: 1.0.0
**Date**: 2026-01-20

## Overview

Internal API for collecting and querying agent system metrics. Implemented as Python module with SQLite backend.

---

## Data Types

### MetricCategory (Enum)
```python
class MetricCategory(Enum):
    AGENT = "agent"
    SKILL = "skill"
    TOOL = "tool"
    WORKFLOW = "workflow"
    ROUTING = "routing"
```

### MetricRecord
```python
@dataclass
class MetricRecord:
    id: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    category: MetricCategory
    entity_name: str
    action: str
    success: bool
    duration_ms: Optional[int] = None
    confidence_score: Optional[float] = None
    user_modified: Optional[bool] = None
    error_type: Optional[str] = None
    metadata: Optional[dict] = None
```

### MetricSummary
```python
@dataclass
class MetricSummary:
    entity_name: str
    total_invocations: int
    success_count: int
    failure_count: int
    success_rate: float
    avg_duration_ms: float
    p95_duration_ms: float
    avg_confidence: Optional[float] = None
    user_modification_rate: Optional[float] = None
```

---

## API Methods

### `record_metric(metric: MetricRecord) -> int`

Record a new metric entry.

**Parameters**:
- `metric`: MetricRecord to store

**Returns**: ID of inserted record

**Side Effects**:
- Triggers 90-day cleanup on write
- Logs to debug output if verbose mode enabled

**Example**:
```python
from paperkit.metrics import MetricsCollector, MetricRecord, MetricCategory

collector = MetricsCollector()
metric_id = collector.record_metric(MetricRecord(
    category=MetricCategory.AGENT,
    entity_name="section-drafter",
    action="draft_section",
    success=True,
    duration_ms=2340,
    confidence_score=0.85
))
```

---

### `get_summary(entity_name: str, category: MetricCategory, days: int = 30) -> MetricSummary`

Get aggregated metrics for an entity over a time period.

**Parameters**:
- `entity_name`: Name of agent/skill/tool/workflow
- `category`: Category of entity
- `days`: Number of days to include (default: 30, max: 90)

**Returns**: MetricSummary with aggregated statistics

**Example**:
```python
summary = collector.get_summary(
    entity_name="orchestrator",
    category=MetricCategory.ROUTING,
    days=7
)
print(f"Routing accuracy: {summary.success_rate:.1%}")
print(f"User override rate: {summary.user_modification_rate:.1%}")
```

---

### `get_routing_accuracy(days: int = 30) -> float`

Calculate overall routing accuracy (percentage of routes not modified by user).

**Parameters**:
- `days`: Number of days to include

**Returns**: Float between 0.0 and 1.0

**Example**:
```python
accuracy = collector.get_routing_accuracy(days=14)
print(f"14-day routing accuracy: {accuracy:.1%}")
```

---

### `get_ab_test_results(test_name: str) -> ABTestResults`

Get statistical comparison for an A/B test.

**Parameters**:
- `test_name`: Name of A/B test from routing registry

**Returns**: ABTestResults with statistical analysis

**ABTestResults**:
```python
@dataclass
class ABTestResults:
    test_name: str
    control_summary: MetricSummary
    treatment_summary: MetricSummary
    sample_size_met: bool
    success_rate_diff: float
    success_rate_p_value: float
    duration_diff_ms: float
    duration_p_value: float
    recommendation: str  # "control", "treatment", or "inconclusive"
```

**Example**:
```python
results = collector.get_ab_test_results("orchestrator-v2-test")
if results.sample_size_met:
    print(f"Recommendation: {results.recommendation}")
    print(f"Success rate improvement: {results.success_rate_diff:+.1%}")
```

---

### `get_trends(category: MetricCategory, days: int = 30) -> List[TrendPoint]`

Get daily aggregated metrics for trend analysis.

**Parameters**:
- `category`: Category to analyze
- `days`: Number of days to include

**Returns**: List of TrendPoint, one per day

**TrendPoint**:
```python
@dataclass
class TrendPoint:
    date: date
    invocations: int
    success_rate: float
    avg_duration_ms: float
```

---

### `cleanup(days: int = 90) -> int`

Remove metrics older than specified days.

**Parameters**:
- `days`: Retention period (default: 90)

**Returns**: Number of records deleted

**Note**: Called automatically on every `record_metric()` call.

---

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS agent_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    category TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    action TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    duration_ms INTEGER,
    confidence_score REAL,
    user_modified BOOLEAN,
    error_type TEXT,
    metadata TEXT  -- JSON blob
);

CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON agent_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_metrics_category ON agent_metrics(category);
CREATE INDEX IF NOT EXISTS idx_metrics_entity ON agent_metrics(entity_name);
CREATE INDEX IF NOT EXISTS idx_metrics_success ON agent_metrics(success);
```

---

## Configuration

**Storage Location**: `.paperkit/data/metrics.db`

**Retention Policy**: 90 days (auto-cleanup on write)

**Connection Pooling**: Single connection per process (SQLite limitation)

---

## Error Handling

| Error | Condition | Handling |
|-------|-----------|----------|
| `DatabaseNotFoundError` | metrics.db doesn't exist | Auto-create on first write |
| `SchemaVersionError` | DB schema outdated | Auto-migrate or fail with instructions |
| `RetentionViolation` | Querying beyond 90 days | Return empty results, log warning |
| `ABTestNotFoundError` | Test name doesn't exist | Return error with available test names |

---

## Thread Safety

- Metrics collection is thread-safe using connection-per-write pattern
- Read operations use shared connection with read-only mode
- No external locking required

---

## Performance Characteristics

| Operation | Expected Latency |
|-----------|------------------|
| `record_metric` | <10ms |
| `get_summary` (30 days) | <50ms |
| `get_routing_accuracy` | <20ms |
| `get_ab_test_results` | <100ms |
| `get_trends` (30 days) | <100ms |
| `cleanup` | <500ms |
