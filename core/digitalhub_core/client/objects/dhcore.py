from __future__ import annotations

import os
import typing
from urllib.parse import urlparse

from digitalhub_core.client.objects.base import Client
from digitalhub_core.utils.exceptions import BackendError
from dotenv import load_dotenv, set_key
from pydantic import BaseModel
from requests import request
from requests.exceptions import JSONDecodeError, RequestException, Timeout

if typing.TYPE_CHECKING:
    from requests import Response


ENV_FILE = ".dhcore"

MAX_API_LEVEL = 100
MIN_API_LEVEL = 5


class AuthConfig(BaseModel):
    """Client configuration model."""

    user: str = os.getlogin()
    """Username."""


class OAuth2TokenAuth(AuthConfig):
    """OAuth2 token authentication model."""

    access_token: str
    """OAuth2 token."""

    refresh_token: str = None
    """OAuth2 refresh token."""

    client_id: str = None
    """OAuth2 client id."""


class BasicAuth(AuthConfig):
    """Basic authentication model."""

    password: str
    """Basic authentication password."""


class ClientDHCore(Client):
    """
    DHCore client.

    The DHCore client is used to communicate with the Digitalhub Core
    backendAPI via REST. The client supports basic authentication and
    OAuth2 token authentication.
    At creation, the client tries to get the endpoint and authentication
    parameters from the environment variables. In case the user incours
    into an authentication/endpoint error during the client creation,
    the user has the possibility to update the correct parameters using
    the `set_dhub_env` function.
    If the dhcore client is already initialized, this function will
    override the configuration, otherwise it simply set the environment
    variables.
    """

    def __init__(self, config: dict | None = None) -> None:
        super().__init__()

        # Endpoints
        self._endpoint_core: str | None = None
        self._endpoint_issuer: str | None = None

        # Authentication
        self._auth_type: str | None = None

        # Basic
        self._user: str | None = None
        self._password: str | None = None

        # OAuth2
        self._access_token: str | None = None
        self._refresh_token: str | None = None

        self._configure(config)

    ##############################
    # CRUD methods
    ##############################

    def create_object(self, api: str, obj: dict, **kwargs) -> dict:
        """
        Create an object in DHCore.

        Parameters
        ----------
        api : str
            Create API.
        obj : dict
            The object to create.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        kwargs["json"] = obj
        return self._prepare_call("POST", api, **kwargs)

    def read_object(self, api: str, **kwargs) -> dict:
        """
        Get an object from DHCore.

        Parameters
        ----------
        api : str
            Read API.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        return self._prepare_call("GET", api, **kwargs)

    def update_object(self, api: str, obj: dict, **kwargs) -> dict:
        """
        Update an object in DHCore.

        Parameters
        ----------
        api : str
            Update API.
        obj : dict
            The object to update.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        kwargs["json"] = obj
        return self._prepare_call("PUT", api, **kwargs)

    def delete_object(self, api: str, **kwargs) -> dict:
        """
        Delete an object from DHCore.

        Parameters
        ----------
        api : str
            Delete API.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        resp = self._prepare_call("DELETE", api, **kwargs)
        if isinstance(resp, bool):
            resp = {"deleted": resp}
        return resp

    def list_objects(self, api: str, **kwargs) -> list[dict]:
        """
        List objects from DHCore.

        Parameters
        ----------
        api : str
            List API.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        list[dict]
            Response objects.
        """
        if kwargs is None:
            kwargs = {}

        if kwargs.get("params") is None:
            kwargs["params"] = {}

        start_page = 0
        if "page" not in kwargs["params"]:
            kwargs["params"]["page"] = start_page

        objects = []
        while True:
            resp = self._prepare_call("GET", api, **kwargs)
            contents = resp["content"]
            total_pages = resp["totalPages"]
            if not contents or kwargs["params"]["page"] >= total_pages:
                break
            objects.extend(contents)
            kwargs["params"]["page"] += 1

        return objects

    ##############################
    # Call methods
    ##############################

    def _prepare_call(self, call_type: str, api: str, **kwargs) -> dict:
        """
        Prepare a call to the DHCore API.

        Parameters
        ----------
        call_type : str
            The type of call to prepare.
        api : str
            The api to call.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        url = self._endpoint_core + api
        kwargs = self._set_auth_header(kwargs)
        return self._make_call(call_type, url, **kwargs)

    def _set_auth_header(self, kwargs: dict) -> dict:
        """
        Set the authentication header.

        Parameters
        ----------
        kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Keyword arguments with the authentication header.
        """
        if self._auth_type == "basic":
            kwargs["auth"] = self._user, self._password
        elif self._auth_type == "oauth2":
            kwargs["headers"] = {"Authorization": f"Bearer {self._access_token}"}

        return kwargs

    def _make_call(self, call_type: str, url: str, refresh_token: bool = True, **kwargs) -> dict:
        """
        Make a call to the DHCore API.

        Parameters
        ----------
        call_type : str
            The type of call to make.
        url : str
            The URL to call.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        # Call the API
        response = request(call_type, url, timeout=60, **kwargs)

        # Evaluate DHCore API version
        self._check_core_version(response)

        # Handle token refresh
        if response.status_code == 401 and refresh_token:
            self._get_new_access_token()
            return self._make_call(call_type, url, refresh_token=False, **kwargs)

        self._raise_for_error(response)
        return self._parse_response(response)

    def _check_core_version(self, response: Response) -> None:
        """
        Raise an exception if the response indicates an error.

        Parameters
        ----------
        response : Response
            The response object.

        Returns
        -------
        None
        """
        if "X-Api-Level" in response.headers:
            core_api_level = int(response.headers["X-Api-Level"])
            if not (MIN_API_LEVEL <= core_api_level <= MAX_API_LEVEL):
                raise BackendError("Backend API level not supported.")

    def _raise_for_error(self, response: Response) -> None:
        """
        Raise an exception if the response indicates an error.

        Parameters
        ----------
        response : Response
            The response object.

        Returns
        -------
        None
        """
        try:
            response.raise_for_status()
        except RequestException as e:
            if isinstance(e, Timeout):
                msg = "Request to DHCore backend timed out."
            elif isinstance(e, ConnectionError):
                msg = "Unable to connect to DHCore backend."
            else:
                raise e
        except Exception as e:
            msg = f"Some error occurred: {e}"
            raise RuntimeError(msg) from e

    def _parse_response(self, response: Response) -> dict:
        """
        Parse the response object.

        Parameters
        ----------
        response : Response
            The response object.

        Returns
        -------
        dict
            The parsed response object.
        """
        try:
            return response.json()
        except JSONDecodeError:
            if response.text == "":
                return {}
            raise BackendError("Backend response could not be parsed.")

    ##############################
    # Configuration methods
    ##############################

    def _configure(self, config: dict | None = None) -> None:
        """
        Configure the client attributes with config (given or from
        environment).
        Regarding authentication parameters, the config parameter
        takes precedence over the env variables, and the token
        over the basic auth. Furthermore, the config parameter is
        validated against the proper pydantic model.

        Parameters
        ----------
        config : dict
            Configuration dictionary.

        Returns
        -------
        None
        """
        self._load_env()

        self._get_endpoints_from_env()

        if config is not None:
            if config.get("access_token") is not None:
                config = OAuth2TokenAuth(**config)
                self._user = config.user
                self._access_token = config.access_token
                self._refresh_token = config.refresh_token
                self._client_id = config.client_id
                self._auth_type = "oauth2"

            elif config.get("user") is not None and config.get("password") is not None:
                config = BasicAuth(**config)
                self._user = config.user
                self._password = config.password
                self._auth_type = "basic"

            return

        self._get_auth_from_env()

    def _load_env(self) -> None:
        """
        Load the env variables from the .dhcore file.

        Returns
        -------
        None
        """
        load_dotenv(dotenv_path=ENV_FILE, override=True)

    def _write_env(self) -> None:
        """
        Write the env variables to the .dhcore file.
        It will overwrite any existing env variables.

        Returns
        -------
        None
        """
        keys = {}
        if self._access_token is not None:
            keys["DHCORE_ACCESS_TOKEN"] = self._access_token
        if self._refresh_token is not None:
            keys["DHCORE_REFRESH_TOKEN"] = self._refresh_token

        for k, v in keys.items():
            set_key(dotenv_path=ENV_FILE, key_to_set=k, value_to_set=v)

    def _get_endpoints_from_env(self) -> None:
        """
        Get the DHCore endpoint and token issuer endpoint from env.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the endpoint of DHCore is not set in the env variables.
        """
        core_endpt = os.getenv("DHCORE_ENDPOINT")
        if core_endpt is None:
            raise BackendError("Endpoint not set as environment variables.")
        self._endpoint_core = self._sanitize_endpoint(core_endpt)

        issr_endpt = os.getenv("DHCORE_ISSUER")
        if issr_endpt is not None:
            self._endpoint_issuer = self._sanitize_endpoint(issr_endpt)

    def _sanitize_endpoint(self, endpoint: str) -> str:
        """
        Sanitize the endpoint.

        Returns
        -------
        None
        """
        parsed = urlparse(endpoint)
        if parsed.scheme not in ["http", "https"]:
            raise BackendError("Invalid endpoint scheme.")

        endpoint = endpoint.strip()
        return endpoint.removesuffix("/")

    def _get_auth_from_env(self) -> None:
        """
        Get authentication parameters from the env.

        Returns
        -------
        None
        """
        self._user = os.getenv("DHCORE_USER", os.getlogin())
        self._refresh_token = os.getenv("DHCORE_REFRESH_TOKEN")
        self._client_id = os.getenv("DHCORE_CLIENT_ID")

        token = os.getenv("DHCORE_ACCESS_TOKEN")
        if token is not None and token != "":
            self._auth_type = "oauth2"
            self._access_token = token
            return

        password = os.getenv("DHCORE_PASSWORD")
        if self._user is not None and password is not None:
            self._auth_type = "basic"
            self._password = password
            return

    def _get_new_access_token(self) -> None:
        """
        Get a new access token.

        Returns
        -------
        None
        """
        # Call issuer and get endpoint for
        # refreshing access token
        url = self._get_refresh_endpoint()

        # Send request to get new access token
        payload = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "refresh_token": self._refresh_token,
        }
        r = request("POST", url, data=payload, timeout=60)
        r.raise_for_status()
        self._access_token = r.json().get("access_token")
        self._refresh_token = r.json().get("refresh_token")
        self._write_env()

    def _get_refresh_endpoint(self) -> str:
        """
        Get the refresh endpoint.

        Returns
        -------
        str
            Refresh endpoint.
        """
        url = self._endpoint_issuer
        if url is None:
            raise BackendError("Issuer endpoint not set.")
        r = request("GET", url, timeout=60)
        r.raise_for_status()
        return r.json().get("endpoint")

    ##############################
    # Static methods
    ##############################

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
