"""
Run base specification module.
"""
from __future__ import annotations

import typing
from typing import Union

from digitalhub_core.entities._base.spec import Spec, SpecParams
from digitalhub_core.entities.artifacts.crud import get_artifact_from_key
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import parse_entity_key

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity


ENTITY_FUNC = {
    "artifacts": get_artifact_from_key,
}


class RunSpec(Spec):
    """Run specification."""

    def __init__(
        self,
        task: str,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        values: list | None = None,
        local_execution: bool = False,
    ) -> None:
        """
        Constructor.
        """
        self.task = task
        self.inputs = inputs
        self.outputs = outputs
        self.parameters = parameters
        self.values = values
        self.local_execution = local_execution

    def get_inputs(self, as_dict: bool = False) -> list[dict[str, Entity]]:
        """
        Get inputs.

        Returns
        -------
        list[dict[str, Entity]]
            The inputs.
        """
        inputs = []
        if self.inputs is None:
            return inputs

        for i in self.inputs:
            for parameter, item in i.items():
                parameter_type = self._parse_parameter(parameter)

                # Get entity from key
                if parameter_type == "key":
                    entity = self._collect_entity(item)
                    if as_dict:
                        entity = entity.to_dict()
                    inputs.append({parameter: entity})

                # Create entity from parameter
                elif parameter_type == "create":
                    raise NotImplementedError

        return inputs

    @staticmethod
    def _parse_parameter(parameter: str) -> str:
        """
        Parse parameter.

        Parameters
        ----------
        parameter : str
            Parameter.

        Returns
        -------
        str
            The parsed parameter.
        """
        if len(parameter.split(":")) == 1:
            return "key"
        return "create"

    def _collect_entity(self, item: str | dict) -> Entity:
        """
        Collect entity from key.

        Parameters
        ----------
        item : str | dict
            Key or dict representation of the entity.

        Returns
        -------
        Entity
            The entity.
        """
        # Get key
        if isinstance(item, str):
            key = item
        else:
            key = item.get("key")
        if not key.startswith("store://"):
            raise EntityError(f"Invalid entity key: {key}")

        # Get entity
        _, entity_type, _, _, _ = parse_entity_key(key)
        return ENTITY_FUNC[entity_type](key)

    @staticmethod
    def _parse_input_key(key: str) -> tuple:
        """
        Parse input parameter.

        Parameters
        ----------
        key : str
            Input key.

        Returns
        -------
        tuple
            The parsed parameter.
        """
        # Get parameter name
        splitted = key.split(":")
        parameter = splitted[0]

        try:
            splitted = splitted[1].split(".")
        except IndexError:
            return parameter, None, None

        # Get entity type
        if len(splitted) == 1:
            return parameter, splitted[0], None

        # Get entity kind
        return parameter, splitted[0], splitted[1]


class RunParams(SpecParams):
    """
    Run parameters.
    """

    task: str = None
    """The task string associated with the run."""

    inputs: list[dict[str, Union[str, dict]]] = None
    """Run inputs."""

    outputs: list[dict[str, Union[str, dict]]] = None
    """Run outputs."""

    parameters: dict = None
    """Parameters to be used in the run."""

    values: list = None
    """Values to be used in the run."""

    local_execution: bool = False
    """Flag to indicate if the run will be executed locally."""
