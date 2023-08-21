"""
S3Store module.
"""
from __future__ import annotations

import typing
from io import BytesIO
from tempfile import mkdtemp
from typing import Type

import boto3
import botocore.client  # pylint: disable=unused-import
from botocore.exceptions import ClientError

from sdk.store.objects.base import Store
from sdk.utils.exceptions import StoreError
from sdk.utils.file_utils import check_make_dir, get_dir
from sdk.utils.uri_utils import (
    build_key,
    get_name_from_uri,
    get_uri_netloc,
    get_uri_path,
    get_uri_scheme,
)

if typing.TYPE_CHECKING:
    import pandas as pd


# Type aliases
S3Client = Type["botocore.client.S3"]


class S3Store(Store):
    """
    S3 store class. It implements the Store interface and provides methods to fetch and persist
    artifacts on S3 based storage.
    """

    ############################
    # IO methods
    ############################

    def download(self, src: str, dst: str | None = None) -> str:
        """
        Download an artifact from S3 based storage.

        See Also
        --------
        fetch_artifact
        """
        return self.fetch_artifact(src, dst)

    def fetch_artifact(self, src: str, dst: str | None = None) -> str:
        """
        Fetch an artifact from S3 based storage. If the destination is not provided,
        a temporary directory will be created and the artifact will be saved there.

        Parameters
        ----------
        src : str
            The source location of the artifact.
        dst : str
            The destination of the artifact on local filesystem.

        Returns
        -------
        str
            Returns a file path.
        """
        if dst is None:
            tmpdir = mkdtemp()
            dst = f"{tmpdir}/{get_name_from_uri(src)}"
            self._register_resource(f"{src}", dst)

        # Get client
        client = self._get_client()
        bucket = get_uri_netloc(self.uri)

        # Check store access
        self._check_access_to_storage(client, bucket)
        key = get_uri_path(src)

        # Check if local destination exists
        self._check_local_dst(dst)

        # Get the file from S3 and save it locally
        client.download_file(bucket, key, dst)
        return dst

    def upload(self, src: str, dst: str | None = None) -> str:
        """
        Upload an artifact to S3 based storage.

        See Also
        --------
        persist_artifact
        """
        return self.persist_artifact(src, dst)

    def persist_artifact(self, src: str, dst: str | None = None) -> str:
        """
        Persist an artifact on S3 based storage.

        Parameters
        ----------
        src : Any
            The source object to be persisted. It can be a file path as a string or Path object.

        dst : str
            The destination partition for the artifact.

        Returns
        -------
        str
            Returns the URI of the artifact on S3 based storage.
        """
        if dst is None:
            dst = get_name_from_uri(src)

        # Get client
        client = self._get_client()
        bucket = self._get_bucket()

        # Check store access
        self._check_access_to_storage(client, bucket)

        # Rebuild key from target path
        key = build_key(dst)

        # Upload file to S3
        client.upload_file(Filename=src, Bucket=bucket, Key=key)
        return f"s3://{bucket}/{key}"

    def write_df(self, df: pd.DataFrame, dst: str | None = None, **kwargs) -> str:
        """
        Write a dataframe to S3 based storage. Kwargs are passed to df.to_parquet().

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe.
        dst : str
            The destination path on S3 based storage.
        **kwargs
            Keyword arguments.

        Returns
        -------
        str
            The path S3 path where the dataframe was saved.
        """
        # Get client and bucket
        client = self._get_client()
        bucket = self._get_bucket()

        # Check store access
        self._check_access_to_storage(client, bucket)

        # Set destination if not provided
        if dst is None or not dst.endswith(".parquet"):
            dst = f"{self.get_root_uri()}/{self.name}.parquet"

        # Rebuild key from target path
        key = get_uri_path(dst)

        # Write dataframe to buffer
        out_buffer = BytesIO()
        df.to_parquet(out_buffer, index=False, **kwargs)

        # Write buffer to S3 as parquet
        client.put_object(Bucket=bucket, Key=key, Body=out_buffer.getvalue())

        # Return uri where dataframe was saved
        return f"s3://{bucket}/{key}"

    ############################
    # Private helper methods
    ############################

    def _get_scheme(self) -> str:
        """
        Get the URI scheme.

        Returns
        -------
        str
            The URI scheme.
        """
        return get_uri_scheme(self.uri)

    def _get_bucket(self) -> str:
        """
        Get the name of the S3 bucket from the URI.

        Returns
        -------
        str
            The name of the S3 bucket.
        """
        return get_uri_netloc(self.uri)

    def _get_client(self) -> S3Client:
        """
        Get an S3 client object.

        Returns
        -------
        S3Client
            Returns a client object that interacts with the S3 storage service.
        """
        return boto3.client("s3", **self.config)

    @staticmethod
    def _check_access_to_storage(client: S3Client, bucket: str) -> None:
        """
        Check if the S3 bucket is accessible by sending a head_bucket request.

        Parameters
        ----------
        client: S3Client
            An instance of 'S3Client' class that provides client interfaces to S3 service.
        bucket: string
            A string representing the name of the S3 bucket for which access needs to be checked.

        Returns
        -------
        None

        Raises
        ------
        StoreError:
            If access to the specified bucket is not available.
        """
        try:
            client.head_bucket(Bucket=bucket)
        except ClientError as exc:
            raise StoreError("No access to s3 bucket!") from exc

    @staticmethod
    def _check_local_dst(dst: str) -> None:
        """
        Check if the local destination directory exists. Create in case it does not.

        Parameters
        ----------
        dst : str
            The destination directory.

        Returns
        -------
        None
        """
        if get_uri_scheme(dst) in ["", "file"]:
            dst_dir = get_dir(dst)
            check_make_dir(dst_dir)

    ############################
    # Store interface methods
    ############################

    def _validate_uri(self) -> None:
        """
        Validate the URI of the store.

        Returns
        -------
        None

        Raises
        ------
        StoreError
            If the URI scheme is not 's3'.

        StoreError
            If no bucket is specified in the URI.
        """
        if self._get_scheme() != "s3":
            raise StoreError("Invalid URI scheme for s3 store!")
        if self._get_bucket() == "":
            raise StoreError("No bucket specified in the URI for s3 store!")

    @staticmethod
    def is_local() -> bool:
        """
        Check if the store is local.

        Returns
        -------
        bool
            False
        """
        return False

    def get_root_uri(self) -> str:
        """
        Get the root URI of the store.

        Returns
        -------
        str
            The root URI of the store.
        """
        return f"s3://{self._get_bucket()}"
