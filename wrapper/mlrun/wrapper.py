"""
Wrapper to execute an arbitrary function.
"""
import os

import digitalhub as dhcore
from digitalhub_core.utils.logger import LOGGER


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

    LOGGER.info("Saving run.")
    run.save(update=True)

    LOGGER.info("Done.")


if __name__ == "__main__":
    main()
