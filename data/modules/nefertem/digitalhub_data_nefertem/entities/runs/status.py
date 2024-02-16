from __future__ import annotations

from digitalhub_core.entities.runs.status import RunStatus


class RunStatusNefertem(RunStatus):
    """
    Run Nefertem status.
    """

    def __init__(
        self,
        state: str | None = None,
        message: str | None = None,
        results: dict | None = None,
        outputs: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        results : dict
            Runtime results.
        outputs : dict
            Runtime entities outputs.
        **kwargs
            Keyword arguments.


        See Also
        --------
        Status.__init__
        """
        super().__init__(state, message)
        self.results = results
        self.outputs = outputs
