"""
Task specification registry module.
"""
from sdk.entities.tasks.kinds import TaskKinds
from sdk.entities.tasks.spec.objects.build import TaskParamsBuild, TaskSpecBuild
from sdk.entities.tasks.spec.objects.job import TaskParamsJob, TaskSpecJob
from sdk.entities.tasks.spec.objects.transform import (
    TaskParamsTransform,
    TaskSpecTransform,
)

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
