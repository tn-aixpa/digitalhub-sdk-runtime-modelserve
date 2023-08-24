"""
S3Store module.
"""
from __future__ import annotations

import typing
from io import BytesIO
from typing import Type

import boto3
import botocore.client  # pylint: disable=unused-import
from botocore.exceptions import ClientError

from sdk.store.objects.base import Store
from sdk.utils.exceptions import StoreError
from sdk.utils.uri_utils import get_uri_netloc, get_uri_path

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
        return self._registry.get(src, self.fetch_artifact(src, dst))

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
            Returns the path of the downloaded artifact.
        """
        dst = dst if dst is not None else self._build_temp(src)
        key = self._get_key(src)
        return self._download_file(key, dst)

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
        Persist an artifact on S3 based storage. If the destination is not provided,
        the key will be extracted from the source path.

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
        key = self._get_key(dst) if dst is not None else self._get_key(src)
        return self._upload_file(src, key)

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
        if dst is None or not dst.endswith(".parquet"):
            dst = f"s3://{self._get_bucket()}/artifacts/data.parquet"
        fileobj = BytesIO()
        df.to_parquet(fileobj, index=False, **kwargs)
        key = self._get_key(dst)
        return self._upload_fileobj(fileobj, key)

    ############################
    # Private helper methods
    ############################

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
    def _get_key(path: str) -> str:
        """
        Build key.

        Parameters
        ----------
        path : str
            The source path to get the key from.

        Returns
        -------
        str
            The key.
        """
        key = get_uri_path(path)
        if key.startswith("/"):
            key = key[1:]
        return key

    def _check_factory(self) -> tuple[S3Client, str]:
        """
        Check if the S3 bucket is accessible by sending a head_bucket request.

        Returns
        -------
        tuple[S3Client, str]
            A tuple containing the S3 client object and the name of the S3 bucket.
        """
        client = self._get_client()
        bucket = self._get_bucket()
        self._check_access_to_storage(client, bucket)
        return client, bucket

    def _check_access_to_storage(self, client: S3Client, bucket: str) -> None:
        """
        Check if the S3 bucket is accessible by sending a head_bucket request.

        Parameters
        ----------
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

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

    def _download_file(self, key: str, dst: str) -> str:
        """
        Download a file from S3 based storage. The function checks if the bucket is accessible
        and if the destination directory exists. If the destination directory does not exist,
        it will be created.

        Parameters
        ----------
        key : str
            The key of the file on S3 based storage.
        dst : str
            The destination of the file on local filesystem.

        Returns
        -------
        str
            The path of the downloaded file.
        """
        client, bucket = self._check_factory()
        self._check_local_dst(dst)
        client.download_file(bucket, key, dst)
        return dst

    def _upload_file(self, src: str, key: str) -> str:
        """
        Upload a file to S3 based storage. The function checks if the bucket is accessible.

        Parameters
        ----------
        src : str
            The source path of the file on local filesystem.
        key : str
            The key of the file on S3 based storage.

        Returns
        -------
        str
            The URI of the uploaded file on S3 based storage.
        """
        client, bucket = self._check_factory()
        client.upload_file(Filename=src, Bucket=bucket, Key=key)
        return f"s3://{bucket}/{key}"

    def _upload_fileobj(self, fileobj: BytesIO, key: str) -> str:
        """
        Upload a fileobject to S3 based storage. The function checks if the bucket is accessible.

        Parameters
        ----------
        fileobj : BytesIO
            The fileobject to be uploaded.
        key : str
            The key of the file on S3 based storage.

        Returns
        -------
        str
            The URI of the uploaded fileobject on S3 based storage.
        """
        client, bucket = self._check_factory()
        client.put_object(Bucket=bucket, Key=key, Body=fileobj.getvalue())
        return f"s3://{bucket}/{key}"

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
            If no bucket is specified in the URI.
        """
        super()._validate_uri()
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
