import pytest
from mock import Mock, patch

from etcdc import errors
from etcdc.client import Client

# pylint:disable=invalid-name


def get_response(key, recursive=False):
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
    if 'update_key' in key:
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
    with pytest.raises(errors.KeyOfDirectory):
        client.get('/k')


@pytest.mark.parametrize('method,kwargs', [
    ('get', {}), ('set', {'value': 1})
])
def test_returns_a_node(method):
    requester = Mock()
    setattr(requester, method, Mock(side_effect=get_response))
    client = Client(requester=requester)
    assert 'key_val' == getattr(client, method)('/{}_key'.format(method)).value


def test_update_key_returns_a_node_with_prev_node():
    requester = Mock()
    requester.put = Mock(return_value=get_response)
    client = Client(requester=requester)
    node = client.set('/update_key', data={'value'})
    assert 'key_val' == node.value
    assert 'old_key_val' == node.prev_node.value


def test_set_without_value_key_sends_none():
    pass
