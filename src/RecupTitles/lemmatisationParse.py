import xml.etree.ElementTree as ET
#import mwparserfromhell
import re
from tqdm import tqdm
#import spacy
import nltk
#nltk.download('wordnet')
import multiprocessing
from multiprocessing import Pool
from nltk.stem.snowball import FrenchStemmer
import sys


# pip install spacy
# python -m spacy download fr_core_news_sm

word_regex = re.compile(r'\b\w+\b')
line_regex = re.compile(r'\b.+')

stemmer = FrenchStemmer()

num_processes = multiprocessing.cpu_count()

if num_processes > 1:
    num_processes//=2

#spacy.require_gpu()
#nlp = spacy.load("fr_core_news_sm", disable=["tagger", "parser", "ner", "textcat"])
#nlp.max_length = 10000000

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} [input file] [output file]")
    sys.exit(1)

with open('out.txt') as f:
    sw_list = f.read().splitlines()

def string_treatment(string, cores=num_processes):
    #doc = [w for w in word_regex.findall(string) if w not in sw_list]
    #with Pool(processes=cores) as pool:
    #    result = pool.map(wnl.lemmatize, doc)
    #return ' '.join(result)

    doc = [w for w in word_regex.findall(string) if w not in sw_list]
    with Pool(processes=cores) as pool:
        words = pool.map(stemmer.stem,doc)
    return ' '.join(words)

    #doc = word_regex.findall(string)
    #words = [token.lemma_ for token in doc if token.text not in sw_list]
    #return ' '.join(words)

def main():
    input_file = sys.argv[1]
    page = None
    nb_pages = 0
    with open(sys.argv[2], 'w') as f:
        f.write('<pages>')

    for event, elem in tqdm(ET.iterparse(input_file, events=("start", "end"))):
        if event == 'start':
            if elem.tag == 'page':
                page = ET.Element('page')
                nb_pages += 1
            elif elem.tag == 'title':
                title = ET.SubElement(page, 'title')
            elif elem.tag == 'text':
                text = ET.SubElement(page, 'text')
            elif elem.tag == 'links':
                links = ET.SubElement(page, 'links')
                #links = ET.Element('links')
        elif event == 'end':
            if elem.tag == 'title':
                title.text = elem.text
                if nb_pages % 1000 == 0:
                    print(f"{nb_pages} :   {title.text}")
            elif elem.tag == 'text':
                text.text = string_treatment(elem.text)
            elif elem.tag == 'links':
                if elem.text is not None:
                    links.text = '\n'.join(set(line_regex.findall(elem.text)))
                with open(sys.argv[2], 'ab') as f:
                    f.write(ET.tostring(page, encoding='utf-8', method='xml'))
                    #f.write(ET.tostring(links, encoding='utf-8', method='xml'))

    with open(sys.argv[2], 'a') as f:
        f.write('</pages>')

if __name__ == '__main__':
    main()
