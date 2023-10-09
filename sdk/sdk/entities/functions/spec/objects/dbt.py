"""
DBT Function specification module.
"""
from sdk.entities.functions.spec.objects.base import FunctionSpec
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

        try:
            sql = decode_string(sql)
        except Exception:
            ...
        self.sql = encode_string(sql)
