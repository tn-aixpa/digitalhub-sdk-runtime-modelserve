import os

import digitalhub_core as dhcore

os.environ["DIGITALHUB_CORE_ENDPOINT"] = "http://localhost:8080/"
os.environ["DIGITALHUB_CORE_WORKFLOW_IMAGE"] = "dhcore/workflow:latest"
os.environ["KFP_ENDPOINT"] = "http://localhost:8888/"

# Get or create project
project = dhcore.get_or_create_project("project-kfp", local=True)

function = project.new_function(
    name="test-kfp", kind="kfp", source_code="test/testkfp_pipeline.py", handler="myhandler"
)

function.run("pipeline", local_execution=True, parameters={"inputs": {"p1": "test", "in1": "test"}})
