__all__ = ["string"]

from aiogoogletrans import Translator

translator = Translator()


class TranslateString(str):

    def __call__(self, value: str):
        return self.__new__(self.__class__, value)

    async def translate_to_lang(self, language_code: str):
        translation = await translator.translate(text=self.__str__(), src="uk", dest=language_code)
        return translation.text