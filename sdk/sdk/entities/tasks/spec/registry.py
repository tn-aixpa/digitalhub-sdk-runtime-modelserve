"""
Task specification registry module.
"""
from sdk.entities.tasks.kinds import TaskKinds
from sdk.entities.tasks.spec.models import TaskParamsBuild, TaskParamsPerform
from sdk.entities.tasks.spec.objects import TaskSpecBuild, TaskSpecJob

TASK_SPEC = {
    TaskKinds.BUILD.value: TaskSpecBuild,
    TaskKinds.JOB.value: TaskSpecJob,
}
TASK_MODEL = {
    TaskKinds.BUILD.value: TaskParamsBuild,
    TaskKinds.JOB.value: TaskParamsPerform,
}
