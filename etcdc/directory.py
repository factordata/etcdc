from etcdc.node import Node


class Directory(object):

    def __init__(self, node):
        j = node
        if 'dir' not in j:
            raise ValueError('Not a directory')

        self.key = j.get('key', None)
        self.created_index = j.get('createdIndex', None)
        self.modified_index = j.get('modifiedIndex', None)
        self.nodes = None
        if 'nodes' in j:
            self.nodes = []
            for node in j['nodes']:
                if 'dir' in node:
                    self.nodes.append(Directory(node))
                else:
                    self.nodes.append(Node(node))

    @property
    def keys(self):
        keys = []
        if self.nodes:
            for node in self.nodes:
                if hasattr(node, 'keys'):
                    keys.extend(node.keys)
                keys.append(node.key)
        return keys
