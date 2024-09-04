from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Type
from urllib.parse import urlparse

import boto3
import botocore.client  # pylint: disable=unused-import
from botocore.exceptions import ClientError
from digitalhub_core.stores.objects.base import Store, StoreConfig
from digitalhub_core.utils.exceptions import StoreError
from digitalhub_core.utils.file_utils import get_file_info_from_s3, get_file_mime_type

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

    ##############################
    # IO methods
    ##############################

    def download(
        self,
        src: list[tuple[str, str | None]],
        dst: str | None = None,
        overwrite: bool = False,
    ) -> list[str]:
        """
        Download artifacts from S3 storage.

        Parameters
        ----------
        src : list[tuple[str, str | None]]
            The source location of the artifact on s3 and eventual origin tree path.
        dst : str
            The destination of the artifact on local filesystem.
        overwrite : bool
            Specify if overwrite existing file(s).

        Returns
        -------
        list[str]
            List of paths of the downloaded artifacts.
        """
        client, bucket = self._check_factory()

        # Handle destination

        # If destination is not specified, build destination
        # as a temporary directory
        if dst is None:
            dst = self._build_temp()

        # Otherwise, check if the destination is local,
        else:
            self._check_local_dst(dst)

        dst_path = Path(dst)

        paths = []
        for s in src:

            # Cycle over keys and original tree paths
            key = self._get_key(s[0])
            tree_path = s[1]

            if key.endswith("/"):
                p = self._download_files(key, tree_path, dst_path, client, bucket, overwrite)
            else:
                p = [self._download_file(key, tree_path, dst_path, client, bucket, overwrite)]
            paths.extend(p)

        return paths

    def upload(self, src: str, dst: str | None = None) -> list[tuple[str, str]]:
        """
        Upload an artifact to storage.

        Parameters
        ----------
        src : str
            The source location of the artifact on local filesystem.
        dst : str
            The destination of the artifact on storage.

        Returns
        -------
        list[str]
            Returns the list of source and destination paths of the
            uploaded artifacts.
        """
        # Destination handling

        # If no destination is provided, build key from source
        # Otherwise build key from destination
        if dst is None:
            dst = self._get_key(src)
        else:
            dst = self._get_key(dst)

        # Source handling

        self._check_local_src(src)
        src_is_dir = Path(src).is_dir()

        # If source is a directory, destination must be a partition
        if src_is_dir and not dst.endswith("/"):
            raise StoreError("Destination must be a partition if the source is a directory.")

        # If source is a file and destination is a partition,
        # build key from source
        if not src_is_dir and dst.endswith("/"):
            dst = f"{dst}{self._get_key(src)}"

        client, bucket = self._check_factory()

        if src_is_dir:
            return self._upload_files(src, dst, client, bucket)
        return [self._upload_file(src, dst, client, bucket)]

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

    def get_file_info(self, paths: list[tuple[str, str]]) -> list[dict]:
        """
        Method to get file metadata.

        Parameters
        ----------
        paths : list
            The list of destination and source paths.

        Returns
        -------
        list[dict]
            Returns files metadata.
        """
        client, bucket = self._check_factory()

        infos = []
        for i in paths:
            s3_path, src_path = i

            # Get metadata
            key = self._get_key(s3_path)
            metadata = client.head_object(Bucket=bucket, Key=key)

            # Get file info
            info = get_file_info_from_s3(s3_path, src_path, metadata)
            infos.append(info)

        return infos

    ##############################
    # Private I/O methods
    ##############################

    def _download_files(
        self,
        key: str,
        tree_path: str | None,
        dst: Path,
        client: S3Client,
        bucket: str,
        overwrite: bool,
    ) -> list[str]:
        """
        Download files from S3 partition.

        Parameters
        ----------
        key : str
            The key partition.
        tree_path : str
            Original source tree path.
        dst : str
            The destination of the files on local filesystem.
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.
        overwrite : bool
            Whether to overwrite existing files.

        Returns
        -------
        list[str]
            The list of paths of the downloaded files.
        """
        # If downloadding from a partition, destination must be a directory
        if not dst.is_dir():
            raise StoreError("Destination must be a directory if the source is a directory.")

        # List keys under the partition
        file_list = client.list_objects_v2(Bucket=bucket, Prefix=key).get("Contents", [])
        keys = [f["Key"] for f in file_list]

        paths = []
        for k in keys:
            # If original source is not specified, use the key as path
            if tree_path is None:
                dst_pth = Path(dst, k)
            else:
                dst_pth = Path(dst, tree_path)

            # Build destination path
            self._build_path(dst_pth.parent)

            # Check if destination path already exists
            dst_pth = str(dst_pth)
            self._check_overwrite(dst_pth, overwrite)

            # Download file
            client.download_file(bucket, k, dst_pth)
            paths.append(dst_pth)
        return paths

    def _download_file(
        self,
        key: str,
        tree_path: str | None,
        dst: Path,
        client: S3Client,
        bucket: str,
        overwrite: bool,
    ) -> str:
        """
        Download a file from S3 based storage. The function checks if the bucket is accessible
        and if the destination directory exists. If the destination directory does not exist,
        it will be created.

        Parameters
        ----------
        key : str
            The key of the file on S3 based storage.
        tree_path : str
            Original source tree path.
        dst : str
            The destination of the file on local filesystem.
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.
        overwrite : bool
            Whether to overwrite existing files.

        Returns
        -------
        str
            The path of the downloaded file.
        """
        # If original source is not specified,
        # use the key as path
        if tree_path is None:
            tree_path = key

        # Build destination path
        if dst.suffix == "" and not Path(tree_path).is_absolute():
            dst_pth = Path(dst, tree_path)
        else:
            dst_pth = Path(dst, key)

        self._build_path(dst_pth.parent)

        # Check if destination path already exists
        dst_pth = str(dst_pth)
        self._check_overwrite(dst_pth, overwrite)

        # Download file
        client.download_file(bucket, key, dst_pth)
        return dst_pth

    def _upload_files(self, src: str, dst: str, client: S3Client, bucket: str) -> list[tuple[str, str]]:
        """
        Upload files to S3 based storage. The function checks if the bucket is accessible.

        Parameters
        ----------
        src : str
            The source path of the files on local filesystem.
        dst : str
            The destination of the files on S3 based storage.
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

        Returns
        -------
        list[tuple[str, str]]
            A list of tuples containing the path of the uploaded files
            and the path of the original files.
        """
        path_src = Path(src)
        paths = []
        files = [i for i in path_src.rglob("*") if i.is_file()]

        for file in files:
            key = self._get_key(str(file.relative_to(path_src)))
            built_key = f"{dst}{key}"
            paths.append(self._upload_file(str(file), built_key, client, bucket))

        return paths

    @staticmethod
    def _upload_file(src: str, key: str, client: S3Client, bucket: str) -> tuple[str, str]:
        """
        Upload a file to S3 based storage. The function checks if the
        bucket is accessible.

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
        tuple[str, str]
            A tuple containing the URI of the uploaded file
            and the path of the original file.
        """
        extra_args = {}
        mime_type = get_file_mime_type(src)
        if mime_type is not None:
            extra_args["ContentType"] = mime_type

        client.upload_file(Filename=src, Bucket=bucket, Key=key, ExtraArgs=extra_args)
        return f"s3://{bucket}/{key}", src

    @staticmethod
    def _upload_fileobject(fileobj: BytesIO, key: str, client: S3Client, bucket: str) -> str:
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

    ##############################
    # Private helper methods
    ##############################

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
        key = urlparse(path).path.replace("\\", "/")
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
