"""
Runtime MLRun module.
"""
from sdk.entities.base.status import State
from sdk.entities.tasks.kinds import TaskKinds
from sdk.runtimes.objects.base import Runtime
from sdk.utils.exceptions import EntityError

####################
# Runtime
####################


class RuntimeMLRun(Runtime):
    """
    Runtime MLRun class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """

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
        # Get action
        action = run.get("spec").get("task").split(":")[0].split("+")[1]

        # Execute action
        if action == TaskKinds.MLRUN.value:
            return self.mlrun(run)

        raise EntityError(f"Task {action} not allowed for runtime")

    ####################
    # MLRUN TASK
    ####################

    def mlrun(self, run: dict) -> dict:
        """
        Execute mlrun task.

        Returns
        -------
        dict
            Status of the executed run.
        """

        # Return run status
        return {
            "state": State.COMPLETED.value,
        }
