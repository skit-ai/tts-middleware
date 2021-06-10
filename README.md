# tts-middleware

![tag](https://img.shields.io/github/v/tag/Vernacular-ai/tts-middleware.svg?style=flat-square) ![ci](https://img.shields.io/github/workflow/status/Vernacular-ai/tts-middleware/CI.svg?style=flat-square)

`tts-middleware` is the pre-processing, for input text, and post-processing, for
output audio, module for our speech synthesis systems.

## Supported SSML tags

Many common tags are assumed implicitly. Read
[this](https://www.w3.org/TR/speech-synthesis/) for an overview of SSML
specification.

+ Sentence level `<prosody>` with `rate` and `volume` attribute, supporting
  percentage descriptors.
+ `<phoneme>` with `ipa` attribute.

## Installation

- Install [sox](http://sox.sourceforge.net/).
- TODO: Package setup.

## Usage

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
