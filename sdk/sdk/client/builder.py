"""
Client builder module.
"""
from sdk.client.client import Client


class ClientBuilder:
    """
    The client builder. It implements the builder pattern to create a client instance.
    It is a singleton class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._instance = None

    def build(self, *args, **kwargs) -> Client:
        """
        Method to create a client instance.

        Parameters
        ----------
        *args
            Arguments list.
        **kwargs
            Keyword arguments.

        Returns
        -------
        Client
            Returns the client instance.
        """
        if not self._instance:
            self._instance = Client(*args, **kwargs)
        return self._instance
