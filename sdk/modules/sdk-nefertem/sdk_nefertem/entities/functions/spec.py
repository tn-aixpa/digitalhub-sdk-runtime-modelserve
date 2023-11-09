"""
Nefertem Function specification module.
"""
from sdk.entities.functions.spec import FunctionParams, FunctionSpec


class FunctionSpecNefertem(FunctionSpec):
    """
    Specification for a Function Nefertem.
    """
    def __init__(self, source: str | None = None, **kwargs):
        super().__init__(source, **kwargs)
        self.platform = "nefertem"


class FunctionParamsNefertem(FunctionParams):
    """
    Function Nefertem parameters model.
    """
