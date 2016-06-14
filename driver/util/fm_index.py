from driver.util.graph import Node


class IntervalSet(set):
    pass


class FMIndex(object):
    def __init__(self, input_str, alphabet=None):
        self.input_str = input_str
        self.alphabet = alphabet or sorted(set(input_str))

    @property
    def suffixes(self):
        if hasattr(self, '_suffixes'):
            return self._suffixes
        self._suffixes = [
            self.input_str[-i:] for i in range(len(self.input_str), 0, -1)]
        return self._suffixes

    @property
    def suffix_array(self):
        """
        Return the suffix array for the input string.

        The suffix array represents the indexes of the starting positions
        for each suffix in the sorted suffix array.

        For example, for the string 'ACG$:

        The suffixes are '$', 'G$', 'CG$', and 'ACG$'. To get the suffix
        array, we order those suffixes and find the position it starts
        in the original string:

        Sorted suffixes: '$', 'ACG$', 'CG$', 'G$'
        Suffix array: [3, 0, 1, 2]
        """
        if hasattr(self, '_suffix_array'):
            return self._suffix_array
        self._suffix_array = [x[0] for x in sorted(
            enumerate(self.suffixes), key=lambda x: x[1])]
        return self._suffix_array

    @property
    def bwt(self):
        """
        Calculate the Burrows-Wheeler Transform on the input string.

        The rules for this transformation are as follows:

        For an input string, S, with Suffix Array, SA, enumarated by symbol i:

        i = 0 => '$'
        i > 0 => S[SA[i] - 1]
        """
        if hasattr(self, '_bwt'):
            return self._bwt
        self._bwt = ''.join([
            '$' if x == 0 else self.input_str[x - 1]
            for i, x in enumerate(self.suffix_array)])
        return self._bwt

    @property
    def lex_rank(self):
        """
        Return a lexographic rank of the suffixes in the input string.

        For each unique symbol, a, in the input string, S, this value contains
        the number of symbols lexographicically smaller than a in S

        For example in the string 'ACG$':

        {
            '$': 0,
            'A': 1,
            'C': 2,
            'G': 3
        }
        """
        if hasattr(self, '_lex_rank'):
            return self._lex_rank
        counts = {}
        for i, suffix in enumerate(sorted(self.suffixes)):
            if suffix[0] in counts:
                continue
            counts[suffix[0]] = i
        self._lex_rank = counts
        return self._lex_rank

    @property
    def occurrences(self):
        """
        Return the symbol occurrence count.

        For each symbol, a, in the alphabet, records the number
        of occurences of a less than or equal to position, i,
        in the Burrows-Wheeler Transform array.

        For example, for the input string 'AAGTA$':

        The BWT of the input string is 'AT$AAG'

        So the symbol occurrence count would be:
        {
            '$': [0, 0, 1, 1, 1, 1],
            'A': [1, 1, 1, 2, 3, 3],
            'G': [0, 0, 0, 0, 0, 1]
        }
        """
        if hasattr(self, '_occurences'):
            return self._occurences
        occurences = dict([(a, []) for a in self.alphabet])
        for i, c in enumerate(self.bwt):
            for a in self.alphabet:
                occ = occurences[a][i - 1] if len(occurences[a]) else 0
                if c == a:
                    # incr occurrences
                    occ += 1
                occurences[a].append(occ)
        self._occurences = occurences
        return self._occurences

    def get_occurrences_lt(self, a, i):
        """
        Calculate the inverse symbol occurrence count.

        Similar to @property occurrences, but instead of returning the count
        of symbols in bwt greater than symbol, a, at position, i, this tallies
        the count of symbols less than symbol, a, at position, i.

        We do not store this as a property since it can be calculated in
        O(|ALPHABET|) time, which is essentially constant, by summing the
        values of @property occurrences for all symbols less than a.

        For example, for the input string 'AAGTA$':

        The BWT of the input string is 'AT$AAG'

        So the inverse symbol occurrence count would be:
        {
            '$': [0, 0, 0, 0, 0, 0],
            'A': [0, 0, 1, 1, 1, 1],
            'G': [1, 1, 2, 3, 4, 5]
        }
        """
        return sum([self.occurrences[c][i] for c in self.alphabet if c < a])

    def _update_backward(self, l, u, a):
        """
        Calculate the range of a substring within the input string.

        Given a string S, with suffix array SA:

        Assume we know the suffix array interval, (l, u) for a given
        substring, s in S. We can calculate the suffix array interval,
        (l', u') for a new string, a + s, using this equation.

        If l' > u', then a + s cannot be found in S

        Otherwise, the range of the substring a + s can be computed
        using SA, such that S[SA[x]:] should contain the query string
        for each x in [l', u'].
        """
        rank = self.lex_rank[a]
        occ = self.occurrences[a]
        return (rank + occ[l - 1], rank + occ[u] - 1)

    def _update_forward_backward(self, l, u, ll, uu, a):
        """ll, uu = l', u'."""
        ll += self.get_occurrences_lt(a, u) - self.get_occurrences_lt(a, l - 1)
        uu = ll + self.occurrences[a][u] - self.occurrences[a][l - 1] - 1
        l, u = self._update_backward(l, u, a)
        return (l, u, ll, uu)

    def _init_search_interval(self, a):
        l = self.lex_rank[a]
        try:
            u = self.lex_rank[self.alphabet[self.alphabet.index(a) + 1]] - 1
        except IndexError:
            u = len(self.suffix_array) - 1
        return (l, u)

    def backward_search(self, query):
        """
        Find the position of a substring within the input string.

        Given a string S, with suffix array SA, and a query Q:

        This function will return the range, l, u in SA that
        corresponds to positions in S matching Q.

        For example,
        Given S = AAGAGTAGAA$, Q = AGA, SA = [10, 9, 8, 0, 6, 1, 3, 7, 2, 4, 5]

        This function will return [4, 5], which corresponds to matches at
        positions S[6] and SA[1] in S, or S[6:9] and S[1:4].

        Runs in O(|query|) time
        """
        l, u = self._init_search_interval(query[-1])

        i = len(query) - 2
        while u >= l and i >= 0:
            l, u = self._update_backward(l, u, query[i])
            i -= 1

        return l, u


