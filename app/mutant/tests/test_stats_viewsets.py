from django.test import TestCase
from django.urls import reverse


class MutantEndpointTests(TestCase):
    def _get_url(self):
        return reverse('mutant:stats-list')

    def test_stats_request(self):
        """ Tests stats request """

        response = self.client.get(self._get_url())
        self.assertContains(response, 'count_human_dna', status_code=200)
        self.assertContains(response, 'count_mutant_dna', status_code=200)
        self.assertContains(response, 'ratio', status_code=200)

