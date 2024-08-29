from __future__ import annotations

from digitalhub_ml.entities.run.status import RunStatusMl


class RunStatusModelserve(RunStatusMl):
    """
    Run Model serve status.
    """

    def __init__(
        self,
        state: str,
        message: str | None = None,
        outputs: list | None = None,
        results: dict | None = None,
        endpoint: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(state, message, outputs, results, **kwargs)
        self.endpoint = endpoint


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
