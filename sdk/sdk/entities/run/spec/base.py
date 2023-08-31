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

        """
        self.inputs = inputs if inputs is not None else {}
        self.outputs = outputs if outputs is not None else {}
        self.parameters = parameters if parameters is not None else {}

    def get_inputs(self) -> dict:
        """
        Get the inputs of the run.

        Returns
        -------
        dict
            The inputs of the run.

        """
        return self.inputs

    def get_outputs(self) -> dict:
        """
        Get the outputs of the run.

        Returns
        -------
        dict
            The outputs of the run.

        """
        return self.outputs

    def get_parameters(self) -> dict:
        """
        Get the parameters of the run.

        Returns
        -------
        dict
            The parameters of the run.

        """
        return self.parameters
