from django.apps import AppConfig


class MutantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.mutant'
    label = 'mutant'
    verbose_name = 'Mutant'
