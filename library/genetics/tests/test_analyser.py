from random import choice
from unittest import TestCase

from library.genetics import Analyser, AminoAcid, CodonPair, DNA, \
    InsufficientCodonPairsError


class AnalyserTests(TestCase):
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

    def _create_dna(self,
                    c1: CodonPair = None,
                    c2: CodonPair = None,
                    c3: CodonPair = None,
                    c4: CodonPair = None,
                    c5: CodonPair = None,
                    c6: CodonPair = None) -> DNA:
        codon1 = c1 or self._create_codon_pair()
        codon2 = c2 or self._create_codon_pair()
        codon3 = c3 or self._create_codon_pair()
        codon4 = c4 or self._create_codon_pair()
        codon5 = c5 or self._create_codon_pair()
        codon6 = c6 or self._create_codon_pair()

        dna = DNA()
        dna.append(codon1)
        dna.append(codon2)
        dna.append(codon3)
        dna.append(codon4)
        dna.append(codon5)
        dna.append(codon6)

        return dna

    def test_error_when_dna_is_invalid(self):
        """ Tests exception when an invalid DNA is being analysed """
        codon1 = self._create_codon_pair()
        codon2 = self._create_codon_pair()

        dna = DNA()
        dna.append(codon1)
        dna.append(codon2)

        # DNA is invalid
        self.assertFalse(dna.is_valid())

        analyser = Analyser()

        with self.assertRaises(InsufficientCodonPairsError):
            analyser.is_mutant(dna)

    def test_creation_of_mutant_dna(self):
        """ Tests whether mutant DNA has the correct sequence """
        sequences = [
            'ATGCGA',
            'CAGTGC',
            'TTATGT',
            'AGAAGG',
            'CCCCTA',
            'TCACTG',
        ]

        analyser = Analyser()
        mutant_dna = analyser.mutant_dna

        for index, code_pair in enumerate(mutant_dna):
            self.assertEqual(code_pair.sequence, sequences[index])

    def test_as_not_mutant_with_no_sequence_exist(self):
        """ Tests as not mutant when there no sequence match on codon pairs """
        analyser = Analyser()
        dna = self._create_dna()

        self.assertFalse(analyser.is_mutant(dna))

    def test_as_not_mutant_with_only_one_sequence(self):
        """
        Tests when one codon pair exists and it is not enough to flag mutant DNA
        """
        analyser = Analyser()

        # Let's create DNA of which one of its codon pairs is the same
        # as mutant DNA
        common_pair = analyser.mutant_dna[1]
        dna = self._create_dna(
            None,
            None,
            common_pair
        )

        # Validating that common codon pair really exists in dna
        self.assertTrue(analyser.mutant_dna.has_sequence(dna[2]))

        # However, it is not enough to define the DNA as mutant
        self.assertFalse(analyser.is_mutant(dna))

    def test_as_mutant_with_more_than_one_sequence(self):
        """ Tests 2 matches and flags DNA as mutant """
        analyser = Analyser()

        # Let's create DNA of which one of its codon pairs is the same
        # as mutant DNA
        common_pair = analyser.mutant_dna[1]
        common_pair2 = analyser.mutant_dna[4]
        dna = self._create_dna(
            None,
            None,
            common_pair,
            None,
            common_pair2
        )

        # However, it is not enough to define the DNA as mutant
        self.assertTrue(analyser.is_mutant(dna))
