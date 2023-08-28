"""
Run specification module.
"""
from sdk.entities.base.spec import EntitySpec


class RunSpec(EntitySpec):
    """Run specification."""

    def __init__(
        self,
        inputs: dict | None = None,
        outputs: list | None = None,
        parameters: dict | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        inputs : dict
            The inputs of the run.
        outputs : list
            The outputs of the run.
        parameters : dict
            The parameters of the run.

        """
        self.inputs = inputs if inputs is not None else {}
        self.outputs = outputs if outputs is not None else []
        self.parameters = parameters if parameters is not None else {}


def build_spec(kind: str, **kwargs) -> RunSpec:
    """
    Build a RunSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of RunSpec to build.
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    RunSpec
        A RunSpec object with the given parameters.

    Raises
    ------
    ValueError
        If the given kind is not supported.
    """
    if kind == "run":
        return RunSpec(**kwargs)
    raise ValueError(f"Unknown kind: {kind}")
