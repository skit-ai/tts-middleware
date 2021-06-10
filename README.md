# tts-middleware

`tts-middleware` is the pre-processing, for input text, and post-processing, for
output audio, module for our speech synthesis systems.

TODO: Design in progress.

## Supported SSML tags

Many common tags are assumed implicitly.

+ Sentence level `<prosody>` with `rate` and `volume` attributes, supporting
  percentage descriptors.
+ `<phoneme>` with `ipa` attribute.
