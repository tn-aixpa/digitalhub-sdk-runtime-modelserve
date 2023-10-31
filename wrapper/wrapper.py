"""
Wrapper to execute an arbitrary function.
"""
import os

import sdk


def main():
    """
    Main function. Get run from backend and execute function.
    """

    # Get run from backend.
    project = sdk.get_project(os.getenv("PROJECT_NAME"))
    run = sdk.get_run(project.metadata.name, os.getenv("RUN_ID"))

    # Run and save.
    run.run()
    run.save(update=True)


if __name__ == "__main__":
    main()
