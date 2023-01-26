import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
import numpy as np

## Exercice 2

# On parse le corpus pour compter les occurences de tout les mots contenus dans les balises <text>

occur = dict()                          # Dictionnaire : clé = mot, value = nombre d'occurence dans tout les documents
word_page_relationships = dict()        # On garde aussi pour chaque mot, la liste des pages dans lesquelles il apparait
page_count = 0                          # L'identifiant de la page traitée

for event, elem in ET.iterparse('out.xml', events=("start", "end")):
    if event == 'end' and elem.tag == 'text':
        words = elem.text.split(' ')
        for w in words:
            if w != '':
                if w in occur:
                    occur[w] = occur[w] + 1
                    if page_count not in word_page_relationships[w]:
                        word_page_relationships[w].append(page_count)
                else:
                    occur[w] = 1
                    word_page_relationships[w] = [page_count]
        page_count += 1


# On tri en fonction du nombre d'occurences (descendant)
sorted_occur = [(k, v) for k, v in sorted(occur.items(), key=lambda item: item[1], reverse=True)]

# On affiche quelques valeurs (il faut changer la condition)
if False:
    print(f'Le corpus est composé de {len(sorted_occur)} mots différents.')
    print("Voici les mots les plus communs :")
    for i in sorted_occur[:20]:
        print(i[0], " " * (15 - len(i[0])), i[1])

# On garde les 20000 mots qui apparaissent le plus
sorted_occur_crop = sorted_occur[:20000]

# On la tri par ordre alphabétique
sorted_occur_crop = sorted(sorted_occur_crop, key=lambda x: x[0])

# Fonction qui prends en paramêtre un mot s "mal écrit" et le compare à une liste de mots words pour retrouver le mot le plus proche
def closest_word(s, words):
    return words[np.argmax([SequenceMatcher(None, s, w[0]).ratio() for w in sorted_occur])][0]

## Exercice 3

# On calcule le coefficient IDF de chaque mot
IDF = dict()
for word, page_array in word_page_relationships.items():
    IDF[word] = np.log10(page_count / len(page_array))