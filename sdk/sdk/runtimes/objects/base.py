"""
Base Runtime module.
"""
from abc import abstractmethod


class Runtime:
    """
    Base Runtime class.
    """

    def __init__(
        self,
        spec: dict,
        run_id: str,
        project_name: str,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        spec : dict
            Run merged specification.
        run_id : str
            The run id.
        project_name : str
            The project name.
        """
        self.spec = spec
        self.run_id = run_id
        self.project_name = project_name

    @abstractmethod
    def run(self) -> None:
        ...
