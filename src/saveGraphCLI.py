import CLI
import pickle
import sys

if (len(sys.argv) != 3):
    print("Waited: python " + sys.argv[0] + " [input file] [output file]")
    exit()

with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'wb') as output:
    graph_wiki = CLI.CLI()
    graph_wiki.saveLinks(input, output)
