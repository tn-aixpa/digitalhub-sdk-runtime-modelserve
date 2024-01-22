"""
Runtime nefertem module.
"""
from __future__ import annotations

import os
import shutil
import typing
from pathlib import Path
from typing import Callable

from digitalhub_core.entities._base.status import State
from digitalhub_core.entities.artifacts.crud import get_artifact_from_key, new_artifact
from digitalhub_core.entities.artifacts.utils import (
    calculate_blob_hash,
    get_artifact_info,
    get_file_extension,
    get_file_mime_type,
    get_file_size,
)
from digitalhub_core.entities.dataitems.crud import get_dataitem
from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.runtimes.results import RunResults
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import build_uuid
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data_nefertem.runtime.nefertem_utils import (
    create_client,
    create_nt_resources,
    create_nt_run_config,
    select_function,
)

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_core.entities.dataitems.entity import Dataitem
    from nefertem.client.client import Client


BUCKET = os.getenv("S3_BUCKET_NAME")


class RuntimeNefertem(Runtime):
    """
    Runtime nefertem class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.output_path = "/tmp/nefertem_run"
        self.store = {"name": "local", "store_type": "local"}
        self.nt_id = build_uuid()

    def build(self, function: dict, task: dict, run: dict) -> dict:
        """
        Merge specs.
        """
        return {
            **function.get("spec", {}),
            **task.get("spec", {}),
            **run.get("spec", {}),
        }

    def run(self, run: dict) -> dict:
        """
        Run function.

        Returns
        -------
        dict
            Status of the executed run.
        """
        # Get action
        action = self._get_action(run)

        # Handle unknown task kind
        if action not in ["validate", "profile", "infer", "metric"]:
            msg = f"Task {action} not allowed for nefertem runtime."
            LOGGER.error(msg)
            raise EntityError(msg)

        # Execute action
        return self.execute(action, run)

    def results(self, run_status: dict) -> RunResults:
        """
        Get run results.

        Returns
        -------
        RunResults
            Run results.
        """
        artifacts = run_status.get("artifacts", [])
        artifact_objs = [get_artifact_from_key(art.get("id")) for art in artifacts]
        return RunResults(artifact_objs)

    ####################
    # Execute
    ####################

    def execute(self, action: str, run: dict) -> dict:
        """
        Execute function.

        Returns
        -------
        dict
            Status of the executed run.
        """
        # Get run specs
        LOGGER.info("Starting task.")
        spec = run.get("spec")
        project = run.get("project")

        # Collect inputs
        LOGGER.info("Collecting inputs.")
        inputs = self._collect_inputs(spec.get("inputs", {}).get("dataitems", []), project)

        # Get nefertem configuration and function
        LOGGER.info("Creating nefertem configuration.")
        parameters = self._generate_nefertem_config(inputs, spec, action)
        func = self._select_function(action)

        # Execute function
        LOGGER.info("Executing nefertem run.")
        results: dict = self._execute(func, **parameters)

        # Collect outputs
        LOGGER.info("Collecting outputs.")
        outputs = self._collect_outputs(results, project, self.nt_id)

        # Remove tmp folder
        LOGGER.info("Removing tmp folder.")
        self.cleanup()

        # Return run status
        LOGGER.info("Task completed, returning run status.")
        return {
            "state": State.COMPLETED.value,
            "artifacts": [get_artifact_info(i[0]) for i in outputs],
            "nefertem_result": results,
            "timings": {
                "start_time": results.get("started"),
                "end_time": results.get("finished"),
            },
        }

    ####################
    # Inputs
    ####################

    def _collect_inputs(self, inputs: list, project: str) -> list[dict]:
        """
        Materialize inputs in postgres.

        Parameters
        ----------
        inputs : list
            The list of inputs dataitems names.
        project : str
            The project name.

        Returns
        -------
        list[dict]
            The list of inputs dataitems.
        """
        Path(f"{self.output_path}/tmp").mkdir(parents=True, exist_ok=True)

        mapper = []
        for name in inputs:
            dataitem = self._get_dataitem(name, project)
            mapper.append(self._persist_dataitem(dataitem, name))
        return mapper

    def _get_dataitem(self, name: str, project: str) -> Dataitem:
        """
        Get dataitem from backend.

        Parameters
        ----------
        name : str
            The dataitem name.
        project : str
            The project name.

        Returns
        -------
        dict
            The dataitem.

        Raises
        ------
        BackendError
            If the dataitem cannot be retrieved.
        """
        try:
            LOGGER.info(f"Getting dataitem '{name}'.")
            return get_dataitem(project, name)
        except Exception:
            msg = f"Error getting dataitem '{name}'."
            LOGGER.exception(msg)
            raise RuntimeError(msg)

    def _persist_dataitem(self, dataitem: Dataitem, name: str) -> dict:
        """
        Persist dataitem locally.

        Parameters
        ----------
        dataitem : Dataitem
            The dataitem to persist.
        name : str
            The dataitem name.

        Returns
        -------
        dict
            The dataitem path.

        Raises
        ------
        EntityError
            If the dataitem cannot be persisted.
        """
        try:
            LOGGER.info(f"Persisting dataitem '{name}' locally.")
            tmp_path = f"{self.output_path}/tmp/{name}.csv"
            dataitem.as_df().to_csv(tmp_path, sep=",", index=False)
            return {"name": name, "path": tmp_path}
        except Exception:
            msg = f"Error during dataitem '{name}' collection."
            LOGGER.exception(msg)
            raise EntityError(msg)

    ####################
    # Configuration
    ####################

    def _generate_nefertem_config(self, inputs: list[dict], spec: dict, action: str) -> tuple[Callable, dict]:
        """
        Generate nefertem configuration.

        Parameters
        ----------
        inputs : list
            The list of inputs dataitems.
        spec : dict
            Run spec.
        action : str
            Action to execute.

        Returns
        -------
        tuple
            Function to execute and its parameters.
        """
        # Create resources
        resources = self._create_nt_resources(inputs, self.store)

        # Create run configuration
        run_config = self._create_nt_run_config(action, spec)

        # Create Nefertem client
        client = self._create_client(self.output_path, self.store)

        # Return parameters
        return {
            "client": client,
            "resources": resources,
            "run_config": run_config,
            "run_id": self.nt_id,
            "metrics": spec.get("metrics"),
            "constraints": spec.get("constraints"),
            "error_report": spec.get("error_report"),
        }

    def _create_client(self, output_path: str, store: dict) -> Client:
        """
        Create Nefertem client.

        Parameters
        ----------
        output_path : str
            Output path where to store Nefertem results.
        store : dict
            Store configuration.

        Returns
        -------
        Client
            Nefertem client.
        """
        try:
            return create_client(output_path, store)
        except Exception:
            msg = "Error. Nefertem client cannot be created."
            LOGGER.exception(msg)
            raise EntityError(msg)

    def _create_nt_resources(self, inputs: list[dict], store: dict) -> list[dict]:
        """
        Create non-terminating resources.

        Parameters
        ----------
        inputs : list
            The list of inputs dataitems.
        store : dict
            The store configuration.

        Returns
        -------
        list[dict] :
            List of nefertem resources.
        """
        try:
            return create_nt_resources(inputs, store)
        except KeyError:
            msg = "Error. Dataitem path is not given."
            LOGGER.exception(msg)
            raise EntityError(msg)

    def _create_nt_run_config(self, action: str, spec: dict) -> dict:
        """
        Create nefertem run configuration.

        Parameters
        ----------
        action : str
            Action to execute.
        spec : dict
            Run spec.

        Returns
        -------
        dict
            The nefertem run configuration.
        """
        return create_nt_run_config(action, spec)

    def _select_function(self, action: str) -> Callable:
        """
        Select function according to action.

        Parameters
        ----------
        action : str
            Action to execute.

        Returns
        -------
        Callable
            Function to execute.
        """
        return select_function(action)

    ####################
    # Outputs
    ####################

    def _collect_outputs(self, results: dict, project: str, run_id: str) -> list[Artifact]:
        """
        Collect outputs.

        Parameters
        ----------
        results : dict
            The nefertem run results.
        project : str
            The project name.
        run_id : str
            Neferetem run id.

        Returns
        -------
        list
            List of artifacts paths.
        """
        output_files = results.get("output_files", [])

        LOGGER.info("Creating artifacts.")
        artifacts = [self._create_artifact(i, project, run_id) for i in output_files]

        LOGGER.info("Uploading artifacts to minio.")
        [self._upload_artifact(*i) for i in artifacts]

        return artifacts

    def _create_artifact(self, src_path: str, project: str, run_id: str) -> tuple[Artifact, str]:
        """
        Create new artifact in backend.

        Parameters
        ----------
        src_path : str
            The artifact source local path.
        project : str
            The project name.
        run_id : str
            Neferetem run id.

        Returns
        -------
        Artifact
            DHCore artifact and its src_path.
        """

        try:
            name = Path(src_path).stem.replace("_", "-")
            LOGGER.info(f"Creating new artifact '{name}'.")
            kwargs = {}
            kwargs["project"] = project
            kwargs["name"] = name
            kwargs["kind"] = "artifact"
            kwargs["target_path"] = f"s3://{BUCKET}/{project}/artifacts/ntruns/{run_id}/{Path(src_path).name}"
            kwargs["hash"] = calculate_blob_hash(src_path)
            kwargs["size"] = get_file_size(src_path)
            kwargs["file_type"] = get_file_mime_type(src_path)
            kwargs["file_extension"] = get_file_extension(src_path)
            return new_artifact(**kwargs), src_path
        except Exception:
            msg = f"Error creating artifact '{name}'."
            LOGGER.exception(msg)
            raise EntityError(msg)

    @staticmethod
    def _upload_artifact(artifact: Artifact, src_path: str) -> None:
        """
        Upload artifact to minio.

        Parameters
        ----------
        name : str
            The artifact name.
        artifact : Artifact
            The artifact to upload.
        src_path : str
            The artifact source local path.

        Returns
        -------
        None
        """
        try:
            LOGGER.info(f"Uploading artifact '{artifact.name}' to minio.")
            artifact.upload(source=src_path)
        except Exception:
            msg = f"Error uploading artifact '{artifact.name}'."
            LOGGER.exception(msg)
            raise EntityError(msg)

    ####################
    # Cleanup
    ####################

    def cleanup(self) -> None:
        """
        Cleanup after run.

        Returns
        -------
        None
        """
        shutil.rmtree(f"{self.output_path}/tmp", ignore_errors=True)
