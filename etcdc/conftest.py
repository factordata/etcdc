import pytest
from mock import Mock


@pytest.fixture
def node():
    return {
        'createdIndex': 1,
        'key': '/a/b',
        'modifiedIndex': 1,
        'value': [1, 2, 3],
    }


@pytest.fixture
def prev_node():
    p_node = node()
    p_node['value'] = 'new_value'
    return p_node


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


@pytest.fixture
def response():
    resp = Mock()
    resp.status_code = 200
    resp.headers = {'content-type': 'application/json'}
    return resp
