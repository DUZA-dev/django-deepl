# Django + Deepl

Интеграция Deepl переводчика в Django для машинного перевода

- [English README.md](README.md)

## Установка

Добавьте django_deepl в начало списка INSTALLED_APPS.
Опционально заполните DEEPL_LOCALES.
**Не забудьте** установить `DEEPL_API_KEY`.

```
INSTALLED_APPS = [
      'django_deepl',
      ...
]

DEEPL_API_KEY = '...'
DEEPL_LOCALES = ['es', 'ru', 'ua']
```

## Перевод .po файлов

Запустите команды
- `python3 Manage.py makemessages`
- `python3 Manage.py Translatemessages`

**Готово, можете компилить!**

## Перевод моделей

Перевод полей модели News

новости/models.py
```
class News:
      title = models.CharField(max_length=256)
      description = models.TextField()
    
      DEEPL_FIELDS = {
          'description': {},
          'title': {
              'locales': ['es', 'ru']
          }
      }
```
Для поля описания будут сгенерированы дополнительные локализованные
поля которые вы указали в `project/settings.py:DEEPL_LOCALES`, а если
она не установлена, будет сгенерировано поле по умолчанию для английского языка.