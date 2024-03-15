"""
RunStatus class module.
"""
from __future__ import annotations

import typing

from digitalhub_core.entities._base.status import Status
from digitalhub_core.entities.artifacts.crud import get_artifact_from_key
from digitalhub_core.utils.generic_utils import parse_entity_key

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity

ENTITY_FUNC = {
    "artifacts": get_artifact_from_key,
}


class RunStatus(Status):
    """
    Status class for run entities.
    """

    def __init__(
        self,
        state: str,
        message: str | None = None,
        outputs: list | None = None,
        values: list | None = None,
        results: dict | None = None,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(state, message)
        self.outputs = outputs
        self.values = values
        self.results = results

    def get_results(self) -> dict:
        """
        Get results.

        Returns
        -------
        dict
            The results.
        """
        return self.results if self.results is not None else {}

    def get_outputs(self, as_key: bool = False, as_dict: bool = False) -> list[dict[str, str | dict | Entity]]:
        """
        Get outputs.

        Returns
        -------
        list[dict[str, str | dict | Entity]]
            The outputs.
        """
        outputs = []
        if self.outputs is None:
            return outputs
        for i in self.outputs:
            for k, v in i.items():
                _, entity_type, _, _, _ = parse_entity_key(v)
                if v.startswith("store://"):
                    entity = ENTITY_FUNC[entity_type](v)
                    if as_key:
                        entity = entity.key
                    if as_dict:
                        entity = entity.to_dict()
                    outputs.append({k: entity})
                else:
                    raise ValueError(f"Invalid entity key: {v}")
        return outputs

    def get_values(self) -> list:
        """
        Get values.

        Returns
        -------
        list
            The values.
        """
        return self.values if self.values is not None else []
