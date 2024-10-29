from __future__ import annotations

from digitalhub.entities._base.runtime_entity.builder import RuntimeEntityBuilder


class RuntimeEntityBuilderKfp(RuntimeEntityBuilder):
    EXECUTABLE_KIND = "kfp"
    TASKS_KINDS = [
        {
            "kind": "kfp+pipeline",
            "action": "pipeline",
        },
        {
            "kind": "kfp+build",
            "action": "build",
        },
    ]
    RUN_KIND = "kfp+run"
