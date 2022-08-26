import numpy as np

from typing import Tuple
from functools import wraps
from pyquery import PyQuery as pq

from tts_middleware.text import preprocess_text
from tts_middleware.audio import postprocess_audio


# Data array and sample rate
Audio = Tuple[np.ndarray, int]


def tts_middleware(tts_function):
    """
    Decorator function for allowing SSML tags for a TTS.
    """

    @wraps(tts_function)
    def _tts(text: str, language_code: str, transliterate: bool=False) -> Audio:
        node = pq(text)
        text = node.text()

        # Text preprocessing
        text = preprocess_text(text, transliterate=transliterate, language_code=language_code)

        audio, sr = tts_function(
            text,
            language_code,
        )

        # Audio postprocessing
        audio = postprocess_audio(audio, sr, node("prosody"))

        return audio, sr

    return _tts
