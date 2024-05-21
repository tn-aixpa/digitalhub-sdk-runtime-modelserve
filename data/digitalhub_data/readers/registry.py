from __future__ import annotations

REGISTRY = {}

try:
    from digitalhub_data.readers.objects.pandas import DataframeReaderPandas

    REGISTRY["pandas"] = DataframeReaderPandas
    REGISTRY["pandas.core.frame.DataFrame"] = DataframeReaderPandas
except ImportError:
    pass
