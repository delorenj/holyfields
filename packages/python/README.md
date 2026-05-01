# Holyfields for Python

`holyfields` provides Pydantic models generated from the Holyfields JSON Schema
registry. The JSON Schemas remain the source of truth; this package is a
publishable Python binding for services that produce or consume 33GOD events.

## Use the package

Import generated models from `holyfields.generated`.

```python
from holyfields.generated.agent.session_started_v1 import AgentSessionStartedV1
```

The package also includes the raw JSON Schemas under `holyfields/schemas` in
published wheels.
