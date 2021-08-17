from django.test import TestCase

from library.genetics.codon_pair import AminoAcid, CodonPair


class CodonPairTests(TestCase):
    def test_correct_sequence(self):
        """
        Tests correct sequence provided in Codon pair after instance is built
        """
        codon1 = (AminoAcid.A, AminoAcid.C, AminoAcid.G)
        codon2 = (AminoAcid.G, AminoAcid.T, AminoAcid.T)

        codon_pair = CodonPair(codon1, codon2)

        seq1 = f'{codon1[0].name}{codon1[1].name}{codon1[2].name}'
        seq2 = f'{codon2[0].name}{codon2[1].name}{codon2[2].name}'
        sequence = f'{seq1}{seq2}'

        self.assertEqual(codon_pair.sequence, sequence)

    def test_sequence_equality(self):
        """ Tests sequence equality """
        codon1 = (AminoAcid.A, AminoAcid.C, AminoAcid.G)
        codon2 = (AminoAcid.G, AminoAcid.T, AminoAcid.T)

        # Let's create two codons using the same sequence
        codon_pair1 = CodonPair(codon1, codon2)
        codon_pair2 = CodonPair(codon1, codon2)

        # Now let's create another codon pair with a different sequence
        other_codon1 = (AminoAcid.A, AminoAcid.A, AminoAcid.G)
        other_codon2 = (AminoAcid.C, AminoAcid.T, AminoAcid.G)
        codon_pair3 = CodonPair(other_codon1, other_codon2)

        # Codon pair 1 and 2 are different of 3
        self.assertFalse(codon_pair1.is_equal(codon_pair3))
        self.assertFalse(codon_pair2.is_equal(codon_pair3))

        # Codon pair 3 is different of 1 and 2
        self.assertFalse(codon_pair3.is_equal(codon_pair1))
        self.assertFalse(codon_pair3.is_equal(codon_pair2))

        # Codon pair 1 is equals 2
        self.assertTrue(codon_pair1.is_equal(codon_pair2))
        self.assertTrue(codon_pair2.is_equal(codon_pair1))
