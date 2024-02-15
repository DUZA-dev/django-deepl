import copy

from typing import Type, Union

from django.db import models
from django.core.exceptions import ImproperlyConfigured


from django_deepl.settings import DEEPL_LOCALES


SUPPORTED_FIELDS = (
    models.fields.CharField,
    models.fields.TextField,
    models.fields.files.FieldFile
)


def create_field(field_name: str, model: Type[models.Model], deepl_fields: dict):
    """
    Creates a new field for each locale
    field_name: name field without locale postfix
    model: target model from which the field is copied
    deepl_fields: options for copy (locales, and etc.)
    """
    for locale in (
            (deepl_fields.get(field_name) or {}).get('locales')
            or DEEPL_LOCALES
    ):
        TranslationField(
            locale,
            target_field_name=field_name,
            target_model=model
        ).save()


class TranslationField:
    def __init__(
            self,
            lang: str,

            name: str = None,

            target_model: Type[models.Model] = None,
            target_field_name: str = None,

            target_field: Union[SUPPORTED_FIELDS] = None
    ):
        """
        Definition new translate field

        target_name: str - name of the target translation field
        target_model: models.Model - model containing target field name
        lang: str - language new translations field
        """

        self.lang = lang
        self.target_model = target_model
        self.target_field = target_field
        self.target_field_name = target_field_name

        self.name = name
        if name:
            self.name = name
        elif self.target_field_name:
            self.name = "_".join([self.target_field_name, 'deepl', lang])

        self.field = self.copy_field(
            self.name,
            self.target_field or (self.target_model, self.target_field_name)
        )

        if not isinstance(self.field, SUPPORTED_FIELDS):
            raise ImproperlyConfigured('Target field type not supported')

    @staticmethod
    def copy_field(
            new_name: str,
            target_field: Union[Union[SUPPORTED_FIELDS], tuple[models.Model, str]],
    ):
        """ Copy target field, with change Names attributes """

        if type(target_field) is tuple:
            model = target_field[0]
            field_name = target_field[1]

            target_field = copy.deepcopy(
                getattr(model, field_name).field
            )
            new_field = target_field.__class__()
        else:
            new_field = target_field()

        new_field.__dict__.update(target_field.__dict__)

        if target_field.__dict__.get('name') is None:
            setattr(new_field, "name", new_name)
        else:
            for key in new_field.__dict__:
                if new_field.__dict__[key] == target_field.__dict__['name']:
                    new_field.__dict__[key] = new_name

        # Set blank translate field
        if 'model' in locals():
            setattr(new_field, "blank", getattr(model, 'blank', True))

        return new_field

    def save(self):
        """ Add field to target model """
        self.target_model.add_to_class(self.name, self.field)
