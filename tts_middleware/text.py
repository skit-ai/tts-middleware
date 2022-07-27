import re

from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from google.transliteration import transliterate_text


def eng_to_hin(word, lang_code):
    reg = re.compile(r'[a-zA-Z]')
    if reg.match(word):
        return transliterate_text(word, lang_code)
    return word


def transliteration(text, lang_code):
    with ThreadPoolExecutor(max_workers=8) as executor:
        trans_arr = list(executor.map(eng_to_hin, text.split(" "), repeat(lang_code)))   
    return (" ".join(trans_arr))
