from typing import Any

from sdk.client.client import Client
from sdk.utils.utils import read_yaml, write_yaml


def file_importer(path: str, obj: Any, fields: list) -> Any:
    dict_ = read_yaml(path)
    kwargs = {k: v for k, v in dict_.items() if k in fields}
    entity = obj(**kwargs)
    if "id" in dict_:
        entity.id = dict_["id"]
    return entity


def file_exporter(path: str, obj: Any) -> None:
    write_yaml(obj, path)


def delete_from_backend(client: Client, api: str) -> None:
    client.delete_object(api)
