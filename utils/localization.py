# utils/localization.py

import json
import os
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from config import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, LOCALES_DIR

class Localization(I18nMiddleware):
    def __init__(self, domain, path):
        super().__init__(domain, path)
        self.translations = {}
        for lang in SUPPORTED_LANGUAGES:
            try:
                with open(os.path.join(path, f'{lang}.json'), 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)
            except FileNotFoundError:
                print(f"Localization file for {lang} not found.")

    async def get_user_locale(self, action, args):
        user = types.User.get_current()
        lang_code = user.language_code if user.language_code in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
        return lang_code

    def t(self, lang_code, text_key, **kwargs):
        translation = self.translations.get(lang_code, self.translations[DEFAULT_LANGUAGE])
        keys = text_key.split('.')
        for key in keys:
            translation = translation.get(key, {})
        if isinstance(translation, str):
            return translation.format(**kwargs)
        else:
            return text_key  # Возвращаем ключ, если перевод не найден

i18n = Localization('messages', LOCALES_DIR)
_ = i18n.t  # Сокращение для удобства
