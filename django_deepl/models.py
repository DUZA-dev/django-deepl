from typing import Any, Type

from django.db import models
from django_deepl.fields import SUPPORTED_FIELDS, create_field


def filter_attrs_models(attr: str) -> dict[Type[models.Model], Any]:
    """
    Detects the models needed for translation in models.py
    of the required project and prepares it for work
    attrs: str - attributes in model with descriptions
    """
    import inspect

    from django.apps import apps
    from django.utils.module_loading import module_has_submodule

    modules = [
        (app_config.name, app_config.module)
        for app_config in apps.get_app_configs()
    ]

    data = dict()

    for app, module in modules:
        if not module_has_submodule(module, 'models'):
            continue

        # Select models
        classes = inspect.getmembers(module.models, inspect.isclass)
        inspect_models = [
            cls for name, cls in classes
            if issubclass(cls, models.Model)
        ]

        # Filter models with select attr
        for _ in inspect_models:
            if hasattr(_, attr):
                data[_] = getattr(_, attr, None)

    return data


def construct():
    """
    Working on creating new translation fields
    targeting fields specified by the user
    """

    deepl_models = filter_attrs_models('DEEPL_FIELDS')
    for model, deepl_fields in deepl_models.items():
        # In future supported set attrs from dict
        if type(deepl_fields) is list:
            deepl_fields = dict.fromkeys(deepl_fields)
        fields_names = deepl_fields.keys()

        # To translate fields
        for field in fields_names or model._meta.fields:
            if (field.__class__ in SUPPORTED_FIELDS and (field := field.name)) \
                or type(field) is str:

                create_field(field, model, deepl_fields)
