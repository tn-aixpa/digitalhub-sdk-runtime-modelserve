"""
Dbt Function specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.functions.spec import FunctionParams, FunctionSpec, SourceCodeStruct
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import decode_string, encode_string


class FunctionSpecDbt(FunctionSpec):
    """
    Specification for a Function Dbt.
    """

    def __init__(
        self,
        source: str | None = None,
        sql: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        sql : str
            SQL query to run inside Dbt.
        """
        super().__init__(source, **kwargs)
        if sql is None:
            raise EntityError("SQL query must be provided.")

        # This is to avoid re-encoding the SQL query when
        # it is already encoded.
        try:
            sql = decode_string(sql)
        except Exception:
            ...
        self.sql = SourceCodeStruct(
                source_code=sql,
                source_encoded=encode_string(sql),
                lang="sql",
            )

    def show_source_code(self) -> str:
        """
        Show source code.

        Returns
        -------
        str
            Source code.
        """
        return str(self.sql.source_code)

    def to_dict(self) -> dict:
        """
        Override to_dict to exclude sql source_code.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        dict_ = super().to_dict()
        dict_["sql"] = self.sql.to_dict()
        return dict_


class FunctionParamsDbt(FunctionParams):
    """
    Function Dbt parameters model.
    """

    sql: str = None
    """SQL query to run inside the container."""
