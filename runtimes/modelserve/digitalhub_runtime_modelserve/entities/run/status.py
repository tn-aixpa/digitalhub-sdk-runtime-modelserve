from __future__ import annotations

from digitalhub_ml.entities.run.status import RunStatusMl


class RunStatusModelserve(RunStatusMl):
    """
    Run Model serve status.
    """

class RunStatusSklearnserve(RunStatusMl):
    """
    Run SKLearn Model serve status.
    """

class RunStatusMlflowserve(RunStatusMl):
    """
    Run Mlflow Model serve status.
    """

class RunStatusHuggingfaceserve(RunStatusMl):
    """
    Run HuggingFace Model serve status.
    """