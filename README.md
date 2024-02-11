# Django + Deepl

Integration Deepl Translate in Django

- [Russian README.md](README.ru.md)

## Install

Add `django_deepl` before installed applications, 
and optional set default `DEEPL_LOCALES`. 
**Don't forget** to install the `DEEPL_API_KEY`.

```
INSTALLED_APPS = [
    'django_deepl',
    ...
]

DEEPL_API_KEY = '...'
DEEPL_LOCALES = ['es', 'ru', 'ua']
```

## Translate .po files

Running commands
- `python3 manage.py makemessages`
- `python3 manage.py translatemessages`

**Complete!**

## Models translate

Translate models field

news/models.py
```
class News:
    title = models.CharField(max_length=256)
    description = models.TextField()
    
    DEEPL_FIELDS = {
        'description': {},
        'name': {
            'locales': ['es', 'ru']
        }
    }
```
For the description field, English or languages from those installed in `project/settings.py:DEEPL_LOCALES`