class ReadLibrary(object):
    def __init__(self, reads):
        self.reads = dict([(r, Node(r)) for r in reads])
        self.concat_reads = '$' + '$'.join(self.reads) + '$'


def find_intervals(index, target, tau=3):
    intervals = IntervalSet()

    i = len(target) - 2
    l, u = index._init_search_interval(target[-1])
    l_, u_ = l, u

    while l <= u and i >= 0:
        if len(target) - i > tau:
            ll, uu, ll_, uu_ = index._update_forward_backward(
                l, u, l_, u_, '$')
            if ll <= uu:
                intervals.add((ll, uu, target[i + 1:]))
                # intervals.add((ll, uu, ll_, uu_, target[i + 1:]))
        l, u, l_, u_ = index._update_forward_backward(l, u, l_, u_, target[i])
        i -= 1
    return intervals


def extract_irreducible(index, index_, intervals):
    if len(intervals) == 0:
        return intervals

    irreducible = IntervalSet()

    for l, u, l_, u_, overlap in intervals:
        ll_, uu_, ll, uu = index_._update_forward_backward(l_, u_, l, u, '$')
        if ll <= uu:
            irreducible.add((ll, uu, overlap))

    if len(irreducible) != 0:
        return irreducible

    for a in index.alphabet:
        intervals_a = IntervalSet()
        for l, u, l_, u_, overlap in intervals:
            la_, ua_, la, ua = index_._update_forward_backward(l_, u_, l, u, a)
            if la <= ua:
                intervals_a.add((la, ua, la_, ua_, overlap))
        for interval in extract_irreducible(index, index_, intervals_a):
            irreducible.add(interval)

    return irreducible
