Sequence Assembly
=================

This library attempts to provide an interface for performing sequence assembly in 
bioinformatics.

The original problem statement can be found [here](http://rosalind.info/problems/long/).

# Quick Start

Clone the repository

```bash
git clone https://github.com/adambom/driver.git
```

The files can be found at the root:

```bash
cd driver
```

For a quickstart, use `python` to run the examples in `main.py`

```bash
python main.py
```

This will run through some sample sequence assembly problems, using two different algorithms.

# Usage

Two solvers are provided out of the box in the `driver/solvers` directory: `rosalind_solver`, which is specific to the Rosalind
problem, and `bwt_solver`, a more robust and performant solver for general purpose sequence
assembly problems.

A generic overlap graph assembler is also provided in `base` so that novel solvers can be constructed.
Tools for constructing graphs and FM-indexes are found in `driver/util`.

## Examples

```python
from driver.solvers import rosalind_solver, bwt_solver


reads = [
    'ATTAGACCTG',
          'CCTGCCGGAA',
       'AGACCTGCCG',
             'GCCGGAATAC', ]

best, all = rosalind_solver.solve(reads)
best_, all_ = bwt_solver.solve(reads)

assert best == best_ == 'ATTAGACCTGCCGGAATAC'
```

`bwt_solver` also takes an optional argument, `tau` [default = 3], which is an integer that represents the minimum
suffix length to consider. This can be useful in tuning specific applications:

```python
from driver.examples import gettysburg
from driver.solvers import bwt_solver


reads = gettysburg.get_reads()

best, all = bwt_solver.solve(reads, tau=100)
```

# Algorithms

## Overlap, Layout, Consensus

The approach to solving sequence assembly problems can be defined as a sequence of phases.
In this work we deal with three (error checking and quality scoring are out of scope).

### Overlap

The first phase is to find the overlaps between the reads. That is, for each read in the
input set, we must find all suffix -> prefix pairs such that the suffix of the source read
is a prefix of the target read. For example:

We would say that for the pair of reads:

`ATTAGACCTG` and `CCTGCCGGAA`

The suffix of the source (`ATTAGACCTG`) matches that of the target (`CCTGCCGGAA`). In this
case, we would say that the reads have an overlap of `CCTG`.

Once all the overlaps have been found, we move to the next phase, layout.

### Layout

If you think of the reads as nodes on a graph, and the edges betwen them being the overlaps
they share, we can construct a directed graph to help conceptualize the problem. Edges point
from the suffixed read to the prefixed read, and the edge is labeled by the overlap.

For example:

`ATTAGACCTG ----[CCTG]----> CCTGCCGGAA`

If this is continued for each read in the set, we get a full overlap graph.

![Example overlap graph](http://journals.plos.org/ploscompbiol/article/figure/image?download&size=large&id=info:doi/10.1371/journal.pcbi.1003345.g003)

The goal of the layout step is to find the shortest path that visits each node exactly once.

This is analogous to the [Traveling Salesman Problem](https://simple.wikipedia.org/wiki/Travelling_salesman_problem),
which is shown to be NP-hard, and can only be computed in O(N!) time.

As an alternative, we choose a "greedy"-based assembly algorithm, which uses a heuristic to guide the
traversal, with edges with longer labels being preferred.

Unfortunately, since heuristics result in approximations, they will not always lead to an optimal solution.

### Consensus

This is the process of combining the reads from the chosen path through the overlap graph into a continous
superstring.

For example:

`ATTAGACCTG + CCTGCCGGAA ---> ATTAGACCGGAA`

## Rosalind Solver

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

## BWT Solver

Whereas the Rosalind solver is ideally suited for solving one type
of problem, it is not robust or fast enough to handle diverse and large
sets of reads.

This solver makes use of an FM-index (described below) to achieve fast 
suffix testing.

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

## FM Index

This warrants some further discussion. An FM Index is a data structure that allows us
to compute overlaps in sub-quadratic time, which is a huge improvement over the brute
force approach.

It makes use of a suffix array, computed over the range, `R = Ri + Ri+1 + Ri+2 + ... + Rn`,
where `R` is the set of reads in the input.

To this, we add a Burrows-Wheeler Transform, or `BWT`, which was originally developed for
text compression, since it is reversible, and tends to group identical characters together
in a string, which allows for efficient runlength encoding, for example.

To complete the index, we add two more adjunct data structures which won't be described here.

For more on the FM Index, have a look at [this article](http://alexbowe.com/fm-index/).


# References

- The FM-Index and Genome Assembly: ftp://ftp.sanger.ac.uk/pub/resources/theses/js18/chapter2.pdf
- [Next-Generation Sequence Assembly: Four Stages of Data Processing and Computational Challenges. El-Metwally, et. Al](http://journals.plos.org/ploscompbiol/article/asset?id=10.1371%2Fjournal.pcbi.1003345.PDF)
- [FM-Indexes and Backwards Search. Alex Bowe. (2011)](http://alexbowe.com/fm-index/)
- [Introduction to the Burrows-Wheeler Transform and FM Index. Langmead, Ben. (2013)](http://www.cs.jhu.edu/~langmea/resources/bwt_fm.pdf)
- [Burrows-Wheeler Transform and FM Index. Langmead, Ben](https://www.cs.jhu.edu/~langmea/resources/lecture_notes/bwt_and_fm_index.pdf)

