import pickle
import argparse
import sys
from lxml import etree
from tqdm import tqdm

if __name__ == '__main__':

    if (len(sys.argv) != 3):
        print(f"Waited: python {sys.argv[0]} [input file] [output file]")
        exit()

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    args = parser.parse_args()

    titles = []

    for event, elem in tqdm(etree.iterparse(args.input_file, events=("end",))):
        if elem.tag == 'title':
            titles.append(elem.text)

    with open(args.output_file, 'wb') as output:
        pickle.dump(titles, output)
