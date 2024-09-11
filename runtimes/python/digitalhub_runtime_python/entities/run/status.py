from __future__ import annotations

import requests
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_ml.entities.run.status import RunStatusMl


class RunStatusPython(RunStatusMl):
    """
    Run Python status.
    """

    def invoke(self, local: bool, **kwargs) -> requests.Response:
        """
        Invoke running process.

        Parameters
        ----------
        kwargs
            Keyword arguments to pass to the request.

        Returns
        -------
        requests.Response
            Response from service.
        """
        try:
            if local:
                raise EntityError("Invoke not supported locally.")

            method = kwargs.pop("method", "POST")
            url = kwargs.get("url", "http://" + self.service.get("url"))

            response = requests.request(method=method, url=url, **kwargs)
            response.raise_for_status()
            return response
        except Exception as e:
            msg = f"Something got wrong during model serving. Exception: {e.__class__}. Error: {e.args}"
            raise EntityError(msg)
