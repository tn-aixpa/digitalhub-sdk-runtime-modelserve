from __future__ import annotations

from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

status_registry = StatusRegistry()
status_registry.register("dataitem", "digitalhub_data.entities.dataitems.status", "DataitemStatus")

spec_registry = SpecRegistry()
spec_registry.register("dataitem", "digitalhub_data.entities.dataitems.spec", "DataitemSpec", "DataitemParams")
spec_registry.register("project", "digitalhub_data.entities.projects.spec", "ProjectSpecData", "ProjectParamsData")
