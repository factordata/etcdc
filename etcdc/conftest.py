import pytest


@pytest.fixture
def node():
    return {
        'createdIndex': 1,
        'key': '/a/b',
        'modifiedIndex': 1,
        'value': [1, 2, 3],
    }


@pytest.fixture
def directory():
    return {
        'dir': True,
        'createdIndex': 1,
        'key': '/d',
        'modifiedIndex': 1,
    }


@pytest.fixture
def flat_directory():
    return {
        'dir': True,
        'createdIndex': 1,
        'key': '/f/d',
        'modifiedIndex': 1,
        'nodes': [directory(), node(), node()],
    }


@pytest.fixture
def recursive_directory():
    return {
        'dir': True,
        'createdIndex': 1,
        'key': '/r/d',
        'modifiedIndex': 1,
        'nodes': [flat_directory(), node()]
    }
