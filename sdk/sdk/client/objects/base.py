"""
Client Base module.
"""
from abc import abstractmethod


class Client:
    """
    Base Client class.
    """

    @abstractmethod
    def create_object(self, obj: dict, api: str) -> dict:
        ...

    @abstractmethod
    def read_object(self, api: str) -> dict:
        ...

    @abstractmethod
    def update_object(self, obj: dict, api: str) -> dict:
        ...

    @abstractmethod
    def delete_object(self, api: str) -> dict:
        ...

    @abstractmethod
    def is_local() -> bool:
        ...
