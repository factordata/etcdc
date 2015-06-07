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
    if 'single_key' in key:
        j = {
            u'action': u'get',
            u'node': {
                u'createdIndex': 24,
                u'key': u'/single_key',
                u'modifiedIndex': 24,
                u'value': u'single_key_value'
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
    ('/single_key', False, ['/single_key']),
    ('/single_key', True, ['/single_key']),
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


def test_get_returns_a_node():
    requester = Mock()
    requester.get = Mock(side_effect=get_response)
    client = Client(requester=requester)
    assert 'single_key_value' == client.get('/single_key').value


def test_get_raises_an_error_if_directory():
    requester = Mock()
    requester.get = Mock(side_effect=get_response)
    client = Client(requester=requester)
    with pytest.raises(errors.KeyOfDirectory):
        client.get('/k')
