import pytest
from mock import Mock, patch

from etcdc.client import Client


def get_response(url):
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
    if 'single_key' in url:
        j = {
            u'action': u'get',
            u'node': {
                u'createdIndex': 24,
                u'key': u'/single_key',
                u'modifiedIndex': 24,
                u'value': u''
            }
        }
    elif 'recursive' in url:
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
    response = Mock()
    response.json = Mock(return_value=j)
    return response


@pytest.mark.parametrize('key,recursive,expected', [
    ('/', False, ['/k', '/d']),
    ('/', True, ['/k', '/k/k', '/d/d', '/d']),
    ('/single_key', False, ['/single_key']),
    ('/single_key', True, ['/single_key']),
])
def test_get_keys(key, recursive, expected):
    with patch('etcdc.client.requests') as requests:
        requests.get.side_effect = get_response
        assert expected == Client().get_keys(key=key, recursive=recursive)


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
