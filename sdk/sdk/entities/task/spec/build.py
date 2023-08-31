"""
Build Task specification module.
"""
from sdk.entities.task.spec.base import TaskSpec


class TaskSpecBuild(TaskSpec):
    """Task build specification."""

    def __init__(
        self,
        image: str | None = None,
        base_image: str | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        image : str
            The image to perform the building task.
        base_image : str
            The base image to create the image from.
        """
        self.image = image
        self.base_image = base_image
