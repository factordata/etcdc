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


@pytest.mark.parametrize('method,kwargs', [
    ('get', {}),
    ('put', {'data': {'value': 1}})
])
def test_404(method, kwargs, response):
    response.status_code = 404
    response.headers = {'content-type': 'text/plain'}
    getattr(REQUESTS_MOCK, method).return_value = response
    with pytest.raises(errors.UrlNotFound):
        getattr(KR, method)('/key', **kwargs)


def test_get_key_error(response):
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


def test_put_can_be_called_with_no_data(response):
    j = {'action': 'set', 'blah': 1}
    response.json = Mock(return_value=j)
    REQUESTS_MOCK.put.return_value = response
    assert j == KR.put('/key')
    response.json.assert_called_with()


@pytest.mark.parametrize('method,kwargs', [
    ('get', {}),
    ('put', {'data': {'value': 1}})
])
def test_response_returns_json(method, kwargs, response):
    j = {'action': 'foo', 'blah': 1}
    response.json = Mock(return_value=j)
    getattr(REQUESTS_MOCK, method).return_value = response
    assert j == getattr(KR, method)('/key', **kwargs)
    response.json.assert_called_with()


@pytest.mark.parametrize('method,kwargs', [
    ('get', {}),
    ('put', {'data': {'value': 1}})
])
def test_response_raises_error_if_status_is_not_200(method, kwargs, response):
    response.status_code = 500
    response.reason = 'to believe'
    getattr(REQUESTS_MOCK, method).return_value = response
    with pytest.raises(errors.HTTPError) as excinfo:
        getattr(KR, method)('/key', **kwargs)
    assert excinfo.value.status_code == 500
    assert excinfo.value.reason == 'to believe'


@pytest.mark.parametrize('method,kwargs', [
    ('get', {}),
    ('put', {'data': {'value': 1}})
])
def test_response_with_bad_json_raises_error(method, kwargs, response):
    response.json = Mock(side_effect=Exception)
    getattr(REQUESTS_MOCK, method).return_value = response
    with pytest.raises(errors.BadResponse):
        getattr(KR, method)('/key', **kwargs)
