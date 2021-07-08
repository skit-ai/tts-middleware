from functools import wraps
from typing import Tuple

import numpy as np
from pyquery import PyQuery as pq

from tts_middleware.audio import (transform_pitch, transform_rate,
                                  transform_volume)

# Data array and sample rate
Audio = Tuple[np.ndarray, int]


def tts_middleware(tts_function):
    """
    Decorator function for allowing SSML tags for a TTS.
    """

    @wraps(tts_function)
    def _tts(text: str) -> Audio:
        node = pq(text)
        raw_text = node.text()

        y, sr = tts_function(raw_text)

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
