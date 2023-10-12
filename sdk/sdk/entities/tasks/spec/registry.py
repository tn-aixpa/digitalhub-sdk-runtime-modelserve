"""
Task specification registry module.
"""
from sdk.entities.tasks.kinds import TaskKinds
from sdk.entities.tasks.spec.objects.build import TaskParamsBuild, TaskSpecBuild
from sdk.entities.tasks.spec.objects.infer import TaskParamsInfer, TaskSpecInfer
from sdk.entities.tasks.spec.objects.job import TaskParamsJob, TaskSpecJob
from sdk.entities.tasks.spec.objects.mlrun import TaskParamsMLRun, TaskSpecMLRun
from sdk.entities.tasks.spec.objects.profile import TaskParamsProfile, TaskSpecProfile
from sdk.entities.tasks.spec.objects.transform import (
    TaskParamsTransform,
    TaskSpecTransform,
)
from sdk.entities.tasks.spec.objects.validate import (
    TaskParamsValidate,
    TaskSpecValidate,
)

TASK_SPEC = {
    TaskKinds.BUILD.value: TaskSpecBuild,
    TaskKinds.JOB.value: TaskSpecJob,
    TaskKinds.MLRUN.value: TaskSpecMLRun,
    TaskKinds.TRANSFORM.value: TaskSpecTransform,
    TaskKinds.VALIDATE.value: TaskSpecValidate,
    TaskKinds.PROFILE.value: TaskSpecProfile,
    TaskKinds.INFER.value: TaskSpecInfer,
}
TASK_MODEL = {
    TaskKinds.BUILD.value: TaskParamsBuild,
    TaskKinds.JOB.value: TaskParamsJob,
    TaskKinds.MLRUN.value: TaskParamsMLRun,
    TaskKinds.TRANSFORM.value: TaskParamsTransform,
    TaskKinds.VALIDATE.value: TaskParamsValidate,
    TaskKinds.PROFILE.value: TaskParamsProfile,
    TaskKinds.INFER.value: TaskParamsInfer,
}
