from functools import wraps
from typing import Tuple
from indictrans import Transliterator
import re
from itertools import repeat
from google.transliteration import transliterate_text

import numpy as np
from pyquery import PyQuery as pq

from tts_middleware.audio import (transform_pitch, transform_rate,
                                  transform_volume)
from tts_middleware.elements import _get_preprocessing_attributes

# Data array and sample rate
Audio = Tuple[np.ndarray, int]


def eng_to_hin(word, lang_code):
    reg = re.compile(r'[a-zA-Z]')
    if word not in '[@_!#$%^&*()<>?/\|}{~:]' and reg.match(word):
        return transliterate_text(word, lang_code)
    return word

def transliteration(text, lang_code):
    trans_arr = list(map(eng_to_hin, text.split(" "), repeat(lang_code)))   
    return (" ".join(trans_arr))

def tts_middleware(tts_function):
    """
    Decorator function for allowing SSML tags for a TTS.
    """

    @wraps(tts_function)
    def _tts(text: str, language_code: str, transliterate: bool) -> Audio:
        node = pq(text)
        raw_text = node.text()
        if transliterate and language_code == 'hi':
            raw_text = transliteration(raw_text, language_code)

        y, sr = tts_function(
            raw_text,
            language_code,
            voice=_get_preprocessing_attributes(node, element="voice"),
        )

        if node("prosody"):
            if node("prosody").attr.pitch:
                n_semitones = float(node("prosody").attr.pitch)
                y = transform_pitch(y, sr, n_semitones)

            if node("prosody").attr.rate:
                rate = float(node("prosody").attr.rate)
                y = transform_rate(y, sr, rate)

            if node("prosody").attr.volume:
                gain_db = float(node("prosody").attr.volume)
                y = transform_volume(y, sr, gain_db)

        return y, sr

    return _tts
