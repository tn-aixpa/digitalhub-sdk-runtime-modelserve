from typing import Callable

class Framework:
    """
    Framework class.
    """

    def execute(self, func: Callable, *args, **kwargs) -> None:
        """
        Execute function.

        Parameters
        ----------
        func : Callable
            Function to execute.
        *args
            Positional arguments.
        **kwargs
            Keyword arguments.

        Returns
        -------
        None
        """
        func(*args, **kwargs)
