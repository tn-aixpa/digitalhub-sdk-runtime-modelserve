from __future__ import annotations

from digitalhub_core.runtimes.registry import KindRegistry

kind_registry = KindRegistry(
    {
        "executable": {"kind": "python"},
        "task": [
            {"kind": "python+job", "action": "job"},
            {"kind": "python+serve", "action": "serve"},
            {"kind": "python+build", "action": "build"},
        ],
        "run": {"kind": "python+run"},
    }
)
