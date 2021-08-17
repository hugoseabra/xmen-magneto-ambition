from . import DNA
from .codon_pair import CodonPair, AminoAcid


class InsufficientCodonPairsError(Exception):
    """
    Raises exception when codon pairs is not enough to support a valid DNA.
    """
    pass


class Analyser:
    """
    Responsible to execute DNA analysis to find out whether an DNA is
    mutant or not.
    """

    def __init__(self):
        # Creating reference DNA for analysis
        self.mutant_dna = self._create_mutant_dna()

    def is_mutant(self, dna: DNA) -> bool:
        """
        Checks whether dna provided is mutant or not if more than one sequence
        found.
        :param dna: DNA provided
        :return: whether DNA is mutant or not
        """
        self._check_dna(dna)

        has_sequences = [
            pair for pair in dna
            if self.mutant_dna.has_sequence(pair)
        ]

        # If more than 1 existent sequence, dna provided is mutant
        return len(has_sequences) > 1

    @staticmethod
    def _create_mutant_dna() -> DNA:
        dna = DNA()

        # Sequence 1
        dna.append(CodonPair(
            (AminoAcid.A, AminoAcid.T, AminoAcid.G),
            (AminoAcid.C, AminoAcid.G, AminoAcid.A),
        ))

        # Sequence 2
        dna.append(CodonPair(
            (AminoAcid.C, AminoAcid.A, AminoAcid.G),
            (AminoAcid.T, AminoAcid.G, AminoAcid.C),
        ))

        # Sequence 3
        dna.append(CodonPair(
            (AminoAcid.T, AminoAcid.T, AminoAcid.A),
            (AminoAcid.T, AminoAcid.G, AminoAcid.T),
        ))

        # Sequence 4
        dna.append(CodonPair(
            (AminoAcid.A, AminoAcid.G, AminoAcid.A),
            (AminoAcid.A, AminoAcid.G, AminoAcid.G),
        ))

        # Sequence 5
        dna.append(CodonPair(
            (AminoAcid.C, AminoAcid.C, AminoAcid.C),
            (AminoAcid.C, AminoAcid.T, AminoAcid.A),
        ))

        # Sequence 6
        dna.append(CodonPair(
            (AminoAcid.T, AminoAcid.C, AminoAcid.A),
            (AminoAcid.C, AminoAcid.T, AminoAcid.G),
        ))

        return dna

    @staticmethod
    def _check_dna(dna: DNA):
        if dna.is_valid() is False:
            raise InsufficientCodonPairsError(
                f'DNA is not valid. It has {len(dna)} codon pairs only.'
            )
