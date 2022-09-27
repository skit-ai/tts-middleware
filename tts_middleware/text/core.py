import re

from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from tts_middleware.text.num2word import process
from tts_middleware.text.alter_word import alter_spelling


def preprocess_text(text, **kwargs):
    transliterate = kwargs["transliterate"]
    language_code = kwargs["language_code"]

    final_text = text
    sub_sent = re.sub(r',', " , ", text)
    
    sub_sent = re.sub(r'\?', " ? ", sub_sent)
    sub_sent = re.sub(r'।', " । ", sub_sent)
    sub_sent = re.sub(r'!', " ! ", sub_sent)
    
    if language_code == "hi":      
        sub_sent = re.sub(r'\|', " । ", sub_sent)

        with ThreadPoolExecutor(max_workers=8) as executor:
            inter_text = list(executor.map(process, sub_sent.split(" "), repeat(language_code), repeat(transliterate)))   
        final_text = " ".join(inter_text).strip()

        sent_ending = r'[\?।|!]'
        if not re.match(sent_ending, final_text[-1]):
            final_text += ' ।'

    elif language_code == "en":
        sub_sent = re.sub(r'\|', " | ", sub_sent)
        sub_sent = re.sub(r'\.', " . ", sub_sent)

        with ThreadPoolExecutor(max_workers=8) as executor:
            inter_text = list(executor.map(alter_spelling, sub_sent.split(" ")))   
        final_text = " ".join(inter_text).strip()

    else:
        final_text = sub_sent
    
    final_text = re.compile(r"\s+").sub(" ", final_text).strip()

    return final_text

# print(preprocess_text("Dear customer, SBI's to activate the 3D secure services on your card, please send the message 3 D S, P C followed by the last 4 digits of your prepaid card, to 9 2 1 5 6 7 6 7 6 6 from your registered mobile number. Do you want me to repeat?.", transliterate=False, language_code="en"))
# print(preprocess_text("समझ गई। आपकी check in date 2022-09-10. कर दी गई है। क्या आप कोई और ATM detail और बदलना चाहते हैं ?", transliterate=True, language_code="hi"))