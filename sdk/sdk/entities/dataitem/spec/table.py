"""
Table Dataitem specification module.
"""
from sdk.entities.dataitem.spec.base import DataitemSpec


class TableDataitemSpec(DataitemSpec):
    """
    Dataitem Table specifications.
    """

    def __init__(
        self,
        key: str | None = None,
        path: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        See Also
        --------
        DataitemSpec.__init__
        """
        super().__init__(key, path, **kwargs)
