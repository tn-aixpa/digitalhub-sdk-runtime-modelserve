from __future__ import annotations

import time
import typing
from typing import Any

import requests
from digitalhub_core.entities._base.crud import (
    list_entity_api_base,
    list_entity_api_ctx,
    logs_api,
    read_entity_api_ctx,
    stop_api,
)
from digitalhub_core.entities._base.entity.unversioned import UnversionedEntity
from digitalhub_core.entities._base.state import State
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.registry.registry import registry
from digitalhub_core.runtimes.builder import build_runtime
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity.material import MaterialEntity
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities.run.spec import RunSpec
    from digitalhub_core.entities.run.status import RunStatus
    from digitalhub_core.runtimes.base import Runtime


class Run(UnversionedEntity):
    """
    A class representing a run.
    """

    ENTITY_TYPE = EntityTypes.RUN.value

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
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpec
        self.status: RunStatus

    ##############################
    #  Run Methods
    ##############################

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
        except EntityError:
            pass

        try:
            status = self._get_runtime().run(self.to_dict())
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

    def wait(self, log_info: bool = True) -> Run:
        """
        Wait for run to finish.

        Parameters
        ----------
        log_info : bool
            If True, log information.

        Returns
        -------
        Run
            Run object.
        """
        start = time.time()
        while True:
            if log_info:
                LOGGER.info(f"Waiting for run {self.id} to finish...")
            self.refresh()
            time.sleep(5)
            if self.status.state in [
                State.STOPPED.value,
                State.ERROR.value,
                State.COMPLETED.value,
            ]:
                if log_info:
                    current = time.time() - start
                    LOGGER.info(f"Run {self.id} finished in {current:.2f} seconds.")
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
            Results.
        """
        try:
            return self.status.get_results()
        except AttributeError:
            msg = f"Run of type {self.kind} has no results."
            raise EntityError(msg)

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
        try:
            return self.status.get_outputs(as_key=as_key, as_dict=as_dict)
        except AttributeError:
            msg = f"Run of type {self.kind} has no outputs."
            raise EntityError(msg)

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
        try:
            value_list = getattr(self.spec, "values", [])
            value_list = value_list if value_list is not None else []
            return self.status.get_values(value_list)
        except AttributeError:
            msg = f"Run of type {self.kind} has no values."
            raise EntityError(msg)

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
        return logs_api(self.project, self.ENTITY_TYPE, self.id)

    def stop(self) -> None:
        """
        Stop run.

        Returns
        -------
        None
        """
        if not self._context().local and not self.spec.local_execution:
            return stop_api(self.project, self.ENTITY_TYPE, self.id)
        try:
            self.status.stop()
        except AttributeError:
            return

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
        try:
            if not self._context().local and not self.spec.local_execution:
                local = False
            else:
                local = True
            if kwargs is None:
                kwargs = {}
            return self.status.invoke(local, **kwargs)
        except AttributeError:
            msg = f"Run of type {self.kind} has no invoke operation."
            raise EntityError(msg)

    ##############################
    #  Helpers
    ##############################

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
        """
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
        splitted = self.spec.task.split("/")
        exec_name = splitted[-1].split(":")[0]
        exec_id = splitted[-1].split(":")[1]
        return read_entity_api_ctx(
            exec_name,
            entity_type=entity_type,
            project=self.project,
            entity_id=exec_id,
        )

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
            tasks = list_entity_api_base(self._context().client, EntityTypes.TASK.value)
            for i in tasks:
                if i.get("spec").get("function") == exec_string:
                    return i
            raise EntityError("Task not found.")

        # Remote backend
        task_kind = self.spec.task.split("://")[0]
        params = {"function": exec_string, "kind": task_kind}
        return list_entity_api_ctx(self.project, EntityTypes.TASK.value, params=params)[0]
