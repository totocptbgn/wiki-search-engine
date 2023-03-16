import CLI
import pickle
import sys

if (len(sys.argv) != 5):
    print("Waited: python " + sys.argv[0] + " [input file] [output file] [epsilon] [n_steps]")
    exit()

with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'wb') as output:
    cli = pickle.load(open(sys.argv[1], 'rb'))
    cli.savePagerank(float(sys.argv[3]), int(sys.argv[4]), open(sys.argv[2], 'wb'))
