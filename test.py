import unittest

from driver.util.fm_index import find_intervals
from driver.util.fm_index import FMIndex


class TestFMIndex(unittest.TestCase):

    def test_init(self):
        input_str = '$AGAG$GACA$'
        fm = FMIndex(input_str)
        self.assertEqual(fm.input_str, input_str)
        self.assertEqual(fm.alphabet, sorted(set(input_str)))
        alphabet = 'ADM'
        fm = FMIndex(input_str, alphabet=alphabet)
        self.assertEqual(fm.alphabet, alphabet)

    def test_suffixes(self):
        fm = FMIndex('ADAM$')
        for sfx in ['$', 'M$', 'AM$', 'DAM$', 'ADAM$']:
            self.assertTrue(sfx in fm.suffixes)

    def test_suffix_array(self):
        fm = FMIndex('ADAM$')
        self.assertEqual([4, 0, 2, 1, 3], fm.suffix_array)

    def test_bwt(self):
        fm = FMIndex('AAGTA$')
        self.assertEqual('AT$AAG', fm.bwt)

    def test_lex_rank(self):
        fm = FMIndex('ATTAGACCTGCCGGAA$')
        self.assertEqual(fm.lex_rank['$'], 0)
        self.assertEqual(fm.lex_rank['A'], 1)
        self.assertEqual(fm.lex_rank['C'], 6)
        self.assertEqual(fm.lex_rank['G'], 10)
        self.assertEqual(fm.lex_rank['T'], 14)

    def test_occurrences(self):
        fm = FMIndex('AAGTA$')
        # bwt = 'AT$AAG'
        self.assertEqual(fm.occurrences, {
            '$': [0, 0, 1, 1, 1, 1],
            'A': [1, 1, 1, 2, 3, 3],
            'G': [0, 0, 0, 0, 0, 1],
            'T': [0, 1, 1, 1, 1, 1], })

    def test_get_occurrences_lt(self):
        fm = FMIndex('AAGTA$')
        ran = range(len(fm.bwt))
        # bwt = 'AT$AAG'
        occ_lt_a = [fm.get_occurrences_lt('A', i) for i in ran]
        occ_lt_t = [fm.get_occurrences_lt('T', i) for i in ran]
        occ_lt_g = [fm.get_occurrences_lt('G', i) for i in ran]
        occ_lt_d = [fm.get_occurrences_lt('$', i) for i in ran]

        self.assertEqual(occ_lt_a, [0, 0, 1, 1, 1, 1])
        self.assertEqual(occ_lt_t, [1, 1, 2, 3, 4, 5])
        self.assertEqual(occ_lt_g, [1, 1, 2, 3, 4, 4])
        self.assertEqual(occ_lt_d, [0, 0, 0, 0, 0, 0])

    def test__update_backward(self):
        fm = FMIndex('AAGTA$')
        # Look for pattern 'GT'
        # Start with last symbol in query, T
        # Interval for single character, a is just:
        # (lex_rank[a], lex_rank[a + 1] - 1)
        # where a + 1 is the next largest symbol in the alphabet.
        # In this case, since T is already the largest,
        # we just assume lex_rank[a + 1] = len(SA)
        l, u = fm.lex_rank['T'], len(fm.suffix_array) - 1
        a = 'G'
        l_, u_ = fm._update_backward(l, u, a)
        self.assertEqual(l_, 4)
        self.assertEqual(u_, 4)

    def test__update_forward_backward(self):
        fm = FMIndex('AAGTA$')
        # Look for pattern 'GT'
        # And determine if it is a right extension
        l, u = fm.lex_rank['T'], len(fm.suffix_array) - 1
        ll, uu = l, u
        a = 'G'
        l_, u_, ll_, uu_ = fm._update_forward_backward(l, u, ll, uu, a)
        self.assertEqual((l_, u_, ll_, uu_), (4, 4, 5, 5))

    def test__init_search_interval(self):
        fm = FMIndex('AB')
        l, u = fm._init_search_interval('A')
        self.assertEqual(l, fm.lex_rank['A'])
        self.assertEqual(u, fm.lex_rank['B'] - 1)

        # Largest character in alphabet
        l, u = fm._init_search_interval('B')
        self.assertEqual(l, fm.lex_rank['B'])
        self.assertEqual(u, len(fm.suffix_array) - 1)

    def test_backward_search(self):
        fm = FMIndex('AAGTA$')
        query = 'AGT'
        l, u = fm.backward_search(query)
        self.assertEqual(
            query,
            fm.input_str[fm.suffix_array[l]:fm.suffix_array[l] + len(query)])

        # Multiple matches
        fm = FMIndex('AAGAGTAGAA$')
        query = 'AGA'
        l, u = fm.backward_search(query)
        for i in xrange(l, u + 1):
            self.assertEqual(
                query,
                fm.input_str[
                    fm.suffix_array[i]:fm.suffix_array[i] + len(query)]
            )

    def test_find_intervals(self):
        fm = FMIndex('$ATTAGACCTG$CCTGCCGGAA$')
        prefix = '$CCTG'

        # Target: ATTAGACCTG
        # Goal: find substrings whose prefix matches a suffix of target
        intervals = find_intervals(fm, 'ATTAGACCTG')

        # Expected: interval for CCTG along with right terminal (GCCGGAA$)
        l, u, label = list(intervals)[0]
        r, sa = fm.input_str, fm.suffix_array

        self.assertEqual(label, 'CCTG')
        self.assertEqual(r[sa[l]:sa[l] + len(prefix)], prefix)


if __name__ == '__main__':
    unittest.main()
