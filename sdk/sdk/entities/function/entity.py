"""
Function module.
"""
from __future__ import annotations

import typing

from sdk.context.factory import get_context
from sdk.entities.base.entity import Entity
from sdk.entities.base.metadata import build_metadata
from sdk.entities.base.status import build_status
from sdk.entities.function.kinds import build_kind
from sdk.entities.function.spec.builder import build_spec
from sdk.entities.task.crud import create_task, delete_task, new_task
from sdk.runtimes.factory import get_runtime
from sdk.utils.api import DTO_FUNC, api_ctx_create, api_ctx_update
from sdk.utils.exceptions import EntityError
from sdk.utils.generic_utils import get_uiid

if typing.TYPE_CHECKING:
    from sdk.entities.base.metadata import Metadata
    from sdk.entities.base.status import Status
    from sdk.entities.function.spec.objects.base import FunctionSpec
    from sdk.entities.run.entity import Run
    from sdk.entities.task.entity import Task


class Function(Entity):
    """
    A class representing a function.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str | None = None,
        metadata: Metadata | None = None,
        spec: FunctionSpec | None = None,
        status: Status | None = None,
        local: bool = False,
        embedded: bool = True,
        uuid: str | None = None,
    ) -> None:
        """
        Initialize the Function instance.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the object.
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        metadata : Metadata
            Metadata of the object.
        spec : FunctionSpec
            Specification of the object.
        status : Status
            State of the object.
        local: bool
            If True, export locally.
        embedded: bool
            If True, embed object in backend.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.id = get_uiid(uuid=uuid)
        self.kind = kind if kind is not None else build_kind()
        self.metadata = metadata if metadata is not None else build_metadata(name=name)
        self.spec = spec if spec is not None else build_spec(self.kind, **{})
        self.status = status if status is not None else build_status()
        self.embedded = embedded

        # Private attributes
        self._local = local
        self._tasks: dict[str, Task] = {}
        self._context = get_context(self.project)

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str | None = None) -> dict:
        """
        Save function into backend.

        Parameters
        ----------
        uuid : str
            Specify uuid for the function update

        Returns
        -------
        dict
            Mapping representation of Function from backend.
        """
        if self._local:
            raise EntityError("Use .export() for local execution.")

        obj = self.to_dict(include_all_non_private=True)

        if uuid is None:
            api = api_ctx_create(self.project, DTO_FUNC)
            return self._context.create_object(obj, api)

        self.id = uuid
        api = api_ctx_update(self.project, DTO_FUNC, self.name, uuid)
        return self._context.update_object(obj, api)

    def export(self, filename: str | None = None) -> None:
        """
        Export object as a YAML file.

        Parameters
        ----------
        filename : str
            Name of the export YAML file. If not specified, the default value is used.

        Returns
        -------
        None
        """
        obj = self.to_dict()
        filename = (
            filename
            if filename is not None
            else f"function_{self.project}_{self.name}.yaml"
        )
        self._export_object(filename, obj)

    #############################
    #  Function Methods
    #############################

    def run(
        self,
        action: str,
        resources: dict | None = None,
        image: str | None = None,
        base_image: str | None = None,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        local_execution: bool = False,
    ) -> Run:
        """
        Run function.

        Parameters
        ----------
        action : str
            Action to execute. Task parameter.
        resources : dict
            K8s resource. Task parameter.
        image : str
            Output image name. Task parameter.
        base_image : str
            Base image name. Task parameter.
        inputs : dict
            Function inputs. Run parameter.
        outputs : dict
            Function outputs. Run parameter.
        parameters : dict
            Function parameters. Run parameter.
        local_execution : bool
            Flag to determine if object has local execution. Run parameter.
        Returns
        -------
        Run
            Run instance.
        """

        # Create task if not exists
        task = self._tasks.get(action)
        if task is None:
            task = self.new_task(
                kind=action,
                resources=resources,
                image=image,
                base_image=base_image,
            )

        # Run function from task
        run = task.run(inputs, outputs, parameters, local_execution)

        # If local execution, merge spec and run locally
        if local_execution:
            run.merge(self.to_dict(), task.to_dict())
            runtime = get_runtime(run)
            return runtime.run()

        # otherwise, return run launched by backend
        return run

    def _get_function_string(self) -> str:
        """
        Get function string.

        Returns
        -------
        str
            Function string.
        """
        return f"{self.kind}://{self.project}/{self.name}:{self.id}"

    #############################
    #  CRUD Methods for Tasks
    #############################

    def new_task(self, **kwargs) -> Task:
        """
        Create new task.

        Parameters
        ----------
        **kwargs
            Keyword arguments.

        Returns
        -------
        Task
            New task.
        """
        kwargs["project"] = self.project
        kwargs["function"] = self._get_function_string()
        kwargs["local"] = self._local
        task = new_task(**kwargs)
        self._tasks[kwargs["kind"]] = task
        return task

    def update_task(self, kind: str, **kwargs) -> None:
        """
        Update task.

        Parameters
        ----------
        kind : str
            Kind of the task.
        **kwargs
            Keyword arguments.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If task does not exist.
        """
        self._raise_if_not_exists(kind)

        # Update kwargs
        kwargs["project"] = self.project
        kwargs["kind"] = kind
        kwargs["function"] = self._get_function_string()
        kwargs["local"] = self._local
        kwargs["uuid"] = self._tasks[kind].id

        # Update task
        task = create_task(**kwargs)
        task.save(kwargs["uuid"])
        self._tasks[kind] = task

    def get_task(self, kind: str) -> Task:
        """
        Get task.

        Parameters
        ----------
        kind : str
            Kind of the task.

        Returns
        -------
        Task
            Task.

        Raises
        ------
        EntityError
            If task is not created.
        """
        self._raise_if_not_exists(kind)
        return self._tasks[kind]

    def delete_task(self, kind: str) -> None:
        """
        Delete task.

        Parameters
        ----------
        kind : str
            Kind of the task.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If task is not created.
        """
        self._raise_if_not_exists(kind)
        delete_task(self.project, self._tasks[kind].name)
        self._tasks[kind] = None

    def _raise_if_not_exists(self, kind: str) -> None:
        """
        Raise error if task is not created.

        Parameters
        ----------
        kind : str
            Kind of the task.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If task does not exist.
        """
        if self._tasks.get(kind) is None:
            raise EntityError("Task does not exist.")

    #############################
    #  Getters and Setters
    #############################

    @property
    def local(self) -> bool:
        """
        Get local flag.

        Returns
        -------
        bool
            Local flag.
        """
        return self._local

    #############################
    #  Generic Methods
    #############################

    @classmethod
    def from_dict(cls, obj: dict) -> "Function":
        """
        Create object instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        Function
            Self instance.
        """
        parsed_dict = cls._parse_dict(obj)
        _obj = cls(**parsed_dict)
        _obj._local = _obj._context.local
        return _obj

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
        name = obj.get("name")
        if project is None or name is None:
            raise EntityError("Project or name are not specified.")

        # Optional fields
        uuid = obj.get("id")
        kind = obj.get("kind")
        kind = build_kind(kind)
        embedded = obj.get("embedded")

        # Build metadata, spec, status
        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(kind=kind, **spec)
        metadata = obj.get("metadata", {"name": name})
        metadata = build_metadata(**metadata)
        status = obj.get("status")
        status = status if status is not None else {}
        status = build_status(**status)

        return {
            "project": project,
            "name": name,
            "kind": kind,
            "uuid": uuid,
            "metadata": metadata,
            "spec": spec,
            "status": status,
            "embedded": embedded,
        }


