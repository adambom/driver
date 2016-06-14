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

    def sorted_edges(self):
        if len(self.out_edges) == 0:
            return None
        return sorted(self.out_edges, key=lambda x: -len(x.label))

    # def get_best_edge(self):
    #     if len(self.out_edges) == 0:
    #         return None
    #     [0]
