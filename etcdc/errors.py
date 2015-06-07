class EtcdcException(Exception):
    pass


class BadKey(EtcdcException):
    message = 'Key must start with a "/"'


class KeyOfDirectory(BadKey):
    message = 'Key must be of a single node, not directory'


class UrlNotFound(EtcdcException):
    pass


class BadResponse(EtcdcException):
    message = 'Response content cannot be converted to Json'

    def __init__(self, content, *args, **kwargs):
        super(BadResponse, self).__init__(*args, **kwargs)
        self.content = content


class HTTPError(EtcdcException):

    def __init__(self, response, *args, **kwargs):
        super(HTTPError, self).__init__(*args, **kwargs)
        self.status_code = response.status_code
        self.reason = response.reason
