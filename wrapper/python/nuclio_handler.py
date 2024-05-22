import os
import sys

import digitalhub as dh
from digitalhub_core.entities._base.status import State
from digitalhub_core.utils.logger import LOGGER


def handler(context, event) -> None:
    """
    Nuclio handler for python function.
    """

    # Get project and run
    project = dh.get_project(event.body["project"])
    run = dh.get_run(project.name, event.body["id"])

    LOGGER.info("Installing run dependencies.")
    for requirement in run.spec.to_dict().get("requirements", []):
        LOGGER.info(f"Installing {requirement}.")
        os.system(f"pip install {requirement}")

    LOGGER.info("Executing function.")
    run.run()

    if run.status.state == State.ERROR.value:
        sys.exit(1)

    LOGGER.info("Done.")
