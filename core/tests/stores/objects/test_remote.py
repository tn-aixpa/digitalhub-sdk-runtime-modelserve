import pytest
import pandas as pd
from unittest.mock import patch
from digitalhub_core.stores.objects.remote import RemoteStore, RemoteStoreConfig

@pytest.fixture
def remote_store():
    config = RemoteStoreConfig()
    return RemoteStore("test_store", "remote", config)

def test_init(remote_store):
    assert remote_store.name == "test_store"
    assert remote_store.type == "remote"

def test_download(remote_store):
    ...

def test_fetch_artifact(remote_store):
    ...

def test_upload_raises_not_implemented_error(remote_store):
    with pytest.raises(NotImplementedError):
        remote_store.upload("src", "dst")

def test_persist_artifact_raises_not_implemented_error(remote_store):
    with pytest.raises(NotImplementedError):
        remote_store.persist_artifact("src", "dst")

def test_write_df_raises_not_implemented_error(remote_store):
    with pytest.raises(NotImplementedError):
        remote_store.write_df(pd.DataFrame(), "dst")

def test_is_local(remote_store):
    assert remote_store.is_local() == False
