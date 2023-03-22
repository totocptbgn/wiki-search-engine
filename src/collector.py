import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
import numpy as np
from tqdm import tqdm
import psutil
import os
import pickle
import sys

## Exercice 2

# On parse le corpus pour compter les occurences de tout les mots contenus dans les balises <text>
print("Memory usage: {:.2f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)))

occur = dict()                          # Dictionnaire : clé = mot, value = nombre d'occurence dans tout les documents
word_page_relationships = dict()        # On garde aussi pour chaque mot, la liste des pages dans lesquelles il apparait
page_count = 0                          # L'identifiant de la page traitée

for event, elem in tqdm(ET.iterparse(sys.argv[1], events=("start", "end"))):
    if event == 'end' and elem.tag == 'text':
        words = elem.text.split(' ')
        for w in words:
            if w != '':
                if w in occur:
                    occur[w] = occur[w] + 1
                    word_page_relationships[w].append(page_count)
                else:
                    occur[w] = 1
                    word_page_relationships[w] = [page_count]
        page_count += 1
print('Done parsing.')
print("Memory usage: {:.2f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)))

# On tri en fonction du nombre d'occurences (descendant)
sorted_occur = [(k, v) for k, v in sorted(occur.items(), key=lambda item: item[1], reverse=True)]
print('Done sorting.')
print("Memory usage: {:.2f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)))

# On garde les 20000 mots qui apparaissent le plus
sorted_occur = sorted_occur[:20000]

# On affiche quelques valeurs (il faut changer la condition)
if False:
    print(f'Le corpus est composé de {len(sorted_occur)} mots différents.')
    print("Voici les mots les plus communs :")
    for i in sorted_occur[:50]:
        print(i[0], " " * (15 - len(i[0])), i[1])

# On la tri par ordre alphabétique
# sorted_occur = sorted(sorted_occur, key=lambda x: x[0])
kept_word = [i[0] for i in sorted_occur]

# Fonction qui prends en paramêtre un mot s "mal écrit" et le compare à une liste de mots words pour retrouver le mot le plus proche
def closest_word(s, words):
    return words[np.argmax([SequenceMatcher(None, s, w[0]).ratio() for w in sorted_occur])][0]

## Exercice 3

# On calcule le coefficient IDF de chaque mot
IDF = dict()
for word, page_array in word_page_relationships.items():
        IDF[word] = np.log10(page_count / len(set(page_array)))
with open('IDF.dict', 'wb') as idf_out:
    pickle.dump(IDF, idf_out)
print('Done IDF.')
print("Memory usage: {:.2f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)))

# Exercice 8
TF = dict()
for page_index in tqdm(range(page_count)):
    array_tf = []
    for word, page_array in word_page_relationships.items():
        if page_index in page_array:
            array_tf.append((1 + np.log10(page_array.count(page_index))) ** 2)
    TF[page_index] = np.sqrt(sum(array_tf))
print('Done TF.')
print("Memory usage: {:.2f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)))
