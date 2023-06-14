"""
Store module.
"""
from abc import ABCMeta, abstractmethod
from typing import Optional


class ResourceRegistry(dict):
    """
    Registry object to keep track of resources fetched from a backend and their temporary local paths.
    """

    def set_resource(self, res_name: str, path: str) -> None:
        """
        Register resource.

        Parameters
        ----------
        res_name : str
            Resource name.
        path : str
            Resource path.

        Returns
        -------
        None
        """
        if res_name not in self:
            self[res_name] = path

    def get_resource(self, res_name: str) -> str:
        """
        Get resource path.

        Parameters
        ----------
        res_name : str
            Resource name.

        Returns
        -------
        str
            Resource path.
        """
        return self.get(res_name)

    def clean_all(self) -> None:
        """
        Clean all resources.

        Returns
        -------
        None
        """
        self.clear()


class Store(metaclass=ABCMeta):
    """
    Store abstract class.
    """

    def __init__(
        self,
        name: str,
        type: str,
        uri: str,
        config: Optional[dict] = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        name : str
            Store name.
        type : str
            Store type.
        uri : str
            Store URI.
        config : Optional[dict], optional
            Store configuration, by default None

        Returns
        -------
        None
        """
        self.name = name
        self.type = type
        self.uri = uri
        self.config = config
        self.registry = ResourceRegistry()

    ############################
    # IO methods
    ############################

    @abstractmethod
    def upload(self, src: str, dst: str = None) -> None:
        """
        Method to upload artifact to storage.
        """

    @abstractmethod
    def download(self, src: str, dst: str = None) -> None:
        """
        Method to download artifact from storage.
        """

    @abstractmethod
    def fetch_artifact(self, src: str, dst: str = None) -> None:
        """
        Method to fetch artifact from storage.
        """

    @abstractmethod
    def persist_artifact(self, src: str, dst: str = None) -> None:
        """
        Method to persist artifact in storage.
        """

    ############################
    # Interface helpers methods
    ############################

    @staticmethod
    @abstractmethod
    def is_local() -> bool:
        """
        Method to check if store is local.
        """

    @abstractmethod
    def get_root_uri(self) -> str:
        """
        Method to get root URI.
        """

    ############################
    # Resource registry methods
    ############################

    def _register_resource(self, key: str, path: str) -> None:
        """
        Register a resource in the registry.
        """
        self.registry.set_resource(key, path)

    def _get_resource(self, key: str) -> str:
        """
        Get a resource from the registry.
        """
        return self.registry.get_resource(key)
