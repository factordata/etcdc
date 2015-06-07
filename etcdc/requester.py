import requests

from etcdc import errors


class KeyRequester(object):

    def __init__(self, url):
        self.base_url = url.rstrip('/')

    def check_for_errors(self, response):
        pass

    def _send(self, key, method, recursive, data=None):
        if not key.startswith('/'):
            raise errors.BadKey()
        qparam = '?recursive=true' if recursive else ''
        url = self.base_url + key + qparam
        r = getattr(requests, method)(url)
        if r.status_code == 404:
            if r.headers['content-type'] == 'text/plain':
                raise errors.UrlNotFound()
            raise KeyError(key)
        if r.status_code != 200:
            raise errors.HTTPError(response=r)
        try:
            return r.json()
        except Exception:
            raise errors.BadResponse(r.content)

    def get(self, key, recursive=False):
        return self._send(key, 'get', recursive)

    def put(self):
        pass

    def post(self):
        pass
