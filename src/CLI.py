import pickle
import numpy as np

class CLI:

    def __init__(self):
        self.n = 0      # nombre de lignes de la matrice
        self.C = []
        self.L = [0]
        self.I = []
        self.curL = 0   # utile pour la construction

    # on insere un article par un article
    # (ie tous les liens de cet article d'un coup)
    def add_line(self, liens):
        nbLiens = len(liens)
        if nbLiens > 0:
            self.C += [1./nbLiens] * nbLiens
        self.curL += nbLiens
        self.L.append(self.curL)
        self.I += sorted(liens)
        self.n += 1

    def produit_pagerank_vector(self, epsilon, vector):
        res = [0.] * self.n # initialisation du vecteur resultat
        som = 0. # pour ajouter les 1/n dans le cas des lignes de 0
        for i in range(self.n): # pour toutes les pages
            for j in range(self.L[i], self.L[i+1]): # pour tous les liens de la page i
                res[self.I[j]] += self.C[j] * vector[i] # pour transposee * vecteur
            if self.L[i] == self.L[i+1]: # si une ligne ne contient aucun coefficient non nul
                som += 1 / self.n * vector[i] # on considere que tous les coefs valent 1/nb_pages (comme matrice transposee chaque telle ligne ajoute 1/nb_pages * coef correspondant du vecteur dans chaque chaque coef du resultat)
        for k in range(self.n): # pour tous les coefficients du resultats
            res[k] += som # on ajoute la somme calculee sur les lignes vides (remplacees par [1/nb_pages ... 1/nb_pages])
            res[k] = (1 - epsilon) * res[k] + epsilon / self.n # (1 - e) res + e/n J vector, et (e/n J vector)[k] = e/n car sum(vector[k]) = 1
        return res

    def pagerank_steps_from_vec(self, epsilon, n_steps, vector, debug=False):
        history = []
        vector = np.array(vector)
        for step in range(n_steps):
            nvVec = np.array(self.produit_pagerank_vector(epsilon, vector))
            history.append(abs(vector - nvVec).sum())
            vector = nvVec
            if debug:
                print(vector)
                print(sum(vector))
        return list(vector), history

    def saveLinks(self, input, output):
        for line in input:
            self.add_line([int(w) for w in line.split(',')[:-1]])
        pickle.dump(self, output)

    def pagerank(self, epsilon, n_steps):
        return self.pagerank_steps_from_vec(epsilon, n_steps, [1 / self.n] * self.n)

    def savePagerank(self, epsilon, n_steps, output):
        pagerank, history = self.pagerank(epsilon, n_steps)
        pickle.dump(pagerank, output)
        return history
