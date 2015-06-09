import requests

from etcdc import errors


class KeyRequester(object):

    def __init__(self, url):
        self.base_url = url.rstrip('/') + '/v2/keys'

    @classmethod
    def check_for_errors(cls, key, response, data):
        status_code = response.status_code
        headers = response.headers

        if status_code / 100 != 2:
            try:
                json = response.json()
            except ValueError:
                json = None
            if status_code == 404:
                if headers['content-type'] == 'text/plain':
                    raise errors.UrlNotFound()
                raise KeyError(key)
            if json and status_code == 400:
                raise errors.NotADirectory(key)
            if json and status_code == 403:
                raise errors.NotAFile(key)
            if json and status_code == 412:
                raise errors.KeyAlreadyExists(key)
            raise errors.HTTPError(response=response, message=response.content)

    def _send(self, key, method, recursive=False, data=None):
        if not key.startswith('/'):
            raise errors.BadKey(key)
        qparam = '?recursive=true' if recursive else ''
        url = self.base_url + key + qparam
        response = getattr(requests, method)(url, data=data)
        self.check_for_errors(key, response, data)
        return response.json()

    def get(self, key, recursive=False):
        return self._send(key, 'get', recursive)

    def put(self, key, data=None):
        return self._send(key, 'put', data=data)

    def post(self):
        pass
