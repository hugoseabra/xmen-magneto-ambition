from random import choice
from unittest import TestCase

from library.genetics import (
    AminoAcid,
    CodonPair,
    DNACodonPairLimitError,
    DNACodonPairRemovalError
)
from library.genetics import DNA


class DNATests(TestCase):
    def _get_random_amino_acid(self) -> AminoAcid:
        return choice([v for v in AminoAcid])

    def _create_codon_pair(self) -> CodonPair:
        codon1 = self._get_random_amino_acid()
        codon2 = self._get_random_amino_acid()
        codon3 = self._get_random_amino_acid()
        codon4 = self._get_random_amino_acid()
        codon5 = self._get_random_amino_acid()
        codon6 = self._get_random_amino_acid()

        return CodonPair(
            (codon1, codon2, codon3),
            (codon4, codon5, codon6)
        )

    def _create_dna(self) -> DNA:
        pair1 = self._create_codon_pair()
        pair2 = self._create_codon_pair()
        pair3 = self._create_codon_pair()
        pair4 = self._create_codon_pair()
        pair5 = self._create_codon_pair()
        pair6 = self._create_codon_pair()

        dna = DNA()
        dna.append(pair1)
        dna.append(pair2)
        dna.append(pair3)
        dna.append(pair4)
        dna.append(pair5)
        dna.append(pair6)

        return dna

    def test_appending_codon_pairs(self):
        codon_pair1 = self._create_codon_pair()
        codon_pair2 = self._create_codon_pair()
        codon_pair3 = self._create_codon_pair()

        dna = DNA()
        dna.append(codon_pair1)
        dna.append(codon_pair2)
        dna.append(codon_pair3)

        self.assertEqual(len(dna), 3)

        self.assertEqual(dna[0], codon_pair1)
        self.assertEqual(dna[1], codon_pair2)
        self.assertEqual(dna[2], codon_pair3)

    def test_valid_dna(self):
        codon_pair1 = self._create_codon_pair()
        codon_pair2 = self._create_codon_pair()
        codon_pair3 = self._create_codon_pair()

        dna = DNA()
        dna.append(codon_pair1)
        dna.append(codon_pair2)
        dna.append(codon_pair3)

        self.assertEqual(len(dna), 3)

        # Not valid because the dna is not complete. It must contain 6 pairs
        self.assertFalse(dna.is_valid())

        codon_pair4 = self._create_codon_pair()
        codon_pair5 = self._create_codon_pair()

        dna.append(codon_pair4)
        dna.append(codon_pair5)

        # still invalid
        self.assertFalse(dna.is_valid())

        codon_pair6 = self._create_codon_pair()
        dna.append(codon_pair6)

        # Now valid
        self.assertTrue(dna.is_valid())

    def test_removal_error_after_valid(self):
        """ Tests DNA to not support codon pair removal after it is valid """
        codon_pair1 = self._create_codon_pair()
        codon_pair2 = self._create_codon_pair()
        codon_pair3_1 = self._create_codon_pair()

        dna = DNA()
        dna.append(codon_pair1)
        dna.append(codon_pair2)
        dna.append(codon_pair3_1)

        self.assertEqual(len(dna), 3)

        # Not valid because the dna is not complete. It must contain 6 pairs
        self.assertFalse(dna.is_valid())

        # Allows removal
        dna.remove(codon_pair3_1)

        self.assertEqual(len(dna), 2)

        codon_pair3_2 = self._create_codon_pair()
        codon_pair4 = self._create_codon_pair()
        codon_pair5 = self._create_codon_pair()
        codon_pair6 = self._create_codon_pair()

        dna.append(codon_pair3_2)
        dna.append(codon_pair4)
        dna.append(codon_pair5)
        dna.append(codon_pair6)

        # Now dna is valid
        self.assertTrue(dna.is_valid())

        # And cannot remove codon pair anymore
        with self.assertRaises(DNACodonPairRemovalError):
            dna.remove(codon_pair4)

    def test_dna_existent_sequence(self):
        """
        Tests whether the sequence of codon pair are set as expected inside DNA
        instance.
        """
        pairs = [
            self._create_codon_pair(),
            self._create_codon_pair(),
            self._create_codon_pair(),
            self._create_codon_pair(),
            self._create_codon_pair(),
            self._create_codon_pair(),
        ]

        dna = DNA()
        for codon_pair in pairs:
            dna.append(codon_pair)

        for index, code_pair in enumerate(dna):
            self.assertEqual(code_pair.sequence, pairs[index].sequence)

    def test_correct_sequence_list(self):
        """ Tests whether the sequence list of codon pairs is correct """
        pairs = [
            self._create_codon_pair(),
            self._create_codon_pair(),
            self._create_codon_pair(),
            self._create_codon_pair(),
            self._create_codon_pair(),
            self._create_codon_pair(),
        ]

        sequences = [p.sequence for p in pairs]

        dna = DNA()
        [dna.append(p) for p in pairs]

        # Sequence must match
        self.assertEqual(dna.to_sequence_list(), sequences)

    def test_vertical_pairs_built(self):
        """
        Tests whether the vertical columns of codon pairs are correctly
        generated
        """
        dna = self._create_dna()

        p1 = dna.data[0]
        p2 = dna.data[1]
        p3 = dna.data[2]
        p4 = dna.data[3]
        p5 = dna.data[4]
        p6 = dna.data[5]

        # Let's build the sequences according to what we have in DNA columns
        col_part1 = []
        col_part2 = []
        for c in range(0, 3):
            c1 = f'{p1.codon1[c].name}{p2.codon1[c].name}{p3.codon1[c].name}'
            c2 = f'{p4.codon1[c].name}{p5.codon1[c].name}{p6.codon1[c].name}'
            col = f'{c1}{c2}'
            col_part1.append(col)

            c1 = f'{p1.codon2[c].name}{p2.codon2[c].name}{p3.codon2[c].name}'
            c2 = f'{p4.codon2[c].name}{p5.codon2[c].name}{p6.codon2[c].name}'
            col = f'{c1}{c2}'
            col_part2.append(col)

        columns = col_part1 + col_part2

        # In columns we have a sequence like (build from DNA columns):
        # ['ACTCAA', 'GTACTA', 'AGTTTA', 'ACTCAA', 'GTACTA', 'AGTTTA']
        # Let's compare the columns above to the ONES built internally in
        # DNA
        for index, col_seq in enumerate(columns):
            dna_column_pair = dna.vertical_pair_columns[index]
            self.assertEqual(col_seq, dna_column_pair.sequence)

    def test_oblique_pairs_built(self):
        """
        Tests whether the oblique sequences of codon pairs are correctly
        generated
        """
        dna = self._create_dna()

        p1 = dna.data[0]
        p2 = dna.data[1]
        p3 = dna.data[2]
        p4 = dna.data[3]
        p5 = dna.data[4]
        p6 = dna.data[5]

        # Let's build the sequences according to what we have in DNA columns
        top_down_seq = f'{p1.codon1[0].name}{p2.codon1[1].name}{p3.codon1[2].name}'
        top_down_seq += f'{p4.codon2[0].name}{p5.codon2[1].name}{p6.codon2[2].name}'

        bottom_up = f'{p6.codon1[0].name}{p5.codon1[1].name}{p4.codon1[2].name}'
        bottom_up += f'{p3.codon2[0].name}{p2.codon2[1].name}{p1.codon2[2].name}'

        # Let's compare the sequences above to the ONES built internally in
        # DNA
        self.assertEqual(top_down_seq, dna.top_left_oblique_pair.sequence)
        self.assertEqual(bottom_up, dna.bottom_left_oblique_pair.sequence)

    def test_horizontal_sequence_match(self):
        """
        Tests whether a sequence matches an horizontal sequence in DNA
        """
        dna = self._create_dna()

        # Existing codon pair
        correct_codon_pair = dna.data[2]

        # Another codon pair
        other_pair = self._create_codon_pair()

        self.assertFalse(dna.has_sequence(other_pair))
        self.assertTrue(dna.has_sequence(correct_codon_pair))

    def test_vertical_sequence_match(self):
        """
        Tests whether a sequence matches a vertical sequence in DNA
        """
        dna = self._create_dna()

        # Existing codon pair
        correct_codon_pair = dna.vertical_pair_columns[2]

        # Another codon pair
        other_pair = self._create_codon_pair()

        self.assertFalse(dna.has_sequence(other_pair))
        self.assertTrue(dna.has_sequence(correct_codon_pair))

    def test_oblique_sequence_match(self):
        """
        Tests whether a sequence matches an oblique sequence in DNA
        """
        dna = self._create_dna()

        # Another codon pair
        other_pair = self._create_codon_pair()

        self.assertFalse(dna.has_sequence(other_pair))

        # Existing codon pair
        self.assertTrue(dna.has_sequence(dna.top_left_oblique_pair))
        self.assertTrue(dna.has_sequence(dna.bottom_left_oblique_pair))

    def test_whether_dna_has_sequence(self):
        codon_pair1 = self._create_codon_pair()
        codon_pair2 = self._create_codon_pair()
        codon_pair3 = self._create_codon_pair()
        codon_pair4 = self._create_codon_pair()
        codon_pair5 = self._create_codon_pair()
        codon_pair6 = self._create_codon_pair()

        dna = DNA()
        dna.append(codon_pair1)
        dna.append(codon_pair2)
        dna.append(codon_pair3)
        dna.append(codon_pair4)
        dna.append(codon_pair5)
        dna.append(codon_pair6)

        self.assertEqual(len(dna), 6)
        self.assertTrue(dna.is_valid())

        # Some other codon to compare to DNA
        other_codon1 = (AminoAcid.A, AminoAcid.A, AminoAcid.A)
        other_codon2 = (AminoAcid.A, AminoAcid.A, AminoAcid.A)
        other_codon_pair = CodonPair(other_codon1, other_codon2)

        # Sequence must not exist
        self.assertFalse(dna.has_sequence(other_codon_pair))

        # Sequence now exists
        self.assertTrue(dna.has_sequence(codon_pair5))

    def test_error_if_more_then_6_codon_pairs(self):
        codon_pair1 = self._create_codon_pair()
        codon_pair2 = self._create_codon_pair()
        codon_pair3 = self._create_codon_pair()
        codon_pair4 = self._create_codon_pair()
        codon_pair5 = self._create_codon_pair()
        codon_pair6 = self._create_codon_pair()
        codon_pair7 = self._create_codon_pair()

        dna = DNA()
        dna.append(codon_pair1)
        dna.append(codon_pair2)
        dna.append(codon_pair3)
        dna.append(codon_pair4)
        dna.append(codon_pair5)
        dna.append(codon_pair6)

        with self.assertRaises(DNACodonPairLimitError):
            dna.append(codon_pair7)
