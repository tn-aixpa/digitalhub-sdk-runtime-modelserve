from sdk.utils.utils import read_yaml, write_yaml


def file_importer(path: str, obj: object) -> object:
    dict_ = read_yaml(path)
    entity = obj(**dict_)
    if "id" in dict_:
        entity.id = dict_["id"]
    return entity


def file_exporter(path: str, obj: dict) -> None:
    write_yaml(obj, path)
