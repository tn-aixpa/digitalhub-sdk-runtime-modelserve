from typing import Any

from sdk.client.client import Client
from sdk.utils.utils import read_yaml, write_yaml


def file_importer(path: str, obj: Any) -> Any:
    dict_ = read_yaml(path)
    entity = obj(**dict_)
    if "id" in dict_:
        entity.id = dict_["id"]
    return entity


def file_exporter(path: str, obj: Any) -> None:
    write_yaml(obj, path)


def delete_from_backend(client: Client, api: str) -> None:
    client.delete_object(api)
