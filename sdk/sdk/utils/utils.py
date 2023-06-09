from collections import OrderedDict
from pathlib import Path
from typing import Union
from uuid import uuid4

import yaml


def write_yaml(obj: dict, file: Union[str, Path]) -> None:
    """
    Write a dict to a yaml file.

    Parameters
    ----------
    obj : dict
        The dict to write.
    file : Union[str, Path]
        The yaml file path to write.

    Returns
    -------
    None
    """

    # Function needed to preserve the order of the keys in the yaml file.
    def ordered_dict_representer(self, value: OrderedDict) -> dict:
        """
        Represent an OrderedDict as a dict.

        Parameters
        ----------
        self : yaml.representer
            The yaml representer.
        value : OrderedDict
            The OrderedDict to represent.

        Returns
        -------
        dict
            The OrderedDict as a dict.
        """
        return self.represent_mapping("tag:yaml.org,2002:map", value.items())

    yaml.add_representer(OrderedDict, ordered_dict_representer)

    obj = OrderedDict(obj)
    with open(file, "w") as f:
        yaml.dump(obj, f)


def read_yaml(file: Union[str, Path]) -> dict:
    """
    Read a yaml file and return a dict.

    Parameters
    ----------
    file : Union[str, Path]
        The yaml file path to read.

    Returns
    -------
    dict
        The yaml file content.
    """
    with open(file, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


def get_uiid() -> str:
    """
    Create a uuid.

    Returns
    -------
    str
        The uuid.
    """
    return uuid4().hex
