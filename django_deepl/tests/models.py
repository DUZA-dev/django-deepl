from django.db import models


class TestModel1(models.Model):
    title = models.CharField("title", max_length=255)
    text = models.TextField(blank=True, null=True)

    DEEPL_FIELDS = {
        'title': {},
        'text': {
            'locales': ['es', 'ru']
        }
    }


class TestModel2(models.Model):
    title = models.CharField("title", max_length=255)
    text = models.TextField(blank=True, null=True)

    DEEPL_FIELDS = {}
