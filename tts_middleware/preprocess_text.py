import re

from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from google.transliteration import transliterate_text
from tts_middleware.num_to_words.num_to_word import num_to_word
from dateutil.parser import parse

MONTH_MAPPING = {1: 'जनवरी',
             2: 'फरवरी',
             3: 'मार्च',
             4: 'अप्रैल',
             5: 'मई',
             6: 'जून',
             7: 'जुलाई',
             8: 'अगस्त',
             9: 'सितम्बर',
             0: 'अक्टूबर',
             11: 'नवम्बर',
             12: 'दिसम्बर'}

CHAR_ENG_TO_HIN_MAP = {'a': 'ए', 'b': 'बी', 'c': 'सी', 'd': 'डी', 'e': 'ई', 'f': 'एफ', 
'g': 'जी', 'h': 'एच', 'i': 'आयी', 'j': 'जे', 'k': 'के', 'l': 'एल', 'm': 'एम', 'n': 'एन', 
'o': 'ओ', 'p': 'पी', 'q': 'क्यू', 'r': 'आर', 's': 'एस', 't': 'टी', 'u': 'यू', 'v': 'वी', 
'w': 'डब्ल्यू', 'x': 'एक्स', 'y': 'वायी', 'z': 'जेड'}

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

def process(word, language_code, transliterate):
    final_word = word
    if transliterate:
        reg_caps = re.compile(r'[A-Z]*\b')
        reg_roman_char = re.compile(r'[a-zA-Z]+')
        if re.match(reg_caps, word) is not None and re.match(reg_caps, word).group():
            # print(word)
            transliterated_char = [CHAR_ENG_TO_HIN_MAP[item] for item in list(word.lower())]
            final_word = " ".join(transliterated_char).strip()
            # return final_word
        elif reg_roman_char.match(word) is not None and reg_roman_char.match(word).group():
            final_word = transliterate_text(word, language_code)
            # return final_word

    # Numeric processing only   
    num2word_equ = ""
    if word.isnumeric():     
        #handle mobile number
        if int(word) > 10000000:
            mapped_num = map(num_to_word, list(word),repeat("hi"))
            num2word_equ += " ".join(mapped_num)
        else:
            num2word_equ += f'{num_to_word(word, "hi")} '
        final_word = num2word_equ
    elif '%' in word:
        print(word)
        if word == "%":
            num2word_equ += 'प्रतिशत '
        else:
            print(word)
            if word.strip()[:-1].isnumeric():
                num2word_equ += f'{num_to_word(word.strip()[:-1], "hi")} प्रतिशत '
            else:
                num2word_equ += f'{word.strip()[:-1]} प्रतिशत '
        
        final_word = num2word_equ
    return final_word


## commented because part of it could be used later.

# def is_date(string, fuzzy=False):
#     try: 
#         parse(string, fuzzy=fuzzy)
#         return True

#     except ValueError:
#         return False
# def num2text(text):
#     num2word_equ = ""
#     for word in text.split(" "):
#         if word.isnumeric():
#             #handle mobile number
#             if word.isnumeric() and int(word) > 10000000:
#                 out = map(num_to_word, list(word),repeat("hi"))
#                 num2word_equ += " ".join(out)
#             else:
#                 num2word_equ += f'{num_to_word(word, "hi")} '
#         #handle Percentage
#         elif '%' in word:
#             if word == "%":
#                 num2word_equ += 'प्रतिशत '
#             else:
#                 print (word)
#                 num2word_equ += f'{num_to_word(word.strip()[:-1], "hi")} प्रतिशत '
#         #handle Time
#         elif ':' in word:
#             time_arr = word.split(":")
#             num2word_equ += f'{num_to_word(time_arr[0], "hi")} बज के {num_to_word(time_arr[1], "hi")} मिनट '
#         #handle Date
#         elif is_date(word):
#             date_arr = word.split("/")
#             num2word_equ += f'{num_to_word(date_arr[0], "hi")} {MONTH_MAPPING[int(date_arr[1])]}, {num_to_word(date_arr[2], "hi")} '
#         else:
#             if 'pm' not in word and 'am' not in word:
#                 num2word_equ += f'{word} '
    
#     return num2word_equ.strip(" ")
