from __future__ import annotations

from digitalhub_core.runtimes.kind_registry import KindRegistry

kind_registry = KindRegistry(
    {
        "executable": {"kind": "kfp"},
        "task": [
            {"kind": "kfp+pipeline", "action": "pipeline"},
            {"kind": "kfp+build", "action": "build"},
        ],
        "run": {"kind": "kfp+run"},
    }
)
