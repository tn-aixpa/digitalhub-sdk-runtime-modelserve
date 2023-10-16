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

    # Execute function in local mode.
    run.spec.local_execution = True

    # Build and run.
    run.build()
    run.run()

    # Reverse flag to remote mode and save.
    run.spec.local_execution = False
    run.save(run.id)

if __name__ == "__main__":
    main()
