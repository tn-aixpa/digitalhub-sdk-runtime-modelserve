from __future__ import annotations

import typing
from typing import Any

import requests

from digitalhub.entities.run._base.entity import Run

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.run.python_run.spec import RunSpecPythonRun
    from digitalhub_runtime_python.entities.run.python_run.status import RunStatusPythonRun

    from digitalhub.entities._base.entity.metadata import Metadata
    from digitalhub.entities._base.material.entity import MaterialEntity


class RunPythonRun(Run):
    """
    RunPythonRun class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecPythonRun,
        status: RunStatusPythonRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecPythonRun
        self.status: RunStatusPythonRun

    def inputs(self, as_dict: bool = False) -> list[dict]:
        """
        Get inputs passed in spec as objects or as dictionaries.

        Parameters
        ----------
        as_dict : bool
            If True, return inputs as dictionaries.

        Returns
        -------
        list[dict]
            List of input objects.
        """
        return self.spec.get_inputs(as_dict=as_dict)

    def results(self) -> dict:
        """
        Get results from runtime execution.

        Returns
        -------
        dict
            Results.
        """
        return self.status.get_results()

    def result(self, key: str) -> Any:
        """
        Get result from runtime execution by key.

        Parameters
        ----------
        key : str
            Key of the result.

        Returns
        -------
        Any
            Result.
        """
        return self.results().get(key)

    def outputs(self, as_key: bool = False, as_dict: bool = False) -> dict:
        """
        Get run objects results.

        Parameters
        ----------
        as_key : bool
            If True, return results as keys.
        as_dict : bool
            If True, return results as dictionaries.

        Returns
        -------
        dict
            List of output objects.
        """
        return self.status.get_outputs(as_key=as_key, as_dict=as_dict)

    def output(self, key: str, as_key: bool = False, as_dict: bool = False) -> MaterialEntity | dict | str | None:
        """
        Get run object result by key.

        Parameters
        ----------
        key : str
            Key of the result.
        as_key : bool
            If True, return result as key.
        as_dict : bool
            If True, return result as dictionary.

        Returns
        -------
        Entity | dict | str | None
            Result.
        """
        return self.outputs(as_key=as_key, as_dict=as_dict).get(key)

    def values(self) -> dict:
        """
        Get values from runtime execution.

        Returns
        -------
        dict
            Values from backend.
        """
        value_list = getattr(self.spec, "values", [])
        value_list = value_list if value_list is not None else []
        return self.status.get_values(value_list)

    def invoke(self, **kwargs) -> requests.Response:
        """
        Invoke run.

        Parameters
        ----------
        kwargs
            Keyword arguments to pass to the request.

        Returns
        -------
        requests.Response
            Response from service.
        """
        if not self._context().local and not self.spec.local_execution:
            local = False
        else:
            local = True
        if kwargs is None:
            kwargs = {}
        return self.status.invoke(local, **kwargs)
