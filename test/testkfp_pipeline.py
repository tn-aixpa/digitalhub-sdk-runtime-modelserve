import kfp
from digitalhub_core_kfp import step


def myhandler():
    step("echo", "Hello World!")