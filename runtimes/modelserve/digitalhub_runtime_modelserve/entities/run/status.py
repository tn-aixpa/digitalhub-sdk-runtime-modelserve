from __future__ import annotations

import psutil
import requests
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_ml.entities.run.status import RunStatusMl


class RunStatusModelserve(RunStatusMl):
    """
    Run Model serve status.
    """

    def invoke(self, **kwargs) -> dict:
        """
        Invoke running process.

        Parameters
        ----------
        kwargs
            Keyword arguments to pass to the request.

        Returns
        -------
        None
        """
        try:
            url = self.results.get("endpoint")
            kwargs["url"] = url
            response = requests.request(**kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            msg = f"Something got wrong during model serving. Exception: {e.__class__}. Error: {e.args}"
            raise EntityError(msg)

    def stop(self) -> None:
        """
        Stop running process.

        Returns
        -------
        None
        """
        pid = self.results.get("pid")
        if self.results is None or pid is None:
            return
        p = psutil.Process(pid)
        p.kill()


class RunStatusSklearnserve(RunStatusModelserve):
    """
    Run SKLearn Model serve status.
    """


class RunStatusMlflowserve(RunStatusModelserve):
    """
    Run Mlflow Model serve status.
    """


class RunStatusHuggingfaceserve(RunStatusModelserve):
    """
    Run HuggingFace Model serve status.
    """
