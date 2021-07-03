import numpy as np
from tts_middleware.core import Audio, tts_middleware


def tts_fn(text: str) -> Audio:
    sr = 8000
    y = np.random.rand(5 * sr)
    return y, sr


def test_ssml_rate():
    rate = 1.1
    raw = "Please keep promises, don't hurt people."
    ssml = f"<prosody rate={rate}>Please keep promises, don't hurt people.</prosody>"

    y, sr = tts_fn(raw)

    _tts_fn = tts_middleware(tts_fn)
    ys, sr = _tts_fn(ssml)

    assert np.isclose(len(ys) / sr, len(y) / (sr * rate), atol=0.001)
