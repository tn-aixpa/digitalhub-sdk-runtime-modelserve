from unittest.mock import patch

import pytest
from digitalhub_core.stores.builder import (
    LocalStoreConfig,
    S3StoreConfig,
    StoreBuilder,
    StoreParameters,
    get_env_store_config,
)
from digitalhub_core.stores.objects.base import Store
from digitalhub_core.utils.exceptions import StoreError


@pytest.fixture
def store_builder():
    return StoreBuilder()


@pytest.fixture
def store_cfg():
    return StoreParameters(name="local", type="local", config=LocalStoreConfig(path="/tmp"))


def test_build(store_builder, store_cfg):
    store_builder.build(store_cfg)
    assert isinstance(store_builder.get("local"), Store)


def test_get(store_builder, store_cfg):
    store_builder.build(store_cfg)
    assert isinstance(store_builder.get("local"), Store)


@patch.dict(
    "os.environ",
    {"S3_ENDPOINT_URL": "url", "AWS_ACCESS_KEY_ID": "id", "AWS_SECRET_ACCESS_KEY": "key", "S3_BUCKET_NAME": "name"},
)
def test_default(store_builder):
    assert isinstance(store_builder.default(), Store)


def test_build_store(store_builder, store_cfg):
    assert isinstance(store_builder.build_store(store_cfg), Store)


def test_build_store_not_implemented(store_builder, store_cfg):
    store_cfg.type = "not_implemented"
    with pytest.raises(NotImplementedError):
        store_builder.build_store(store_cfg)


def test_check_config(store_builder, store_cfg):
    assert isinstance(store_builder._check_config(store_cfg), StoreParameters)


def test_check_config_invalid_type(store_builder):
    with pytest.raises(StoreError, match="Invalid store configuration type."):
        store_builder._check_config("invalid_type")


def test_check_config_malformed_parameters(store_builder):
    with pytest.raises(StoreError, match="Malformed store configuration parameters."):
        store_builder._check_config({"name": "local", "type": "local", "config": "invalid_config"})


@patch.dict(
    "os.environ",
    {"S3_ENDPOINT_URL": "url", "AWS_ACCESS_KEY_ID": "id", "AWS_SECRET_ACCESS_KEY": "key", "S3_BUCKET_NAME": "name"},
)
def test_get_env_store_config_local():
    store_cfg = get_env_store_config("s3")
    assert isinstance(store_cfg, StoreParameters)
    assert store_cfg.name == "s3"
    assert store_cfg.type == "s3"
    assert isinstance(store_cfg.config, S3StoreConfig)


def test_get_env_store_config_not_supported():
    with pytest.raises(ValueError):
        get_env_store_config("not_supported")
