class EtcdcException(Exception):
    message = 'Etcdc general exception'

    def __str__(self):
        return self.message


class BadKey(EtcdcException):
    message = 'Key must start with a "/"'

    def __init__(self, key, *args, **kwargs):
        super(BadKey, self).__init__(*args, **kwargs)
        self.key = key


class NotAFile(BadKey):
    message = 'Key must be of a single node, not a directory'


class NotADirectory(BadKey):
    message = 'Path must be of a directory'


class KeyAlreadyExists(BadKey):
    message = 'Key already exists'


class UrlNotFound(EtcdcException):
    message = 'Bad URL'


class HTTPError(EtcdcException):

    def __init__(self, response, message, reason=None, *args, **kwargs):
        super(HTTPError, self).__init__(*args, **kwargs)
        self.status_code = response.status_code
        self.reason = reason or response.reason
        self.message = message


class Timeout(HTTPError):

    def __init__(self, response, message, reason, *args, **kwargs):
        super(Timeout, self).__init__(response, message, reason, *args, **kwargs)
