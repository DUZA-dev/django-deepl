from django.conf import settings

DEEPL_API = getattr(settings, 'DEEPL_API_KEY', None)

DEEPL_LOCALES = getattr(settings, 'DEEPL_LOCALES', ['en', ])
