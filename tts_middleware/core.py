from functools import wraps

from pyquery import PyQuery as pq

from tts_middleware.audio import transform_rate


def tts_middleware(tts_function):
    """
    Decorator function for allowing SSML tags for a TTS.
    """

    @wraps(tts_function)
    def _tts(text: str):
        node = pq(text)
        raw_text = node.text()

        rate = None
        if node("prosody"):
            if node("prosody").attr.rate:
                rate = float(node("prosody").attr.rate)

        output = tts_function(raw_text)

        if rate is not None:
            # TODO: Remove assumption about sample rate
            sample_rate = 8000
            return transform_rate(output, sample_rate, 1.1)
        return output

    return _tts
