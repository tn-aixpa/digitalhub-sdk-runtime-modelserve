"""
Client module.
"""
from typing import Union

import requests

from sdk.client.env_utils import get_dhub_env


class Client:
    """
    The client. It's a singleton. Use the builder to get an instance. It is used to make requests to the DHCore API.
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
        endpoint = self._get_endpoint(api)
        r = requests.post(endpoint, json=obj)
        d = self._dictify(r)
        self._parse_status(d)
        return d

    def get_object(self, api: str) -> dict:
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
        endpoint = self._get_endpoint(api)
        r = requests.get(endpoint)
        d = self._dictify(r)
        self._parse_status(d)
        return d

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
        endpoint = self._get_endpoint(api)
        r = requests.put(endpoint, json=obj)
        d = self._dictify(r)
        self._parse_status(d)
        return d

    def delete_object(self, api: str) -> bool:
        """
        Delete an object.

        Parameters
        ----------
        api : str
            The api to delete the object with.

        Returns
        -------
        bool
            Always true.
        """
        endpoint = self._get_endpoint(api)
        r = requests.delete(endpoint)
        d = self._dictify(r)
        self._parse_status(d)
        return d

    @staticmethod
    def _parse_status(d: Union[dict, bool]) -> None:
        """
        Parse the status of a response.

        Parameters
        ----------
        d : Union[dict, bool]
            The response.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the response is not valid (a dict that contains the status key).
        """
        if isinstance(d, dict) and "status" in d:
            raise Exception(d)

    @staticmethod
    def _dictify(r: requests.Response) -> dict:
        """
        Convert a response to a dict.

        Parameters
        ----------
        r : requests.Response
            The response.

        Returns
        -------
        dict
            The dictified response.

        Raises
        ------
        Exception
            If the response is not convertible to a dict.
        """
        try:
            return r.json()
        except Exception as ex:
            raise ex

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
            If the endpoint of DHCore is not setted in the env variables.
        """
        endpoint = get_dhub_env().endpoint
        if endpoint is not None:
            return endpoint + api
        raise Exception(
            "Endpoint not setted. Please set env variables with 'set_dhub_env()' function."
        )
