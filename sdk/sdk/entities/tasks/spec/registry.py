"""
Task specification registry module.
"""
from sdk.entities.tasks.kinds import TaskKinds
from sdk.entities.tasks.spec.models import TaskParamsBuild, TaskParamsJob, TaskParamsTransform
from sdk.entities.tasks.spec.objects import TaskSpecBuild, TaskSpecJob, TaskSpecTransform

TASK_SPEC = {
    TaskKinds.BUILD.value: TaskSpecBuild,
    TaskKinds.JOB.value: TaskSpecJob,
    TaskKinds.TRANSFORM.value: TaskSpecTransform,
}
TASK_MODEL = {
    TaskKinds.BUILD.value: TaskParamsBuild,
    TaskKinds.JOB.value: TaskParamsJob,
    TaskKinds.TRANSFORM.value: TaskParamsTransform,
}
