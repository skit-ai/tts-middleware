import numpy as np
from tts_middleware.core import tts_middleware

SAMPLE_RATE = 8000

def tts_fn(text: str) -> np.ndarray:
    y = np.random.rand(5 * SAMPLE_RATE)
    return y


def test_ssml_rate():
    rate = 1.1
    raw = "Please keep promises, don't hurt people."
    ssml = f"<prosody rate={rate}>Please keep promises, don't hurt people.</prosody>"

    y = tts_fn(raw)

    _tts_fn = tts_middleware(tts_fn)
    ys = _tts_fn(ssml)

    assert np.isclose(len(ys) / SAMPLE_RATE, len(y) / (SAMPLE_RATE * rate), atol=0.001)
