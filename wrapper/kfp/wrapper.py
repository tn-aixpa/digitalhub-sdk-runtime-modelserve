import os

from digitalhub_runtime_kfp.entities.run.kfp_run.builder import RunKfpRunBuilder

import digitalhub as dh
from digitalhub.entities._commons.enums import EntityTypes
from digitalhub.utils.logger import LOGGER


def main():
    """
    Main function. Get run from backend and execute function.
    """

    LOGGER.info("Getting run from backend.")
    project = dh.get_project(os.getenv("PROJECT_NAME"))
    run_key = f"store://{project.name}/{EntityTypes.RUN.value}/{RunKfpRunBuilder.RUN_KIND}/{os.getenv('RUN_ID')}"
    run = dh.get_run(run_key)

    LOGGER.info("Executing function.")
    run.run()

    LOGGER.info("Done.")


if __name__ == "__main__":
    main()
