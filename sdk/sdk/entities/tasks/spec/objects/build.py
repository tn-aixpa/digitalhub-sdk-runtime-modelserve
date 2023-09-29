"""
Build Task specification module.
"""
from sdk.entities.tasks.spec.objects.base import TaskSpec


class TaskSpecBuild(TaskSpec):
    """Task build specification."""

    def __init__(
        self,
        function: str,
        image: str | None = None,
        base_image: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        image : str
            The image to job the building task.
        base_image : str
            The base image to create the image from.

        See Also
        --------
        TaskSpec.__init__
        """
        super().__init__(function, **kwargs)
        self.image = image
        self.base_image = base_image
