from enum import Enum
from typing import Sequence, Tuple


class AminoAcid(Enum):
    """
    A, C, G, and T are the "letters" of the DNA code;
    they stand for the chemicals adenine (A), cytosine (C), guanine (G),
     and thymine (T), respectively, that make up the nucleotide bases of DNA.
    """
    A = 'Adenine'
    C = 'Cytosine'
    G = 'Guanine'
    T = 'Thymine'


class CodonPair:
    """
    Codons are made up of any triplet combination of the four nitrogenous
    bases adenine (A), guanine (G), cytosine (C), or uracil (U)
    """

    def __init__(self,
                 codon1: Tuple[AminoAcid, AminoAcid, AminoAcid],
                 codon2: Tuple[AminoAcid, AminoAcid, AminoAcid]):
        """
        :param codon1: First codon triplet
        :param codon2: Second codon triplet
        """
        self.codon1 = codon1
        self.codon2 = codon2

    @property
    def sequence(self) -> str:
        """ Returns sequence altogether """
        s1 = f'{self.codon1[0].name}{self.codon1[1].name}{self.codon1[2].name}'
        s2 = f'{self.codon2[0].name}{self.codon2[1].name}{self.codon2[2].name}'
        return f'{s1}{s2}'

    def is_equal(self, codon_pair: 'CodonPair') -> bool:
        """
        Checks whether the provided codon pair sequence is the same as the
        current instance's sequence.
        :param codon_pair: Provided codon pair instance
        :return: whether sequence is equals to the codon pair provided
        """
        return self.sequence == codon_pair.sequence
