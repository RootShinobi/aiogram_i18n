import gettext
from typing import Dict


from cores.base import BaseCore


class BabelCore(BaseCore):
    locales: Dict[str, gettext.GNUTranslations]

    def __init__(
            self,
            *,
            path: str,
            default_locale: str = "en"
    ) -> None:
        self.path = path
        self.default_locale = default_locale

    async def startup(self, *args, **kwargs):
        self.locales = self.find_locales()

    def find_locales(self) -> Dict[str, gettext.GNUTranslations]:
        """
        Load all compiled locales from path

        :return: dict with locales
        """
        translations: Dict[str, gettext.GNUTranslations] = {}
        locales = self._extract_locales(self.path)
        for locale, paths in self._find_locales(self.path, locales, ".mo").items():
            trans = translations[locale] = gettext.GNUTranslations()
            for path in paths:
                with open(path, "rb") as fp:
                    trans._parse(fp=fp) # noqa

        return translations

    def get(self, locale: str, key: str, *args, **kwargs):
        translator = self.get_translator(locale=locale)
        return translator.gettext(key).format(*args, **kwargs)
