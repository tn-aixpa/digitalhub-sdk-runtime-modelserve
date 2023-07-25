"""
Client module.
"""
import requests

from sdk.client.env_utils import get_dhub_env
from sdk.utils.exceptions import BackendError


class Client:
    """
    The client. It's a singleton. Use the builder to get an instance.
    It is used to make requests to the DHCore API.
    """

    def __init__(self) -> None:
        self.session = requests.Session()

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
        try:
            response = self.session.request(call_type, endpoint, timeout=60, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise BackendError(
                f"Request error: {exc}. Text response: {response.text}"
            ) from exc

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

    def __del__(self) -> None:
        self.session.close()
