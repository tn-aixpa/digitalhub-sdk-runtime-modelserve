from tempfile import TemporaryDirectory
from pathlib import Path
from typing import Optional, Type

import boto3
import botocore.client
from botocore.exceptions import ClientError

from sdk.store.objects.store import Store
from sdk.utils.file_utils import check_make_dir, check_path, get_path
from sdk.utils.io_utils import write_bytes
from sdk.utils.uri_utils import (
    build_key,
    get_name_from_uri,
    get_uri_netloc,
    get_uri_path,
)

S3Client = Type["botocore.client.S3"]


class S3Store(Store):
    def __init__(
        self,
        name: str,
        type: str,
        config: Optional[dict] = None,
    ) -> None:
        super().__init__(name, type, config)

    def fetch_artifact(self, src: str, dst: str = None) -> str:
        """
        Method to fetch an artifact from the backend and to register it on the paths registry.

        Parameters:
        -----------
        src : str
            The source location of the artifact.
        dst : str, optional
            The destination of the artifact on local filesystem.

        Returns:
        --------
        str
            Returns a file path.
        """
        if dst is None:
            dst = TemporaryDirectory().name

        client = self._get_client()
        bucket = get_uri_netloc(src)
        self._check_access_to_storage(client, bucket)
        key = get_uri_path(src)

        # Get the file from S3 and save it locally
        obj = self._get_data(client, bucket, key)
        filepath = self._store_data(obj, dst, key)
        self._register_resource(f"{src}_{dst}", filepath)
        return filepath

    def persist_artifact(self, src: str, dst: str, src_name: str) -> None:
        """
        Persist an artifact on S3 based storage.

        Parameters:
        -----------
        src : Any
            The source object to be persisted. It can be a file path as a string or Path object.

        dst : str
            The destination partition for the artifact.

        src_name : str
            The name of the source object.

        Raises:
        -------
        NotImplementedError :
            If the source object is not a file path, dictionary, StringIO/BytesIO buffer.

        Returns:
        --------
        None
        """
        client = self._get_client()
        bucket = get_uri_netloc(dst)
        self._check_access_to_storage(client, bucket)

        # Build the key for the artifact
        key = build_key(dst, src_name)

        # Local file
        if isinstance(src, (str, Path)) and check_path(src):
            self._upload_file(client, bucket, str(src), key)

        else:
            raise NotImplementedError

    def _get_client(self) -> S3Client:
        """
        Return a boto client.

        Returns:
        --------
        S3Client
            Returns a client object that interacts with the S3 storage service.
        """
        return boto3.client("s3", **self.config)

    def _check_access_to_storage(self, client: S3Client, bucket: str) -> None:
        """
        Check if the S3 bucket is accessible by sending a head_bucket request.

        Parameters:
        -----------
        client: S3Client
            An instance of 'S3Client' class that provides client interfaces to S3 service.
        bucket: string
            A string representing the name of the S3 bucket for which access needs to be checked.

        Returns:
        --------
        None

        Raises:
        -------
        StoreError:
            If access to the specified bucket is not available.

        """
        try:
            client.head_bucket(Bucket=bucket)
        except ClientError:
            raise Exception("No access to s3 bucket!")

    @staticmethod
    def _upload_file(
        client: S3Client,
        bucket: str,
        src: str,
        key: str,
    ) -> None:
        """
        Upload file to S3.

        Parameters
        ----------
        client : S3Client
            An instance of the S3 Client used for uploading the file.
        bucket : str
            The name of the S3 bucket where the file will be uploaded.
        src : str
            The path to the file that needs to be uploaded to S3.
        key : str
            The key under which the file needs to be saved in S3.

        Returns
        -------
        None
        """
        client.upload_file(Filename=src, Bucket=bucket, Key=key)

    @staticmethod
    def _get_data(client: S3Client, bucket: str, key: str) -> bytes:
        """
        Download an object from S3.

        Parameters
        ----------
        client : S3Client
            An instance of the S3 Client used for downloading the object.
        bucket : str
            The name of the S3 bucket where the object resides.
        key : str
            The key under which the object is stored in the specified bucket.

        Returns
        -------
        bytes
            A bytes object representing the downloaded object.

        """
        obj = client.get_object(Bucket=bucket, Key=key)
        return obj["Body"].read()

    def _store_data(self, obj: bytes, dst: str, key: str) -> str:
        """
        Store binary data in a temporary directory and return the file path.

        Parameters
        ----------
        obj : bytes
            Binary data to store in a temporary directory.
        key : str
            Key of the S3 object to store.

        Returns
        -------
        str
            Path of the stored data file.
        """
        check_make_dir(dst)
        name = get_name_from_uri(key)
        filepath = get_path(dst, name)
        write_bytes(obj, filepath)
        return filepath
