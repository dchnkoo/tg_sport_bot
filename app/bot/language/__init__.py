from googletrans import Translator

translator = Translator()


def translate(text: str, language_code: str):
    translation = translator.translate(text=text, dest=language_code)

    return translation.text