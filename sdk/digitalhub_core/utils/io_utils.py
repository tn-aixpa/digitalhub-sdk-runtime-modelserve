"""
Common IO utils.
"""
from __future__ import annotations

import json
import shutil
from collections import OrderedDict
from io import BufferedReader, BytesIO, StringIO, TextIOBase, TextIOWrapper
from pathlib import Path
from typing import IO

import yaml

####################
# Wrappers
####################


#  https://stackoverflow.com/questions/55889474/convert-io-stringio-to-io-bytesio
#  made by foobarna, improved by imporsen
#  Documentation added with copilot
class BytesIOWrapper(BufferedReader):
    """
    Wrap a buffered bytes stream over TextIOBase string stream.
    """

    def __init__(
        self,
        text_io_buffer: TextIOBase,
        encoding: str | None = None,
        errors: str | None = None,
        **kwargs,
    ) -> None:
        """
        Keyword arguments.

        Wrap a buffered bytes stream over TextIOBase string stream.

        Parameters
        ----------
        text_io_buffer : TextIOBase
            The string stream to wrap.
        encoding : str
            The encoding to use, by default None
        errors : str
            ...
        **kwargs
            Keyword arguments.
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
        *args : list
            Arguments list.
        **kwargs
            Keyword arguments.

        Returns
        -------
        bytes
            The encoded result of the method call.
        """
        raw_method = getattr(self.raw, method_name)
        val = raw_method(*args, **kwargs)
        return val.encode(self.encoding, errors=self.errors)

    def read(self, size: int | None = -1) -> bytes:
        """
        Read bytes from the stream.

        Parameters
        ----------
        size : int
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
        size : int
            The number of bytes to read.

        Returns
        -------
        bytes
            The read bytes.
        """
        return self._encoding_call("read1", size)

    def peek(self, size: int = 0) -> bytes:
        """
        Peek bytes from the stream.

        Parameters
        ----------
        size : int
            The number of bytes to peek.

        Returns
        -------
        bytes
            The peeked bytes.
        """
        return self._encoding_call("peek", size)


def wrap_bytes(src: BytesIO | StringIO) -> TextIOWrapper | StringIO:
    """
    Wrap a BytesIO in a StringIO.

    Parameters
    ----------
    src : BytesIO | StringIO
        The source object to be wrapped.

    Returns
    -------
    TextIOWrapper | StringIO
        The wrapped object.
    """
    if isinstance(src, BytesIO):
        return TextIOWrapper(src)
    return src


def wrap_string(src: BytesIO | StringIO) -> BytesIOWrapper | BytesIO:
    """
    Wrap a StringIO in a BytesIO.

    Parameters
    ----------
    src : BytesIO | StringIO
        The source object to be wrapped.

    Returns
    -------
    BytesIOWrapper | BytesIO
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
        The source string to be wrapped.

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
        The source string to be wrapped.

    Returns
    -------
    BytesIO
        The wrapped object.
    """
    bytesio = BytesIO()
    bytesio.write(src.encode())
    bytesio.seek(0)
    return bytesio


def write_json(data: dict, path: str | Path) -> None:
    """
    Store JSON file.

    Parameters
    ----------
    data : dict
        The data to be stored.
    path : str | Path
        The path to the file.

    Returns
    -------
    None
    """
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)


def write_text(string: str, path: str | Path) -> None:
    """
    Write text on a file.

    Parameters
    ----------
    string : str
        The string to be written.
    path : str | Path
        The path to the file.

    Returns
    -------
    None
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write(string)


def write_bytes(byt: bytes, path: str | Path) -> None:
    """
    Write bytes on a file.

    Parameters
    ----------
    byt : bytes
        The bytes to be written.
    path : str | Path
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


def write_yaml(obj: dict, file: str | Path) -> None:
    """
    Write a dict to a yaml file.

    Parameters
    ----------
    obj : dict
        The dict to write.
    file : str | Path
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
    with open(file, "w", encoding="utf-8") as out_file:
        yaml.dump(obj, out_file)


####################
# Readers
####################


def read_yaml(file: str | Path) -> dict:
    """
    Read a yaml file and return a dict.

    Parameters
    ----------
    file : str | Path
        The yaml file path to read.

    Returns
    -------
    dict
        The yaml file content.
    """
    with open(file, "r", encoding="utf-8") as in_file:
        data = yaml.load(in_file, Loader=yaml.SafeLoader)
    return data


def read_bytes(file: str | Path) -> bytes:
    """
    Read a file and return the bytes.

    Parameters
    ----------
    file : str | Path
        The file path to read.

    Returns
    -------
    bytes
        The file content.
    """
    with open(file, "rb") as in_file:
        data = in_file.read()
    return data


def read_text(file: str | Path) -> str:
    """
    Read a file and return the text.

    Parameters
    ----------
    file : str | Path
        The file path to read.

    Returns
    -------
    str
        The file content.
    """
    with open(file, "r", encoding="utf-8") as in_file:
        data = in_file.read()
    return data
