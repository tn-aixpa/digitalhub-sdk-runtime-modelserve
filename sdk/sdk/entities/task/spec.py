"""
Task spec module.
"""
from sdk.entities.base.spec import EntitySpec


class TaskSpec(EntitySpec):
    """Task specification."""

    def __init__(
        self,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        input : str, optional
            Input dataitem.
        output : str, optional
            Output dataitem.
        parameters : dict, optional
            Parameters of the task.
        k8s_resources : dict, optional
        **kwargs
            Additional keyword arguments.

        Notes
        -----
        If some of the attributes are not in the signature,
        they will be added as new attributes.
        """

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__:
                self.__setattr__(k, v)
