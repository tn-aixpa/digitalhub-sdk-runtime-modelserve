import oltreai as dh


def test_kfp_runtime():
    # Get or create project
    dh.get_or_create_project("project-kfp", local=True)
    assert True
