from __future__ import annotations

import psutil
import requests

from digitalhub.entities.run._base.status import RunStatus
from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.logger import LOGGER


class RunStatusModelserveRun(RunStatus):
    """
    RunStatusModelserveRun status.
    """

    def invoke(self, local: bool, model_name: str | None = None, **kwargs) -> requests.Response:
        """
        Invoke running process. By default it exposes infer v2 endpoint.

        Parameters
        ----------
        model_name : str
            Name of the model for the endpoint.
        kwargs
            Keyword arguments to pass to the request.

        Returns
        -------
        requests.Response
            Response from the request.
        """
        try:
            method = kwargs.pop("method", "POST")
            url = kwargs.pop("url", None)
            if url is None:
                if local:
                    url = self.results.get("endpoint")
                else:
                    model_name = model_name if model_name is not None else "model"
                    url = f"http://{self.service.get('url')}/v2/models/{model_name}/infer"

            response = requests.request(
                method=method,
                url=url,
                **kwargs,
            )
            response.raise_for_status()
            return response
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
            raise EntityError("No running process to stop.")
        p = psutil.Process(pid)
        p.kill()
        LOGGER.info(f"Process {pid} stopped.")
