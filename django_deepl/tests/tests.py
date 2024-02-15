from django.test import TestCase
from django.db import models

from django_deepl.models import filter_attrs_models
from django_deepl.fields import TranslationField, create_field
from django_deepl.tests.models import Model1Test, Model2Test


class TestFieldsPy(TestCase):
    class TestModelFieldsPy(models.Model):
        text = models.CharField(max_length=256)

    def test_create_fields(self):
        create_field(
            'text',
            self.TestModelFieldsPy,
            deepl_fields = {
                'text': {
                    'locales': ['locale1', 'locale2']
                }
            }
        )

        fields = dir(self.TestModelFieldsPy)

        self.assertIn('text_deepl_locale1', fields)
        self.assertIn('text_deepl_locale2', fields)

        self.assertNotIn('text_deepl_locale3', fields)

    def test_translation_field(self):
        test_target_field_name = TranslationField(
            lang='ru',
            target_model=self.TestModelFieldsPy,
            target_field_name='text'
        )

        self.assertEqual('text_deepl_ru', test_target_field_name.field.name)

        test_target_field = TranslationField(
            lang = 'en',
            name = 'test_deepl_en',
            target_field = models.fields.CharField
        )

        self.assertEqual('test_deepl_en', test_target_field.field.name)


class TestModelsPy(TestCase):
    def test_filter_attrs_models(self):
        self.assertEqual(0, len(filter_attrs_models('NO_DEEPL_FIELDS')))
        self.assertNotEqual(0, filter_attrs_models('NO_DEEPL_FIELDS'))


class TestModels(TestCase):
    def test_model_field_deepl1(self):
        obj = Model1Test(title='test_title_1', text='test_text_1')
        obj.save()

        self.assertEqual('test_text_1', obj.text)
        self.assertEqual('test_title_1', obj.title)

        fields = dir(obj)

        self.assertIn('text_deepl_es', fields)
        self.assertIn('text_deepl_ru', fields)
        self.assertIn('title_deepl_en', fields)

        self.assertNotIn('text_deepl_en', fields)
        self.assertNotIn('title_deepl_es', fields)
        self.assertNotIn('title_deepl_ru', fields)

    def test_model_field_deepl2(self):
        obj = Model2Test(title='test_title_2', text='test_text_2')
        obj.save()

        self.assertEqual('test_text_2', obj.text)
        self.assertEqual('test_title_2', obj.title)

        fields = dir(obj)

        self.assertIn('text_deepl_en', fields)
        self.assertIn('title_deepl_en', fields)

        self.assertNotIn('test_deepl_ru', fields)
        self.assertNotIn('title_deepl_es', fields)
