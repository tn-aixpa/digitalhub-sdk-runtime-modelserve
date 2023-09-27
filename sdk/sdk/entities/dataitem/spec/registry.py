"""
Dataitem specification registry module.
"""
from sdk.entities.dataitem.kinds import DataitemKinds
from sdk.entities.dataitem.spec.models import DataitemParamsDBT, DataitemParamsTable
from sdk.entities.dataitem.spec.objects import DataitemSpecDBT, DataitemSpecTable

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
