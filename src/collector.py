from lxml import etree
from tqdm import tqdm
import psutil
import os
import pickle
import math
from collections import Counter
import re
import multiprocessing
from multiprocessing import Pool
import numpy as np
from queue import Queue
import argparse
import sys

def printerr(str=None):
    print("Waited: python " + sys.argv[0] + " [input file] [input file idf] [output file word page relationship] [minimum tf-idf gardé]")
    if str != None:
        print(str)

def processPageDict(text, idf, minTF_IDF, page_count, word_regex):
    words = [w for w in word_regex.findall(text) if w in idf.keys()]
    tf = Counter(words)
    for w in tf:
        tf[w] = 1 + math.log10(tf[w])
    Nd = math.sqrt(sum([t**2 for t in tf.values()]))
    for w in tf:
        tf[w] /= Nd
    result = {}
    for w in tf:
        if tf[w] * idf[w] >= minTF_IDF:
            if w in result:
                result[w].append((page_count, tf[w]))
            else:
                result[w] = [(page_count, tf[w])]
    return result

if __name__ == '__main__':

    if (len(sys.argv) != 5):
        printerr()
        exit()

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('idf_file')
    parser.add_argument('word_page_file')
    parser.add_argument('minTF_IDF')
    args = parser.parse_args()

    affPlaceDiv = 1024 * 1024
    mem_info = psutil.Process(os.getpid())

    minTF_IDF = float(args.minTF_IDF)

    if minTF_IDF < 0. or minTF_IDF >= 1.:
        printerr("Le minimum de TF-IDF à garder doit être un flottant compris entre 0 inclus et 1 exclu")
        exit()

    with open(args.idf_file, 'rb') as idf_file:
        idfAll = pickle.load(idf_file)

    idf_file = open(args.idf_file, 'wb')
    word_page_file = open(args.word_page_file, 'wb')

    word_regex = re.compile(r'\b\w+\b')
    num_processes = multiprocessing.cpu_count() - 2

    print("début du calcul des relations mot-page")

    page_count = 0
    word_page_relationships = dict()

    with Pool(processes=num_processes) as pool:
        results = Queue()
        for event, elem in tqdm(etree.iterparse(args.input_file, events=("end",))):
            if elem.tag == 'text':
                results.put(pool.apply_async(processPageDict, args=(elem.text, idfAll, minTF_IDF, page_count, word_regex)))
                page_count += 1
                if page_count % 10000 == 0:
                    print(str(page_count) + "   Memory usage: {:.2f} MB".format(mem_info.memory_info().rss / affPlaceDiv))

        print("sous-dicos ok")
        print("nombre de résultats:", len(results))

        nb_add = 0

        while not results.empty():
            page_dict = results.get().get()
            for w, l in page_dict.items():
                wordEntry = word_page_relationships.get(w)
                if wordEntry is not None:
                    wordEntry.extend(l)
                else:
                    word_page_relationships[w] = l
            nb_add += 1
            if nb_add % 1000 == 0:
                print("nombre pages traitées:", nb_add)
                print(str(nb_add) + "    Memory usage: {:.2f} MB".format(mem_info.memory_info().rss / affPlaceDiv))

    print("calcul des relations mot-page fini")
    print("début suppression des idf non utilisés")

    idf = dict()

    for w in tqdm(word_page_relationships):
        idf[w] = idfAll[w]

    del idfAll

    print("fin suppression des idf non utilisés")

    print("nombre de mots gardés:", len(idf))
    print("nombre de mots gardés (vérification):", len(word_page_relationships))

    print("début de la sauvegarde des idf")

    pickle.dump(idf, idf_file)

    print("fin de la sauvegarde des idf")
    print("début de la sauvegarde des relations mot-page")

    pickle.dump(word_page_relationships, word_page_file)

    print("fin de la sauvegarde des relations mot-page")

    idf_file.close()
    word_page_file.close()
