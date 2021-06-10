# tts-middleware

`tts-middleware` is the pre-processing, for input text, and post-processing, for
output audio, module for our speech synthesis systems.

TODO: Design in progress.

## Supported SSML tags

Many common tags are assumed implicitly. Read
[this](https://www.w3.org/TR/speech-synthesis/) for overview of SSML
specifications.

+ Sentence level `<prosody>` with `rate` and `volume` attributes, supporting
  percentage descriptors.
+ `<phoneme>` with `ipa` attribute.
