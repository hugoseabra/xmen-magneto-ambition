from collections import UserList
from typing import Tuple, List

from .codon_pair import CodonPair


class DNACodonPairLimitError(Exception):
    """
    Raises exception when DNA reaches the maximum of codon pairs.
    """
    pass


class DNACodonPairRemovalError(Exception):
    """
    Raises exception whe a Codon Pair removal is not allowed.
    """
    pass


class DNA(UserList):
    """
    A collection of Codon Pairs that represent an emulation of human DNA.
    The object will contain exactly 6 codon pairs that will represent the
    the nucleotide bases of the DNA.

    Attributes:
        top_left_oblique_pair       Codon pairs to generated obliquely from top
                                    left to right bottom.
        bottom_left_oblique_pair    Codon pairs to generated obliquely from
                                    bottom right to left top.
        vertical_pair_columns       Codon pairs to generated vertically as the
                                    the 6 supported columns.
    """
    top_left_oblique_pair: CodonPair
    bottom_left_oblique_pair: CodonPair
    vertical_pair_columns: Tuple[
        CodonPair,
        CodonPair,
        CodonPair,
        CodonPair,
        CodonPair,
        CodonPair
    ] = ()

    def remove(self, codon_pair: CodonPair) -> None:
        """
        Blocks the support to remove Codon Pair after DNA is already valid
        """
        if self.is_valid():
            raise DNACodonPairRemovalError('You cannot remove a Codon Pair')
        super().remove(codon_pair)

    def append(self, codon_pair: CodonPair) -> None:
        """
        Appends a Codon pair to collection
        :param codon_pair: Codon pair instance
        """
        if self.is_valid():
            raise DNACodonPairLimitError(
                'There are enough codon pairs added to the DNA'
            )

        self.data.append(codon_pair)
        if self.is_valid():
            self._build_oblique_pairs()
            self._build_column_pairs()

    def to_sequence_list(self) -> List[str]:
        sequences = []
        for code_pair in self:
            sequences.append(code_pair.sequence)
        return sequences

    def is_valid(self) -> bool:
        """
        Checks whether the DNA is complete and valid the expected numbers of
        Codon pairs
        :return: whether DNA is valid
        """
        return len(self) == 6

    def has_sequence(self, codon_pair: CodonPair) -> bool:
        """
        Checks whether codon pair provided has its sequence inside the current
        DNA.
        :param codon_pair: Provided codon pair instance
        :return: whether codon pair has sequence in DNA or not
        """

        # Horizontal sequence check
        for dna_codon_pair in self:
            if dna_codon_pair.is_equal(codon_pair):
                return True

        # Vertical sequence check
        for dna_codon_pair in self.vertical_pair_columns:
            if dna_codon_pair.is_equal(codon_pair):
                return True

        # Oblique sequence check, top-down
        if self.top_left_oblique_pair.is_equal(codon_pair):
            return True

        # Oblique sequence check, bottom-up
        if self.bottom_left_oblique_pair.is_equal(codon_pair):
            return True

        # There is no sequence match in every directions of the DNA
        return False

    def _build_oblique_pairs(self):
        """ Builds oblique pairs from left to right, top-down and bottom-up """
        # seq 1
        codon1_1 = self[0].codon1
        codon1_2 = self[0].codon2

        # seq 2
        codon2_1 = self[1].codon1
        codon2_2 = self[1].codon2

        # seq 3
        codon3_1 = self[2].codon1
        codon3_2 = self[2].codon2

        # seq 4
        codon4_1 = self[3].codon1
        codon4_2 = self[3].codon2

        # seq 5
        codon5_1 = self[4].codon1
        codon5_2 = self[4].codon2

        # seq 6
        codon6_1 = self[5].codon1
        codon6_2 = self[5].codon2

        # Oblique sequence from left to right, top-down
        self.top_left_oblique_pair = CodonPair(
            (codon1_1[0], codon2_1[1], codon3_1[2]),
            (codon4_2[0], codon5_2[1], codon6_2[2]),
        )

        # Oblique sequence from left to right, bottom-up
        self.bottom_left_oblique_pair = CodonPair(
            (codon6_1[0], codon5_1[1], codon4_1[2]),
            (codon3_2[0], codon2_2[1], codon1_2[2]),
        )

    def _build_column_pairs(self):
        """ Builds column pairs """
        # seq 1
        codon1_1 = self[0].codon1
        codon1_2 = self[0].codon2

        # seq 2
        codon2_1 = self[1].codon1
        codon2_2 = self[1].codon2

        # seq 3
        codon3_1 = self[2].codon1
        codon3_2 = self[2].codon2

        # seq 4
        codon4_1 = self[3].codon1
        codon4_2 = self[3].codon2

        # seq 5
        codon5_1 = self[4].codon1
        codon5_2 = self[4].codon2

        # seq 6
        codon6_1 = self[5].codon1
        codon6_2 = self[5].codon2

        c1 = CodonPair(
            (codon1_1[0], codon2_1[0], codon3_1[0]),
            (codon4_1[0], codon5_1[0], codon6_1[0]),
        )

        c2 = CodonPair(
            (codon1_1[1], codon2_1[1], codon3_1[1]),
            (codon4_1[1], codon5_1[1], codon6_1[1]),
        )

        c3 = CodonPair(
            (codon1_1[2], codon2_1[2], codon3_1[2]),
            (codon4_1[2], codon5_1[2], codon6_1[2]),
        )

        c4 = CodonPair(
            (codon1_2[0], codon2_2[0], codon3_2[0]),
            (codon4_2[0], codon5_2[0], codon6_2[0]),
        )

        c5 = CodonPair(
            (codon1_2[1], codon2_2[1], codon3_2[1]),
            (codon4_2[1], codon5_2[1], codon6_2[1]),
        )

        c6 = CodonPair(
            (codon1_2[2], codon2_2[2], codon3_2[2]),
            (codon4_2[2], codon5_2[2], codon6_2[2]),
        )

        self.vertical_pair_columns = (c1, c2, c3, c4, c5, c6)
