import csv
import glob
import pickle
import bz2

file_paths = glob.glob("dictionary/*.csv")

def save_dict():
    dictionary = {}
    for filename in file_paths:
        with open(filename, mode='r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            if 'bypass' in filename:
                pass
            elif 'remove' in filename:
                pass
            else:
                for row in csv_reader:
                    tieng_viet = row['tieng_viet']
                    tieng_tay = row['tieng_tay']
                    dictionary[tieng_viet] = tieng_tay

    with bz2.BZ2File("dictionary.pkl.bz2", "wb") as file:
        pickle.dump(dictionary, file)