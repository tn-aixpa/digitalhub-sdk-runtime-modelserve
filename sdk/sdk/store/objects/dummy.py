"""
DummyStore module.
"""
from typing import Optional

from sdk.store.objects.store import Store


class DummyStore(Store):
    """
    DummyStore class. It implements the Store interface and provides dummy methods.
    """

    def __init__(self, name: str, type: str, config: Optional[dict] = None) -> None:
        """
        Constructor.

        See Also
        --------
        Store.__init__
        """
        super().__init__(name, type, config)

    def fetch_artifact(self, *args) -> None:
        """
        Placeholder method.

        Returns:
        --------
        None
        """
        ...

    def persist_artifact(self, *args) -> None:
        """
        Placeholder method.

        Returns:
        --------
        None
        """
        ...

    def _check_access_to_storage(self, *args) -> None:
        """
        Placeholder method.

        Returns:
        --------
        None
        """
        ...

    def _get_data(self, *args) -> None:
        """
        Placeholder method.

        Returns:
        --------
        None
        """
        ...
