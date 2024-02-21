import digitalhub_core as dhcore
import digitalhub_core_kfp as dh_kfp

from pathlib import Path
import os

os.environ['DIGITALHUB_CORE_ENDPOINT'] = 'http://localhost:8080/'

# Get or create project
project = dhcore.get_or_create_project("project-kfp", local=True)

function = project.new_function(name="test-kfp",
                                kind="kfp",
                                source_code="test/testkfp_pipeline.py",
                                handler="myhandler")

function.run("pipeline", local_execution=True)