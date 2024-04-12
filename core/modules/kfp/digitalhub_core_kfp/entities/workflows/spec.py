"""
KFP pipeline Workflow specification module.
"""
from __future__ import annotations

from digitalhub_core_kfp.entities.functions.spec import FunctionSpecKFP, FunctionParamsKFP

class WorkflowSpecKFP(FunctionSpecKFP):
    """
    Specification for a Workflow pipeline.
    """

    def __init__(
        self,
        source: dict,
        image: str | None = None,
        tag: str | None = None,
        handler: str | None = None,
        command: str | None = None,
        requirements: list | None = None
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        image : str
            Name of the Workflow's container image.
        tag : str
            Tag of the Workflow's container image.
        source : str
            Workflow source name.
        handler : str
            Workflow handler name.
        command : str
            Command to run inside the container.
        requirements : list
            List of requirements for the Workflow.
        """
        super().__init__(
            source=source,
            image=image,
            tag=tag,
            handler=handler,
            command=command,
            requirements=requirements

        )


class WorkflowParamsKFP(FunctionParamsKFP):
    """
    Workflow kfp parameters model.
    """
