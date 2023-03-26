import math
import pickle
import unicodedata
from nltk.stem.snowball import FrenchStemmer
import re

stemmer = FrenchStemmer()

with open("../data/idf.dict", 'rb') as idf_file:
    idf = pickle.load(idf_file)

with open("../data/pagerank.vector", 'rb') as pagerank_file:
    pageranks = pickle.load(pagerank_file)

with open("../data/word_page.dict", 'rb') as word_page_file:
    word_page_relationships = pickle.load(word_page_file)

spec_regex = re.compile(r'[^a-z ]+')

with open('stopwords.txt', 'r') as f:
    sw_list = set(f.read().splitlines())

def common_pages(list):
    k=len(list)
    pointeur = [0]*k
    L = []
    count = 0
    while not anyEnd(list, pointeur):
        p = max([list[i][pointeur[i]][0] for i in range(k)])
        count = 0
        for i in range(k):
            numPagesI = list[i][pointeur[i]][0]
            while numPagesI < p:
                pointeur[i]+=1
                numPagesI = list[i][pointeur[i]][0]
            if  numPagesI == p:
                count+=1
        if count == k:
            L.append((p,[list[i][pointeur[i]][1] for i in range(k)]))
            for i in range(k):
                pointeur[i]+=1
    return L

def anyEnd(list, pointeur):
    return [pointeur[i] == len(list[i]) for i in range(len(list))].count(True) > 0

def score_frequence(idfs, tfs):
    Nr = math.sqrt(sum([idf**2 for idf in idfs]))
    return sum([idfs[i] * tfs[i] for i in range(len(idfs))]) / Nr

def score(alpha, beta, gamma, idfs, tfs, pagerank):
    return alpha * score_frequence(idfs, tfs) + beta * pagerank**gamma

def scores(alpha, gamma, idfs, pages, pageranks):
    beta = 1. - alpha
    res = []
    for page, tfs in pages:
        res.append((page, score(alpha, beta, gamma, idfs, tfs, pageranks[page])))
    res.sort(key = lambda x: x[1], reverse = True)
    return [r[0] for r in res]

def bestPages(alpha, gamma, requete):
    words = requete2words(requete)
    word_page = [word_page_relationships[w] for w in words]
    idfs = [idf[w] for w in words]
    pages = common_pages(word_page)
    return scores(alpha, gamma, idfs, pages, pageranks)

def requete2words(requete):
    requete = requete.lower()
    requete = unicodedata.normalize('NFKD', requete)
    requete = ''.join(c for c in requete if not unicodedata.combining(c))
    requete = spec_regex.sub(r'', requete)
    return [stemmer.stem(w) for w in requete.split() if w not in sw_list]
