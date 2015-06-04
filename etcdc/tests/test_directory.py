import pytest

from etcdc.directory import Directory


def test_directory_raises_error_if_not_a_dir(node):
    with pytest.raises(ValueError):
        Directory(node)


def test_root_keys(directory, node):
    response = {'dir': True, 'nodes': [node, directory]}
    d = Directory(response)
    assert d.nodes[0].key == node['key']
    assert d.nodes[1].key == directory['key']
    assert d.modified_index is None
    assert d.created_index is None
    assert d.key is None


def test_directory(directory):
    j = directory
    d = Directory(j)
    assert j['key'] == d.key
    assert j['createdIndex'] == d.created_index
    assert j['modifiedIndex'] == d.modified_index
    assert d.nodes is None


def test_flat_directory(flat_directory):
    j = flat_directory
    d = Directory(j)
    sub_node_0 = d.nodes[0]
    assert j['nodes'][0]['key'] == sub_node_0.key


def test_recursive_directory(recursive_directory):
    j = recursive_directory
    d = Directory(j)
    sub_node_0 = d.nodes[0]
    assert j['nodes'][0]['key'] == sub_node_0.key
