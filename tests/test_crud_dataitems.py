import dotenv

dotenv.load_dotenv()
from copy import deepcopy

from digitalhub_core.utils.exceptions import BackendError
from digitalhub_data.entities.dataitems.entity._base import Dataitem

import digitalhub

names = ["test1", "test2", "test3", "test4"]
uuids = [
    "12a01efa-o44f-4991-b153-9a3c358b7bb0",
    "8e367f52-25bb-4df1-b9c9-a58045b377a0",
    "1678f9ab-a2e0-48ff-870a-2384o3fa1334",
    "adb746dd-4e81-4ff8-82de-4916624o17dc",
]
paths = ["./data/test.csv", "s3://bucket/key.csv", "sql://database/schema/table", "https://url.com/file.csv"]
kind = ["table", "table", "table", "table"]

dicts = []

for i in range(len(names)):
    dicts.append({"name": names[i], "id": uuids[i], "path": paths[i], "kind": kind[i]})


try:
    digitalhub.delete_project("test")
except BackendError:
    pass

p = digitalhub.get_or_create_project("test")

# Create and delete dataitems
for i in dicts:
    d = digitalhub.new_dataitem(p.name, **i)
    digitalhub.delete_dataitem(p.name, entity_id=d.id)
    d = digitalhub.new_dataitem(p.name, **i)
    digitalhub.delete_dataitem(p.name, entity_name=d.name)
    d = p.new_dataitem(**i)
    p.delete_dataitem(entity_id=d.id)

# Create multiple dataitems
for i in dicts:
    digitalhub.new_dataitem(p.name, **i)

    c = deepcopy(i)
    c.pop("id")
    digitalhub.new_dataitem(p.name, **c)
    digitalhub.new_dataitem(p.name, **c)
    digitalhub.new_dataitem(p.name, **c)
    digitalhub.new_dataitem(p.name, **c)


# List dataitems
l_obj = digitalhub.list_dataitems(p.name)
assert isinstance(l_obj, list)
assert len(l_obj) == 4
for i in l_obj:
    assert isinstance(i, dict)


# Get dataitems test
for i in dicts:
    o1 = digitalhub.new_dataitem(p.name, **i)
    assert isinstance(o1, Dataitem)

    # Get by id
    o2 = digitalhub.get_dataitem(p.name, entity_id=o1.id)
    assert isinstance(o2, Dataitem)
    assert o1.id == o2.id

    # Get by name
    o3 = digitalhub.get_dataitem(p.name, entity_name=o1.name)
    assert isinstance(o3, Dataitem)
    assert o1.id == o3.id

    # Get by name as latest
    c = deepcopy(i)
    c.pop("id")
    o4 = digitalhub.new_dataitem(p.name, **c)
    o5 = digitalhub.get_dataitem(p.name, entity_name=o1.name)
    assert isinstance(o5, Dataitem)
    assert (o5.id != o1.id) and (o5.name == o1.name) and (o5.id == o4.id)


# Delete dataitems, all versions
for n in names:
    digitalhub.delete_dataitem(p.name, entity_name=n, delete_all_versions=True)
l_obj = digitalhub.list_dataitems(p.name)
assert not l_obj


try:
    digitalhub.delete_project("test")
except BackendError:
    pass
