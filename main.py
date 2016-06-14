import logging
import time

from driver.examples import gettysburg, rosalind, tubthumping
from driver.solvers import bwt_solver, rosalind_solver


log = logging.getLogger(__name__)


def linebreak(n=1):
    print
    for x in xrange(n):
        print '#########################################'
    print


def main():
    print'Reconstructing the Rosalind sequence using our naive solver'
    reads = rosalind.get_reads()
    start = time.clock()
    result = rosalind_solver.solve(reads)
    print 'Found assembly: %s' % result
    print 'Computed in %fs' % (time.clock() - start)

    linebreak(n=5)

    print'Reconstructing the Rosalind sequence using our BWT solver'
    reads = rosalind.get_reads()
    start = time.clock()
    result = bwt_solver.solve(reads, tau=100)
    print 'Found assembly: %s' % result
    print 'Computed in %fs' % (time.clock() - start)

    linebreak(n=5)

    N, min_len, max_len = 1000, 85, 100
    print(
        'Reconstructing the Gettysburg Address '
        'from %i reads of %i to %i symbols long' % (N, min_len, max_len))
    reads = gettysburg.get_reads(N, min_len, max_len)
    start = time.clock()
    result = bwt_solver.solve(reads, tau=10)
    print 'Found assembly: %s' % result
    print 'Computed in %fs' % (time.clock() - start)

    linebreak(n=5)

    N, min_len, max_len = 500, 25, 50
    print(
        'Reconstructing Tubthumping '
        'from %i reads of %i to %i symbols long' % (N, min_len, max_len))
    reads = tubthumping.get_reads(N, min_len, max_len)
    start = time.clock()
    result = bwt_solver.solve(reads, tau=25)
    print 'Found assembly: %s' % result
    print 'Computed in %fs' % (time.clock() - start)

if __name__ == '__main__':
    main()
