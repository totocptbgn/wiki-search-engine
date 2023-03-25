import argparse
import sys
from lxml import etree
from tqdm import tqdm
import psutil
import os
import re
from collections import Counter
import math

def printerr(str=None):
    print("Waited: python " + sys.argv[0] + " [input file] [output file idf] [nombre mots max gardés]")
    if str != None:
        print(str)


if __name__ == '__main__':

    if (len(sys.argv) != 4):
        printerr()
        exit()

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('idf_file')
    parser.add_argument('nb_words')
    args = parser.parse_args()

    affPlaceDiv = 1024 * 1024
    mem_info = psutil.Process(os.getpid())

    nbWords = int(args.nb_words)

    if nbWords < 15000:
        printerr("Minimum de mots à garder: 15000")
        exit()

    idf_file = open(args.idf_file, 'wb')

    word_regex = re.compile(r'\b\w+\b')

    print(f"début du calcul des {nbWords} mots les plus fréquents et init idf")

    occur = dict()                          # Dictionnaire : clé = mot, value = nombre d'occurence dans tout les documents
    page_count = 0                          # L'identifiant de la page traitée
    inPages = dict()
    text = []

    for event, elem in tqdm(etree.iterparse(args.input_file, events=("end",))):
        if elem.tag == 'text':
            words = word_regex.findall(elem.text)
            page = Counter(words)
            for w in page:
                if w in occur:
                    occur[w] += page[w]
                    inPages[w] += 1
                else:
                    occur[w] = page[w]
                    inPages[w] = 1
            page_count += 1
            if page_count % 10000 == 0:
                print(str(page_count) + "  Memory usage: {:.2f} MB".format(mem_info.memory_info().rss / affPlaceDiv))

    most_commons = [k for k, v in sorted(occur.items(), key=lambda item: item[1], reverse=True)][:nbWords]

    del occur

    print(f"fin du calcul des {nbWords} mots les plus fréquents et init idf")
    print("début du calcul des idf")

    idfAll = dict()

    for w in tqdm(most_commons):
        idfAll[w] = math.log10(page_count / inPages[w])

    del inPages

    print("calcul des idf fini")
    print("début de la sauvegarde des idf")

    pickle.dump(idfAll, idf_file)

    idf_file.close()
