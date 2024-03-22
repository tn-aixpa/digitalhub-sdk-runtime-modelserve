import kfp
from digitalhub_core_kfp.dsl import step
import digitalhub_core as dhcore


def myhandler(p1, in1):
    project = dhcore.get_project("project-kfp", local=True)
    s = step(name="step1", project=project.name, function="myfunc", action="job", parameters={"p1": p1}, inputs={"in1": in1}, outputs={"out1": None})