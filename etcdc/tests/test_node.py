import pytest

from etcdc.node import Node

# pylint:disable=invalid-name,pointless-statement


def test_node_attrs(node):
    n = Node(node)
    assert node['value'] == n.value
    assert node['modifiedIndex'] == n.modified_index
    assert node['createdIndex'] == n.created_index
    assert node['key'] == n.key
    with pytest.raises(AttributeError):
        n.prev_node


def test_node_raises_error_if_not_a_node(directory):
    with pytest.raises(ValueError):
        Node(directory)


def test_node_with_prev_node(node, prev_node):
    n = Node(node, prev_node)
    assert prev_node['value'] == n.prev_node.value
