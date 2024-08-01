from __future__ import annotations

from pathlib import Path
from typing import Any

from digitalhub_data.datastores.objects.base import Datastore
from digitalhub_data.readers.builder import get_reader_by_object


class LocalDatastore(Datastore):
    """
    Local Datastore class.
    """

    def write_df(self, df: Any, dst: str, extension: str | None = None, **kwargs) -> str:
        """
        Method to write a dataframe to a file. Kwargs are passed to df.to_parquet().
        If destination is not provided, the dataframe is written to the default
        store path with generated name.

        Parameters
        ----------
        df : Any
            The dataframe to write.
        dst : str
            The destination of the dataframe.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        str
            Path of written dataframe.
        """
        self.store._check_local_dst(dst)
        self._validate_extension(Path(dst).suffix.removeprefix("."))

        # Write dataframe
        reader = get_reader_by_object(df)
        reader.write_df(df, dst, extension=extension, **kwargs)

        return dst
