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
        self.longest_in_edge = None
        self.longest_out_edge = None

    def __repr__(self):
        """Return repr."""
        return 'Node<%s>' % self.value

    def __len__(self):
        """Get the length of the value string."""
        return len(self.value)

    def add_in_edge(self, edge):
        if self.longest_in_edge is None:
            self.longest_in_edge = edge
        elif len(edge.label) > len(self.longest_in_edge.label):
            self.longest_in_edge = edge
        self.in_edges.append(edge)

    def add_out_edge(self, edge):
        if self.longest_out_edge is None:
            self.longest_out_edge = edge
        if len(edge.label) > len(self.longest_out_edge.label or ''):
            self.longest_out_edge = edge
        self.out_edges.append(edge)

    def longest_edge(self, reverse=False):
        if reverse is True:
            return self.longest_in_edge
        else:
            return self.longest_out_edge

    def edges(self, reverse=False):
        edges = self.in_edges if reverse is True else self.out_edges
        if len(edges) == 0:
            return None

    def sorted_edges(self, reverse=False):
        edges = self.edges(reverse=reverse)
        return sorted(edges, key=lambda x: -len(x.label))
