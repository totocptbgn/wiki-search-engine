
def requetes(list):
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