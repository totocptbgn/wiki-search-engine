


class CLI:

    def __init__(self):
        self.C = []
        self.L = [0]
        self.I = []
        self.curL = 0 # utile pour la construction

    # on insere un article par un article
    # (ie tous les liens de cet article d'un coup)
    def add_ligne(self, liens):
        nbLiens = len(liens)
        self.C.expend([1./nbLiens] * nbLiens)
        self.curL += nbLiens
        self.L.append(self.curL)
        self.I.expend(sorted(liens))

    def produit_pagerank_vector(epsilon, vector):
        nb_pages = len(self.L) - 1
        res = [0.] * nb_pages # initialisation du vecteur resultat
        som = 0. # pour ajouter les 1/n dans le cas des lignes de 0
        for i in range(nb_pages-1): # pour toutes les pages
            for j in range(self.L[i], self.L[i+1]): # pour tous les liens de la page i
                res[self.I[j]] += self.C[j] * vector[i] # pour transposee * vecteur
            if L[i] == L[i+1]: # si une ligne ne contient aucun coefficient non nul
                som += 1 / nb_pages * vector[i] # on considere que tous les coefs valent 1/nb_pages (comme matrice transposee chaque telle ligne ajoute 1/nb_pages * coef correspondant du vecteur dans chaque chaque coef du resultat)
        for k in range(nb_pages): # pour tous les coefficients du resultats
            res[k] += som # on ajoute la somme calculee sur les lignes vides (remplacees par [1/nb_pages ... 1/nb_pages])
            res[k] = (1 - epsilon) * res[k] + epsilon / nb_pages # (1 - e) res + e/n J vector, et (e/n J vector)[k] = e/n car sum(vector[k]) = 1
        return res
