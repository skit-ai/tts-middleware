from distutils.command.build import build
from distutils.command.config import LANG_EXT
from functools import wraps
from typing import Tuple
from indictrans import Transliterator
import re

import numpy as np
from pyquery import PyQuery as pq

from tts_middleware.audio import (transform_pitch, transform_rate,
                                  transform_volume)
from tts_middleware.elements import _get_preprocessing_attributes

# Data array and sample rate
Audio = Tuple[np.ndarray, int]


def transliteration(text):
    reg = re.compile(r'[a-zA-Z]')
    trans = Transliterator(source='eng', target='hin', build_lookup=True)
    trans_text = ""
    lang_code = {}
    for word in text.split(" "):
        if word not in '[@_!#$%^&*()<>?/\|}{~:]' and reg.match(word):
            lang_code[word] = "en"
        else: 
            lang_code[word] = "hi"
    for key in lang_code:
        #print (keys)
        if lang_code[key] == "en":
            trans_text += f'{trans.transform(key)} ' 
        else:
            trans_text += f'{key} '
    
    return trans_text

def tts_middleware(tts_function):
    """
    Decorator function for allowing SSML tags for a TTS.
    """

    @wraps(tts_function)
    def _tts(text: str, language_code: str) -> Audio:
        node = pq(text)
        raw_text = node.text()

        trans_text = transliteration(raw_text)

        y, sr = tts_function(
            trans_text,
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
