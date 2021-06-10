import numpy as np
import pytest
from tts_middleware.audio import transform_rate


@pytest.mark.parametrize("duration, rate", [
    (5, 1.1),
    (5, 1.4),
    (5, 2.1),
    (5, 0.1),
    (5, 0.9)
])
def test_transform_rate(duration, rate):
    sample_rate = 8000
    y = np.random.rand(duration * sample_rate)

    assert np.isclose(len(transform_rate(y, sample_rate, rate)) / sample_rate, duration / rate, atol=0.001)
