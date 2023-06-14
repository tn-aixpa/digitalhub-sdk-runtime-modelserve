"""
S3Store module.
"""
from tempfile import mkdtemp
from typing import Optional, Type

import boto3
import botocore.client
from botocore.exceptions import ClientError

from sdk.store.objects.store import Store
from sdk.utils.file_utils import check_make_dir, get_dir
from sdk.utils.uri_utils import (
    get_name_from_uri,
    get_uri_netloc,
    get_uri_path,
    get_uri_scheme,
    rebuild_uri,
    build_key
)


# Type aliases
S3Client = Type["botocore.client.S3"]


class S3Store(Store):
    """
    S3 store class. It implements the Store interface and provides methods to fetch and persist
    artifacts on S3 based storage.
    """

    def __init__(
        self,
        name: str,
        type: str,
        uri: str,
        config: Optional[dict] = None,
    ) -> None:
        """
        Constructor.

        See Also
        --------
        Store.__init__
        """
        super().__init__(name, type, uri, config)
        self._validate_uri()

    ############################
    # IO methods
    ############################

    def upload(self, src: str, dst: str = None) -> str:
        """
        Upload an artifact to S3 based storage.

        See Also
        --------
        self.persist_artifact
        """
        return self.persist_artifact(src, dst)

    def download(self, src: str, dst: str = None) -> str:
        """
        Download an artifact from S3 based storage.

        See Also
        --------
        self.fetch_artifact
        """
        return self.fetch_artifact(src, dst)

    def fetch_artifact(self, src: str, dst: str = None) -> str:
        """
        Fetch an artifact from S3 based storage.

        Parameters
        ----------
        src : str
            The source location of the artifact.
        dst : str, optional
            The destination of the artifact on local filesystem.

        Returns
        -------
        str
            Returns a file path.
        """
        if dst is None:
            dir = mkdtemp()
            dst = f"{dir}/{get_name_from_uri(src)}"
            self._register_resource(f"{src}_{dst}", dst)

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

    def persist_artifact(self, src: str, dst: str = None) -> str:
        """
        Persist an artifact on S3 based storage.

        Parameters
        ----------
        src : Any
            The source object to be persisted. It can be a file path as a string or Path object.

        dst : str, optional
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
        bucket = get_uri_netloc(self.uri)

        # Check store access
        self._check_access_to_storage(client, bucket)

        # Rebuild key from target path
        key = build_key(get_uri_path(dst))

        # Upload file to S3
        client.upload_file(Filename=src, Bucket=bucket, Key=key)
        return rebuild_uri(f"s3://{bucket}/{key}")

    ############################
    # Private helper methods
    ############################

    def _validate_uri(self) -> None:
        """
        Validate the URI of the store.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the URI scheme is not 's3'.

        Exception
            If no bucket is specified in the URI.
        """
        scheme = get_uri_scheme(self.uri)
        if scheme != "s3":
            raise Exception(f"Invalid URI scheme for s3 store: {scheme}. Should be 's3'")
        bucket = get_uri_netloc(self.uri)
        if bucket == "":
            raise Exception("No bucket specified in the URI for s3 store!")

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
        -------
        StoreError:
            If access to the specified bucket is not available.

        """
        try:
            client.head_bucket(Bucket=bucket)
        except ClientError:
            raise Exception("No access to s3 bucket!")

    @staticmethod
    def _check_local_dst(dst: str) -> None:
        """
        Check if the local destination directory exists. Create in case it does not.

        Parameters
        ----------
        dst : str
            The destination directory.

        """
        if get_uri_scheme(dst) in ["", "file"]:
            dst_dir = get_dir(dst)
            check_make_dir(dst_dir)

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

    def get_root_uri(self) -> str:
        """
        Get the root URI of the store.

        Returns
        -------
        str
            The root URI of the store.
        """
        return f"s3://{get_uri_netloc(self.uri)}"
