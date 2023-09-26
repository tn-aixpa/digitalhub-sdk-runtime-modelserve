"""
DBT Function specification module.
"""
from sdk.entities.function.spec.objects.base import FunctionSpec
from sdk.utils.exceptions import EntityError
from sdk.utils.generic_utils import decode_string, encode_string


class FunctionSpecDBT(FunctionSpec):
    """
    Specification for a Function DBT.
    """

    def __init__(
        self,
        source: str = "",
        sql: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        sql : str
            SQL query to run inside DBT.
        """
        super().__init__(source, **kwargs)
        if sql is None:
            raise EntityError("SQL query must be provided.")

        try:
            sql = decode_string(sql)
        except Exception:
            pass
        self.sql = encode_string(sql)
