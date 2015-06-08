import requests

from etcdc import errors


class KeyRequester(object):

    def __init__(self, url):
        self.base_url = url.rstrip('/') + '/v2/keys'

    @classmethod
    def check_for_errors(cls, key, response, data):
        status_code = response.status_code
        headers = response.headers
        if status_code != 200:
            if status_code == 404:
                if headers['content-type'] == 'text/plain':
                    raise errors.UrlNotFound()
                raise KeyError(key)
            if status_code == 403 and data and data.get('dir', False):
                cause = response.json()['cause']
                raise errors.KeyOfDirectory(cause)
            raise errors.HTTPError(response=response)

    def _send(self, key, method, recursive=False, data=None):
        if not key.startswith('/'):
            raise errors.BadKey()
        data = {} or data
        if recursive:
            data = {'recursive': True}
        url = self.base_url + key
        response = getattr(requests, method)(url, data=data)
        self.check_for_errors(key, response, data)
        try:
            return response.json()
        except Exception:
            raise errors.BadResponse(response.content)

    def get(self, key, recursive=False):
        return self._send(key, 'get', recursive)

    def put(self, key, data=None):
        return self._send(key, 'put', data=data)

    def post(self):
        pass
