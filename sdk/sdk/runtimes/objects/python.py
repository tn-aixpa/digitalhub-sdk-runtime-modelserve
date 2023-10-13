"""
Runtime Python module.
"""
from __future__ import annotations

import json
import subprocess
import typing
from pathlib import Path

from sdk.entities.artifacts.crud import new_artifact
from sdk.entities.artifacts.kinds import ArtifactKinds
from sdk.entities.base.status import State
from sdk.entities.tasks.kinds import TaskKinds
from sdk.runtimes.objects.base import Runtime
from sdk.utils.exceptions import EntityError
from sdk.utils.generic_utils import decode_string

if typing.TYPE_CHECKING:
    from sdk.entities.artifacts.entity import Artifact


####################
# Template
####################

FUNCTION_TEMPLATE = """
{}

if __name__ == "__main__":
    parameters = {}
    {}(**parameters)

"""


####################
# Runtime
####################


class RuntimePython(Runtime):
    """
    Runtime Python class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.root = Path("python_run")

    def build(self, function: dict, task: dict, run: dict) -> dict:
        """
        Merge specs.
        """
        return {
            **function.get("spec"),
            **task.get("spec"),
            **run.get("spec"),
        }

    def run(self, run: dict) -> dict:
        """
        Run function.

        Returns
        -------
        dict
            Status of the executed run.
        """
        # Verify if run is in pending state and task is allowed
        if not run.get("status").get("state") == State.PENDING.value:
            raise EntityError("Run is not in pending state. Build it again.")

        # Get action
        action = run.get("spec").get("task").split(":")[0].split("+")[1]

        # Execute action
        if action == TaskKinds.PYTHON.value:
            return self.python(run)

        raise EntityError(f"Task {action} not allowed for runtime")

    ####################
    # PYTHON TASK
    ####################

    def python(self, run: dict) -> dict:
        """
        Execute validate task.

        Returns
        -------
        dict
            Status of the executed run.
        """
        spec = run.get("spec")
        project = run.get("metadata").get("project")

        # Parse outputs and get parameters
        output = self.parse_outputs(spec.get("outputs", {}).get("artifacts", []))
        parameters = spec.get("parameters", {})

        # Setup environment
        path = self.setup(spec, parameters)

        # Execute python script
        result = self.execute(path)

        # Create artifact
        artifact = self.create_artifact(result, project, output)

        # Persist artifact
        artifact.upload()

        # Return run status
        return {
            **self._get_artifact_info(output, artifact),
            "state": State.COMPLETED.value,
        }

    ####################
    # Parse outputs
    ####################

    def parse_outputs(self, outputs: list) -> str:
        """
        Parse outputs from run spec.

        Parameters
        ----------
        outputs : list
            The list of outputs.

        Returns
        -------
        str
            The output artifact/table name.
        """
        return str(outputs[0])

    ####################
    # Setup
    ####################

    def setup(self, spec: dict, parameters: dict) -> Path:
        """
        Setup environment.

        Parameters
        ----------
        spec : dict
            The run spec.
        parameters : dict
            The parameters to pass to the script.

        Returns
        -------
        Path
            The path to the script file.
        """
        # Create root directory
        self.root.mkdir(parents=True, exist_ok=True)

        # Get script and save it
        code = spec.get("code")
        name = spec.get("handler")
        path = self.root / "script.py"
        text = FUNCTION_TEMPLATE.format(
            decode_string(code),
            json.dumps(parameters),
            name,
        )
        path.write_text(text)
        return path

    ####################
    # Execute
    ####################

    def execute(self, path: Path) -> Path:
        """
        Execute python script. Save stdout and stderr to file.

        Parameters
        ----------
        path : Path
            The path to the script file.

        Returns
        -------
        Path
            The path to the stdout file.
        """
        # Execute script
        filepath = self.root / "stdout.txt"
        with open(filepath, "w", encoding="utf-8") as stdout:
            subprocess.run(["python", str(path)], stdout=stdout, check=False)
        return filepath

    ####################
    # CRUD
    ####################

    def create_artifact(self, path: Path, project: str, output: str) -> Artifact | None:
        """
        Create new artifact.

        Parameters
        ----------
        path : Path
            The path to the stdout file.
        project : str
            The project name.
        output : str
            The output artifact name.

        Returns
        -------
        Artifact
            The artifact.
        """
        try:
            return new_artifact(
                project=project,
                name=output,
                kind=ArtifactKinds.ARTIFACT.value,
                src_path=str(path),
                target_path=f"s3://{project}/artifacts/{output}.txt",
            )
        except Exception:
            raise RuntimeError("Something got wrong during artifact creation.")

    @staticmethod
    def _get_artifact_info(output: str, artifact: Artifact) -> dict:
        """
        Create artifact info.

        Parameters
        ----------
        output : str
            The output table name.
        artifact : Artifact
            The artifact.
        """
        kind = artifact.kind
        project = artifact.metadata.project
        name = artifact.metadata.name
        version = artifact.id
        return {
            "artifacts": [
                {
                    "key": output,
                    "kind": kind,
                    "id": f"store://{project}/artifacts/{kind}/{name}:{version}",
                }
            ]
        }
