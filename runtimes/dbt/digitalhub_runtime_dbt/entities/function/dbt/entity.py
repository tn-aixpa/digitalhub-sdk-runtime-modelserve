from __future__ import annotations

import typing

from digitalhub.entities.function._base.entity import Function
from digitalhub.utils.generic_utils import decode_string
from digitalhub.utils.io_utils import write_text, write_yaml
from digitalhub.utils.uri_utils import map_uri_scheme

if typing.TYPE_CHECKING:
    from digitalhub_runtime_dbt.entities.function.dbt.spec import FunctionSpecDbt
    from digitalhub_runtime_dbt.entities.function.dbt.status import FunctionStatusDbt

    from digitalhub.entities._base.entity.metadata import Metadata


class FunctionDbt(Function):
    """
    FunctionDbt class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: FunctionSpecDbt,
        status: FunctionStatusDbt,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: FunctionSpecDbt
        self.status: FunctionStatusDbt

    def export(self, filename: str | None = None) -> str:
        """
        Export object as a YAML file.

        Parameters
        ----------
        filename : str
            Filename to export object to. If None, the object is exported to the
            default filename.

        Returns
        -------
        str
        """
        obj = self.to_dict()

        # Strip base64 from source at following conditions:
        # - base64 is not None
        # - source is local path
        base64 = obj.get("spec", {}).get("source", {}).get("base64")
        source = obj.get("spec", {}).get("source", {}).get("source")
        if base64 is not None and source is not None and map_uri_scheme(source) == "local":
            obj["spec"]["source"].pop("base64")
            src_pth = self._context().root / source
            write_text(src_pth, decode_string(base64))

        if filename is None:
            filename = f"{self.ENTITY_TYPE}-{self.name}-{self.id}.yml"
        pth = self._context().root / filename
        write_yaml(pth, obj)
        return str(pth)
