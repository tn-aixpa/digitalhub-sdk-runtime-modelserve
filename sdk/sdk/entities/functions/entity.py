"""
Function module.
"""
from __future__ import annotations

import typing
from concurrent.futures import ThreadPoolExecutor

from sdk.context.builder import get_context
from sdk.entities.base.entity import Entity
from sdk.entities.builders.kinds import build_kind
from sdk.entities.builders.metadata import build_metadata
from sdk.entities.builders.spec import build_spec
from sdk.entities.builders.status import build_status
from sdk.entities.tasks.crud import create_task, delete_task, new_task
from sdk.utils.api import api_ctx_create, api_ctx_update
from sdk.utils.commons import FUNC
from sdk.utils.exceptions import EntityError
from sdk.utils.generic_utils import build_uuid

if typing.TYPE_CHECKING:
    from sdk.context.context import Context
    from sdk.entities.functions.metadata import FunctionMetadata
    from sdk.entities.functions.spec.objects.base import FunctionSpec
    from sdk.entities.functions.status import FunctionStatus
    from sdk.entities.runs.entity import Run
    from sdk.entities.tasks.entity import Task


class Function(Entity):
    """
    A class representing a function.
    """

    def __init__(
        self,
        uuid: str,
        kind: str,
        metadata: FunctionMetadata,
        spec: FunctionSpec,
        status: FunctionStatus,
    ) -> None:
        """
        Initialize the Function instance.

        Parameters
        ----------
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        metadata : FunctionMetadata
            Metadata of the object.
        spec : FunctionSpec
            Specification of the object.
        status : FunctionStatus
            State of the object.
        """
        super().__init__()

        self.id = uuid
        self.kind = kind
        self.metadata = metadata
        self.spec = spec
        self.status = status
        self._tasks: dict[str, Task] = {}

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
        obj = self.to_dict(include_all_non_private=True)

        # TODO: Remove this when backend is fixed
        obj["project"] = self.metadata.project
        obj["name"] = self.metadata.name
        obj["embedded"] = self.metadata.embedded

        if uuid is None:
            api = api_ctx_create(self.metadata.project, FUNC)
            return self._context().create_object(obj, api)

        self.id = uuid
        api = api_ctx_update(self.metadata.project, FUNC, self.metadata.name, uuid)
        return self._context().update_object(obj, api)

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
            else f"function_{self.metadata.project}_{self.metadata.name}.yaml"
        )
        self._export_object(filename, obj)

    #############################
    #  Context
    #############################

    def _context(self) -> Context:
        """
        Get context.

        Returns
        -------
        Context
            Context.
        """
        return get_context(self.metadata.project)

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

        # If execution is done by backend, return run
        if not local_execution:
            return run

        # If local execution, build run and run it
        run.build(local=True)
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = executor.submit(run.run, local=True)
        return result.result()

    def _get_function_string(self) -> str:
        """
        Get function string.

        Returns
        -------
        str
            Function string.
        """
        return f"{self.kind}://{self.metadata.project}/{self.metadata.name}:{self.id}"

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
        kwargs["project"] = self.metadata.project
        kwargs["function"] = self._get_function_string()
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
        kwargs["project"] = self.metadata.project
        kwargs["kind"] = kind
        kwargs["function"] = self._get_function_string()
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
        delete_task(self.metadata.project, self._tasks[kind].name)
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
        return cls(**parsed_dict)

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

        # Build UUID, kind, metadata, spec and status
        uuid = obj.get("id")
        uuid = build_uuid(uuid)

        kind = obj.get("kind")
        kind = build_kind(FUNC, kind)

        metadata = obj.get("metadata")
        metadata = (
            metadata
            if metadata is not None
            else {"project": project, "name": name, "version": uuid}
        )
        metadata = build_metadata(FUNC, **metadata)

        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(FUNC, kind=kind, **spec)

        status = obj.get("status")
        status = status if status is not None else {}
        status = build_status(FUNC, **status)

        return {
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
        }


def function_from_parameters(
    project: str,
    name: str,
    description: str | None = None,
    kind: str | None = None,
    source: str | None = None,
    image: str | None = None,
    tag: str | None = None,
    handler: str | None = None,
    command: str | None = None,
    arguments: list | None = None,
    requirements: list | None = None,
    sql: str | None = None,
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
    arguments : list
        List of arguments for the command.
    requirements : list
        List of requirements for the Function.
    sql : str
        SQL query.
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
    uuid = build_uuid(uuid)
    kind = build_kind(FUNC, kind)
    spec = build_spec(
        FUNC,
        kind,
        source=source,
        image=image,
        tag=tag,
        handler=handler,
        command=command,
        args=arguments,
        requirements=requirements,
        sql=sql,
        **kwargs,
    )
    metadata = build_metadata(
        FUNC,
        project=project,
        name=name,
        version=uuid,
        description=description,
        embedded=embedded,
    )
    status = build_status(FUNC)
    return Function(
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
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
