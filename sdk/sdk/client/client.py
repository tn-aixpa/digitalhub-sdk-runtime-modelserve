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
        return self.call("POST", api, json=obj)

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
        return self.call("GET", api)

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
        return self.call("PUT", api, json=obj)

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
        return self.call("DELETE", api)

    def call(self, call_type: str, api: str, **kwargs) -> dict:
        """
        Make a call to the DHCore API.

        Parameters
        ----------
        call_type : str
            The type of call to make.
        api : str
            The api to call.
        **kwargs
            The arguments to pass to the call.

        Returns
        -------
        dict
            The response object.
        """
        endpoint = self._get_endpoint(api)
        try:
            response = requests.request(call_type, endpoint, timeout=60, **kwargs)
        except ConnectionError as exc:
            raise BackendError("Connection error.") from exc
        obj = self._dictify(response)
        self._raise_if_status(obj)
        return obj

    @staticmethod
    def _raise_if_status(obj: dict) -> None:
        """
        Parse the status of a response and raise an exception if it contains the status key.

        Parameters
        ----------
        obj : dict
            The response.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the response is not valid (a dict that contains the status key).
        """
        if isinstance(obj, dict) and "status" in obj:
            if not obj.get("kind") == "run":
                raise BackendError(obj)

    @staticmethod
    def _dictify(response: requests.Response) -> dict:
        """
        Convert a response to a dict.

        Parameters
        ----------
        response : requests.Response
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
            obj = response.json()
            if isinstance(obj, bool):
                obj = {"result": obj}
            return obj
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
        raise BackendError(
            "Endpoint not setted. Please set env variables with 'set_dhub_env()' function."
        )
