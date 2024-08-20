from __future__ import annotations

from digitalhub_core.entities.function.status import FunctionStatus


class FunctionStatusModelserve(FunctionStatus):
    """
    Function Model serve status.
    """


class FunctionStatusSklearnserve(FunctionStatusModelserve):
    """
    Function SKLearn Model serve status.
    """


class FunctionStatusHuggingfaceserve(FunctionStatusModelserve):
    """
    Function HuggingFace Model serve status.
    """


class FunctionStatusMlflowserve(FunctionStatusModelserve):
    """
    Function Mlflow Model serve status.
    """
