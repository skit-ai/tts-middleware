# file to alter the word for appropriate pronunciation

import re

ENG_SPELL_MAP_VAANYA = {"query": "qvery",
    "ivr" : "eye we are",
    "atm" : "eighty am",
    "pos" : "peeoo ess",
    "e-commerce" : "ee commerce",
    "3d" : "3 dee",
    "kindly" : "kind lee",
    "assist" : "essist",
    "icici" : "eyeicy eyeicy eye",
    "prepaid": "pre paid"
    }

def alter_spelling(word, tts_agent):

    if tts_agent == "vaanya":
        if word.lower() in ENG_SPELL_MAP_VAANYA.keys():
            key = re.compile(r"\s+").sub(" ", word).strip()
            return ENG_SPELL_MAP_VAANYA[key.lower()]
    return word
