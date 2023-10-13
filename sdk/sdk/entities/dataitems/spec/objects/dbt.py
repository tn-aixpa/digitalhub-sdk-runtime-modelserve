"""
DBT Dataitem specification module.
"""
from sdk.entities.dataitems.spec.objects.base import DataitemParams, DataitemSpec


class DataitemSpecDBT(DataitemSpec):
    """
    Dataitem DBT specifications.
    """

    def __init__(
        self,
        key: str | None = None,
        path: str | None = None,
        raw_code: str | None = None,
        compiled_code: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        raw_code : str
            The raw code of the dataitem.
        compiled_code : str
            The compiled code of the dataitem.

        See Also
        --------
        DataitemSpec.__init__
        """
        super().__init__(key, path, **kwargs)
        self.raw_code = raw_code
        self.compiled_code = compiled_code


class DataitemParamsDBT(DataitemParams):
    """
    Dataitem DBT parameters.
    """

    raw_code: str | None = None
    "The raw code of the dataitem."

    compiled_code: str | None = None
    "The compiled code of the dataitem."
