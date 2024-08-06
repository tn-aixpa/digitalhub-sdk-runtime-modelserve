from unittest.mock import patch

import pandas as pd
import pytest
from oltreai_core.stores.objects.sql import SqlStore, SQLStoreConfig


@pytest.fixture
def sql_store():
    config = SQLStoreConfig(
        user="test", password="test", host="localhost", port=5432, database="test_db", pg_schema="public"
    )
    return SqlStore("test_store", "sql", config)


def test_init(sql_store):
    assert sql_store.name == "test_store"
    assert sql_store.type == "sql"
    assert sql_store.config.user == "test"


@patch("oltreai_core.stores.objects.sql.SqlStore._download_table")
def test_download(mock_download_table, sql_store):
    mock_download_table.return_value = "table.parquet"
    assert sql_store.download("sql://database/schema/table", "table.parquet") == "table.parquet"
    mock_download_table.assert_called_once()


@patch("oltreai_core.stores.objects.sql.SqlStore._download_table")
def test_fetch_artifact(mock_download_table, sql_store):
    mock_download_table.return_value = "table.parquet"
    assert sql_store.fetch_artifact("sql://database/schema/table", "table.parquet") == "table.parquet"
    mock_download_table.assert_called_once()


def test_upload_raises_not_implemented_error(sql_store):
    with pytest.raises(NotImplementedError):
        sql_store.upload("src", "sql://database/schema/table")


def test_persist_artifact_raises_not_implemented_error(sql_store):
    with pytest.raises(NotImplementedError):
        sql_store.persist_artifact("src", "sql://database/schema/table")


@patch("oltreai_core.stores.objects.sql.SqlStore._upload_table")
def test_write_df(mock_upload_table, sql_store):
    df = pd.DataFrame({"A": [1, 2, 3]})
    mock_upload_table.return_value = "sql://database/schema/table"
    assert sql_store.write_df(df, "sql://database/schema/table") == "sql://database/schema/table"
    mock_upload_table.assert_called_once()
