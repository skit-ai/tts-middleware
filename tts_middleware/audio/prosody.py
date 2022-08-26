import numpy as np
import sox


def transform_pitch(y: np.ndarray, sample_rate: int, n_semitones: float) -> np.ndarray:
    """
    Transform pitch of the given audio chunk and return new chunk. Pitch is
    changed using the number of semitones, like in sox.
    """

    tfm = sox.Transformer()
    tfm.pitch(n_semitones)
    return tfm.build_array(input_array=y, sample_rate_in=sample_rate)


def transform_volume(y: np.ndarray, sample_rate: int, gain_db: float) -> np.ndarray:
    """
    Transform loudness of the given audio chunk and return new chunk. `gain_db`
    must be between -50 and 15.
    """

    tfm = sox.Transformer()
    tfm.loudness(gain_db)
    return tfm.build_array(input_array=y, sample_rate_in=sample_rate)


def transform_rate(y: np.ndarray, sample_rate: int, rate: float) -> np.ndarray:
    """
    Transform speaking rate of the given audio chunk and return new chunk.
    """

    tfm = sox.Transformer()
    tfm.tempo(rate)
    return tfm.build_array(input_array=y, sample_rate_in=sample_rate)
