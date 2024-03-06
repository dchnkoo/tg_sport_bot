import regex


check_text = lambda x: regex.findall("(.+)-(.+)", x)
