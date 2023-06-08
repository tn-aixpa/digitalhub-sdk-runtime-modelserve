from abc import ABCMeta, abstractmethod
from typing import Optional, Any


class ResourceRegistry(dict):
    """
    Generic registry object to keep track of resources.
    """

    def set_resource(self, res_name: str, path: str) -> None:
        """
        Register a resource path.
        """
        if res_name not in self:
            self[res_name] = path

    def get_resource(self, res_name: str) -> str:
        """
        Return resource path.
        """
        return self.get(res_name)

    def clean_all(self) -> None:
        """
        Remove resource from registry.
        """
        self.clear()


class Store(metaclass=ABCMeta):
    def __init__(
        self,
        name: str,
        type: str,
        config: Optional[dict] = None,
    ) -> None:
        self.name = name
        self.type = type
        self.config = config
        self.registry = ResourceRegistry()

    @abstractmethod
    def fetch_artifact(self, src: str, dst: str) -> None:
        ...

    @abstractmethod
    def persist_artifact(self, src: str, dst: str) -> None:
        """
        Method to persist artifact in storage.
        """

    @abstractmethod
    def _get_data(self, *args) -> Any:
        """
        Method that retrieve data from a storage.
        """

    @abstractmethod
    def _store_data(self, *args) -> str:
        """
        Store data locally in temporary folder and return tmp path.
        """

    @abstractmethod
    def _check_access_to_storage(self) -> None:
        """
        Check if there is access to the storage.
        """

    def _register_resource(self, key: str, path: str) -> None:
        """
        Method to register a resource into the path registry.
        """
        self.registry.set_resource(key, path)

    def _get_resource(self, key: str) -> str:
        """
        Method to return temporary path of a registered resource.
        """
        return self.registry.get_resource(key)
