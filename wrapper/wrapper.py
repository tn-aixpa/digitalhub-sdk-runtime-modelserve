"""
Wrapper to execute an arbitrary function.
"""
import os

import sdk


def main():
    """
    Main function. Get run from backend and execute function.
    """

    project = sdk.get_project(os.getenv("PROJECT_NAME"))
    run = sdk.get_run(project.metadata.name, os.getenv("RUN_ID"))
    run.spec.local_execution = True
    run.build()
    run.run()

if __name__ == "__main__":
    main()
