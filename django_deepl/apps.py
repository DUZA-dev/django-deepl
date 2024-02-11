from django.apps import AppConfig


class DjangoDeeplConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_deepl'

    def ready(self):
        from django_deepl.models import construct

        construct()
