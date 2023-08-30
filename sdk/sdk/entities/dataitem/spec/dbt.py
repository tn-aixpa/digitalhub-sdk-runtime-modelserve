"""
DBT Dataitem specification module.
"""
from sdk.entities.dataitem.spec.base import DataitemSpec


class DBTDataitemSpec(DataitemSpec):
    """
    Dataitem DBT specifications.
    """

    def __init__(
        self, key: str | None = None, path: str | None = None, raw_code: str | None = None,
        compiled_code: str | None = None, **kwargs
    ) -> None:
        """
        Constructor.

        See Also
        --------
        DataitemSpec.__init__
        """
        super().__init__(key, path, **kwargs)
        self.raw_code = raw_code
        self.compiled_code = compiled_code
