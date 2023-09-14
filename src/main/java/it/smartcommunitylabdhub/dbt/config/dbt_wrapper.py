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
    run = sdk.get_run(project.name, os.getenv("RUN_ID"))
    task = sdk.get_task(project.name, run.task_id)
    func = sdk.get_function_from_task(task.task)

    spec = {
        **func.spec.to_dict(),
        **task.spec.to_dict(),
        **run.spec.to_dict(),
    }

    sdk.get_runtime(func.kind, spec, run.id, project.name).run()

if __name__ == "__main__":
    main()
