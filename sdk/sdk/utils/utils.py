from collections import OrderedDict
from pathlib import Path
from typing import Union
from uuid import uuid4

import yaml


def write_yaml(obj: dict, file: Union[str, Path]) -> None:
    def ordered_dict_representer(self, value):
        return self.represent_mapping("tag:yaml.org,2002:map", value.items())

    yaml.add_representer(OrderedDict, ordered_dict_representer)

    obj = OrderedDict(obj)
    with open(file, "w") as f:
        yaml.dump(obj, f)


def read_yaml(file: Union[str, Path]) -> dict:
    with open(file, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


def get_uiid() -> str:
    """
    Return an UUID.
    """
    return uuid4().hex
