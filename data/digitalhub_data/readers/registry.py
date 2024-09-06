from __future__ import annotations

REGISTRY_FRAMEWORK = {}
REGISTRY_DATAFRAME = {}
DATAFRAME_TYPES = []

try:
    from digitalhub_data.readers.objects.pandas import DataframeReaderPandas

    REGISTRY_FRAMEWORK["pandas"] = DataframeReaderPandas
    REGISTRY_DATAFRAME["pandas.core.frame.DataFrame"] = DataframeReaderPandas
    DATAFRAME_TYPES.append("pandas.core.frame.DataFrame")

except ImportError:
    pass
