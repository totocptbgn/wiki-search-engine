import xml.etree.ElementTree as ET
from tqdm import tqdm
import psutil
import os
import pickle
import sys
import math
from collections import Counter
import re
import multiprocessing
from multiprocessing import Pool, Queue
import numpy as np

def printerr(str=None):
    print("Waited: python " + sys.argv[0] + " [input file] [output file idf] [output file word page relationship] [minimum tf-idf gardé] [nombre mots max gardés]")
    if str != None:
        print(str)

def processPage(text, most_commons, idf, minTF_IDF, word_regex, queue):
    words = [w for w in word_regex.findall(text) if w in most_commons]
    tf = Counter(words)
    for w in tf:
        tf[w] = 1 + math.log10(tf[w])
    Nd = math.sqrt(sum([t**2 for t in tf.values()]))
    for w in tf:
        tf[w] /= Nd
    for w in tf:
        if tf[w] * idfAll[w] >= minTF_IDF:
            if w in result:
                result[w].append((page_count, tf[w]))
            else:
                result[w] = [(page_count, tf[w])]
    queue.put(result)

if __name__ == '__main__':
    affPlaceDiv = 1024 * 1024
    mem_info = psutil.Process(os.getpid()).memory_info()

    if (len(sys.argv) != 6):
        printerr()
        exit()

    minTF_IDF = float(sys.argv[4])

    if minTF_IDF < 0. or minTF_IDF >= 1.:
        printerr("Le minimum de TF-IDF à garder doit être un flottant compris entre 0 inclus et 1 exclu")
        exit()

    nbWords = int(sys.argv[5])

    if nbWords < 15000:
        printerr("Minimum de mots à garder: 15000")
        exit()

    idf_file = open(sys.argv[2], 'wb')
    word_page_file = open(sys.argv[3], 'wb')

    word_regex = re.compile(r'\b\w+\b')
    num_processes = multiprocessing.cpu_count()

    if num_processes > 1:
        num_processes //= 2

    page_count = 0

    print(f"début du calcul des {nbWords} mots les plus fréquents et init idf")

    occur = dict()                          # Dictionnaire : clé = mot, value = nombre d'occurence dans tout les documents
    page_count = 0                          # L'identifiant de la page traitée
    inPages = dict()
    text = []

    for event, elem in tqdm(ET.iterparse(sys.argv[1], events=("start", "end"))):
        if event == 'end' and elem.tag == 'text':
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
                print("Memory usage: {:.2f} MB".format(mem_info.rss / affPlaceDiv))

    most_commons = [k for k, v in sorted(occur.items(), key=lambda item: item[1], reverse=True)][:nbWords]

    del occur

    print(f"fin du calcul des {nbWords} mots les plus fréquents et init idf")
    print("début du calcul des idf")

    idfAll = dict()

    for w in tqdm(most_commons):
        idfAll[w] = math.log10(page_count / inPages[w])

    del inPages

    print("calcul des idf fini")
    print("début du calcul des relations mot-page")

    page_count = 0

    pool = Pool(processes=num_processes)
    queue = Queue()
    results = []

    for event, elem in tqdm(ET.iterparse(sys.argv[1], events=("start", "end"))):
        if event == 'end' and elem.tag == 'text':
            results.append(pool.apply_async(processPage, args=(elem.text, most_commons, idfAll, minTF_IDF, page_count, word_regex, queue)))
            page_count += 1
            if page_count % 10000 == 0:
                print("Memory usage: {:.2f} MB".format(mem_info.rss / affPlaceDiv))

    print("sous-dicos ok")

    word_page_relationships = dict()

    nb_add = 0

    while not queue.empty():
        page_dict = queue.get()
        for w, l in page_dict.items():
            if w in word_page_relationships:
                word_page_relationships[w].extend(l)
            else:
                word_page_relationships[w] = l
        nb_add += 1
        if nb_add % 1000 == 0:
            print("nombre pages traitées:", nb_add)
            print("Memory usage: {:.2f} MB".format(mem_info.rss / affPlaceDiv))

    pool.close()

    #for event, elem in tqdm(ET.iterparse(sys.argv[1], events=("start", "end"))):
    #    if event == 'end' and elem.tag == 'text':
    #        words = [w for w in word_regex.findall(elem.text) if w in most_commons]
    #        tf = Counter(words)
    #        for w in tf:
    #            tf[w] = 1 + math.log10(tf[w])
    #        Nd = math.sqrt(sum([t**2 for t in tf.values()]))
    #        for w in tf:
    #            tf[w] /= Nd
    #        for w in tf:
    #            if tf[w] * idfAll[w] >= minTF_IDF:
    #                if w in word_page_relationships:
    #                    word_page_relationships[w].append((page_count, tf[w]))
    #                else:
    #                    word_page_relationships[w] = [(page_count, tf[w])]
    #        page_count += 1
    #        if page_count % 10000 == 0:
    #            print("Memory usage: {:.2f} MB".format(mem_info.rss / affPlaceDiv))

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
