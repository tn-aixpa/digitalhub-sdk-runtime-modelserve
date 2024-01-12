"""
Runtime Nefertem module.
"""
from __future__ import annotations

import os
import shutil
import typing
from pathlib import Path

import nefertem
from digitalhub_core.entities._base.status import State
from digitalhub_core.entities.artifacts.crud import new_artifact
from digitalhub_core.entities.artifacts.utils import (
    calculate_blob_hash,
    get_artifact_info,
    get_file_extension,
    get_file_mime_type,
    get_file_size,
)
from digitalhub_core.entities.dataitems.crud import get_dataitem
from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import build_uuid
from digitalhub_core.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_core.entities.dataitems.entity import Dataitem
    from nefertem.client.client import Client


BUCKET = os.getenv("S3_BUCKET_NAME")


class RuntimeNefertem(Runtime):
    """
    Runtime Nefertem class.
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
            msg = f"Task {action} not allowed for Nefertem runtime"
            LOGGER.error(msg)
            raise EntityError(msg)

        # Execute action
        return self.execute(action, run)

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

        # Get inputs and parameters
        LOGGER.info("Getting inputs and parameters.")
        inputs = self._get_inputs(spec.get("inputs", {}).get("dataitems", []), project)
        resources = self._get_resources(inputs)
        run_config = self._get_run_config(action, spec)

        # Create client
        client = nefertem.create_client(output_path=self.output_path)
        try:
            client.add_store(self.store)
        except nefertem.utils.exceptions.StoreError:
            pass

        # Operation to execute
        LOGGER.info("Executing nefertem run.")

        if action == "infer":
            nt_run = self.infer(client, resources, run_config, self.nt_id)

        elif action == "profile":
            nt_run = self.profile(client, resources, run_config, self.nt_id)

        elif action == "validate":
            constraints = spec.get("constraints")
            error_report = spec.get("error_report")
            nt_run = self.validate(client, resources, run_config, self.nt_id, constraints, error_report)

        elif action == "metric":
            metrics = spec.get("metrics")
            nt_run = self.metric(client, resources, run_config, self.nt_id, metrics)

        # Create artifacts
        LOGGER.info("Creating artifacts.")
        artifacts = [self._create_artifact(i, project, self.nt_id) for i in nt_run.get("output_files", [])]

        # Upload outputs
        LOGGER.info("Uploading artifacts to minio.")
        for i in artifacts:
            self._upload_artifact(*i)

        # Remove tmp folder
        LOGGER.info("Removing tmp folder.")
        self.cleanup()

        # Return run status
        LOGGER.info("Task completed, returning run status.")
        return {
            "state": State.COMPLETED.value,
            "artifacts": [get_artifact_info(i[0]) for i in artifacts],
            "timings": {
                "start_time": nt_run.get("started"),
                "end_time": nt_run.get("finished"),
            },
        }

    ####################
    # INFER TASK
    ####################

    @staticmethod
    def infer(
        client: Client,
        resources: list[dict],
        run_config: dict,
        run_id: str,
    ) -> dict:
        """
        Execute infer task.

        Parameters
        ----------
        client : Client
            Nefertem client.
        resources : list[dict]
            The list of nefertem resources.
        run_config : dict
            The nefertem run configuration.
        run_id : str
            The nefertem run id.

        Returns
        -------
        dict
            Nefertem run info.
        """
        with client.create_run(resources, run_config, run_id=run_id) as nt_run:
            nt_run.infer()
            nt_run.log_schema()
            nt_run.persist_schema()
        return nt_run.run_info.to_dict()

    ####################
    # PROFILE TASK
    ####################

    @staticmethod
    def profile(
        client: Client,
        resources: list[dict],
        run_config: dict,
        run_id: str,
    ) -> dict:
        """
        Execute profile task.

        Parameters
        ----------
        client : Client
            Nefertem client.
        resources : list[dict]
            The list of nefertem resources.
        run_config : dict
            The nefertem run configuration.
        run_id : str
            The nefertem run id.

        Returns
        -------
        dict
            Nefertem run info.
        """
        with client.create_run(resources, run_config, run_id=run_id) as nt_run:
            nt_run.profile()
            nt_run.log_profile()
            nt_run.persist_profile()
        return nt_run.run_info.to_dict()

    ####################
    # VALIDATE TASK
    ####################

    @staticmethod
    def validate(
        client: Client,
        resources: list[dict],
        run_config: dict,
        run_id: str,
        constraints: list[dict],
        error_report: str | None = None,
    ) -> dict:
        """
        Execute validate task.

        Parameters
        ----------
        client : Client
            Nefertem client.
        resources : list[dict]
            The list of nefertem resources.
        run_config : dict
            The nefertem run configuration.
        run_id : str
            The nefertem run id.
        constraints : list[dict]
            The list of nefertem constraints.
        error_report : str
            The error report modality.

        Returns
        -------
        dict
            Nefertem run info.

        Raises
        ------
        RuntimeError
            If no constraints are given.
        """
        if constraints is None:
            msg = "Error. No constraints given."
            LOGGER.error(msg)
            raise RuntimeError(msg)
        if error_report is None:
            error_report = "partial"

        with client.create_run(resources, run_config, run_id=run_id) as nt_run:
            nt_run.validate(constraints=constraints, error_report=error_report)
            nt_run.log_report()
            nt_run.persist_report()
        return nt_run.run_info.to_dict()

    ####################
    # METRIC TASK
    ####################

    @staticmethod
    def metric(
        client: Client,
        resources: list[dict],
        run_config: dict,
        run_id: str,
        metrics: list[dict],
    ) -> dict:
        """
        Execute metric task.

        Parameters
        ----------
        client : Client
            Nefertem client.
        resources : list[dict]
            The list of nefertem resources.
        run_config : dict
            The nefertem run configuration.
        run_id : str
            The nefertem run id.
        metrics : list[dict]
            The list of nefertem metrics.

        Returns
        -------
        dict
            Nefertem run info.

        Raises
        ------
        RuntimeError
            If no metrics are given.
        """
        if metrics is None:
            msg = "Error. No metrics given."
            LOGGER.error(msg)
            raise RuntimeError(msg)

        with client.create_run(resources, run_config, run_id=run_id) as nt_run:
            nt_run.metric(metrics=metrics)
            nt_run.log_metric()
            nt_run.persist_metric()
        return nt_run.run_info.to_dict()

    ####################
    # Inputs
    ####################

    def _get_inputs(self, inputs: list, project: str) -> list[dict]:
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

    def _get_resources(self, inputs: list[dict]) -> list[dict]:
        """
        Create nefertem resources.

        Parameters
        ----------
        inputs : list
            The list of inputs dataitems.

        Returns
        -------
        list[dict]
            The list of nefertem resources.
        """
        try:
            resources = []
            for i in inputs:
                res = {}
                res["name"] = i["name"]
                res["path"] = i["path"]
                res["store"] = self.store["name"]
                resources.append(res)
            return resources
        except KeyError:
            msg = "Error. Dataitem path is not given."
            LOGGER.exception(msg)
            raise EntityError(msg)

    @staticmethod
    def _get_run_config(action: str, spec: dict) -> dict:
        """
        Build nefertem run configuration.

        Parameters
        ----------
        spec : dict
            Run specification.

        Returns
        -------
        dict
            The nefertem run configuration.
        """
        if action == "infer":
            operation = "inference"
        elif action == "profile":
            operation = "profiling"
        elif action == "validate":
            operation = "validation"
        elif action == "metric":
            operation = "metric"
        run_config = {
            "operation": operation,
            "exec_config": [
                {
                    "framework": spec.get("framework"),
                    "exec_args": spec.get("exec_args", {}),
                }
            ],
            "parallel": spec.get("parallel", False),
            "num_worker": spec.get("num_worker", 1),
        }
        return run_config

    ####################
    # Outputs
    ####################

    def _parse_results(self, run_info: dict) -> tuple[list[str], str]:
        """
        Parse results from nefertem run.

        Parameters
        ----------
        run_info : dict
            The Nefertem run info.

        Returns
        -------
        tuple[list[str], str]
            List of artifacts paths and Nefertem run id.
        """
        artifact_paths = run_info.get("output_files", [])
        run_id = run_info.get("run_id")
        return artifact_paths, run_id

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