def function_from_parameters(
    project: str,
    name: str,
    description: str = "",
    kind: str | None = None,
    source: str | None = None,
    image: str | None = None,
    tag: str | None = None,
    handler: str | None = None,
    command: str | None = None,
    requirements: list | None = None,
    sql: str | None = None,
    local: bool = False,
    embedded: bool = True,
    uuid: str | None = None,
    **kwargs,
) -> Function:
    """
    Create function.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        Identifier of the Function.
    description : str
        Description of the Function.
    kind : str
        The type of the Function.
    source : str
        Path to the Function's source code on the local file system.
    image : str
        Name of the Function's container image.
    tag : str
        Tag of the Function's container image.
    handler : str
        Function handler name.
    command : str
        Command to run inside the container.
    requirements : list
        List of requirements for the Function.
    sql : str
        SQL query.
    local : bool
        Flag to determine if object will be exported to backend.
    embedded : bool
        Flag to determine if object must be embedded in project.
    uuid : str
        UUID.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Function
        Function object.
    """
    kind = build_kind(kind)
    spec = build_spec(
        kind,
        source=source,
        image=image,
        tag=tag,
        handler=handler,
        command=command,
        requirements=requirements,
        sql=sql,
        **kwargs,
    )
    meta = build_metadata(name=name, description=description)
    return Function(
        project=project,
        name=name,
        kind=kind,
        metadata=meta,
        spec=spec,
        local=local,
        embedded=embedded,
        uuid=uuid,
    )


def function_from_dict(obj: dict) -> Function:
    """
    Create function from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create function from.

    Returns
    -------
    Function
        Function object.
    """
    return Function.from_dict(obj)
