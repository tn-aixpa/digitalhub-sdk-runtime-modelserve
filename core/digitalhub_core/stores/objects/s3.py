from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Type
from urllib.parse import urlparse
import glob

import boto3
import botocore.client  # pylint: disable=unused-import
from botocore.exceptions import ClientError
from digitalhub_core.stores.objects.base import Store, StoreConfig
from digitalhub_core.utils.file_utils import get_file_info_from_s3

# Type aliases
S3Client = Type["botocore.client.S3"]


class S3StoreConfig(StoreConfig):
    """
    S3 store configuration class.
    """

    endpoint_url: str
    """S3 endpoint URL."""

    aws_access_key_id: str
    """AWS access key ID."""

    aws_secret_access_key: str
    """AWS secret access key."""

    bucket_name: str
    """S3 bucket name."""


class S3Store(Store):
    """
    S3 store class. It implements the Store interface and provides methods to fetch and persist
    artifacts on S3 based storage.
    """

    def __init__(self, name: str, store_type: str, config: S3StoreConfig) -> None:
        super().__init__(name, store_type)
        self.config = config

    ############################
    # IO methods
    ############################

    def download(self, src: str, dst: str | None = None, force: bool = False, overwrite: bool = False) -> str:
        """
        Download an artifact from S3 based storage.

        See Also
        --------
        fetch_artifact
        """
        if dst is None:
            dst = self._build_temp(src)
        else:
            self._check_local_dst(dst)
            if Path(dst).suffix != "":
                self._check_overwrite(dst, overwrite)
            self._build_path(dst)

        if force:
            return self.fetch_artifact(src, dst)
        return self._registry.get(src, self.fetch_artifact(src, dst))

    def fetch_artifact(self, src: str, dst: str) -> str:
        """
        Fetch an artifact from S3 based storage. If the destination is not provided,
        a temporary directory will be created and the artifact will be saved there.

        Parameters
        ----------
        src : str
            The source location of the artifact on S3.
        dst : str
            The destination of the artifact on local filesystem.

        Returns
        -------
        str
            Returns the path of the downloaded artifact.
        """
        parsed = urlparse(src)
        bucket = parsed.netloc
        client = self._get_client()
        self._check_access_to_storage(client, bucket)

        if Path(parsed.path).suffix == "":
            path = self._download_files(parsed.path, dst, client, bucket)
        else:
            path = self._download_file(parsed.path, dst, client, bucket)
        self._set_path_registry(src, path)
        return path

    def upload(self, src: str, dst: str | None = None) -> str:
        """
        Upload an artifact to S3 based storage.

        See Also
        --------
        persist_artifact
        """
        self._check_local_src(src)
        if dst is None:
            key = self._get_key(src)
        else:
            key = self._get_key(dst)
        return self.persist_artifact(src, key)

    def upload_fileobject(self, src: BytesIO, dst: str) -> str:
        """
        Upload an BytesIO to S3 based storage.

        Parameters
        ----------
        src : BytesIO
            The source object to be persisted.
        dst : str
            The destination partition for the artifact.

        Returns
        -------
        str
            Returns the URI of the artifact on S3 based storage.
        """
        client, bucket = self._check_factory()
        return self._upload_fileobject(src, dst, client, bucket)

    def persist_artifact(self, src: str, dst: str) -> str:
        """
        Persist an artifact on S3 based storage. If the destination is not provided,
        the key will be extracted from the source path.

        Parameters
        ----------
        src : Any
            The source object to be persisted.
        dst : str
            The destination partition for the artifact.

        Returns
        -------
        str
            Returns the URI of the artifact on S3 based storage.
        """
        client, bucket = self._check_factory()
        if Path(src).suffix == "":
            return self._upload_files(src, dst, client, bucket)
        return self._upload_file(src, dst, client, bucket)

    def get_file_info(self, path: str, src_path: str | None = None) -> list:
        """
        Method to get file metadata.

        Parameters
        ----------
        path : str
            The path of the file.
        src_path : str
            The source path of the file.

        Returns
        -------
        list
            Returns files metadata.
        """
        client, bucket = self._check_factory()
        key = self._get_key(path)
        if Path(path).suffix == "":
            try:
                # check if the key exists (file without extension)
                client.head_object(Bucket=bucket, Key=key)
                keys = [key]
            except ClientError:
                file_list = client.list_objects_v2(Bucket=bucket, Prefix=key).get("Contents", [])
                keys = [i["Key"] for i in file_list]
        else:
            keys = [key]

        infos = []
        for key in keys:
            metadata = client.head_object(Bucket=bucket, Key=key)
            key = f"s3://{bucket}/{key}"
            infos.append(get_file_info_from_s3(metadata, key))
        return infos

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
        return str(self.config.bucket_name)

    def _get_client(self) -> S3Client:
        """
        Get an S3 client object.

        Returns
        -------
        S3Client
            Returns a client object that interacts with the S3 storage service.
        """
        cfg = {
            "endpoint_url": self.config.endpoint_url,
            "aws_access_key_id": self.config.aws_access_key_id,
            "aws_secret_access_key": self.config.aws_secret_access_key,
        }
        return boto3.client("s3", **cfg)

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
        key = urlparse(path).path
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
        ClientError:
            If access to the specified bucket is not available.
        """
        try:
            client.head_bucket(Bucket=bucket)
        except ClientError as e:
            raise ClientError("No access to s3 bucket!") from e

    ############################
    # Private I/O methods
    ############################

    def _download_files(self, path: str, dst: str, client: S3Client, bucket: str) -> str:
        """
        Download files from S3 based storage. The function checks if the bucket is accessible
        and if the destination directory exists. If the destination directory does not exist,
        it will be created.

        Parameters
        ----------
        path : str
            The path of the files on S3 based storage.
        dst : str
            The destination of the files on local filesystem.
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

        Returns
        -------
        str
            The path of the downloaded files.
        """
        path = path.removeprefix("/")
        file_list = client.list_objects_v2(Bucket=bucket, Prefix=path).get("Contents", [])
        for file in file_list:
            dst_pth = Path(dst) / Path(file["Key"])
            dst_pth.parent.mkdir(parents=True, exist_ok=True)
            client.download_file(bucket, file["Key"], str(dst_pth))
        return dst

    def _download_file(self, path: str, dst: str, client: S3Client, bucket: str) -> str:
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
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

        Returns
        -------
        str
            The path of the downloaded file.
        """
        path = path.removeprefix("/")
        dst_pth = str(Path(dst) / Path(path))
        client.download_file(bucket, path, dst_pth)
        return dst_pth

    def _upload_files(self, src: str, key: str, client: S3Client, bucket: str) -> str:
        """
        Upload files to S3 based storage. The function checks if the bucket is accessible.

        Parameters
        ----------
        src : str
            The source path of the files on local filesystem.
        key : str
            The key of the files on S3 based storage.
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

        Returns
        -------
        str
            The URI of the uploaded files on S3 based storage.
        """
        client, bucket = self._check_factory()
        paths = list(Path(src).rglob("*"))
        files = [i for i in paths if i.is_file()]
        for file in files:
            built_key = str(Path(key) / Path(file))
            client.upload_file(Filename=str(file), Bucket=bucket, Key=built_key)
        return f"s3://{bucket}/{key}"

    def _upload_file(self, src: str, key: str, client: S3Client, bucket: str) -> str:
        """
        Upload a file to S3 based storage. The function checks if the bucket is accessible.

        Parameters
        ----------
        src : str
            The source path of the file on local filesystem.
        key : str
            The key of the file on S3 based storage.
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

        Returns
        -------
        str
            The URI of the uploaded file on S3 based storage.
        """
        client.upload_file(Filename=src, Bucket=bucket, Key=key)
        return f"s3://{bucket}/{key}"

    def _upload_fileobject(self, fileobj: BytesIO, key: str, client: S3Client, bucket: str) -> str:
        """
        Upload a fileobject to S3 based storage. The function checks if the bucket is accessible.

        Parameters
        ----------
        fileobj : BytesIO
            The fileobject to be uploaded.
        key : str
            The key of the file on S3 based storage.
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

        Returns
        -------
        str
            The URI of the uploaded fileobject on S3 based storage.
        """
        client.put_object(Bucket=bucket, Key=key, Body=fileobj.getvalue())
        return f"s3://{bucket}/{key}"

    ############################
    # Store interface methods
    ############################

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
