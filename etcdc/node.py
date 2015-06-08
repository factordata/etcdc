class Node(object):

    def __init__(self, node, prev_node=None):
        try:
            self.value = node['value']
        except KeyError:
            message = 'Bad node. value key is missing. Is this a directory?'
            raise ValueError(message)
        self.created_index = node['createdIndex']
        self.key = node['key']
        self.modified_index = node['modifiedIndex']
        if prev_node:
            self.prev_node = Node(prev_node)
