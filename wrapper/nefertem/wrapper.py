"""
Wrapper to execute an arbitrary function.
"""
import os

from digitalhub_core.utils.logger import LOGGER

import digitalhub as dh


def main():
    """
    Main function. Get run from backend and execute function.
    """

    LOGGER.info("Getting run from backend.")
    project = dh.get_project(os.getenv("PROJECT_NAME"))
    run_key = f"store://{project.name}/runs/run+nefertem/{os.getenv('RUN_ID')}"
    run = dh.get_run(run_key)

    LOGGER.info("Executing function.")
    run.run()

    LOGGER.info("Done.")


if __name__ == "__main__":
    main()
