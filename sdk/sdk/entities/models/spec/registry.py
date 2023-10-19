"""
Model specification registry module.
"""
from sdk.entities.base.spec import SpecRegistry
from sdk.entities.models.kinds import ModelKinds
from sdk.entities.models.spec.objects.model import ModelParamsModel, ModelSpecModel

model_registry = SpecRegistry()
model_registry.register(ModelKinds.MODEL.value, ModelSpecModel, ModelParamsModel)
