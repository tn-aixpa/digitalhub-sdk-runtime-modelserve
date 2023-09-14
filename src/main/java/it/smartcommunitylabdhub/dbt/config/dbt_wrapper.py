import os

import sdk

def main():
    """
    Main function. Get run from backend and run dbt.
    """

    cfg =  sdk.store.models.SQLStoreConfig(**{
    'host': "192.168.49.1",
    'port': "5433",
    'user': "testuser",
    'password': "testpassword",
    'database': "dbt",
    'pg_schema': "public"
    })
    stcfg = sdk.StoreParameters(name="sql", type="sql", is_default=True, config=cfg)
    sdk.set_store(stcfg)

    project = sdk.get_project(os.getenv("PROJECT_NAME"))
    run = sdk.get_run(project.name, os.getenv("RUN_ID"))

    task = sdk.get_task(project.name, run.task_id)
    func_name, func_version = task.task.split("/")[-1].split(":")
    func = sdk.get_function(project.name, func_name, func_version)

    spec = {
        **func.spec.to_dict(),
        **task.spec.to_dict(),
        **run.spec.to_dict(),
    }

    sdk.get_runtime("dbt", spec, run.id, project.name).run()

if __name__ == "__main__":
    main()
