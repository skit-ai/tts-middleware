# file to alter the word for appropriate pronunciation

import re

ENG_SPELL_MAP_VAANYA = {"query": "qvery",
    "ivr" : "eye vee are",
    "atm" : "eighty am",
    "pos" : "peeoo ess",
    "e-commerce" : "ee commerce",
    "3d" : "3 dee",
    "kindly" : "kind lee",
    "assist" : "essist",
    "icici" : "eyeicy eyeicy eye",
    "prepaid": "pre paid",
    "s" : "ess",
    "p" : "pee",
    "c" : "see",
    "d" : "dee",
    "sms": "ess em ess",
    "sbi": "ess be eye",
    "sbi's": "ess be eye's"
    }

AYUSHI_WORD_MAPPING = {"pos" : "पी ओ एस",
    "atm": "एटीयम",
    "e-commerce" : "इ कौमर्स",
    "3d" : "थ्री डी",
    "secure" : "सिक्योर",
    "service":"सर्विस",
    "transaction" : "ट्रांज़ेक्शन"
}

def alter_spelling(word):
    key = re.compile(r"\s+").sub(" ", word).strip()
    if key.lower() in ENG_SPELL_MAP_VAANYA.keys():
        return ENG_SPELL_MAP_VAANYA[key.lower()]
    return word

def replace_word(word):
    key = re.compile(r"\s+").sub(" ", word).strip()
    if key.lower() in AYUSHI_WORD_MAPPING.keys():    
        return AYUSHI_WORD_MAPPING[key.lower()]

    return word