"""
DBT Runtime module.
"""
from sdk.runtimes.base import BaseRuntime


class DBTRuntime(BaseRuntime):
    def __init__(self) -> None:
        super().__init__()

    def get_enviroment(self) -> None:
        ...

    def parse_inputs(self, inputs: dict) -> None:
        ...

    def parse_outputs(self, outputs: dict) -> None:
        ...

    def parse_parameters(self, parameters: dict) -> None:
        ...

    def set_enviroment(self, environment: dict) -> None:
        ...

    def execute(self, inputs: dict, parameters: dict) -> None:
        ...

    def parse_results(self, results: dict) -> None:
        ...

    def persist_results(self, outputs: dict) -> None:
        ...
