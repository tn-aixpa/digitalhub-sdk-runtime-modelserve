"""
Task module.
"""

from sdk.entities.base.entity import Entity, EntitySpec
from sdk.utils.api import DTO_TASK, api_base_update, api_base_create
from sdk.utils.exceptions import EntityError, BackendError
from sdk.utils.factories import get_context
from sdk.utils.uri_utils import get_uri_path


class TaskSpec(EntitySpec):
    """Task specification."""

    def __init__(
        self,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments.

        Notes
        -----
        If some of the attributes are not in the signature,
        they will be added as new attributes.
        """

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__:
                self.__setattr__(k, v)


class Task(Entity):
    """
    Task entity.
    """

    def __init__(
        self,
        kind: str,
        spec: TaskSpec,
        project: str,
        function: str,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        project : str
            Name of the project.
        kind : str
            The kind of the task.
        spec : TaskSpec
            The specification of the task.
        function : str
            The function of the task.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.kind = kind if kind is not None else "job"
        self.spec = spec
        self.function = function

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        self._local = kind == "local"

        self.task = f"{self.kind}://{self.project}/{self.function}"
        self.context = get_context(self.project)

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str = None) -> dict:
        """
        Save task into backend.

        Parameters
        ----------
        uuid : str, optional
            Ignore this parameter.

        Returns
        -------
        dict
            Mapping representation of Function from backend.

        """
        if self._local:
            raise EntityError("Use .export() for local execution.")

        obj = self.to_dict()

        try:
            api = api_base_create(DTO_TASK)
            return self.context.client.create_object(obj, api)
        except BackendError:
            api = api_base_update(DTO_TASK, self.task)
            return self.context.client.update_object(obj, api)

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
            else f"task_{self.project}_{self.function}.yaml"
        )
        self._export_object(filename, obj)

    #############################
    #  Task methods
    #############################

    def run(self, **kwargs) -> None:
        """
        Run task.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments.

        Returns
        -------
        Run
            Run object.

        """

    #############################
    # Generic Methods
    #############################

    @classmethod
    def from_dict(cls, obj: dict) -> "Task":
        """
        Create Task object from dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary representation of Task.

        Returns
        -------
        Task
            Task object.

        """
        project = obj.get("project")
        kind = obj.get("kind")
        if project is None or kind is None:
            raise EntityError("Project or kind is not specified.")

        # Parse task
        task = obj.get("task")
        if task is None:
            raise EntityError("Task is not specified.")
        function = get_uri_path(task)

        # Get spec
        spec = TaskSpec.from_dict(obj.get("spec", {}))

        return cls(kind=kind, spec=spec, project=project, function=function)
