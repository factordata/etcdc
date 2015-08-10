import pytest
from mock import Mock

from etcdc import errors
from etcdc.requester import KeyRequester

# pylint: disable=invalid-name

KR = KeyRequester('http://localhost')
KR.session = Mock()


def test_key_must_start_with_slash():
    with pytest.raises(errors.BadKey):
        KR.get('bad_key')


def test_base_url():
    assert KeyRequester('http://b').base_url == 'http://b/v2/keys'


@pytest.mark.parametrize('method,kwargs', [
    ('get', {}),
    ('put', {'data': {'value': 1}})
])
def test_404(method, kwargs, response):
    response.status_code = 404
    response.headers = {'content-type': 'text/plain'}
    getattr(KR.session, method).return_value = response
    with pytest.raises(errors.UrlNotFound):
        getattr(KR, method)('/key', **kwargs)


@pytest.mark.parametrize('status_code', [200, 201, 204])
def test_2xx_succeeds(status_code, response):
    j = {'action': 'set', 'blah': 1}
    response.json = Mock(return_value=j)
    response.status_code = status_code
    KR.session.get.return_value = response
    assert j == KR.get('/key')


def test_get_key_error(response):
    response.status_code = 404
    response.json = Mock(return_value={
        u'cause': u'/ppccc',
        u'errorCode': 100,
        u'index': 26,
        u'message': u'Key not found'
    })
    KR.session.get.return_value = response
    with pytest.raises(KeyError) as excinfo:
        KR.get('/non_existing', recursive=True)
    assert '/non_existing' == excinfo.value.message


def test_put_raises_error_if_not_a_file(response):
    key = '/dir/dir/'
    response.status_code = 403
    response.json = Mock(return_value={
        u'cause': key,
        u'errorCode': 102,
        u'index': 13,
        u'message': u'Not a file'
    })
    KR.session.put.return_value = response
    with pytest.raises(errors.NotAFile) as excinfo:
        KR.put(key, 1)
    assert key == excinfo.value.key


def test_put_raises_error_if_not_a_dir(response):
    key = '/dir/file/some_key'
    response.status_code = 400
    response.json = Mock(return_value={
        u'cause': key,
        u'errorCode': 104,
        u'index': 13,
        u'message': u'Not a directory'
    })
    KR.session.put.return_value = response
    with pytest.raises(errors.NotADirectory) as excinfo:
        KR.put(key, 2)
    assert key == excinfo.value.key


def test_put_can_be_called_with_no_data(response):
    j = {'action': 'set', 'blah': 1}
    response.json = Mock(return_value=j)
    KR.session.put.return_value = response
    assert j == KR.put('/key')
    response.json.assert_called_with()


@pytest.mark.parametrize('method,kwargs', [
    ('get', {}),
    ('put', {'data': {'value': 1}})
])
def test_response_returns_json(method, kwargs, response):
    j = {'action': 'foo', 'blah': 1}
    response.json = Mock(return_value=j)
    getattr(KR.session, method).return_value = response
    assert j == getattr(KR, method)('/key', **kwargs)
    response.json.assert_called_with()


@pytest.mark.parametrize('method,kwargs', [
    ('get', {}),
    ('put', {'data': {'value': 1}})
])
def test_response_raises_error_if_status_is_not_200(method, kwargs, response):
    response.status_code = 500
    response.reason = 'to believe'
    getattr(KR.session, method).return_value = response
    with pytest.raises(errors.HTTPError) as excinfo:
        getattr(KR, method)('/key', **kwargs)
    assert excinfo.value.status_code == 500
    assert excinfo.value.reason == 'to believe'


@pytest.mark.parametrize('method,kwargs', [
    ('get', {}),
    ('put', {'data': {'value': 1}})
])
def test_response_with_bad_json_raises_error(method, kwargs, response):
    response.json = Mock(side_effect=ValueError)
    response.content = 'blah'
    response.status_code = 500
    getattr(KR.session, method).return_value = response
    with pytest.raises(errors.HTTPError):
        getattr(KR, method)('/key', **kwargs)
