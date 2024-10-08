from __future__ import annotations

import typing

from digitalhub_core.entities._base.spec.base import Spec, SpecParams
from digitalhub_core.entities.artifact.crud import get_artifact
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.entities.task.models import K8s
from digitalhub_core.entities.utils import parse_entity_key

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity.base import Entity


ENTITY_FUNC = {
    EntityTypes.ARTIFACT.value: get_artifact,
}


class RunSpec(Spec):
    """Run specification."""

    def __init__(
        self,
        task: str,
        local_execution: bool = False,
        function: str | None = None,
        node_selector: dict | None = None,
        volumes: list | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list | None = None,
        envs: list | None = None,
        secrets: list | None = None,
        profile: str | None = None,
        **kwargs,
    ) -> None:
        self.task = task
        self.local_execution = local_execution
        self.function = function
        self.node_selector = node_selector
        self.volumes = volumes
        self.resources = resources
        self.affinity = affinity
        self.tolerations = tolerations
        self.envs = envs
        self.secrets = secrets
        self.profile = profile

    def get_inputs(self, as_dict: bool = False) -> dict:
        """
        Get inputs.

        Returns
        -------
        dict
            The inputs.
        """
        inputs = {}
        if not hasattr(self, "inputs") or self.inputs is None:
            return inputs

        for parameter, item in self.inputs.items():
            parameter_type = self._parse_parameter(parameter)

            # Get entity from key
            if parameter_type == "key":
                key = self._collect_key(item)
                entity = self._collect_entity(key)
                if as_dict:
                    entity = entity.to_dict()
                inputs[parameter] = entity

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

    @staticmethod
    def _collect_key(item: str | dict) -> str:
        """
        Collect key from item.

        Parameters
        ----------
        item : str | dict
            Key or dict representation of the entity.

        Returns
        -------
        str
            The key.
        """
        if isinstance(item, str):
            return item
        return item.get("key")

    @staticmethod
    def _collect_entity(key: str) -> Entity:
        """
        Collect entity from key.

        Parameters
        ----------
        key : str
            Key of the entity.

        Returns
        -------
        Entity
            The entity.
        """
        _, entity_type, _, _, _ = parse_entity_key(key)
        return ENTITY_FUNC[entity_type](key)


class RunParams(SpecParams, K8s):
    """
    Run parameters.
    """

    function: str = None
    """The function associated with the run."""

    task: str = None
    """The task string associated with the run."""

    local_execution: bool = False
    """Flag to indicate if the run will be executed locally."""
