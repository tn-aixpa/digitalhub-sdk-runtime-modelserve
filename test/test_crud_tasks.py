import dotenv
from oltreai_core.entities.task.entity import Task

import oltreai

dotenv.load_dotenv()


def add_param(kwargs) -> dict:
    if kwargs["kind"] == "mlrun+job":
        kwargs["function"] = f1._get_function_string()

    if kwargs["kind"] == "dbt+transform":
        kwargs["function"] = f2._get_function_string()

    if kwargs["kind"] == "container+job":
        kwargs["function"] = f3._get_function_string()

    if kwargs["kind"] == "nefertem+infer":
        kwargs["function"] = f4._get_function_string()
        kwargs["framework"] = "test"

    return kwargs


names = ["test1", "test2", "test3", "test4"]
uuids = [
    "12a01efa-o44f-4991-b153-9a3c358b7bb0",
    "8e367f52-25bb-4df1-b9c9-a58045b377a0",
    "1678f9ab-a2e0-48ff-870a-2384o3fa1334",
    "adb746dd-4e81-4ff8-82de-4916624o17dc",
]
kind = ["mlrun+job", "dbt+transform", "container+job", "nefertem+infer"]

dicts = []
for i in range(len(names)):
    dicts.append({"name": names[i], "uuid": uuids[i], "kind": kind[i]})

oltreai.delete_project("test")

p = oltreai.get_or_create_project("test")

f1 = p.new_function(name="t1", kind="mlrun", source={"code": "test"})
f2 = p.new_function(name="t2", kind="dbt", source={"code": "test"})
f3 = p.new_function(name="t3", kind="container", image="test")
f4 = p.new_function(name="t4", kind="nefertem")


# Create and delete tasks
for i in dicts:
    i = add_param(i)
    d = oltreai.new_task(p.name, **i)
    oltreai.delete_task(p.name, entity_id=d.id)

# Create multiple tasks
for i in dicts:
    i = add_param(i)
    oltreai.new_task(p.name, **i)

# List tasks
l_obj = oltreai.list_tasks(p.name)
assert isinstance(l_obj, list)
assert len(l_obj) == 4
for i in l_obj:
    assert isinstance(i, dict)

for uuid in uuids:
    oltreai.delete_task(p.name, entity_id=uuid)

# Get tasks test
for i in dicts:
    i = add_param(i)
    o1 = oltreai.new_task(p.name, **i)
    assert isinstance(o1, Task)

    # Get by id
    o2 = oltreai.get_task(p.name, entity_id=o1.id)
    assert isinstance(o2, Task)
    assert o1.id == o2.id

oltreai.delete_project("test")
