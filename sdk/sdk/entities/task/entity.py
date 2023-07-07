"""
Task module.
"""
from sdk.entities.base.entity import Entity
from sdk.entities.task.spec import TaskSpec
from sdk.utils.api import DTO_TASK, api_base_create, api_base_update
from sdk.utils.exceptions import BackendError, EntityError
from sdk.utils.factories import get_context
from sdk.utils.utils import get_uiid


class Task(Entity):
    """
    Task entity.
    """

    def __init__(
        self,
        kind: str,
        spec: TaskSpec,
        project: str,
        task: str,
        local: bool = False,
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
        task : str
            The task string.
        local : bool, optional
            Flag to indicate if the task is local or not.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.kind = kind if kind is not None else "task"
        self.spec = spec
        self.id = get_uiid()
        self.task = task

        self._local = local
        self._obj_attr += ["task"]

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

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
            api = api_base_update(DTO_TASK, self.id)
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
        filename = filename if filename is not None else f"task_{self.id}.yaml"
        self._export_object(filename, obj)

    #############################
    #  Task methods
    #############################

    def run(self, task_id: str, inputs: dict, outputs: dict, parameters: dict) -> dict:
        """
        Run task.

        Parameters
        ----------
        task_id : str
            The task id.


        **kwargs
            Additional keyword arguments.

        Returns
        -------
        Run
            Run object.

        """
        if self._local:
            raise EntityError("Use .run_local() for local execution.")

        # Create run
        run = {
            "task_id": task_id,
            "spec": {
                "inputs": inputs,
                "outputs": outputs,
                "parameters": parameters,
            },
        }

        api = api_base_create("runs")
        run_obj = self.context.client.create_object(run, api)

        return run_obj

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

        # Get spec
        spec = TaskSpec.from_dict(obj.get("spec", {}))

        return cls(kind=kind, spec=spec, project=project, task=task)
