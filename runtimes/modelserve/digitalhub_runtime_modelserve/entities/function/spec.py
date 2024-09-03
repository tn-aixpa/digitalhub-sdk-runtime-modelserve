from __future__ import annotations

from digitalhub_core.entities.function.spec import FunctionParams, FunctionSpec


class FunctionSpecModelserve(FunctionSpec):
    """
    Specification for a Function for model serving.
    """

    def __init__(
        self,
        path: str | None = None,
        model_name: str | None = None,
        image: str | None = None,
    ) -> None:
        super().__init__()
        self.path = path
        self.model_name = model_name
        self.image = image


class FunctionParamsModelserve(FunctionParams):
    """
    Function model serving parameters model.
    """

    path: str = None
    "Path to the model files"

    model_name: str = None
    "Name of the model"

    image: str = None
    "Image where the function will be executed"


class FunctionSpecSklearnserve(FunctionSpecModelserve):
    """
    Specification for a Function for SKLearn model serving.
    """


class FunctionSpecMlflowserve(FunctionSpecModelserve):
    """
    Specification for a Function for MLFlow model serving.
    """


class FunctionSpecHuggingfaceserve(FunctionSpecModelserve):
    """
    Specification for a Function for HuggingFace model serving.
    """


class FunctionParamsSklearnserve(FunctionParamsModelserve):
    """
    Function SKLearn model serving parameters model.
    """


class FunctionParamsMlflowserve(FunctionParamsModelserve):
    """
    Function MLFlow model serving parameters model.
    """


class FunctionParamsHuggingfaceserve(FunctionParamsModelserve):
    """
    Function HuggingFace model serving parameters model.
    """
