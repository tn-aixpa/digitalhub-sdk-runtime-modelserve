from unittest.mock import patch

import pandas as pd
import pytest
from oltreai_core.stores.objects.s3 import S3Store, S3StoreConfig


@pytest.fixture
def s3_store():
    config = S3StoreConfig(
        bucket_name="test_bucket",
        endpoint_url="http://localhost:9000",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    return S3Store("test_store", "s3", config)


def test_init(s3_store):
    assert s3_store.name == "test_store"
    assert s3_store.type == "s3"
    assert s3_store.config.bucket_name == "test_bucket"


@patch("oltreai_core.stores.objects.s3.S3Store._download_file")
def test_download(mock_download_file, s3_store):
    mock_download_file.return_value = "dst"
    assert s3_store.download("s3://test_bucket/src", "dst") == "dst"
    mock_download_file.assert_called_once_with("test_bucket", "src", "dst")


@patch("oltreai_core.stores.objects.s3.S3Store._download_file")
def test_fetch_artifact(mock_download_file, s3_store):
    mock_download_file.return_value = "dst"
    assert s3_store.fetch_artifact("s3://test_bucket/src", "dst") == "dst"
    mock_download_file.assert_called_once_with("test_bucket", "src", "dst")


@patch("oltreai_core.stores.objects.s3.S3Store._upload_file")
def test_upload(mock_upload_file, s3_store):
    mock_upload_file.return_value = "dst"
    assert s3_store.upload("src", "dst") == "dst"
    mock_upload_file.assert_called_once_with("src", "dst")


@patch("oltreai_core.stores.objects.s3.S3Store._upload_file")
def test_persist_artifact(mock_upload_file, s3_store):
    mock_upload_file.return_value = "dst"
    assert s3_store.persist_artifact("src", "dst") == "dst"
    mock_upload_file.assert_called_once_with("src", "dst")


@patch("oltreai_core.stores.objects.s3.S3Store._upload_fileobject")
def test_write_df(mock_upload_fileobject, s3_store):
    df = pd.DataFrame({"A": [1, 2, 3]})
    mock_upload_fileobject.return_value = "dst.parquet"
    assert s3_store.write_df(df, "dst.parquet") == "dst.parquet"
    mock_upload_fileobject.assert_called_once()
