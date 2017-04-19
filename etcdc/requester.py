import requests

from etcdc import errors


class KeyRequester(object):

    def __init__(self, url, timeout=45):
        self.base_url = url.rstrip('/') + '/v2/keys'
        self.session = requests.Session()
        self.timeout = timeout

    @classmethod
    def check_for_errors(cls, key, response):
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

            if json:

                error_code = json.get('errorCode', None)
                reason = json.get('cause', '')
                if error_code == 300 and 'timed out' in reason:
                    message = json.get('message', 'timeout')

                    raise errors.Timeout(
                        response=response, message=message, reason=reason)

                if status_code == 400:
                    raise errors.NotADirectory(key)
                if status_code == 403:
                    raise errors.NotAFile(key)
                if status_code == 412:
                    raise errors.KeyAlreadyExists(key)

            raise errors.HTTPError(response=response, message=response.content)

    def _send(self, key, method, recursive=False, data=None):
        if not key.startswith('/'):
            raise errors.BadKey(key)
        qparam = '?recursive=true' if recursive else ''
        url = self.base_url + key + qparam
        response = getattr(self.session, method)(url, data=data, timeout=self.timeout)
        self.check_for_errors(key, response)
        return response.json()

    def get(self, key, recursive=False):
        return self._send(key, 'get', recursive)

    def put(self, key, data=None):
        return self._send(key, 'put', data=data)

    def post(self):
        pass

    def delete(self, key, recursive=False):
        return self._send(key, 'delete', recursive)
