# tts-middleware

`tts-middleware` is the pre-processing, for input text, and post-processing, for
output audio, module for our speech synthesis systems.

## Supported SSML tags

Many common tags are assumed implicitly. Read
[this](https://www.w3.org/TR/speech-synthesis/) for overview of SSML
specifications.

+ Sentence level `<prosody>` with `rate` and `volume` attributes, supporting
  percentage descriptors.
+ `<phoneme>` with `ipa` attribute.

## Usage

There are the following components here, all of which can be used in isolation:

1. `Normalizer` for implicit normalization of SSML marked text. No normalization
   level tags are supported at the moment, so this only touches raw text.
1. `Phonemizer` for converting normalized and `<phoneme>` marked text in phone
   symbols. This can be used independently for pre-processing training data too.
2. `Output-Processor` for applying signal level post processing steps (mostly
   `rate` and `volume` attributes) on generated audios.
