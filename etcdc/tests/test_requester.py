import pytest
from mock import Mock, patch

from etcdc import errors
from etcdc.requester import KeyRequester

# pylint: disable=invalid-name

KR = KeyRequester('http://localhost')
REQUESTS_MOCK = patch('etcdc.requester.requests').start()


def test_key_must_start_with_slash():
    with pytest.raises(errors.BadKey):
        KR.get('bad_key')


def test_404(response):
    response.status_code = 404
    response.headers = {'content-type': 'text/plain'}
    REQUESTS_MOCK.get.return_value = response
    with pytest.raises(errors.UrlNotFound):
        KR.get('/key')


def test_key_error(response):
    response.status_code = 404
    response.json = Mock(return_value={
        u'cause': u'/ppccc',
        u'errorCode': 100,
        u'index': 26,
        u'message': u'Key not found'
    })
    REQUESTS_MOCK.get.return_value = response
    with pytest.raises(KeyError) as excinfo:
        KR.get('/non_existing')
    assert '/non_existing' == excinfo.value.message


def test_response_returns_json(response):
    j = {'action': 'get', 'blah': 1}
    response.json = Mock(return_value=j)
    REQUESTS_MOCK.get.return_value = response
    assert KR.get('/key') == j
    response.json.assert_called_with()


def test_response_raises_error_if_status_is_not_200(response):
    response.status_code = 500
    response.reason = 'to believe'
    REQUESTS_MOCK.get.return_value = response
    with pytest.raises(errors.HTTPError) as excinfo:
        KR.get('/key')
    assert excinfo.value.status_code == 500
    assert excinfo.value.reason == 'to believe'


def test_response_with_no_json_raises_error(response):
    response.json = Mock(side_effect=IOError)
    REQUESTS_MOCK.get.return_value = response
    with pytest.raises(errors.BadResponse):
        KR.get('/key')
