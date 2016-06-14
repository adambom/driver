class Edge(object):
    def __init__(self, node, label):
        self.node = node
        self.label = label


class Node(object):
    def __init__(self, value):
        self.value = value
        self.out_edges = []
        self.in_edges = []
        self.visited = False

    def __repr__(self):
        """Return repr."""
        return 'Node<%s>' % self.value

    def __len__(self):
        """Get the length of the value string."""
        return len(self.value)

    def sorted_edges(self, reverse=False):
        edges = self.in_edges if reverse is True else self.out_edges
        if len(edges) == 0:
            return None
        return sorted(edges, key=lambda x: -len(x.label))
