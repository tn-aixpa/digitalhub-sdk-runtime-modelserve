"""
Task specification registry module.
"""
from sdk.entities.task.kinds import TaskKinds
from sdk.entities.task.spec.models import TaskParamsBuild, TaskParamsPerform
from sdk.entities.task.spec.objects import TaskSpecBuild, TaskSpecPerform

REGISTRY_SPEC = {
    TaskKinds.BUILD.value: TaskSpecBuild,
    TaskKinds.PERFORM.value: TaskSpecPerform,
}
REGISTRY_MODEL = {
    TaskKinds.BUILD.value: TaskParamsBuild,
    TaskKinds.PERFORM.value: TaskParamsPerform,
}
