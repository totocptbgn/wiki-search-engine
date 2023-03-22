import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
import numpy as np
from tqdm import tqdm
import psutil
import os
import pickle
import sys
import math

if (len(sys.argv) != 4):
    print("Waited: python " + sys.argv[0] + " [input file] [output file word page relationship] [output file idf]")
    exit()

## Exercice 2

word_page_relationships = dict()        # On garde pour chaque mot, la liste des pages dans lesquelles il apparait
page_count = 0                          # L'identifiant de la page traitée

for event, elem in tqdm(ET.iterparse(sys.argv[1], events=("start", "end"))):
    if event == 'end' and elem.tag == 'text':
        TFd = dict()
        words = elem.text.split(' ')
        for w in words:
            if w != '':
                if w in TFd:
                    TFd[w] += 1
                else:
                    TFd[w] = 1
        for w in TFd:
            TFd[w] = 1 + math.log10(TFd[w])
        Nd = math.sqrt(sum([tf**2 for tf in TFd.values()]))
        for w in TFd:
            if w in word_page_relationships:
                word_page_relationships[w].append((page_count, TFd[w] / Nd))
            else:
                word_page_relationships[w] = [(page_count, TFd[w] / Nd)]
        page_count += 1
        if page_count % 1000 == 0:
            print("taille de la relation mot page:", len(word_page_relationships))
            print("nombre de mots différents dans la page en cours:", len(TFd))
            print("Memory usage: {:.2f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)))

print('Done parsing.')
print("Memory usage: {:.2f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)))

print("nombre de mots du corpus:", len(word_page_relationships))

with open(sys.argv[2], 'wb') as wpr_out:
    pickle.dump(word_page_relationships, wpr_out)


# Fonction qui prends en paramêtre un mot s "mal écrit" et le compare à une liste de mots words pour retrouver le mot le plus proche
#def closest_word(s, words):
#    return words[np.argmax([SequenceMatcher(None, s, w[0]).ratio() for w in sorted_occur])][0]

## Exercice 3

# On calcule le coefficient IDF de chaque mot
IDF = dict()
for word, page_array in word_page_relationships.items():
        IDF[word] = math.log10(page_count / len(page_array))
with open(sys.argv[3], 'wb') as idf_out:
    pickle.dump(IDF, idf_out)

print('Done IDF.')
print("Memory usage: {:.2f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)))

# Exercice 8
#TF = dict()
#for page_index in tqdm(range(page_count)):
#    array_tf = []
#    for word, page_array in word_page_relationships.items():
#        if page_index in page_array:
#            array_tf.append((1 + np.log10(page_array.count(page_index))) ** 2)
#    TF[page_index] = np.sqrt(sum(array_tf))
#print('Done TF.')
#print("Memory usage: {:.2f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)))
