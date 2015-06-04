import pytest

from etcdc.node import Node


def test_node_attrs(node):
    n = Node(node)
    assert node['value'] == n.value
    assert node['modifiedIndex'] == n.modified_index
    assert node['createdIndex'] == n.created_index
    assert node['key'] == n.key


def test_node_raises_error_if_not_a_node(directory):
    with pytest.raises(ValueError):
        Node(directory)
