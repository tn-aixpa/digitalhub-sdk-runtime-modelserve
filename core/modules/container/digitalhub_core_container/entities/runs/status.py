from __future__ import annotations

from digitalhub_core.entities.runs.status import RunStatus


class RunStatusContainer(RunStatus):
    """
    Run Container status.
    """


status_registry = {
    "container+run": RunStatusContainer,
}
