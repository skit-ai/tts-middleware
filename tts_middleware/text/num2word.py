import re

from itertools import repeat

from google.transliteration import transliterate_text
from tts_middleware.text.num_to_words.num_to_word import num_to_word
from tts_middleware.text.alter_word import replace_word


MONTH_MAPPING = {1: 'जनवरी', 2: 'फरवरी', 3: 'मार्च', 4: 'अप्रैल', 5: 'मई',
             6: 'जून', 7: 'जुलाई', 8: 'अगस्त', 9: 'सितम्बर', 10: 'अक्टूबर',
             11: 'नवम्बर', 12: 'दिसम्बर'}


CHAR_ENG_TO_HIN_MAP = {'a': 'ए', 'b': 'बी', 'c': 'सी', 'd': 'डी', 'e': 'ई', 'f': 'एफ', 
'g': 'जी', 'h': 'एच', 'i': 'आयी', 'j': 'जे', 'k': 'के', 'l': 'एल', 'm': 'एम', 'n': 'एन', 
'o': 'ओ', 'p': 'पी', 'q': 'क्यू', 'r': 'आर', 's': 'एस', 't': 'टी', 'u': 'यू', 'v': 'वी', 
'w': 'डब्ल्यू', 'x': 'एक्स', 'y': 'वायी', 'z': 'जेड'}


def parse_date(word, language_code):
    yy, mm, dd = word.split('-')

    # remove special characters .
    yy = re.sub('[^0-9]+', '', yy)
    mm = re.sub('[^0-9]+', '', mm)
    dd = re.sub('[^0-9]+', '', dd)

    hi_dd = num_to_word(dd.strip(), language_code)

    # splitting year as the pronunciation changes
    yy_p1 = yy[:2]
    yy_p2 = yy[2:]

    if int(yy_p1) < 20:
        hi_yy = num_to_word(yy_p1, language_code) + " सौ " + num_to_word(yy_p2, language_code)
    else:
        hi_yy = num_to_word(yy_p1 + "00", language_code) + " " + num_to_word(yy_p2, language_code)
    
    hi_mm = MONTH_MAPPING[int(mm.strip())]

    return " ".join([hi_dd, hi_mm, ", " + hi_yy]) 


def process(word, language_code, transliterate):
    final_word = word
    reg_date = re.compile(r'\d{4}-\d{2}-\d{2}')
    reg_caps = re.compile(r'[A-Z]*\b')
    reg_roman_char = re.compile(r'[a-zA-Z]+')
    
    if re.match(reg_caps, word) is not None and re.match(reg_caps, word).group():
        
        if transliterate:
            transliterated_char = [CHAR_ENG_TO_HIN_MAP[item] for item in list(word.lower())]
            final_word = " ".join(transliterated_char).strip()
        else:
            final_word = replace_word(word)

    elif reg_roman_char.match(word) is not None and reg_roman_char.match(word).group():
        if transliterate:
            final_word = transliterate_text(word, language_code)
        else:
            final_word = replace_word(word)

    # date parser
    if re.match(reg_date, word) is not None and re.match(reg_date,word).group():
        final_word = parse_date(word, language_code)

    # Numeric processing only   
    num2word_equ = ""
    if word.isnumeric():     
        #handle mobile number
        if int(word) > 10000000:
            mapped_num = map(num_to_word, list(word),repeat(language_code))
            num2word_equ += " ".join(mapped_num)
        else:
            num2word_equ += f'{num_to_word(word, language_code)} '
        final_word = num2word_equ
    elif '%' in word:

        if word == "%":
            num2word_equ += 'प्रतिशत '
        else:
            if word.strip()[:-1].isnumeric():
                num2word_equ += f'{num_to_word(word.strip()[:-1], language_code)} प्रतिशत '
            else:
                num2word_equ += f'{word.strip()[:-1]} प्रतिशत '
        
        final_word = num2word_equ
    return final_word

# print(preprocess_text("समझ गई। आपकी check in date 2022-09-10. कर दी गई है। क्या आप कोई और detail और बदलना चाहते हैं ?", transliterate=True, language_code="hi"))
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
