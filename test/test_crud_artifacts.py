import shutil
from copy import deepcopy

import dotenv
from digitalhub_core.entities.artifact.entity._base import Artifact

import digitalhub as dh

dotenv.load_dotenv()


def main():
    ctx = "./test-prg"
    names = ["test1", "test2", "test3", "test4"]
    uuids = [
        "d150bcca-bb64-451d-8455-dff862254b95",
        "31acdd2d-0c41-428c-b68b-1b133da9e97b",
        "b4a3dfdc-b917-44c4-9a29-613dcf734244",
        "2618d9c4-cd61-440f-aebb-7e5761709f3b",
    ]
    paths = ["./data/test.csv", "s3://bucket/key.csv", "sql://database/schema/table", "https://url.com/file.csv"]
    kind = ["artifact", "artifact", "artifact", "artifact"]

    dicts = []
    for i in range(len(names)):
        dicts.append({"name": names[i], "uuid": uuids[i], "path": paths[i], "kind": kind[i]})

    dh.delete_project("test")

    p = dh.get_or_create_project("test", context=ctx)

    # Create and delete artifacts
    for i in dicts:
        d = dh.new_artifact(p.name, **i)
        dh.delete_artifact(d.key)
        d = dh.new_artifact(p.name, **i)
        dh.delete_artifact(d.name, project=p.name, entity_id=d.id)
        d = p.new_artifact(**i)
        p.delete_artifact(d.key)

    print("Done 1")

    # Create multiple artifacts
    for i in dicts:
        dh.new_artifact(p.name, **i)

        c = deepcopy(i)
        c.pop("uuid")
        dh.new_artifact(p.name, **c)
        dh.new_artifact(p.name, **c)
        dh.new_artifact(p.name, **c)
        dh.new_artifact(p.name, **c)

    # List artifacts
    l_obj = dh.list_artifacts(p.name)
    assert isinstance(l_obj, list)
    assert len(l_obj) == 4
    for i in l_obj:
        assert isinstance(i, Artifact)

    for a in l_obj:
        dh.delete_artifact(a.key)

    print("Done 2")

    # Get artifacts test
    for i in dicts:
        o1 = dh.new_artifact(p.name, **i)
        assert isinstance(o1, Artifact)

        # Get by name and id
        o2 = dh.get_artifact(o1.name, project=p.name, entity_id=o1.id)
        assert isinstance(o2, Artifact)
        assert o1.id == o2.id

        # Get by key
        o3 = dh.get_artifact(o1.key)
        assert isinstance(o3, Artifact)
        assert o1.id == o3.id

    print("Done 3")

    # Delete artifacts, all versions
    for n in names:
        dh.delete_artifact(n, project=p.name, delete_all_versions=True)
    l_obj = dh.list_artifacts(p.name)
    assert not l_obj

    dh.delete_project("test")
    shutil.rmtree(ctx)

    print("Done 4")


if __name__ == "__main__":
    main()
