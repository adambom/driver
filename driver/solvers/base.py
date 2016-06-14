from Queue import Queue


class CheckableQueue(Queue):
    def __contains__(self, item):
        """Allow for testing of queue membership."""
        with self.mutex:
            return item in self.queue


def assemble(overlaps):
    best_sequence = None
    sequences = set()
    longest_path = 0

    # Implements "best"-first search
    # Run one search for each overlap record
    # so we can compute all possible assemblies
    # and determine the best
    #
    # The proper heuristic for determining the best assembly
    # is TBD, but for a first pass, assemblies are evaluated
    # based on path length (traversal depth)
    for root in overlaps:
        frontier = CheckableQueue()
        frontier.put(root)
        path = []
        explored = set()

        while not frontier.empty():
            node = frontier.get()

            # We are revisiting a node that's already been explored
            if node in explored:
                break

            # Get the valid edge with the longest overlap
            edges = node.sorted_edges() or []
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

        # Merge the sequences, starting with root
        sequence = root.value
        for edge in path:
            sequence += edge.node.value[len(edge.label):]

        # Test traversal depth (quality heuristic)
        if len(path) > longest_path:
            best_sequence = sequence
            longest_path = len(path)

        sequences.add(sequence)

    return best_sequence, sequences
