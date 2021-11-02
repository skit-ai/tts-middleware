import operator as op

import numpy as np
import pytest

from tts_middleware.audio import transform_rate, transform_volume


@pytest.mark.parametrize(
    "duration, rate", [(5, 1.1), (5, 1.4), (5, 2.1), (5, 0.1), (5, 0.9)]
)
def test_transform_rate(duration, rate):
    sample_rate = 8000
    y = np.random.rand(duration * sample_rate)

    assert np.isclose(
        len(transform_rate(y, sample_rate, rate)) / sample_rate,
        duration / rate,
        atol=0.001,
    )


@pytest.mark.parametrize(
    "gain, sign_op", [(10, op.gt), (-10, op.lt), (-50, op.lt), (0, np.isclose)]
)
def test_transform_volume(gain, sign_op):
    sample_rate = 8000
    y = np.random.rand(5 * sample_rate)
    ref = np.mean(y ** 2)

    assert sign_op(np.mean(transform_volume(y, sample_rate, gain) ** 2), ref)
