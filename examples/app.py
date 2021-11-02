"""
Basic streamlit app for showcasing capabilities of the middleware. Run it
by using the following command:

poetry run streamlit run ./examples/app.py
"""

import os
import tempfile

import librosa
import pyttsx3
import soundfile as sf
import streamlit as st

from tts_middleware.core import Audio, tts_middleware


def initialize_engine():
    return pyttsx3.init()


ENGINE = initialize_engine()


@tts_middleware
def tts(text: str) -> Audio:

    # HACK: Not checked for thread safety
    with tempfile.TemporaryDirectory() as tmp:
        file_path = os.path.join(tmp, "synth.wav")
        ENGINE.save_to_file(text, file_path)
        ENGINE.runAndWait()
        y, sr = librosa.load(file_path)

    return y, sr


st.write("# tts-middleware")
st.write(
    "Go [here](https://github.com/Vernacular-ai/tts-middleware) for details on the project and SSML syntax."
)

text = st.text_area("Enter input here. You can use SSML markers")

if st.button("Submit"):
    y, sr = tts(text)

    # TODO: Don't dirty the directory
    file_path = "generated.wav"
    sf.write(file_path, y, sr)
    st.audio(file_path)
