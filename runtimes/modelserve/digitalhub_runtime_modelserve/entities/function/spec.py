from __future__ import annotations

from digitalhub.entities.function.spec import FunctionSpec, FunctionValidator


class FunctionSpecModelserve(FunctionSpec):
    """
    specifications.for a Function for model serving.
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


class FunctionValidatorModelserve(FunctionValidator):
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
    specifications.for a Function for SKLearn model serving.
    """


class FunctionSpecMlflowserve(FunctionSpecModelserve):
    """
    specifications.for a Function for MLFlow model serving.
    """


class FunctionSpecHuggingfaceserve(FunctionSpecModelserve):
    """
    specifications.for a Function for HuggingFace model serving.
    """


class FunctionValidatorSklearnserve(FunctionValidatorModelserve):
    """
    Function SKLearn model serving parameters model.
    """


class FunctionValidatorMlflowserve(FunctionValidatorModelserve):
    """
    Function MLFlow model serving parameters model.
    """


class FunctionValidatorHuggingfaceserve(FunctionValidatorModelserve):
    """
    Function HuggingFace model serving parameters model.
    """
