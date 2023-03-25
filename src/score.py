import math

def requete(list):
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
    return sum([idfs[i] * tfs[i] for i in range(len(page))]) / Nr

def score(alpha, beta, gamma, idfs, tfs, pagerank):
    return alpha * score_frequence(idfs) + beta * pagerank**gamma

def scores(alpha, gamma, idfs, pages, pageranks):
    beta = 1. - alpha
    res = []
    for page, tfs in pages:
        res.append((page, score(alpha, beta, gamma, idfs, tfs, pageranks[page])))
    res.sort(key = lambda x: x[1], reverse = True)
    return [r[0] for r in res]

def bestPages(alpha, gamma, word_page, idfs, pageranks):
    pages = requete(word_page)
    return scores(alpha, gamma, idfs, pages, pageranks)
