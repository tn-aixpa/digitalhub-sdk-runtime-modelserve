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

    def get_local_execution(self) -> bool:
        """
        Get the local_execution flag of the run.

        Returns
        -------
        bool
            The local_execution flag of the run.

        """
        return self.local_execution

    @staticmethod
    def get_dataitems_list(obj: dict) -> list[str]:
        """
        Get the list of dataitems used in the run.

        Parameters
        ----------
        obj : dict
            The object to get the dataitems from.

        Returns
        -------
        list[str]
            The list of dataitems used in the run.

        """
        return obj.get("dataitems", [])

    @staticmethod
    def get_artifacts_list(obj: dict) -> list[str]:
        """
        Get the list of artifacts used in the run.

        Parameters
        ----------
        obj : dict
            The object to get the artifacts from.

        Returns
        -------
        list[str]
            The list of artifacts used in the run.

        """
        return obj.get("artifacts", [])
