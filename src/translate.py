import csv
import glob

file_paths = glob.glob("dictionary/*.csv")

dictionary = {}
for file_path in file_paths:
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            tieng_viet = row['tieng_viet']
            tieng_tay = row['tieng_tay']
            dictionary[tieng_viet] = tieng_tay

# dict(sorted(dictionary.items(), key=lambda x: len(x[0].split()), reverse=True))


def translate(text):
    translated = []
    is_upper = False
    texts = text.split()
    index = 0

    while index < len(texts):
        num_word = 3
        while num_word > 0:
            word = ' '.join(texts[index: index+num_word])
            if index == 0:
                if word[0].isupper():
                    word = word[0].lower() + word[1:]
                    is_upper = True

            search = dictionary.get(word)
            if search:
                translated.append(search)
                break
            if num_word == 1:
                translated.append(word)
                break
            num_word -= 1

        index += num_word

    result = ' '.join(translated)
    if is_upper:
        result = result[0].upper() + result[1:]
    return result
