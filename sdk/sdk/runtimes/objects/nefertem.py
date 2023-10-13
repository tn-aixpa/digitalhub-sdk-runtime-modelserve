"""
Runtime Nefertem module.
"""
from sdk.entities.base.status import State
from sdk.entities.tasks.kinds import TaskKinds
from sdk.runtimes.objects.base import Runtime
from sdk.utils.exceptions import EntityError

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
        if action == TaskKinds.VALIDATE.value:
            return self.validate(run)
        if action == TaskKinds.PROFILE.value:
            return self.profile(run)
        if action == TaskKinds.INFER.value:
            return self.infer(run)

        raise EntityError(f"Task {action} not allowed for runtime")

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

        # Return run status
        return {
            "state": State.COMPLETED.value,
        }

    ####################
    # VALIDATE TASK
    ####################

    def profile(self, run: dict) -> dict:
        """
        Execute profile task.

        Returns
        -------
        dict
            Status of the executed run.
        """

        # Return run status
        return {
            "state": State.COMPLETED.value,
        }

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

        # Return run status
        return {
            "state": State.COMPLETED.value,
        }
