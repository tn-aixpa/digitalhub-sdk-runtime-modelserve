"""
Run module.
"""
from sdk.entities.base.entity import Entity
from sdk.entities.run.spec import RunSpec
from sdk.utils.api import (DTO_RUNS, api_base_create, api_base_delete,
                           api_base_read)
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context


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
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.kind = "run"
        self.task_id = task_id
        self.spec = spec if spec is not None else RunSpec()

        self._local = local

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

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
    def from_dict(cls, obj: dict) -> "Run":
        """
        Create Run instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create Run from.

        Returns
        -------
        Run
            Run instance.

        """
        project = obj.get("project")
        task_id = obj.get("task_id")
        if project is None or task_id is None:
            raise EntityError("Project or task_id are not specified.")
        task = obj.get("task")
        spec = RunSpec.from_dict(obj.get("spec", {}))
        return cls(project, task_id, task=task, spec=spec)
