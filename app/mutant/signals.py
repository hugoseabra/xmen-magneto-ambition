import shutil
from decimal import Decimal

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.mutant.models import LogRequest, LogRequestStatistics


@receiver(post_save, sender=LogRequest)
def update_stats(instance, raw, created, **_):
    if raw is True:
        return

    num_humans = LogRequest.objects.filter(mutant=False).count()
    num_mutants = LogRequest.objects.filter(mutant=True).count()

    if num_humans > 1:
        ratio = num_mutants / num_humans
    else:
        ratio = 0

    # Clean cache
    if hasattr(settings, 'FILE_CACHE_DIR'):
        shutil.rmtree(settings.FILE_CACHE_DIR)

    try:
        stats = LogRequestStatistics.objects.get(pk=1)
        stats.count_human_dna = num_humans
        stats.count_mutant_dna = num_mutants
        stats.ratio = ratio
        stats.save()

    except LogRequestStatistics.DoesNotExist:
        LogRequestStatistics.objects.create(
            count_human_dna=num_humans,
            count_mutant_dna=num_mutants,
            ratio=round(Decimal(ratio), 1),
        )
