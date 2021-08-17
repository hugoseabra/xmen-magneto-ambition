from django.db import models


class LogRequest(models.Model):
    """ Model to a log request """

    class Meta:
        verbose_name = 'Log Request'
        verbose_name_plural = 'Log requests'
        ordering = ['requested_at']

    requested_at = models.DateTimeField(
        verbose_name='requested at',
        blank=False,
        null=False,
        auto_now=True,
        db_index=True,
        editable=False
    )

    dna_sequence = models.TextField(
        verbose_name='DNA Sequence',
        help_text='Logs the sequence requested for audition',
        blank=False,
        null=False
    )

    mutant = models.BooleanField(
        verbose_name='Is mutant?',
        help_text='Logs the result whether DNA sequence is mutant or not',
        null=False,
        blank=False
    )


class LogRequestStatistics(models.Model):
    """ Log request statistics """

    class Meta:
        verbose_name = 'Log Request Statistic'
        verbose_name_plural = 'Log Request Statistics'

    count_human_dna = models.IntegerField(
        verbose_name='# human DNA',
        blank=False,
        null=False,
        editable=False
    )

    count_mutant_dna = models.IntegerField(
        verbose_name='# mutant DNA',
        blank=False,
        null=False,
        editable=False
    )

    ratio = models.DecimalField(
        verbose_name='Ratio mutant found',
        decimal_places=1,
        max_digits=6,
        blank=False,
        null=False,
        editable=False
    )
