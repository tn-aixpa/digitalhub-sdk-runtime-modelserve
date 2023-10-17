"""
Dataitem specification registry module.
"""
from sdk.entities.base.spec import SpecRegistry
from sdk.entities.dataitems.kinds import DataitemKinds
from sdk.entities.dataitems.spec.objects.dbt import DataitemParamsDBT, DataitemSpecDBT
from sdk.entities.dataitems.spec.objects.table import DataitemParamsTable, DataitemSpecTable

dataitem_registry = SpecRegistry()
dataitem_registry.register(DataitemKinds.TABLE.value, DataitemSpecTable, DataitemParamsTable)
dataitem_registry.register(DataitemKinds.DBT.value, DataitemSpecDBT, DataitemParamsDBT)
dataitem_registry.register(DataitemKinds.DATAITEM.value, DataitemSpecTable, DataitemParamsTable)
