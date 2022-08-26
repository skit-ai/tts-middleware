from tts_middleware.audio.prosody import (
    transform_pitch,
    transform_rate,
    transform_volume
)


def postprocess_audio(y, sr, prosody):
    if prosody:
        if prosody.attr.pitch:
            n_semitones = float(prosody.attr.pitch)
            y = transform_pitch(y, sr, n_semitones)

        if prosody.attr.rate:
            rate = float(prosody.attr.rate)
            y = transform_rate(y, sr, rate)

        if prosody.attr.volume:
            gain_db = float(prosody.attr.volume)
            y = transform_volume(y, sr, gain_db)

    return y