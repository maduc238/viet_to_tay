import csv
import glob
import re
from pympler import asizeof

file_paths = glob.glob("dictionary/*.csv")
saved_file = "dictionary.csv"

dictionary = {}
bypass = []
remove = []
for filename in file_paths:
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        if 'bypass' in filename:
            for row in csv_reader:
                bypass.append(row['tieng_viet'])
        elif 'remove' in filename:
            for row in csv_reader:
                remove.append(row['tieng_viet'])
        else:
            for row in csv_reader:
                tieng_viet = row['tieng_viet']
                tieng_tay = row['tieng_tay']
                dictionary[tieng_viet] = tieng_tay

print(f"Dictionary size {asizeof.asizeof(dictionary)/1000} KB with {len(dictionary)} words")


def translate_sentence(text):
    translated = []
    word_by_word = {}
    is_upper = False
    first_special_char = ''
    texts = text.split()
    index = 0

    while index < len(texts):
        num_word = 3
        
        while num_word > 0:
            word = ' '.join(texts[index: index+num_word])
            append_char = ''
            special_char = ''

            if len(word) > 0 and not word[-1].isalpha() and not word[-1].isnumeric():
                append_char = word[-1]
                word = word[:-1]
            if index == 0:
                if len(word) > 0:
                    if word[0] in ["\"", "'", "("]:
                        first_special_char = word[0]
                        word = word[1:]
                    if word[0].isupper():
                        word = word[0].lower() + word[1:]
                        is_upper = True

            if len(word) > 0 and word[0] in ["\"", "'", "("]:
                special_char = word[0]
                word = word[1:]
            if word in bypass:
                translated.append(word + append_char)
                break
            if word in remove:
                break
            
            search = dictionary.get(word)
            if search:
                if word not in word_by_word:
                    word_by_word[word] = search
                translated.append(special_char + search + append_char)
                break
            if num_word == 1:
                translated.append(special_char + word + append_char)
                break
            num_word -= 1

        index += num_word

    result = ' '.join(translated)
    if is_upper:
        result = first_special_char + result[0].upper() + result[1:]
    return result, word_by_word


def translate(text):
    result = []
    for sen in re.split(r'(?<=[.?!])\s*', text):
        if len(sen) > 0 and sen[-1] in ['.','?','!']:
            dot = sen[-1]
            sen = sen[:-1]
            translated, word_by_word = translate_sentence(sen)
            result.append(translated + dot)
        else:
            translated, word_by_word = translate_sentence(sen)
            result.append(translated)
    return ' '.join(result)


def translate_with_subtitle(text):
    result = []
    global_word = dict()
    for sen in re.split(r'(?<=[.?!])\s*', text):
        if len(sen) > 0 and sen[-1] in ['.','?','!']:
            dot = sen[-1]
            sen = sen[:-1]
            translated, word_by_word = translate_sentence(sen)
            result.append(translated + dot)
        else:
            translated, word_by_word = translate_sentence(sen)
            result.append(translated)
        global_word.update(word_by_word)
    
    title_word = ''
    for word in global_word:
        title_word += f'{word}->{global_word[word]}; '
    return ' '.join(result), title_word

def convert_to_csv():
    data = sorted(dictionary.items(), key=lambda x: x[0])
    with open(saved_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["source", "target"])
        writer.writerows(data)
