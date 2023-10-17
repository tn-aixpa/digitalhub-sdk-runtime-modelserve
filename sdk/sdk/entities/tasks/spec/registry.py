"""
Task specification registry module.
"""
from sdk.entities.base.spec import SpecRegistry
from sdk.entities.tasks.kinds import TaskKinds
from sdk.entities.tasks.spec.objects.build import TaskParamsBuild, TaskSpecBuild
from sdk.entities.tasks.spec.objects.infer import TaskParamsInfer, TaskSpecInfer
from sdk.entities.tasks.spec.objects.job import TaskParamsJob, TaskSpecJob
from sdk.entities.tasks.spec.objects.mlrun import TaskParamsMLRun, TaskSpecMLRun
from sdk.entities.tasks.spec.objects.profile import TaskParamsProfile, TaskSpecProfile
from sdk.entities.tasks.spec.objects.python import TaskParamsPython, TaskSpecPython
from sdk.entities.tasks.spec.objects.transform import TaskParamsTransform, TaskSpecTransform
from sdk.entities.tasks.spec.objects.validate import TaskParamsValidate, TaskSpecValidate

task_registry = SpecRegistry()
task_registry.register(TaskKinds.BUILD.value, TaskSpecBuild, TaskParamsBuild)
task_registry.register(TaskKinds.INFER.value, TaskSpecInfer, TaskParamsInfer)
task_registry.register(TaskKinds.JOB.value, TaskSpecJob, TaskParamsJob)
task_registry.register(TaskKinds.MLRUN.value, TaskSpecMLRun, TaskParamsMLRun)
task_registry.register(TaskKinds.PROFILE.value, TaskSpecProfile, TaskParamsProfile)
task_registry.register(TaskKinds.PYTHON.value, TaskSpecPython, TaskParamsPython)
task_registry.register(TaskKinds.TRANSFORM.value, TaskSpecTransform, TaskParamsTransform)
task_registry.register(TaskKinds.VALIDATE.value, TaskSpecValidate, TaskParamsValidate)
