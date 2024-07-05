from __future__ import annotations

import typing

from digitalhub_core.context.builder import get_context
from digitalhub_core.entities._base.entity import Entity
from digitalhub_core.entities._base.status import State
from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.registry.registry import registry
from digitalhub_core.runtimes.builder import build_runtime
from digitalhub_core.utils.api import api_base_list, api_ctx_create, api_ctx_list, api_ctx_read, api_ctx_update
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import build_uuid, get_timestamp
from digitalhub_core.utils.io_utils import write_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.context.context import Context
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities.runs.spec import RunSpec
    from digitalhub_core.entities.runs.status import RunStatus
    from digitalhub_core.runtimes.base import Runtime


class Run(Entity):
    """
    A class representing a run.
    """

    ENTITY_TYPE = EntityTypes.RUNS.value

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpec,
        status: RunStatus,
        user: str | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        project : str
            Project name.
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        metadata : Metadata
            Metadata of the object.
        spec : RunSpec
            Specification of the object.
        status : RunStatus
            Status of the object.
        user : str
            Owner of the object.
        """
        super().__init__()
        self.project = project
        self.id = uuid
        self.kind = kind
        self.key = f"store://{project}/{self.ENTITY_TYPE}/{kind}/{uuid}"
        self.metadata = metadata
        self.spec = spec
        self.status = status
        self.user = user

        # Add attributes to be used in the to_dict method
        self._obj_attr.extend(["project", "id", "key"])

    #############################
    #  Save / Refresh / Export
    #############################

    def save(self, update: bool = False) -> Run:
        """
        Save entity into backend.

        Parameters
        ----------
        update : bool
            If True, the object will be updated.

        Returns
        -------
        Run
            Entity saved.
        """
        obj = self.to_dict(include_all_non_private=True)

        if not update:
            api = api_ctx_create(self.project, self.ENTITY_TYPE)
            new_obj = self._context().create_object(api, obj)
            self._update_attributes(new_obj)
            return self

        self.metadata.updated = obj["metadata"]["updated"] = get_timestamp()
        api = api_ctx_update(self.project, self.ENTITY_TYPE, self.id)
        new_obj = self._context().update_object(api, obj)
        self._update_attributes(new_obj)
        return self

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
        if filename is None:
            filename = f"{self.kind}_{self.name}_{self.id}.yml"
        pth = self._context().root / filename
        pth.parent.mkdir(parents=True, exist_ok=True)
        write_yaml(pth, obj)

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
        return get_context(self.project)

    #############################
    #  Run Methods
    #############################

    def build(self) -> None:
        """
        Build run.

        Returns
        -------
        None
        """
        runtime = self._get_runtime()
        executable = self._get_executable(runtime)
        task = self._get_task(runtime)
        new_spec = runtime.build(executable, task, self.to_dict())
        self.spec = build_spec(
            self.kind,
            **new_spec,
        )
        self._set_state(State.BUILT.value)
        self.save()

    def run(self) -> Run:
        """
        Run run.

        Returns
        -------
        Run
            Run object.
        """
        self.refresh()
        if self.spec.local_execution:
            if not self._is_built():
                raise EntityError("Run is not in built state. Build it again.")
            self._set_state(State.RUNNING.value)
            self.save(update=True)

        # Try to get inputs if they exist
        try:
            self.spec.inputs = self.inputs(as_dict=True)
        except Exception:
            pass

        try:
            status = self._get_runtime().run(self.to_dict(include_all_non_private=True))
        except Exception as e:
            self.refresh()
            if self.spec.local_execution:
                self._set_state(State.ERROR.value)
            self._set_message(str(e))
            self.save(update=True)
            raise e

        self.refresh()
        if not self.spec.local_execution:
            status.pop("state", None)
        new_status = {**self.status.to_dict(), **status}
        self._set_status(new_status)
        self.save(update=True)
        return self

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
        try:
            return self.spec.get_inputs(as_dict=as_dict)
        except AttributeError:
            msg = f"Run of type {self.kind} has no inputs."
            raise EntityError(msg)

    def results(self) -> dict:
        """
        Get results from runtime execution.

        Returns
        -------
        dict
            Results from backend.
        """
        try:
            return self.status.get_results()
        except AttributeError:
            msg = f"Run of type {self.kind} has no results."
            raise EntityError(msg)

    def outputs(self, as_key: bool = False, as_dict: bool = False) -> list:
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
        list
            List of output objects.
        """
        try:
            return self.status.get_outputs(as_key=as_key, as_dict=as_dict)
        except AttributeError:
            msg = f"Run of type {self.kind} has no outputs."
            raise EntityError(msg)

    def values(self) -> dict:
        """
        Get values from runtime execution.

        Returns
        -------
        dict
            Values from backend.
        """
        try:
            value_list = getattr(self.spec, "values", [])
            value_list = value_list if value_list is not None else []
            return self.status.get_values(value_list)
        except AttributeError:
            msg = f"Run of type {self.kind} has no values."
            raise EntityError(msg)

    def refresh(self) -> Run:
        """
        Refresh object from backend.

        Returns
        -------
        Run
            Run object.
        """
        api = api_ctx_read(self.project, self.ENTITY_TYPE, self.id)
        obj = self._context().read_object(api)
        self._update_attributes(obj)
        return self

    def logs(self) -> dict:
        """
        Get object from backend.
        Returns empty dictionary if context is local.

        Returns
        -------
        dict
            Logs from backend.
        """
        if self._context().local:
            return {}
        api = api_ctx_read(self.project, self.ENTITY_TYPE, self.id) + "/logs"
        return self._context().read_object(api)

    def stop(self) -> None:
        """
        Stop run.

        Returns
        -------
        None
        """
        # Do nothing if context is local
        if self._context().local:
            return
        api = api_ctx_create(self.project, self.ENTITY_TYPE) + f"/{self.id}/stop"
        self._context().create_object(api)
        self.status.state = State.STOPPED.value

    #############################
    #  Helpers
    #############################

    def _is_built(self) -> bool:
        """
        Check if run is in built state.

        Returns
        -------
        bool
            True if run is in built state, False otherwise.
        """
        return self.status.state == State.BUILT.value

    def _set_status(self, status: dict) -> None:
        """
        Set run status.

        Parameters
        ----------
        status : dict
            Status to set.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If status is not a dictionary or a Status object.
        """
        if not isinstance(status, dict):
            raise EntityError("Status must be a dictionary.")
        self.status: RunStatus = build_status(self.kind, **status)

    def _set_state(self, state: str) -> None:
        """
        Update run state.

        Parameters
        ----------
        state : str
            State to set.

        Returns
        -------
        None
        """
        self.status.state = state

    def _set_message(self, message: str) -> None:
        """
        Update run message.

        Parameters
        ----------
        message : str
            Message to set.

        Returns
        -------
        None
        """
        self.status.message = message

    def _get_runtime(self) -> Runtime:
        """
        Build runtime to build run or execute it.

        Returns
        -------
        Runtime
            Runtime object.
        """
        return build_runtime(self.kind, self.project)

    def _get_executable(self, runtime: Runtime) -> dict:
        """
        Get object from backend. Reimplemented to avoid circular imports.

        Parameters
        ----------
        runtime : Runtime
            Runtime object.

        Returns
        -------
        dict
            Executable (function or workflow) from backend.
        """
        exec_kind = runtime.get_executable_kind()
        entity_type = registry.get_entity_type(exec_kind)
        exec_id = self.spec.task.split(":")[-1]
        api = api_ctx_read(self.project, entity_type, exec_id)
        return self._context().read_object(api)

    def _get_task(self, runtime: Runtime) -> dict:
        """
        Get object from backend. Reimplemented to avoid circular imports.

        Parameters
        ----------
        runtime : Runtime
            Runtime object.

        Returns
        -------
        dict
            Task from backend.
        """
        executable_kind = runtime.get_executable_kind()
        exec_string = f"{executable_kind}://{self.spec.task.split('://')[1]}"

        # Local backend
        if self._context().local:
            api = api_base_list("tasks")
            tasks = self._context().list_objects(api)
            for i in tasks:
                if i.get("spec").get("function") == exec_string:
                    return i
            raise EntityError("Task not found.")

        # Remote backend
        task_kind = self.spec.task.split("://")[0]
        api = api_ctx_list(self.project, "tasks")
        params = {"function": exec_string, "kind": task_kind}
        obj = self._context().list_objects(api, params=params)
        return obj[0]

    #############################
    #  Static interface methods
    #############################

    @staticmethod
    def _parse_dict(obj: dict, validate: bool = True) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        entity : str
            Entity type.
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        project = obj.get("project")
        kind = obj.get("kind")
        uuid = build_uuid(obj.get("id"))
        metadata = build_metadata(kind, **obj.get("metadata", {}))
        spec = build_spec(kind, validate=validate, **obj.get("spec", {}))
        status = build_status(kind, **obj.get("status", {}))
        user = obj.get("user")
        return {
            "project": project,
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
            "user": user,
        }


def run_from_parameters(
    project: str,
    kind: str,
    uuid: str | None = None,
    source: str | None = None,
    labels: list[str] | None = None,
    **kwargs,
) -> Run:
    """
    Create run.

    Parameters
    ----------
    project : str
        Project name.
    kind : str
        Kind of the object.
    uuid : str
        ID of the object in form of UUID.
    source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Run
        Run object.
    """
    uuid = build_uuid(uuid)
    metadata = build_metadata(
        kind=kind,
        project=project,
        name=uuid,
        source=source,
        labels=labels,
    )
    spec = build_spec(kind, **kwargs)
    status = build_status(kind)
    return Run(
        project=project,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def run_from_dict(obj: dict) -> Run:
    """
    Create run from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Run
        Run object.
    """
    return Run.from_dict(obj)
