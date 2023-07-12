"""
Run module.
"""
from __future__ import annotations

import typing
from typing import Self

from sdk.entities.base.entity import Entity
from sdk.entities.run.spec import build_spec
from sdk.utils.api import DTO_RUNS, api_base_create, api_base_delete, api_base_read
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context

if typing.TYPE_CHECKING:
    from sdk.entities.run.spec import RunSpec


class Run(Entity):
    """
    A class representing a run.
    """

    def __init__(
        self,
        project: str,
        task_id: str,
        task: str = None,
        spec: RunSpec = None,
        local: bool = False,
        **kwargs,
    ) -> None:
        """
        Initialize the Run instance.

        Parameters
        ----------
        project : str
            Name of the project.
        task_id : str
            Identifier of the task.
        spec : RunSpec, optional
            Specification for the run, default is None.
        local: bool, optional
            Specify if run locally, default is False.
        """
        super().__init__()
        self.project = project
        self.kind = "run"
        self.task_id = task_id
        self.task = task
        self.spec = spec if spec is not None else build_spec(self.kind, **{})

        self._local = local

        # Set new attributes
        self._any_setter(**kwargs)

        self._context = get_context(self.project)
        self._obj_attr += ["task_id"]

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str = None) -> "Run":
        """
        Save run into backend.

        Parameters
        ----------
        uuid : str, optional
            Ignore this parameter.

        Returns
        -------
        dict
            Mapping representation of Run from backend.

        """
        if self._local:
            raise EntityError("Use .export() for local execution.")

        obj = self.to_dict()
        print(obj)

        api = api_base_create(DTO_RUNS)
        response = self._context.create_object(obj, api)
        self.id = response.get("id")
        return self

    def export(self, filename: str = None) -> None:
        """
        Export object as a YAML file.

        Parameters
        ----------
        filename : str, optional
            Name of the export YAML file. If not specified, the default value is used.

        Returns
        -------
        None

        """
        obj = self.to_dict()
        filename = (
            filename
            if filename is not None
            else f"run_{self.project}_{self.task_id}_{self.id}.yaml"
        )
        self._export_object(filename, obj)

    #############################
    #  Run Methods
    #############################

    def refresh(self) -> dict:
        """
        Get run from backend.

        Returns
        -------
        dict
            Mapping representation of Run from backend.
        """
        if self._local:
            raise EntityError("Cannot refresh local run.")

        api = api_base_read(DTO_RUNS, self.id)
        return self._context.read_object(api)

    def delete(self) -> dict:
        """
        Delete run from backend.

        Returns
        -------
        dict
            Delete response from backend.
        """
        if self._local:
            raise EntityError("Cannot delete local run.")

        api = api_base_delete(DTO_RUNS, self.id)
        return self._context.delete_object(api)

    def stop(self) -> dict:
        """
        Not implemented yet.
        """
        raise NotImplementedError

    def logs(self) -> dict:
        """
        Get run's logs from backend.

        Returns
        -------
        dict
            Logs from backend.
        """
        api = api_base_read(DTO_RUNS, self.id) + "/log"
        return self._context.read_object(api)

    #############################
    #  Getters and Setters
    #############################

    @property
    def local(self) -> bool:
        """
        Get local flag.
        """
        return self._local

    #############################
    #  Generic Methods
    #############################

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        """
        Create object instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        Self
            Self instance.

        """
        parsed_dict = cls._parse_dict(obj)
        obj_ = cls(**parsed_dict)
        obj_._local = obj_._context.local
        return obj_

    @staticmethod
    def _parse_dict(obj: dict) -> dict:
        """
        Parse dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            Parsed dictionary.
        """

        # Mandatory fields
        project = obj.get("project")
        task_id = obj.get("task_id")
        if project is None or task_id is None:
            raise EntityError("Project or task_id are not specified.")

        # Optional fields
        uuid = obj.get("id")
        kind = obj.get("kind", "run")

        # Build metadata and spec
        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(kind=kind, **spec)

        return {
            "project": project,
            "task_id": task_id,
            "kind": kind,
            "uuid": uuid,
            "spec": spec,
        }


def run_from_parameters(
    project: str,
    task_id: str,
    task: str,
    kind: str = "run",
    inputs: dict = None,
    outputs: list = None,
    parameters: dict = None,
    local: bool = False,
) -> Run:
    """
    Create run.

    Parameters
    ----------
    project : str
        Name of the project associated with the run.
    task_id : str
        Identifier of the task associated with the run.
    task : str
        Name of the task associated with the run.
    kind : str, optional
        The type of the run.
    inputs : dict, optional
        Inputs of the run.
    outputs : list, optional
        Outputs of the run.
    parameters : dict, optional
        Parameters of the run.
    local : bool, optional
        Flag to determine if object has local execution.
    embedded : bool, optional
        Flag to determine if object must be embedded in project.

    Returns
    -------
    Run
        Run object.
    """
    spec = build_spec(kind, inputs=inputs, outputs=outputs, parameters=parameters)
    return Run(
        project=project,
        task_id=task_id,
        task=task,
        kind=kind,
        spec=spec,
        local=local,
    )


def run_from_dict(obj: dict) -> Run:
    """
    Create run from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create run from.

    Returns
    -------
    Run
        Run object.

    """
    return Run.from_dict(obj)
