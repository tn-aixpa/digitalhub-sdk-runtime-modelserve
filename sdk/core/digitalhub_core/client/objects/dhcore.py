"""
DHCore Client module.
"""
from __future__ import annotations

import os

import requests
from digitalhub_core.client.objects.base import Client
from digitalhub_core.utils.exceptions import BackendError


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
        url = self._get_endpoint() + api
        response = None
        try:
            response = requests.request(call_type, url, timeout=60, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            if response is None:
                msg = "Unable to connect to DHCore backend."
            else:
                msg = f"Backend error: {response.status_code} - {response.text}"
            raise BackendError(msg)

    @staticmethod
    def _get_endpoint() -> str:
        """
        Get DHub Core endpoint environment variables.

        Returns
        -------
        str
            DHub Core endpoint environment variables.

        Raises
        ------
        Exception
            If the endpoint of DHCore is not set in the env variables.
        """
        endpoint = os.getenv("DHUB_CORE_ENDPOINT")
        if endpoint is None:
            raise BackendError("Endpoint not set as environment variables.")
        if endpoint.endswith("/"):
            endpoint = endpoint[:-1]
        return endpoint

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
