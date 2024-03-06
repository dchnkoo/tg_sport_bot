from googletrans import Translator

def translate(text: str, language_code: str):
    tr = Translator().translate(text=text, src="uk", dest=language_code)

    return tr.text