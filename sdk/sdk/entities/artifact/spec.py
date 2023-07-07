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
        key: str = None,
        src_path: str = None,
        target_path: str = None,
        **kwargs,
    ) -> None:
        self.key = key
        self.src_path = src_path
        self.target_path = target_path

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__:
                self.__setattr__(k, v)
