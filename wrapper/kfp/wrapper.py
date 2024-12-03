import os

import digitalhub as dh
from digitalhub.runtimes.enums import RuntimeEnvVar
from digitalhub.utils.logger import LOGGER


def main():
    """
    Main function. Get run from backend and execute function.
    """

    LOGGER.info("Getting run from backend.")
    run = dh.get_run(os.getenv(RuntimeEnvVar.RUN_ID.value), os.getenv(RuntimeEnvVar.PROJECT.value))

    LOGGER.info("Executing workflow.")
    run.run()

    LOGGER.info("Done.")


if __name__ == "__main__":
    main()
