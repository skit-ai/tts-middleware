from functools import wraps
from typing import Tuple

import numpy as np
from pyquery import PyQuery as pq

from num_to_words.num_to_words import num_to_word
from tts_middleware.audio import (transform_pitch, transform_rate,
                                  transform_volume)
from tts_middleware.text import transliteration, num2text

# Data array and sample rate
Audio = Tuple[np.ndarray, int]

def tts_middleware(tts_function):
    """
    Decorator function for allowing SSML tags for a TTS.
    """

    @wraps(tts_function)
    def _tts(text: str, language_code: str, transliterate: bool=False) -> Audio:
        node = pq(text)
        raw_text = node.text()

        # Text preprocessing
        if transliterate and language_code in ["hi"]:
            raw_text = transliteration(raw_text, language_code)

        prep_text = num2text(raw_text)
        # TTS function call
        y, sr = tts_function(
            prep_text,
            language_code,
        )

        # Audio postprocessing
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
