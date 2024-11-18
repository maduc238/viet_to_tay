import csv
import glob
import re
from pympler import asizeof

file_paths = glob.glob("dictionary/*.csv")

dictionary = {}
for file_path in file_paths:
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            tieng_viet = row['tieng_viet']
            tieng_tay = row['tieng_tay']
            dictionary[tieng_viet] = tieng_tay

print(f"Dictionary size {asizeof.asizeof(dictionary)/1000} KB with {len(dictionary)} words")


def translate_sentence(text):
    translated = []
    is_upper = False
    texts = text.split()
    index = 0

    while index < len(texts):
        num_word = 3
        
        while num_word > 0:
            word = ' '.join(texts[index: index+num_word])
            append_char = ''
            if len(word) > 0 and not word[-1].isalpha() and not word[-1].isnumeric():
                append_char = word[-1]
                word = word[:-1]
            if index == 0:
                if word[0].isupper():
                    word = word[0].lower() + word[1:]
                    is_upper = True

            search = dictionary.get(word)
            if search:
                translated.append(search + append_char)
                break
            if num_word == 1:
                translated.append(word + append_char)
                break
            num_word -= 1

        index += num_word

    result = ' '.join(translated)
    if is_upper:
        result = result[0].upper() + result[1:]
    return result


def translate(text):
    result = []
    for sen in re.split(r'(?<=[.?!])\s*', text):
        if len(sen) > 0 and sen[-1] in ['.','?','!']:
            dot = sen[-1]
            sen = sen[:-1]
            result.append(translate_sentence(sen) + dot)
        else:
            result.append(translate_sentence(sen))
    return ' '.join(result)
