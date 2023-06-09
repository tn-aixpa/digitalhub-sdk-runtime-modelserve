"""
Common IO utils.
"""
import json
import shutil
from collections import OrderedDict
from io import BufferedReader, BytesIO, StringIO, TextIOBase, TextIOWrapper
from pathlib import Path
from typing import IO, Union

import yaml


####################
# Wrappers
####################


#  https://stackoverflow.com/questions/55889474/convert-io-stringio-to-io-bytesio
#  made by foobarna, improved by imporsen
class BytesIOWrapper(BufferedReader):
    """
    Wrap a buffered bytes stream over TextIOBase string stream.
    """

    def __init__(
        self,
        text_io_buffer: TextIOBase,
        encoding: str = None,
        errors: str = None,
        **kwargs
    ):
        """
        Wrap a buffered bytes stream over TextIOBase string stream.

        Parameters
        ----------
        text_io_buffer : TextIOBase
            The string stream to wrap.
        encoding : str, optional
            The encoding to use, by default None
        errors : str, optional
            ...
        """
        super().__init__(text_io_buffer, **kwargs)
        self.encoding = encoding or text_io_buffer.encoding or "utf-8"
        self.errors = errors or text_io_buffer.errors or "strict"

    def _encoding_call(self, method_name: str, *args, **kwargs) -> bytes:
        """
        Call a method of the raw stream, and encode the result.

        Parameters
        ----------
        method_name : str
            The name of the method to call.
        args : list
            The arguments to pass to the method.
        kwargs : dict
            The keyword arguments to pass to the method.

        Returns
        -------
        bytes
            The encoded result of the method call.
        """
        raw_method = getattr(self.raw, method_name)
        val = raw_method(*args, **kwargs)
        return val.encode(self.encoding, errors=self.errors)

    def read(self, size: int = -1) -> bytes:
        """
        Read bytes from the stream.

        Parameters
        ----------
        size : int, optional
            The number of bytes to read.

        Returns
        -------
        bytes
            The read bytes.
        """
        return self._encoding_call("read", size)

    def read1(self, size: int = -1) -> bytes:
        """
        Read bytes from the stream.

        Parameters
        ----------
        size : int, optional
            The number of bytes to read.

        Returns
        -------
        bytes
            The read bytes.
        """
        return self._encoding_call("read1", size)

    def peek(self, size: int = -1) -> bytes:
        """
        Peek bytes from the stream.

        Parameters
        ----------
        size : int, optional
            The number of bytes to peek.

        Returns
        -------
        bytes
            The peeked bytes.
        """
        return self._encoding_call("peek", size)


def wrap_bytes(src: IO) -> StringIO:
    """
    Wrap a BytesIO in a StringIO.

    Parameters
    ----------
    src : IO
        The source object to be wrapped.

    Returns
    -------
    StringIO
        The wrapped object.
    """
    if isinstance(src, BytesIO):
        return TextIOWrapper(src)
    return src


def wrap_string(src: IO) -> BytesIO:
    """
    Wrap a StringIO in a BytesIO.

    Parameters
    ----------
    src : IO
        The source object to be wrapped.

    Returns
    -------
    BytesIO
        The wrapped object.
    """
    if isinstance(src, StringIO):
        return BytesIOWrapper(src)
    return src


####################
# Writers
####################


def write_stringio(src: str) -> StringIO:
    """
    Write string in TextStream StringIO.

    Parameters
    ----------
    src : str
        The source string to be written.

    Returns
    -------
    StringIO
        The wrapped object.
    """
    stringio = StringIO()
    stringio.write(src)
    stringio.seek(0)
    return stringio


def write_bytesio(src: str) -> BytesIO:
    """
    Write string in ByteStream BytesIO.

    Parameters
    ----------
    src : str
        The source string to be written.

    Returns
    -------
    BytesIO
        The wrapped object.
    """
    bytesio = BytesIO()
    bytesio.write(src.encode())
    bytesio.seek(0)
    return bytesio


def write_json(data: dict, path: Union[str, Path]) -> None:
    """
    Store JSON file.

    Parameters
    ----------
    data : dict
        The data to be stored.
    path : Union[str, Path]
        The path to the file.

    Returns
    -------
    None
    """
    with open(path, "w") as file:
        json.dump(data, file)


def write_text(string: str, path: Union[str, Path]) -> None:
    """
    Write text on a file.

    Parameters
    ----------
    string : str
        The string to be written.
    path : Union[str, Path]
        The path to the file.

    Returns
    -------
    None
    """
    with open(path, "w") as file:
        file.write(string)


def write_bytes(byt: bytes, path: Union[str, Path]) -> None:
    """
    Write bytes on a file.

    Parameters
    ----------
    byt : bytes
        The bytes to be written.
    path : Union[str, Path]
        The path to the file.

    Returns
    -------
    None
    """
    with open(path, "wb") as file:
        file.write(byt)


def write_object(buff: IO, dst: str) -> None:
    """
    Write a buffer as file.

    Parameters
    ----------
    buff : IO
        The buffer to be written.
    dst : str
        The path to the file.

    Returns
    -------
    None
    """
    buff.seek(0)
    write_mode = "wb" if isinstance(buff, BytesIO) else "w"
    with open(dst, write_mode) as file:
        shutil.copyfileobj(buff, file)


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


####################
# Readers
####################


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


####################
# Utils
####################


def file_importer(path: str, filetype: str = "yaml") -> dict:
    """
    Import an object from a file using the specified file path.

    Parameters
    ----------
    path : str
        The absolute or relative path to the file containing the object.
    filetype : str, optional
        The type of file from which the object is imported. The default value is "yaml".

    Returns
    -------
    dict
        The object imported from the file using the specified path.
    """
    if filetype == "yaml":
        return read_yaml(path)
    else:
        raise NotImplementedError


def file_exporter(path: str, obj: dict, filetype: str = "yaml") -> None:
    """
    Export an object to a file using the specified file path.

    Parameters
    ----------
    path : str
        Path to the file to which the object is exported.
    obj : dict
        The object to be exported.
    filetype : str, optional
        The type of file to which the object is exported. The default value is "yaml".

    Returns
    -------
    None
    """
    if filetype == "yaml":
        write_yaml(obj, path)
    else:
        raise NotImplementedError
