"""
RunStatus class module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.status import Status


class RunStatus(Status):
    """
    Status class for run entities.
    """

    def __init__(
        self,
        state: str | None = None,
        message: str | None = None,
        results: dict | None = None,
        entities: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        results : dict
            Runtime results.
        entities : dict
            Runtime entities outputs.
        **kwargs
            Keyword arguments.


        See Also
        --------
        Status.__init__
        """
        super().__init__(state, message)
        self.results = results
        self.entities = entities

        self._any_setter(**kwargs)
