import re
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

        # Speech synthesis
        if language_code in ["hi"]:
            audio, sr = parallel_stitch(
                text,
                language_code,
                tts_function,
            )
        else:
            audio, sr = tts_function(
                text,
                language_code,
            )

        # Audio postprocessing
        audio = postprocess_audio(audio, sr, node("prosody"))

        return audio, sr

    return _tts


def parallel_stitch(text, language_code, tts_function):
    def tts_function_wrapper(args):
        return tts_function(*args)

    tasks = [(x.strip() + " ।", language_code) for x in re.split("।", text)]
    results = run_multithreading(tts_function_wrapper, tasks)
    
    audio = AudioSegment.empty()
    sr = results[0][1]
    for res in results:
        audio += AudioSegment(res[0].tobytes(), frame_rate=sr, sample_width=2, channels=1)

    audio = np.array(audio.get_array_of_samples())
    return audio, sr


def run_multithreading(func, tasks, num_workers=4):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(func, tasks))
    return results