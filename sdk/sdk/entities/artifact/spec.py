"""
Artifact spec module.
"""
from sdk.entities.base.spec import EntitySpec


class ArtifactSpec(EntitySpec):
    """
    Artifact specification.
    """

    def __init__(
        self,
        key: str | None = None,
        src_path: str | None = None,
        target_path: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        key : str
            The key of the artifact.
        src_path : str
            The source path of the artifact.
        target_path : str
            The target path of the artifact.
        **kwargs : dict
            Keywords arguments.
        """
        self.key = key
        self.src_path = src_path
        self.target_path = target_path

        self._any_setter(**kwargs)


def build_spec(kind: str, **kwargs) -> ArtifactSpec:
    """
    Build an ArtifactSpecJob object with the given parameters.
    Parameters
    ----------
    kind : str
        The type of ArtifactSpec to build.
    **kwargs : dict
        Keywords to pass to the constructor.
    Returns
    -------
    ArtifactSpec
        An ArtifactSpecJob object with the given parameters.
    Raises
    ------
    ValueError
        If the given kind is not supported.
    """
    if kind in ["artifact", "dataset"]:
        return ArtifactSpec(**kwargs)
    raise ValueError(f"Unknown kind: {kind}")
