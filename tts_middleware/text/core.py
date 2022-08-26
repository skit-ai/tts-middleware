import re

from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from tts_middleware.text.num2word import process


def preprocess_text(text, **kwargs):
    transliterate = kwargs["transliterate"]
    language_code = kwargs["language_code"]
    final_text = text
    if language_code == "hi":
        sub_sent = re.sub(r',', " , ", text)
        sub_sent = re.sub(r'\?', " ? ", sub_sent)
        sub_sent = re.sub(r'।', " । ", sub_sent)
        sub_sent = re.sub(r'!', " ! ", sub_sent)
        sub_sent = re.sub(r'\|', " । ", sub_sent)

        with ThreadPoolExecutor(max_workers=8) as executor:
            inter_text = list(executor.map(process, sub_sent.split(" "), repeat(language_code), repeat(transliterate)))   
        final_text = " ".join(inter_text).strip()

        sent_ending = r'[\?।|!]'
        if not re.match(sent_ending, final_text[-1]):
            final_text += ' ।'
    final_text = re.compile(r"\s+").sub(" ", final_text).strip()

    return final_text