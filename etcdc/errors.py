class EtcdcException(Exception):
    message = 'Etcdc general exception'

    def __str__(self):
        return self.message


class BadKey(EtcdcException):
    message = 'Key must start with a "/"'


class NotAFile(BadKey):
    message = 'Key must be of a single node, not a directory'

    def __init__(self, key, *args, **kwargs):
        super(NotAFile, self).__init__(*args, **kwargs)
        self.key = key


class NotADirectory(BadKey):
    message = 'Path must be of a directory'

    def __init__(self, key, *args, **kwargs):
        super(NotADirectory, self).__init__(*args, **kwargs)
        self.key = key


class UrlNotFound(EtcdcException):
    message = 'Bad URL'


class HTTPError(EtcdcException):

    def __init__(self, response, message, *args, **kwargs):
        super(HTTPError, self).__init__(*args, **kwargs)
        self.status_code = response.status_code
        self.reason = response.reason
        self.message = message
