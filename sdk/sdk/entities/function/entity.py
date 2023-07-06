"""
Function module.
"""
from sdk.entities.base.entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.task.entity import Task, TaskSpec
from sdk.utils.api import DTO_FUNC, api_ctx_create, api_ctx_update
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context
from sdk.utils.utils import get_uiid


class FunctionMetadata(EntityMetadata):
    """
    Function metadata
    """


class FunctionSpec(EntitySpec):
    """
    Function specification.
    """

    def __init__(
        self,
        source: str = None,
        image: str = None,
        tag: str = None,
        handler: str = None,
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
        self.source = source
        self.image = image
        self.tag = tag
        self.handler = handler

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__:
                self.__setattr__(k, v)


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
        embed: bool = False,
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
        embed: bool, optional
            Specify if embed the function, default is False.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.kind = kind if kind is not None else "local"
        self.metadata = (
            metadata if metadata is not None else FunctionMetadata(name=name)
        )
        self.spec = spec if spec is not None else FunctionSpec()
        self.embedded = embed
        self.id = uuid if uuid is not None else get_uiid()

        self._local = local

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        self.context = get_context(self.project)
        self.task = None

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

        obj = self.to_dict()

        if uuid is None:
            api = api_ctx_create(self.project, DTO_FUNC)
            return self.context.client.create_object(obj, api)

        self.id = uuid
        api = api_ctx_update(self.project, DTO_FUNC, self.name, uuid)
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
            else f"function_{self.project}_{self.name}.yaml"
        )
        self._export_object(filename, obj)

    #############################
    #  Function Methods
    #############################

    def run(self, **kwargs) -> None:
        """
        Run function.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments.

        Returns
        -------
        Run
            Run instance.
        """
        # Create task if not exists
        if self.task is None:
            tasc_spec = TaskSpec.from_dict(self.spec.to_dict())
            self.task = Task(
                "task", tasc_spec, self.project, self.name, local=self._local
            )
            self.task.save()

        # Run function from task
        return self.task.run(**kwargs)

    def update_task(self, new_spec: dict) -> None:
        """
        Update task.

        Parameters
        ----------
        new_spec : dict
            The new specification for the task.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If the task is not created.
        """
        if self.task is None:
            raise EntityError("Task is not created.")
        self.task.spec = TaskSpec.from_dict(new_spec)
        self.task.save(self.task.task)

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
    def from_dict(cls, obj: dict) -> "Function":
        """
        Create Function instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create Function from.

        Returns
        -------
        Function
            Function instance.

        """
        project = obj.get("project")
        name = obj.get("name")
        uuid = obj.get("id")
        if project is None or name is None:
            raise EntityError("Project or name are not specified.")
        metadata = FunctionMetadata.from_dict(obj.get("metadata", {"name": name}))
        spec = FunctionSpec.from_dict(obj.get("spec", {}))
        return cls(project, name, metadata=metadata, spec=spec, uuid=uuid)
