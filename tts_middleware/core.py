from functools import wraps
from typing import Tuple

import numpy as np
from pyquery import PyQuery as pq

from tts_middleware.audio import (transform_pitch, transform_rate,
                                  transform_volume)
from tts_middleware.elements import _get_preprocessing_attributes

# Data array and sample rate
Audio = Tuple[np.ndarray, int]

def gtts_to_vtts(pitch, rate):
    if (pitch and "%" in pitch): 
        pitch = 1+float(pitch.strip("%"))/100
    if (rate and "%" in rate):
        rate = float(rate.strip("%"))/100
    return pitch, rate

def tts_middleware(tts_function):
    """
    Decorator function for allowing SSML tags for a TTS.
    """

    @wraps(tts_function)
    def _tts(text: str, language_code: str) -> Audio:
        node = pq(text)
        raw_text = node.text()
        y, sr = tts_function(
            raw_text,
            language_code,
            voice=_get_preprocessing_attributes(node, element="voice"),
        )

        if node("prosody"):
            if node("prosody").attr.pitch:
                n_semitones, _ = gtts_to_vtts(node("prosody").attr.pitch, None)
                y = transform_pitch(y, sr, n_semitones)

            if node("prosody").attr.rate:
                _, rate = gtts_to_vtts(None, node("prosody").attr.rate)
                y = transform_rate(y, sr, rate)

            if node("prosody").attr.volume:
                gain_db = float(node("prosody").attr.volume)
                y = transform_volume(y, sr, gain_db)

        return y, sr

    return _tts
