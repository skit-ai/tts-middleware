import re
from unittest import result
import numpy as np

from typing import Tuple
from functools import wraps
from pyquery import PyQuery as pq
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor

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

        tasks = [(x, language_code) for x in re.split("\.।", text)]
        results = run_multithreading(tts_function, tasks)
        
        audio = AudioSegment.empty()
        sr = results[0][1]
        for res in results:
            audio += res[0]

        audio = audio.get_array_of_samples()

        # Audio postprocessing
        audio = postprocess_audio(audio, sr, node("prosody"))

        return audio, sr

    return _tts


def run_multithreading(func, tasks, num_workers=4):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(func, tasks), total=len(tasks))
    return results