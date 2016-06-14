from driver.solvers.base import assemble

from driver.util.fm_index import find_intervals
from driver.util.fm_index import FMIndex
from driver.util.fm_index import ReadLibrary

from driver.util.graph import Edge


def _expand_right(index, position):
    """
    Get the full text of the string that was matched.

    Start at the beginning of the entry in the suffix array
    corresponding to the matched prefix, and look rightwards
    until we reach a $, indicating the end of the matched
    substring.
    """
    match = ''
    j = 1
    while True:
        c = index.input_str[index.suffix_array[position] + j]
        if c == '$':
            break
        match += c
        j += 1
    return match


def build_overlap_graph(reads, tau=3):
    lib = ReadLibrary(reads)
    index = FMIndex(lib.concat_reads)

    for read in lib.reads.values():
        edges = find_intervals(index, read.value, tau=tau)

        for l, u, label in edges:
            if read.value.startswith(label):
                continue

            for i in range(l, u + 1):
                match = _expand_right(index, i)
                if match == read.value:
                    continue
                edge_node = lib.reads[match]
                read.add_out_edge(Edge(edge_node, label))
                edge_node.add_in_edge(Edge(read, label))
    return lib.reads

"""
This solver uses an FM-index to achieve fast suffix testing.

We precompute the index in O(C * log C), where C is the number of total base
pairs sequenced. The advantage of building this index is that reads with a
prefix, P, matching a suffix, S, can be retrieved in O(S) time, and allows us
to avoid the N^2 complexity of the naive approach.

For each read, X, we iterate through the set of its suffixes, and check for
the presence of prefixes that match this suffix. When a matching prefix is
located, we output an edge in the string graph.

In the worst case, we visit each base pair in the set of reads, doing O(1) work
for each suffix, allowing the ovelap detection phase run in simply O(C) time.

The assembly phase is essentially breadth-first search, so the time complexity
is O(N + M), where N is the number of reads and M is the number of edges
between them.

When we combine the index computation and overlap detection, we get a total
runtime of O(N + M + C + C * log C). When read length is assumed to be constant
this reduces to: O(N + M + N * log N).

The space complexity involves the total of the index and the string graph,
which comes out to O(C + M), or O(R + M) when the reads are constant length.
"""


def solve(reads, tau=3):
    overlaps = build_overlap_graph(reads, tau=tau)
    return assemble(overlaps.values())
