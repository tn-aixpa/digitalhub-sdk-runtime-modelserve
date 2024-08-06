from __future__ import annotations

from oltreai_core.entities._base.spec.material import MaterialParams, MaterialSpec


class ModelSpec(MaterialSpec):
    """
    Model specifications.
    """

    def __init__(
        self,
        path: str,
        framework: str | None = None,
        algorithm: str | None = None,
        base_model: str | None = None,
        parameters: dict | None = None,
        metrics: dict | None = None,
    ) -> None:
        self.path = path
        self.framework = framework
        self.algorithm = algorithm
        self.base_model = base_model
        self.parameters = parameters
        self.metrics = metrics


class ModelParams(MaterialParams):
    """
    Model parameters.
    """

    path: str
    """Path to the model."""

    framework: str = None
    """Model framework (e.g. 'pytorch')."""

    algorithm: str = None
    """Model algorithm (e.g. 'resnet')."""

    base_model: str = None
    """Base model."""

    parameters: dict = None
    """Model parameters."""

    metrics: dict = None
    """Model metrics."""


class ModelSpecModel(ModelSpec):
    """
    Model specifications.
    """


class ModelParamsModel(ModelParams):
    """
    Model parameters.
    """


class ModelSpecMlflow(ModelSpec):
    """
    Mlflow model specifications.
    """


class ModelParamsMlflow(ModelParams):
    """
    Mlflow model parameters.
    """


class ModelSpecPickle(ModelSpec):
    """
    Pickle model specifications.
    """


class ModelParamsPickle(ModelParams):
    """
    Pickle model parameters.
    """


class ModelSpecHuggingface(ModelSpec):
    """
    Huggingface model specifications.
    """


class ModelParamsHuggingface(ModelParams):
    """
    Huggingface model parameters.
    """
