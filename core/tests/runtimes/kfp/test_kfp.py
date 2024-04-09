import digitalhub_core as dhcore


def test_kfp_runtime():
    # Get or create project
    dhcore.get_or_create_project("project-kfp", local=True)
    assert True
