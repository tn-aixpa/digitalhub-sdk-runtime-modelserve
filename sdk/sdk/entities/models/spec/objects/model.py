"""
Model Model specification module.
"""
from sdk.entities.models.spec.objects.base import ModelParams, ModelSpec


class ModelSpecModel(ModelSpec):
    """
    Specification for a Model model.
    """


class ModelParamsModel(ModelParams):
    """
    Model model parameters.
    """

    test: str
    """Placeholder for test parameter."""
