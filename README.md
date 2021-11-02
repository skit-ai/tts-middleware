# tts-middleware

![PyPI](https://img.shields.io/pypi/v/tts-middleware?style=flat-square) ![tag](https://img.shields.io/github/v/tag/Vernacular-ai/tts-middleware.svg?style=flat-square) ![ci](https://img.shields.io/github/workflow/status/Vernacular-ai/tts-middleware/CI.svg?style=flat-square)

Middleware module for our speech synthesis systems.

## Supported SSML tags

Many common tags are assumed implicitly. Read
[this](https://www.w3.org/TR/speech-synthesis/) for an overview of SSML
specification.

+ Sentence level `<prosody>` with `rate`, `pitch`, and `volume` attributes.
+ `<phoneme>` with `ipa` attribute.

## Installation

- Install [sox](http://sox.sourceforge.net/).
- `pip install tts-middleware`

## Usage

For full featured inference, simply wrap your TTS function (text to audio) with
the decorator like this:

```python
from tts_middleware.core import tts_middleware, Audio
import numpy as np

@tts_middleware
def tts(text: str, language_code: str) -> Audio:
    # Do requests and return audio
    ...

# Now calls to `tts` will support SSML with all features enabled.
```

Attributes for SSML tags are described next:

1. `<prosody rate='1.3'>hello world</prosody>`.
2. `<prosody pitch='2'>hello world</prosody>`. Parameter is number of semitones
   as described in pysox
   [here](https://pysox.readthedocs.io/en/latest/api.html#sox.transform.Transformer.pitch).
3. `<prosody volume='10'>hello world</prosody>`. Parameter is gains in db
   similar to pysox
   [here](https://pysox.readthedocs.io/en/latest/api.html#sox.transform.Transformer.loudness).
4. `<voice gender="female" name="excited"> hello world! </voice>`. [`Voice` element](https://www.w3.org/TR/speech-synthesis11/#S3.2.1) supports two attributes:
    `gender` and `name`.

There is a [streamlit](https://streamlit.io/) app which you can use to try the
API by doing the following:

```
# You need to install espeak for this.

poetry install
poetry run streamlit run ./examples/app.py
```

There are three major components here, all of which can be used in isolation.

### `tts_middleware.normalizer`

For implicit normalization of SSML marked text. No normalization level tags are
supported at the moment, so this only touches raw text.

### `tts_middleware.phonemizer`
For converting normalized and `<phoneme>` marked text in phone symbols. This can
be used independently for pre-processing training data too.

### `tts_middleware.audio`
For applying signal level post processing steps (mostly `rate` and `volume`
attributes) on generated audios.
