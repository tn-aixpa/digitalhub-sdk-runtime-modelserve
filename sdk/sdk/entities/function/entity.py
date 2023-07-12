"""
Function module.
"""
from __future__ import annotations

import typing
from typing import Self

from sdk.entities.base.entity import Entity
from sdk.entities.function.metadata import build_metadata
from sdk.entities.function.spec import build_spec
from sdk.entities.task.crud import new_task, create_task
from sdk.utils.api import DTO_FUNC, api_ctx_create, api_ctx_update
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context
from sdk.entities.utils.utils import get_uiid

if typing.TYPE_CHECKING:
    from sdk.entities.run.entity import Run
    from sdk.entities.function.metadata import FunctionMetadata
    from sdk.entities.function.spec import FunctionSpec


class Function(Entity):
    """
    A class representing a function.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str = None,
        metadata: FunctionMetadata = None,
        spec: FunctionSpec = None,
        local: bool = False,
        embedded: bool = False,
        uuid: str = None,
        **kwargs,
    ) -> None:
        """
        Initialize the Function instance.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the function.
        kind : str, optional
            Kind of the function.
        metadata : FunctionMetadata, optional
            Metadata for the function, default is None.
        spec : FunctionSpec, optional
            Specification for the function, default is None.
        local: bool, optional
            Specify if run locally, default is False.
        embedded: bool, optional
            Specify if embedded the function, default is False.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.kind = kind if kind is not None else "job"
        self.metadata = metadata if metadata is not None else build_metadata(name=name)
        self.spec = spec if spec is not None else build_spec(self.kind, **{})
        self.embedded = embedded
        self.id = uuid if uuid is not None else get_uiid()

        self._local = local

        # Set new attributes
        self._any_setter(**kwargs)

        self._context = get_context(self.project)
        self._task = None

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str = None) -> dict:
        """
        Save function into backend.

        Parameters
        ----------
        uuid : str, optional
            Specify uuid for the function update, default is None.

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
            else f"function_{self.project}_{self.name}.yaml"
        )
        self._export_object(filename, obj)

    #############################
    #  Function Methods
    #############################

    def run(
        self,
        inputs: dict = None,
        outputs: list = None,
        parameters: dict = None,
        k8s_resources: dict = None,
    ) -> Run:
        """
        Run function.

        Parameters
        ----------
        inputs : dict
            Function inputs. Used in Run.
        outputs : dict
            Function outputs. Used in Run.
        parameters : dict
            Function parameters. Used in Run.
        k8s_resources : dict
            K8s resource. Used in Task.

        Returns
        -------
        Run
            Run instance.
        """
        # Create task if not exists
        if self._task is None:
            # https://docs.mlrun.org/en/latest/runtimes/configuring-job-resources.html
            # task spec k8s
            task = f"{self.kind}://{self.project}/{self.name}:{self.id}"
            self._task = new_task(
                project=self.project,
                kind="task",
                task=task,
                k8s_resources=k8s_resources,
                local=self._local,
                uuid=self.id,
            )

        # Run function from task
        return self._task.run(inputs, outputs, parameters)

    def update_task(self, new_spec: dict) -> dict:
        """
        Update task.

        Parameters
        ----------
        new_spec : dict
            The new specification for the task.

        Returns
        -------
        dict
            Mapping representation of Task from backend.

        Raises
        ------
        EntityError
            If the task is not created.
        """
        if self._task is None:
            raise EntityError("Task is not created.")
        task_id = self._task.id
        task_kind = self._task.kind
        task_task = self._task.task
        self._task = create_task(
            project=self.project,
            kind=task_kind,
            task=task_task,
            k8s_resources=new_spec,
            local=self._local,
        )
        self._task.id = task_id
        return self._task.save(task_id)

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
        name = obj.get("name")
        if project is None or name is None:
            raise EntityError("Project or name are not specified.")

        # Optional fields
        uuid = obj.get("id")
        kind = obj.get("kind")
        embedded = obj.get("embedded")

        # Build metadata and spec
        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(kind=kind, **spec)
        metadata = obj.get("metadata", {"name": name})
        metadata = build_metadata(**metadata)

        return {
            "project": project,
            "name": name,
            "kind": kind,
            "uuid": uuid,
            "metadata": metadata,
            "spec": spec,
            "embedded": embedded,
        }


def function_from_parameters(
    project: str,
    name: str,
    description: str = "",
    kind: str = "job",
    source: str = None,
    image: str = None,
    tag: str = None,
    handler: str = None,
    command: str = None,
    requirements: list = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str = None,
) -> Function:
    """
    Create function.

    Parameters
    ----------
    project : str
        Name of the project associated with the function.
    name : str
        Identifier of the function.
    description : str, optional
        Description of the function.
    kind : str, optional
        The type of the function.
    key : str
        Representation of function like store://etc..
    src_path : str
        Path to the function on local file system or remote storage.
    targeth_path : str
        Destination path of the function.
    local : bool, optional
        Flag to determine if object has local execution.
    embedded : bool, optional
        Flag to determine if object must be embedded in project.
    uuid : str, optional
        UUID.

    Returns
    -------
    Function
        Function object.
    """
    meta = build_metadata(name=name, description=description)
    spec = build_spec(
        kind,
        source=source,
        image=image,
        tag=tag,
        handler=handler,
        command=command,
        requirements=requirements,
    )
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
