import copy

from typing import Type

from django.db import models
from django.core.exceptions import ImproperlyConfigured


from django_deepl.settings import DEEPL_LOCALES


SUPPORTED_FIELDS = (
    models.fields.CharField,
    models.fields.TextField,
    models.fields.files.FieldFile
)


def create_field(field_name: str, model: Type[models.Model], deepl_fields: dict):
    """ Creates a new field for each locale """
    for locale in (
            (deepl_fields.get(field_name) or {}).get('locales')
            or DEEPL_LOCALES
    ):
        TranslationField(field_name, model, locale).save()


class TranslationField:
    def __init__(
            self,
            target_name: str,
            target_model: Type[models.Model],
            lang: str
    ):
        """
        Definition new translate field
        target_name: str - name of the target translation field
        target_model: models.Model - model containing target field name
        lang: str - language new translations field
        """

        self.target_name = target_name
        self.target_model = target_model
        self.name = "_".join([self.target_name, 'deepl', lang])

        self.target_field = copy.deepcopy(
            getattr(self.target_model, self.target_name).field
        )

        self.field = self.target_field.__class__()

        if not isinstance(self.field, SUPPORTED_FIELDS):
            raise ImproperlyConfigured('Target field type not supported')

        self.construction_field()

    def construction_field(self):
        """ Copy target field, with change Names attributes """
        self.field.__dict__.update(self.target_field.__dict__)

        for key in self.field.__dict__:
            if self.field.__dict__[key] == self.target_field.__dict__['name']:
                self.field.__dict__[key] = self.name

        # Set blank translate field
        setattr(self.field, "blank", getattr(self.target_model, 'blank', True))

    def save(self):
        """ Add field to target model """
        self.target_model.add_to_class(self.name, self.field)
