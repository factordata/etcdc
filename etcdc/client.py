import requests

from etcdc import errors
from etcdc.requester import KeyRequester
from etcdc.directory import Node, Directory


class Client(object):

    def __init__(self, address='localhost', port='4001', requester=None):
        self.url = 'http://{}:{}'.format(address, port)
        self._version = None
        if requester:
            self.requester = requester
        else:
            self.requester = KeyRequester(url=self.url)

    @property
    def version(self):
        if self._version:
            return self._version
        self._version = requests.get(self.url + '/version').content
        return self._version

    def get_keys(self, key='/', recursive=False):
        result = self.ls(key=key, recursive=recursive)
        if isinstance(result, Node):
            return [result.key]
        return result.keys

    # pylint:disable=invalid-name
    def ls(self, key='/', recursive=False):
        j = self.requester.get(key, recursive=recursive)
        node = j['node']
        if 'dir' in node:
            return Directory(node)
        return Node(node)

    def get(self, key):
        j = self.requester.get(key)
        node = j['node']
        if 'dir' in node:
            raise errors.NotAFile(key)
        return Node(node)

    def set(self, key, value=None):
        data = {'value': value, 'dir': False}
        j = self.requester.put(key, data=data)
        node = j['node']
        prev_node = j.get('prevNode', None)
        return Node(node, prev_node)
