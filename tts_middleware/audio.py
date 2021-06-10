import numpy as np
import sox


def transform_rate(y: np.ndarray, sample_rate: int, rate: float) -> np.ndarray:
    """
    Transform speaking rate of the give audio chunk and return new chunk.
    """

    tfm = sox.Transformer()
    tfm.tempo(rate)
    return tfm.build_array(input_array=y, sample_rate_in=sample_rate)
