import os

from unittest import TestCase

from polib import pofile
from deepl.api_data import TextResult

from django_deepl.management.commands.translatemessages import Command

class TestTranslateMessages(TestCase):
    def setUp(self):
        cmd = Command()
        cmd.set_options(**dict(
            locale=[],
            en_dialect='EN-GB',
            fuzzy=False,
            DEEPL_API_KEY=''
        ))
        self.cmd = cmd
        self.po = pofile(os.path.join(os.path.dirname(__file__), 'data/django.po'))

    def test_get_untranslated_entries(self):
        entries = self.cmd.get_untranslated_entries(self.po)
        self.assertIs(type(entries), set)

        entries_msgid = [entry.msgid or entry.msgid_plural for entry in entries]
        self.assertIn('Пароль', entries_msgid)
        self.assertNotIn('Почта', entries_msgid)

    def test_get_messages_for_translate(self):
        entries = self.cmd.get_untranslated_entries(self.po)
        messages = self.cmd.get_messages_for_translate(entries)

        self.assertIs(type(messages), list)
        self.assertIn('Пароль', messages)
        self.assertNotIn('Почта', messages)

    def test_modify_po_entries(self):
        entries = self.cmd.get_untranslated_entries(self.po)
        self.assertEqual(len(entries), 2)

        messages = ['DUZA-dev', 'Second example']
        translated_messages = [TextResult(msg, 'EN') for msg in messages]

        self.cmd.modify_po_entries(
            entries,
            translated_messages
        )

        for entry in entries:
            self.assertIn(entry.msgstr, messages)

        entries = self.cmd.get_untranslated_entries(self.po)
        self.assertEqual(len(entries), 0)
