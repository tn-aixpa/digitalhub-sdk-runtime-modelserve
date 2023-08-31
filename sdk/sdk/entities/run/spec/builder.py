"""
Run specification module.
"""
from sdk.entities.run.spec.base import RunSpec
from sdk.utils.exceptions import EntityError


REGISTRY = {
    "run": RunSpec,
}


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
    try:
        return REGISTRY[kind](**kwargs)
    except KeyError:
        raise EntityError(f"Unsupported kind: {kind}")
