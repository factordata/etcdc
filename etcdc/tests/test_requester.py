import pytest
from mock import Mock, patch

from etcdc import errors
from etcdc.requester import KeyRequester


BASE_URL = 'http://localhost'


def test_key_must_start_with_slash():
    kr = KeyRequester(BASE_URL)
    with pytest.raises(errors.BadKey):
        kr.get('bad_key')


@patch('etcdc.requester.requests')
def test_404(requests):
    response = Mock()
    response.status_code = 404
    response.headers = {'content-type': 'text/plain'}
    requests.get.return_value = response
    kr = KeyRequester(BASE_URL)
    with pytest.raises(errors.UrlNotFount):
        kr.get('/key')


@patch('etcdc.requester.requests')
def test_key_error(requests):
    response = Mock()
    response.status_code = 404
    response.headers = {'content-type': 'application/json'}
    response.json = Mock(return_value={
        u'cause': u'/ppccc',
        u'errorCode': 100,
        u'index': 26,
        u'message': u'Key not found'
    })
    requests.get.return_value = response
    kr = KeyRequester(BASE_URL)
    with pytest.raises(KeyError) as excinfo:
        kr.get('/non_existing')
    assert '/non_existing' == excinfo.value.message


@patch('etcdc.requester.requests')
def test_response_returns_json(requests):
    response = Mock()
    response.status_code = 200
    j = {'action': 'get', 'blah': 1}
    response.json = Mock(return_value=j)
    requests.get.return_value = response
    kr = KeyRequester(BASE_URL)
    assert kr.get('/key') == j
    response.json.assert_called_with()


@patch('etcdc.requester.requests')
def test_response_raises_error_if_status_is_not_200(requests):
    response = Mock()
    response.status_code = 500
    response.reason = 'to believe'
    requests.get.return_value = response
    kr = KeyRequester(BASE_URL)
    with pytest.raises(errors.HTTPError) as excinfo:
        kr.get('/key')
    assert excinfo.value.status_code == 500
    assert excinfo.value.reason == 'to believe'


@patch('etcdc.requester.requests')
def test_response_with_no_json_raises_error(requests):
    response = Mock()
    response.status_code = 200
    response.json = Mock(side_effect=IOError)
    requests.get.return_value = response
    kr = KeyRequester(BASE_URL)
    with pytest.raises(errors.BadResponse) as excinfo:
        kr.get('/key')
