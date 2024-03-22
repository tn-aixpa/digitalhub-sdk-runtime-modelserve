"""
Wrapper to execute an arbitrary function.
"""
import os
import sys

from digitalhub_core.utils.logger import LOGGER
from digitalhub_core.entities._base.status import State

import digitalhub as dhcore


def main():
    """
    Main function. Get run from backend and execute function.
    """

    LOGGER.info("Getting run from backend.")
    project = dhcore.get_project(os.getenv("PROJECT_NAME"))
    run = dhcore.get_run(project.name, os.getenv("RUN_ID"))

    LOGGER.info("Installing run dependencies.")
    for requirement in run.spec.to_dict().get("requirements", []):
        LOGGER.info(f"Installing {requirement}.")
        os.system(f"pip install {requirement}")

    LOGGER.info("Executing function.")
    run.run()

    if run.status.state == State.ERROR.value:
        sys.exit(1)

    LOGGER.info("Done.")


if __name__ == "__main__":
    main()
