"""
Runtime Nefertem module.
"""
from __future__ import annotations

import shutil
import typing
from pathlib import Path

import nefertem

from sdk.entities._base.status import State
from sdk.entities.artifacts.crud import new_artifact
from sdk.entities.dataitems.crud import get_dataitem
from sdk.runtimes.base import Runtime
from sdk.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from nefertem.run.run_info import RunInfo

####################
# Runtime
####################


class RuntimeNefertem(Runtime):
    """
    Runtime Nefertem class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.output_path = "./ntruns"
        self.store = {"name": "local", "store_type": "local"}

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

        # Execute action
        if action == "validate":
            return self.validate(run)
        if action == "profile":
            return self.profile(run)
        if action == "infer":
            return self.infer(run)
        if action == "metric":
            return self.metric(run)

        # Handle unknown task kind
        raise EntityError(f"Task {action} not allowed for runtime")

    ####################
    # INFER TASK
    ####################

    def infer(self, run: dict) -> dict:
        """
        Execute infer task.

        Returns
        -------
        dict
            Status of the executed run.
        """

        # Get run specs
        spec = run.get("spec")
        project = run.get("metadata").get("project")

        # Get inputs and parameters
        inputs = self._get_inputs(spec.get("inputs", {}).get("dataitems", []), project)

        resources = self._get_resources(inputs)
        run_config = spec.get("run_config")

        # Execute run
        client = nefertem.create_client(output_path=self.output_path, stores=[self.store])
        with client.create_run(resources, run_config) as nt_run:
            nt_run.infer()
            nt_run.log_schema()
            nt_run.persist_schema()

        # Upload outputs
        artifacts = self._upload_outputs(nt_run.run_info, project)

        # Remove tmp folder
        shutil.rmtree(f"{self.output_path}/tmp", ignore_errors=True)

        # Return run status
        return {
            "state": State.COMPLETED.value,
            **artifacts,
        }

    ####################
    # PROFILE TASK
    ####################

    def profile(self, run: dict) -> dict:
        """
        Execute profile task.

        Returns
        -------
        dict
            Status of the executed run.
        """

        # Get run specs
        spec = run.get("spec")
        project = run.get("metadata").get("project")

        # Get inputs and parameters
        inputs = self._get_inputs(spec.get("inputs", {}).get("dataitems", []), project)

        resources = self._get_resources(inputs)
        run_config = spec.get("run_config")

        # Execute run
        client = nefertem.create_client(output_path=self.output_path, stores=[self.store])
        with client.create_run(resources, run_config) as nt_run:
            nt_run.profile()
            nt_run.log_profile()
            nt_run.persist_profile()

        # Upload outputs
        artifacts = self._upload_outputs(nt_run.run_info, project)

        # Remove tmp folder
        shutil.rmtree(f"{self.output_path}/tmp", ignore_errors=True)

        # Return run status
        return {
            "state": State.COMPLETED.value,
            **artifacts,
        }

    ####################
    # VALIDATE TASK
    ####################

    def validate(self, run: dict) -> dict:
        """
        Execute validate task.

        Returns
        -------
        dict
            Status of the executed run.
        """

        # Get run specs
        spec = run.get("spec")
        project = run.get("metadata").get("project")

        # Get inputs and parameters
        inputs = self._get_inputs(spec.get("inputs", {}).get("dataitems", []), project)

        resources = self._get_resources(inputs)
        run_config = spec.get("run_config")
        constraints = spec.get("constraints")
        error_report = spec.get("error_report")

        # Execute run
        client = nefertem.create_client(output_path=self.output_path, stores=[self.store])
        with client.create_run(resources, run_config) as nt_run:
            nt_run.validate(constraints=constraints, error_report=error_report)
            nt_run.log_report()
            nt_run.persist_report()

        # Upload outputs
        artifacts = self._upload_outputs(nt_run.run_info, project)

        # Remove tmp folder
        shutil.rmtree(f"{self.output_path}/tmp", ignore_errors=True)

        # Return run status
        return {
            "state": State.COMPLETED.value,
            **artifacts,
        }

    ####################
    # METRIC TASK
    ####################

    def metric(self, run: dict) -> dict:
        """
        Execute metric task.

        Returns
        -------
        dict
            Status of the executed run.
        """

        # Get run specs
        spec = run.get("spec")
        project = run.get("metadata").get("project")

        # Get inputs and parameters
        inputs = self._get_inputs(spec.get("inputs", {}).get("dataitems", []), project)

        resources = self._get_resources(inputs)
        run_config = spec.get("run_config")
        metrics = spec.get("metrics")

        # Execute run
        client = nefertem.create_client(output_path=self.output_path, stores=[self.store])
        with client.create_run(resources, run_config) as nt_run:
            nt_run.metric(metrics=metrics)
            nt_run.log_metric()
            nt_run.persist_metric()

        # Upload outputs
        artifacts = self._upload_outputs(nt_run.run_info, project)

        # Remove tmp folder
        shutil.rmtree(f"{self.output_path}/tmp", ignore_errors=True)

        # Return run status
        return {
            "state": State.COMPLETED.value,
            **artifacts,
        }

    ####################
    # Helpers
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
            try:
                di = get_dataitem(project, name)
            except Exception:
                raise RuntimeError(f"Dataitem {name} not found in project {project}")
            tmp_path = f"{self.output_path}/tmp/{name}.csv"
            di.as_df().to_csv(tmp_path, sep=",", index=False)
            mapper.append({"name": name, "path": tmp_path})
        return mapper

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
        resources = []
        for i in inputs:
            res = {}
            res["name"] = i["name"]
            res["path"] = i["path"]
            res["store"] = self.store["name"]
            resources.append(res)
        return resources

    def _upload_outputs(self, run_info: RunInfo, project: str) -> dict:
        """
        Upload outputs as artifacts to minio.

        Parameters
        ----------
        run_info : dict
            The run info.
        project : str
            The project name.

        Returns
        -------
        dict
            List of artifacts.
        """
        artifacts = {
            "artifacts": [],
        }
        for file in run_info.output_files:
            dst = f"s3://{project}/artifacts/nefertem/{run_info.run_id}/{Path(file).name}"
            name = Path(file).stem
            artifact = new_artifact(project, name, "artifact", src_path=file, target_path=dst)
            artifact.upload()
            artifacts["artifacts"].append(
                {
                    "key": name,
                    "kind": "artifact",
                    "id": f"store://{project}/artifacts/artifact/{name}:{artifact.metadata.version}",
                }
            )
        return artifacts
