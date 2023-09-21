"""
Run base specification module.
"""
from sdk.entities.base.spec import EntitySpec


class RunSpec(EntitySpec):
    """Run specification."""

    def __init__(
        self,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        local_execution: bool = False,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        inputs : dict
            The inputs of the run.
        outputs : dict
            The outputs of the run.
        parameters : dict
            The parameters of the run.
        local_execution : bool
            Flag to indicate if the run will be executed locally
        **kwargs
            Keywords arguments.
        """
        self.inputs = inputs if inputs is not None else {}
        self.outputs = outputs if outputs is not None else {}
        self.parameters = parameters if parameters is not None else {}
        self.local_execution = local_execution

        self._any_setter(**kwargs)
