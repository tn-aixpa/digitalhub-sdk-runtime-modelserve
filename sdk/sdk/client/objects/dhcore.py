"""
DHCore Client module.
"""
import os

import requests
from pydantic import BaseModel

from sdk.client.objects.base import Client
from sdk.utils.exceptions import BackendError


class ClientDHCore(Client):
    """
    The client. It's a singleton. Use the builder to get an instance.
    It is used to make requests to the DHCore API.
    """

    def create_object(self, obj: dict, api: str) -> dict:
        """
        Create an object.

        Parameters
        ----------
        obj : dict
            The object to create.
        api : str
            The api to create the object with.

        Returns
        -------
        dict
            The created object.
        """
        return self._call("POST", api, json=obj)

    def read_object(self, api: str) -> dict:
        """
        Get an object.

        Parameters
        ----------
        api : str
            The api to get the object with.

        Returns
        -------
        dict
            The object.
        """
        return self._call("GET", api)

    def update_object(self, obj: dict, api: str) -> dict:
        """
        Update an object.

        Parameters
        ----------
        obj : dict
            The object to update.
        api : str
            The api to update the object with.

        Returns
        -------
        dict
            The updated object.
        """
        return self._call("PUT", api, json=obj)

    def delete_object(self, api: str) -> dict:
        """
        Delete an object.

        Parameters
        ----------
        api : str
            The api to delete the object with.

        Returns
        -------
        dict
            A generic dictionary.
        """
        resp = self._call("DELETE", api)
        if isinstance(resp, bool):
            resp = {"deleted": resp}
        return resp

    def _call(self, call_type: str, api: str, **kwargs) -> dict:
        """
        Make a call to the DHCore API.
        Keyword arguments are passed to the session.request function.

        Parameters
        ----------
        call_type : str
            The type of call to make.
        api : str
            The api to call.
        **kwargs
            Keyword arguments.

        Returns
        -------
        dict
            The response object.
        """
        endpoint = self._get_endpoint(api)
        response = None
        try:
            response = requests.request(call_type, endpoint, timeout=60, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            if response is None:
                msg = "Unable to connect to DHCore backend."
            else:
                msg = f"Backend error: {response.status_code} - {response.text}"
            raise BackendError(msg)

    @staticmethod
    def _get_endpoint(api: str) -> str:
        """
        Get the endpoint.

        Parameters
        ----------
        api : str
            The api path.

        Returns
        -------
        str
            The endpoint formatted with the api path.

        Raises
        ------
        Exception
            If the endpoint of DHCore is not set in the env variables.
        """
        endpoint = get_dhub_env().endpoint
        if endpoint is not None:
            return endpoint + api
        raise BackendError(
            "Endpoint not set. Please set env variables with 'set_dhub_env()' function."
        )

    @staticmethod
    def is_local() -> bool:
        """
        Declare if Client is local.

        Returns
        -------
        bool
            False
        """
        return False


class DHCoreConfig(BaseModel):
    """
    DigitalHUB backend configuration.
    """

    endpoint: str
    """Backend endpoint."""

    user: str | None = None
    """User."""

    password: str | None = None
    """Password."""

    token: str | None = None
    """Auth token."""


def get_dhub_env() -> DHCoreConfig:
    """
    Function to get DHub Core environment variables.

    Returns
    -------
    DHCoreConfig
        An object that contains endpoint, user, password, and token of a DHub Core configuration.
    """
    return DHCoreConfig(
        endpoint=os.getenv("DHUB_CORE_ENDPOINT"),
        user=os.getenv("DHUB_CORE_USER"),
        password=os.getenv("DHUB_CORE_PASSWORD"),
        token=os.getenv("DHUB_CORE_TOKEN"),
    )
