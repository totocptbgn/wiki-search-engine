import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
import numpy as np
from tqdm import tqdm
import psutil
import os
import pickle
import sys
import math

def printerr(str=None):
    print("Waited: python " + sys.argv[0] + " [input file] [output file idf] [output file word page relationship] [minimum tf-idf gardé] [nombre mots max gardés]")
    if str != None:
        print(str)

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

page_count = 0

print(f"début du calcul des {nbWords} mots les plus fréquents et init idf")

occur = dict()                          # Dictionnaire : clé = mot, value = nombre d'occurence dans tout les documents
page_count = 0                          # L'identifiant de la page traitée
idf = dict()

for event, elem in tqdm(ET.iterparse(sys.argv[1], events=("start", "end"))):
    if event == 'end' and elem.tag == 'text':
        page = dict()
        words = elem.text.split()
        for w in words:
            if w in page:
                page[w] += 1
            else:
                page[w] = 1
        for w in page:
            if w in occur:
                occur[w] += page[w]
                idf[w] += 1
            else:
                occur[w] = page[w]
                idf[w] = 1
        page_count += 1
        if page_count % 10000 == 0:
            print("Memory usage: {:.2f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)))

most_commons = [k for k, v in sorted(occur.items(), key=lambda item: item[1], reverse=True)][:nbWords]

del occur

print(f"fin du calcul des {nbWords} mots les plus fréquents et init idf")
print("début du calcul des idf")

for w in tqdm(list(idf)):
    if w not in most_commons:
        del idf[w]
    else:
        idf[w] = math.log10(page_count / idf[w])

print("calcul des idf fini")
print("début du calcul des relations mot-page")

page_count = 0

word_page_relationships = dict()

for event, elem in tqdm(ET.iterparse(sys.argv[1], events=("start", "end"))):
    if event == 'end' and elem.tag == 'text':
        tf = dict()
        words = elem.text.split()
        for w in words:
            if w in tf:
                tf[w] += 1
            elif w in most_commons:
                tf[w] = 1
        for w in tf:
            tf[w] = 1 + math.log10(tf[w])
        Nd = math.sqrt(sum([t**2 for t in tf.values()]))
        for w in tf:
            tf[w] /= Nd
        for w in tf:
            if tf[w] * idf[w] >= minTF_IDF:
                if w in word_page_relationships:
                    word_page_relationships[w].append((page_count, tf[w]))
                else:
                    word_page_relationships[w] = [(page_count, tf[w])]
        page_count += 1
        if page_count % 10000 == 0:
            print("Memory usage: {:.2f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)))

print("calcul des relations mot-page fini")
print("début suppression des idf non utilisés")

for w in tqdm(list(idf)):
    if w not in word_page_relationships:
        del idf[w]

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
