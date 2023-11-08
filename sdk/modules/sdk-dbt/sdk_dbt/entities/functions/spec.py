"""
DBT Function specification module.
"""
from sdk.entities.functions.spec import FunctionParams, FunctionSpec
from sdk.utils.exceptions import EntityError
from sdk.utils.generic_utils import decode_string, encode_string


class FunctionSpecDBT(FunctionSpec):
    """
    Specification for a Function DBT.
    """

    def __init__(
        self,
        source: str | None = None,
        image: str | None = None,
        command: str | None = None,
        args: list | None = None,
        sql: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        image : str
            Name of the Function's container image.
        command : str
            Command to run inside the container.
        args : list
            List of arguments for the command.
        sql : str
            SQL query to run inside DBT.
        """
        super().__init__(source, **kwargs)
        self.image = image
        self.command = command
        self.args = args
        if sql is None:
            raise EntityError("SQL query must be provided.")

        # This is to avoid re-encoding the SQL query when
        # it is already encoded.
        try:
            sql = decode_string(sql)
        except Exception:
            ...
        self.sql = encode_string(sql)


class FunctionParamsDBT(FunctionParams):
    """
    Function DBT parameters model.
    """

    image: str | None = None
    """Name of the Function's container image."""

    command: str | None = None
    """Command to run inside the container."""

    args: list | None = None
    """List of arguments for the command."""

    sql: str | None = None
    """SQL query to run inside the container."""
