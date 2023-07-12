"""
Dataitem spec module.
"""
from sdk.entities.base.spec import EntitySpec


class DataitemSpec(EntitySpec):
    """
    Dataitem specifications.
    """

    def __init__(self, key: str = None, path: str = None) -> None:
        """
        Constructor.

        Parameters
        ----------
        key : str, optional
            The key of the dataitem.
        path : str, optional
            The path of the dataitem.

        """
        self.key = key
        self.path = path


def build_spec(kind: str, **kwargs) -> DataitemSpec:
    """
    Build a DataItemSpec object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of DataItemSpec to build.
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    DataItemSpec
        A DataItemSpec object with the given parameters.

    Raises
    ------
    ValueError
        If the given kind is not supported.
    """
    if kind == "dataitem":
        return DataitemSpec(**kwargs)
    raise ValueError(f"Unknown kind: {kind}")
