import re

from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from google.transliteration import transliterate_text
from num_to_words.num_to_words import num_to_word
from dateutil.parser import parse

def eng_to_hin(word, lang_code):
    reg = re.compile(r'[a-zA-Z]')
    if reg.match(word):
        return transliterate_text(word, lang_code)
    return word


def transliteration(text, lang_code):
    with ThreadPoolExecutor(max_workers=8) as executor:
        trans_arr = list(executor.map(eng_to_hin, text.split(" "), repeat(lang_code)))   
    return (" ".join(trans_arr))

month_arr = {'01': 'जनवरी',
             '02': 'फरवरी',
             '03': 'मार्च',
             '04': 'अप्रैल',
             '05': 'मई',
             '06': 'जून',
             '07': 'जुलाई',
             '08': 'अगस्त',
             '09': 'सितम्बर',
             '10': 'अक्टूबर',
             '11': 'नवम्बर',
             '12': 'दिसम्बर'}

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def num2text(text):
    num2word_equ = ""
    for word in text.split(" "):
        if word.isnumeric():
            #handle mobile number
            if word.isnumeric() and int(word) > 10000000:
                out = map(num_to_word, list(word),repeat("hi"))
                num2word_equ += " ".join(out)
            else:
                num2word_equ += f'{num_to_word(word, "hi")} '
        #handle Percentage
        elif '%' in word:
            if word == "%":
                num2word_equ += 'प्रतिशत '
            else:
                print (word)
                num2word_equ += f'{num_to_word(word.strip()[:-1], "hi")} प्रतिशत '
        #handle Time
        elif ':' in word:
            time_arr = word.split(":")
            num2word_equ += f'{num_to_word(time_arr[0], "hi")} बज के {num_to_word(time_arr[1], "hi")} मिनट '
        #handle Date
        elif is_date(word):
            date_arr = word.split("/")
            num2word_equ += f'{num_to_word(date_arr[0], "hi")} {month_arr[date_arr[1]]}, {num_to_word(date_arr[2], "hi")} '
        else:
            if 'pm' not in word and 'am' not in word:
                num2word_equ += f'{word} '
    
    return num2word_equ.strip(" ")
