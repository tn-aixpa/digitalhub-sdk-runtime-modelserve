from sdk.utils.utils import read_yaml, write_yaml


def file_importer(path: str) -> dict:
    return read_yaml(path)


def file_exporter(path: str, obj: dict) -> None:
    write_yaml(obj, path)


def parse_api_response(r: dict) -> None:
    if "status" in r:
        raise Exception(r)
