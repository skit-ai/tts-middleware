from functools import wraps
from typing import Tuple

import numpy as np
from pyquery import PyQuery as pq

from tts_middleware.audio import transform_rate

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

        rate = None
        if node("prosody"):
            if node("prosody").attr.rate:
                rate = float(node("prosody").attr.rate)

        y, sr = tts_function(raw_text)

        if rate is not None:
            return transform_rate(y, sr, 1.1), sr
        return y, sr

    return _tts
