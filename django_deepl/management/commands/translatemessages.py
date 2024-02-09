import os
import logging

import polib
import deepl

from django.core.management.base import BaseCommand
from django.conf import settings

from deepl.api_data import TextResult


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = '''
        Translates .po files. The values of the msgid parameter 
        are translated and stored in the msgstr parameter, 
        provided that there are no values already set there.
    '''

    def add_arguments(self, parser):
        parser.add_argument('--locale', '-l', nargs='?', default=[], dest='locale',
                            action='append', help='Translate .po files, selected locales')
        parser.add_argument('--en-dialect', '-ed', default='EN-US', dest='en_dialect',
                            help='English default dialect (EN-US or EN-GB) for locales "EN"')
        parser.add_argument('--deepl_api_key', dest='DEEPL_API_KEY', action='store_const',
                            help='Use django settings or set deepl API key here')
        parser.add_argument('--fuzzy', '-f', dest='fuzzy', action='store_true',
                            help='Set "fuzzy" flag for entries')

    def set_options(self, **options):
        self.locale = options['locale']
        self.fuzzy = options['fuzzy']
        self.en_dialect = options['en_dialect']

        self.translator = deepl.Translator(options['DEEPL_API_KEY'] or settings.DEEPL_API_KEY)

    def handle(self, *args, **options):
        assert getattr(settings, 'USE_I18N', False), 'I18N is disabled'
        assert getattr(settings, 'LOCALE_PATHS', False), 'Locale paths not find'
        assert getattr(settings, 'DEEPL_API_KEY', False) or options['DEEPL_API_KEY'], 'Deepl is disabled'

        self.set_options(**options)

        for _ in settings.LOCALE_PATHS:
            # Search .po files
            for root, dirs, files in os.walk(_):
                lang = os.path.basename(os.path.dirname(root))
                # If pass user locale not contains current .po file lang
                if lang not in self.locale and self.locale:
                    continue

                for file in files:
                    if file.endswith('.po'):
                        self.translate_po(root, file, lang)

    def get_messages_for_translate(self, entries: set[polib.MOEntry]) -> list[str]:
        """ Collects the contents of records for translation """
        messages = list()
        for entrie in entries:
            # Get not translated singular and plural msg entries
            if entrie.msgid and not entrie.msgstr:
                messages.append(entrie.msgid)
            if entrie.msgid_plural and not entrie.msgstr_plural:
                messages.append(entrie.msgid_plural)
        return messages

    def modify_po_entries(
            self,
            entries: set[polib.MOEntry],
            translated_messages: list[TextResult]
    ) -> None:
        """
        Modifies the passed record objects according
        to the received translation
        """
        for entrie in entries:
            # Set translated messages
            if entrie.msgid and not entrie.msgstr:
                entrie.msgstr = translated_messages[0].text
                del translated_messages[0]

            if entrie.msgid_plural and not entrie.msgid_plural:
                entrie.msgstr_plural = translated_messages[0].text
                del translated_messages[0]

            # If user set fuzzy, in entries sets the flag
            if self.fuzzy and not entrie.fuzzy:
                entrie.flags.append('fuzzy')

    def translate_po(self, root: str, name_file: str, lang: str) -> None:
        """ Переводит указанный .po файл в указанный язык """
        file = polib.pofile(os.path.join(root, name_file))

        # Entries from the get file, are untranslated and not obsolete
        entries = set(file.untranslated_entries()) - set(file.obsolete_entries())
        messages = self.get_messages_for_translate(entries)

        if not messages:
            return

        translated_messages = self.translator.translate_text(
            messages,
            target_lang=self.en_dialect if lang.upper() == "EN" else lang
        )

        self.modify_po_entries(entries, translated_messages)
        file.save()
