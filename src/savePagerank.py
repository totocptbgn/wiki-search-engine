import CLI
import pickle
import sys
import matplotlib.pyplot as plt
import numpy as np

nb_args = len(sys.argv)

if (nb_args != 5 and nb_args != 6):
    print("Waited: python " + sys.argv[0] + " [input file] [output file] [epsilon] [n_steps] [output file to save pagerank convergence]")
    exit()

with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'wb') as output:
    cli = pickle.load(open(sys.argv[1], 'rb'))
    nb_steps = int(sys.argv[4])
    history = cli.savePagerank(float(sys.argv[3]), nb_steps, open(sys.argv[2], 'wb'))
    x = np.arange(1, nb_steps+1)
    fig, ax = plt.subplots()
    ax.plot(x, np.array(history))
    ax.set(xlabel="nombre d'étapes", ylabel="modification", title="Convergence du Pagerank", yscale="log")
    if nb_args == 6:
        plt.savefig(sys.argv[5])
