"""
Dataitem specification registry module.
"""
from sdk.entities.dataitems.kinds import DataitemKinds
from sdk.entities.dataitems.spec.objects.dbt import (
    DataitemParamsDBT,
    DataitemSpecDBT,
)
from sdk.entities.dataitems.spec.objects.table import (
    DataitemParamsTable,
    DataitemSpecTable,
)

DATAITEM_SPEC = {
    DataitemKinds.DATAITEM.value: DataitemSpecTable,
    DataitemKinds.TABLE.value: DataitemSpecTable,
    DataitemKinds.DBT.value: DataitemSpecDBT,
}
DATAITEM_MODEL = {
    DataitemKinds.DATAITEM.value: DataitemParamsTable,
    DataitemKinds.TABLE.value: DataitemParamsTable,
    DataitemKinds.DBT.value: DataitemParamsDBT,
}
