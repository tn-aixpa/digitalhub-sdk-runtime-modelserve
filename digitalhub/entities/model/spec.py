from __future__ import annotations

from digitalhub.entities._base.material.spec import MaterialSpec, MaterialValidator
from digitalhub.entities.model.models import Dataset, Signature


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


class ModelValidator(MaterialValidator):
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


class ModelValidatorModel(ModelValidator):
    """
    Model parameters.
    """


class ModelSpecMlflow(ModelSpec):
    """
    Mlflow model specifications.
    """

    def __init__(
        self,
        path: str,
        framework: str | None = None,
        algorithm: str | None = None,
        base_model: str | None = None,
        parameters: dict | None = None,
        metrics: dict | None = None,
        flavor: str | None = None,
        model_config: dict | None = None,
        input_datasets: list[Dataset] | None = None,
        signature: Signature = None,
    ) -> None:
        super().__init__(path, framework, algorithm, base_model, parameters, metrics)
        self.flavor = flavor
        self.model_config = model_config
        self.input_datasets = input_datasets
        self.signature = signature


class ModelValidatorMlflow(ModelValidator):
    """
    Mlflow model parameters.
    """

    flavor: str = None
    """Mlflow model flavor."""
    model_config: dict = None
    """Mlflow model config."""
    input_datasets: list[Dataset] = None
    """Mlflow input datasets."""
    signature: Signature = None
    """Mlflow model signature."""


class ModelSpecSklearn(ModelSpec):
    """
    SKLearn model specifications.
    """


class ModelValidatorSklearn(ModelValidator):
    """
    SKLearn model parameters.
    """


class ModelSpecHuggingface(ModelSpec):
    """
    Huggingface model specifications.
    """

    def __init__(
        self,
        path: str,
        framework: str | None = None,
        algorithm: str | None = None,
        base_model: str | None = None,
        parameters: dict | None = None,
        metrics: dict | None = None,
        model_id: str | None = None,
        model_revision: str = None,
    ) -> None:
        super().__init__(path, framework, algorithm, base_model, parameters, metrics)
        self.model_id = model_id
        self.model_revision = model_revision


class ModelValidatorHuggingface(ModelValidator):
    """
    Huggingface model parameters.
    """

    model_id: str = None
    """Huggingface model id. Optional. If not specified, the model is loaded from the model path"""
    model_revision: str = None
    """Huggingface model revision. Optional."""
