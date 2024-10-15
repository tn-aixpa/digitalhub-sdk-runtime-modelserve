from __future__ import annotations

import os
import typing

if typing.TYPE_CHECKING:
    pass


def get_s3_bucket() -> str | None:
    """
    Function to get S3 bucket name.

    Returns
    -------
    str
        The S3 bucket name.
    """
    return os.getenv("S3_BUCKET_NAME", "datalake")
