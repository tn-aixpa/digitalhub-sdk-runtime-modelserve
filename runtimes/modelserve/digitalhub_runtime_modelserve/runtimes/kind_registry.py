from __future__ import annotations

from digitalhub_core.runtimes.kind_registry import KindRegistry

sklearnserve_kind_registry = KindRegistry(
    {
        "executable": {"kind": "sklearnserve"},
        "task": [{"kind": "sklearnserve+serve", "action": "serve"}],
        "run": {"kind": "sklearnserve+run"},
    }
)
mlflowserve_kind_registry = KindRegistry(
    {
        "executable": {"kind": "mlflowserve"},
        "task": [{"kind": "mlflowserve+serve", "action": "serve"}],
        "run": {"kind": "mlflowserve+run"},
    }
)
huggingfaceserve_kind_registry = KindRegistry(
    {
        "executable": {"kind": "huggingfaceserve"},
        "task": [{"kind": "huggingfaceserve+serve", "action": "serve"}],
        "run": {"kind": "huggingfaceserve+run"},
    }
)
