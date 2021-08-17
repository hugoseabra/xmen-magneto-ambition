from django.test import TestCase
from django.urls import reverse


class MutantEndpointTests(TestCase):
    def _get_url(self):
        return reverse('mutant:mutant-list')

    def test_validation_of_how_many_items(self):
        """Tests error when less than 6 sequences is sent """
        data = {
            'dna': [
                "ATGCGA",
                "CAGTGC",
                "TTATGT",
                "AGAAGG",
                "CCCCTA"
            ]
        }
        response = self.client.post(self._get_url(), data=data)
        self.assertContains(response, 'DNA is not valid', status_code=400)

        data = {
            'dna': [
                "ATGCGA",
                "CABTGC",  # <-- WRONG char
                "TTATGT",
                "AGAAGG",
                "CCCCTA",
                "TCACTG",
            ]
        }
        response = self.client.post(self._get_url(), data=data)
        self.assertContains(
            response,
            'You must provide correct amino acid values with 6 digits:'
            ' A, C, G, T',
            status_code=400
        )

    def test_post_mutant_check(self):
        """Tests whether a sequence of amino acids of a DNA is mutant """
        data = {
            'dna': [
                "TTATTT",
                "CAGTGC",
                "TTATTT",
                "TTATTT",
                "GCGTCA",
                "TTATTT",
            ]
        }
        response = self.client.post(self._get_url(), data=data)
        self.assertContains(response, 'DNA is not mutant', status_code=403)

        data = {
            'dna': [
                "ATGCGA",
                "CAGTGC",
                "TTATGT",
                "AGAAGG",
                "CCCCTA",
                "TCACTG"
            ]
        }
        response = self.client.post(self._get_url(), data=data)
        self.assertContains(response, 'DNA is mutant', status_code=200)
