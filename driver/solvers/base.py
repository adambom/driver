from Queue import Queue


class CheckableQueue(Queue):
    def __contains__(self, item):
        """Allow for testing of queue membership."""
        with self.mutex:
            return item in self.queue


def bfs(root, explored=None, reverse=False):
    frontier = CheckableQueue()
    frontier.put(root)
    path = []
    explored = explored or set()

    while not frontier.empty():
        node = frontier.get()

        # We are revisiting a node that's already been explored
        if node in explored:
            break

        # Get the valid edge with the longest overlap
        edges = node.sorted_edges(reverse=reverse) or []
        edges = [
            e for e in edges
            if e.node not in frontier and e.node not in explored]

        # This node is a leaf
        if len(edges) == 0:
            break

        # Queue the next best edge for exploration
        explored.add(node)
        edge = edges[0]
        frontier.put(edge.node)
        path.append(edge)

    return path if reverse is False else reversed(path)


def assemble(overlaps):
    # Pick a node at random
    root = overlaps[0]

    # Walk backwards until a node with no in-edges is found
    # (or until we reach a visited node)
    reverse_path = list(bfs(root, reverse=True))
    forward_path = bfs(root)

    # Initialize sequence
    sequence = ''

    # Walk through path upstream to root
    for edge in reverse_path:
        sequence += edge.node.value[:-len(edge.label)]

    # Append root value
    sequence += root.value

    # Walk through path downstream from root
    for edge in forward_path:
        sequence += edge.node.value[len(edge.label):]

    return sequence
