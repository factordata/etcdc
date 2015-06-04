import requests

from etcdc.directory import Directory


class Requester(object):

    def __init__(self, url):
        self.url = url

    def _send(self, path, method='get', data=None):
        pass


class Client(object):

    def __init__(self, address='localhost', port='4001'):
        self.url = 'http://{}:{}'.format(address, port)
        self.version = requests.get(self.url + '/version').content

    def get_keys(self, key='/', recursive=False):
        qparam = '?recursive=true' if recursive else ''
        url = self.url + '/v2/keys' + key + qparam
        node = requests.get(url).json()['node']
        if 'dir' not in node:
            return [key]
        return Directory(node).keys
