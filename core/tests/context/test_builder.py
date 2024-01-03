import pytest
from digitalhub_core.context.builder import ContextBuilder, delete_context, get_context, set_context
from digitalhub_core.context.context import Context
from digitalhub_core.entities.projects.crud import get_or_create_project


@pytest.fixture(autouse=True, scope="session")
def context_builder():
    return ContextBuilder()


@pytest.fixture(autouse=True, scope="session")
def project():
    return get_or_create_project(name="test-project", local=True)


def test_build(context_builder, project):
    # Test build method
    context_builder.build(project)
    assert isinstance(context_builder.get(project.name), Context)


def test_get(context_builder, project):
    # Test get method
    context_builder.build(project)
    assert context_builder.get(project.name).name == project.name


def test_get_not_found(context_builder):
    # Test get method with a project that does not exist
    with pytest.raises(ValueError):
        context_builder.get("nonexistent")


def test_remove(context_builder, project):
    # Test remove method
    context_builder.build(project)
    context_builder.remove(project.name)
    with pytest.raises(ValueError):
        context_builder.get(project.name)


def test_set_context(project):
    # Test set_context function
    set_context(project)
    assert isinstance(get_context(project.name), Context)


def test_get_context(project):
    # Test get_context function
    set_context(project)
    assert get_context(project.name).name == project.name


def test_get_context_not_found():
    # Test get_context function with a project that does not exist
    with pytest.raises(ValueError):
        get_context("nonexistent")


def test_delete_context(project):
    # Test delete_context function
    set_context(project)
    delete_context(project.name)
    with pytest.raises(ValueError):
        get_context(project.name)
