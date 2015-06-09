import pytest
from mock import Mock, patch

from etcdc import errors
from etcdc.directory import Node, Directory
from etcdc.client import Client

# pylint:disable=invalid-name


def get_response(key, recursive=False, data=None):
    j = {
        u'action': u'get',
        u'node': {
            u'dir': True,
            u'nodes': [
                {
                    u'createdIndex': 24,
                    u'key': u'/k',
                    u'modifiedIndex': 24,
                    u'value': u''
                },
                {
                    u'createdIndex': 6,
                    u'dir': True,
                    u'key': u'/d',
                    u'modifiedIndex': 6
                }
            ]
        }
    }
    if 'key_dir' in key:
        j = {
            u'action': u'set',
            u'node': {
                u'createdIndex': 30,
                u'dir': True,
                u'key': u'{}'.format(key),
                u'modifiedIndex': 30
            }
        }
    elif 'update_key' in key:
        j = {
            u'action': u'set',
            u'node': {
                u'createdIndex': 8,
                u'key': u'/p3',
                u'modifiedIndex': 8,
                u'value': u'key_val'

            },
            u'prevNode': {
                u'createdIndex': 7,
                u'key': u'/p3',
                u'modifiedIndex': 7,
                u'value': u'old_key_val'
            }
        }

    elif 'get' in key or 'set' in key:
        j = {
            u'action': u'get' if 'get' in key else u'set',
            u'node': {
                u'createdIndex': 24,
                u'key': u'{}'.format(key),
                u'modifiedIndex': 24,
                u'value': u'key_val'
            }
        }
    elif recursive:
        j['node']['nodes'][-1]['nodes'] = [
            {
                u'createdIndex': 5,
                u'key': u'/k/k',
                u'modifiedIndex': 5,
                u'value': u''
            },
            {
                u'createdIndex': 6,
                u'dir': True,
                u'key': u'/d/d',
                u'modifiedIndex': 6
            }
        ]
    return j


@pytest.mark.parametrize('key,recursive,expected', [
    ('/', False, ['/k', '/d']),
    ('/', True, ['/k', '/k/k', '/d/d', '/d']),
    ('/get_key', False, ['/get_key']),
    ('/get_key', True, ['/get_key']),
])
def test_get_keys(key, recursive, expected):
    requester = Mock()
    requester.get = Mock(side_effect=get_response)
    client = Client(requester=requester)
    assert expected == client.get_keys(key=key, recursive=recursive)


# pylint:disable=pointless-statement
def test_version():
    version = 'etcd 2.0.11'
    response = Mock()
    response.content = version
    with patch('etcdc.client.requests') as requests:
        requests.get.return_value = response
        client = Client()
        assert version == client.version
        client.version  # check caching
        assert requests.get.call_count == 1
        requests.get.assert_called_with(client.url + '/version')


def test_get_raises_an_error_if_directory():
    requester = Mock()
    requester.get = Mock(side_effect=get_response)
    client = Client(requester=requester)
    with pytest.raises(errors.NotAFile):
        client.get('/k')


@pytest.mark.parametrize('method,kwargs', [
    ('get', {}), ('set', {'value': 1})
])
def test_returns_a_node(method, kwargs):
    requester = Mock()
    attr_name = 'put' if method == 'set' else method
    getattr(requester, attr_name).side_effect = get_response
    client = Client(requester=requester)
    key = '/{}_key'.format(method)
    node = getattr(client, method)(key, **kwargs)
    assert isinstance(node, Node)
    assert 'key_val' == node.value


def test_update_key_returns_a_node_with_prev_node():
    requester = Mock()
    requester.put.side_effect = get_response
    client = Client(requester=requester)
    node = client.set('/update_key', value=1)
    assert 'key_val' == node.value
    assert 'old_key_val' == node.prev_node.value


def test_set_without_value_key_sends_none():
    requester = Mock()
    requester.put.side_effect = get_response
    client = Client(requester=requester)
    key = '/update_key'
    client.set(key)
    requester.put.assert_called_with(key, data={'value': None, 'dir': False})


def test_mkdir_returns_a_dir():
    requester = Mock()
    requester.put.side_effect = get_response
    client = Client(requester=requester)
    directory = client.mkdir('/key_dir')
    assert isinstance(directory, Directory)
    assert '/key_dir' == directory.key


@patch('etcdc.requester.requests')
def test_mkdir_raises_error_if_already_exists(requests, response):
    j = {
        u'cause': u'/somedir',
        u'errorCode': 105,
        u'index': 30,
        u'message': u'Key already exists'
    }
    response.json = Mock(return_value=j)
    response.status_code = 412
    requests.put.return_value = response
    with pytest.raises(errors.KeyAlreadyExists):
        Client().mkdir('/somedir')
