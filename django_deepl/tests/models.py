from django.db import models


class Model1Test(models.Model):
    title = models.CharField("title", max_length=255)
    text = models.TextField(blank=True, null=True)

    DEEPL_FIELDS = {
        'title': {},
        'text': {
            'locales': ['es', 'ru']
        }
    }


class Model2Test(models.Model):
    title = models.CharField("title", max_length=255)
    text = models.TextField(blank=True, null=True)

    DEEPL_FIELDS = {}
