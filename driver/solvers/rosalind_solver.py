from driver.solvers.base import assemble

from driver.util.graph import Edge, Node


def build_overlap_graph(reads):
    reads = [Node(r) for r in reads]
    for x in reads:
        for y in reads:
            if x == y:
                continue
            # Check all suffixes from x[1:] through x[|x|/2:]
            for i in xrange(1, len(x.value) / 2 + 1):
                suffix = x.value[i:]
                if y.value.startswith(suffix):
                    x.out_edges.append(Edge(y, suffix))
                    y.in_edges.append(Edge(x, suffix))
    return reads


"""
The Rosalind solver handles the special case where reads
are reasonably small (<= 1kbp) and few in number (<= 50).
It also relies on the condition that the superset of reads
can be reduced in a unique way to reconstruct the entire
superstring by combining reads that overlap by more than
half their length.

The algorithm traverses each of the N reads up to N - 1 times
in order to iteratively determine the overlaps between each pair
of reads.

Calculating the overlap takes O(|Xi|) time, where |Xi| is the
length of read i.

If we assume that reads are mostly identical in length, the time
complexity simplifies to O(N^2).

For space, the overlap graph requires O(N) storage for nodes
and O(M) storage for the overlaps. Since we are guaranteed a
unique traverasll through the graph, we know that each node
is connected by exactly one or fewer outbound edges, so the space
complexity simplifies to O(N).
"""


def solve(reads):
    overlaps = build_overlap_graph(reads)
    return assemble(overlaps)
