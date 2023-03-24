import xml.etree.ElementTree as ET
import mwparserfromhell
import re
from tqdm import tqdm
import spacy
from nltk.stem.snowball import SnowballStemmer
import sys

# pip install spacy
# python -m spacy download fr_core_news_sm

spacy.require_gpu()
nlp = spacy.load("fr_core_news_sm", disable=["tagger", "parser", "ner", "textcat"])
nlp.max_length = 10000000

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} [input file]")
    sys.exit(1)

with open('out.txt') as f:
    sw_list = f.read().splitlines()

def string_treatment(string):
    doc = nlp(string)
    words = [token.lemma_ for token in doc if token.text not in sw_list]
    return ' '.join(words)

def main():
    input_file = sys.argv[1]
    page = None
    nb_pages = 0

    with open('corpusLemm.xml', 'w') as f:
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
        elif event == 'end':
            if elem.tag == 'title':
                title.text = elem.text
                if nb_pages % 1000 == 0:
                    print(f"{nb_pages} :   {title.text}")
            elif elem.tag == 'text':
                text.text = string_treatment(elem.text)
            elif elem.tag == 'links':
                links.text = elem.text
                with open('corpusLemm.xml', 'ab') as f:
                    f.write(ET.tostring(page, encoding='utf-8', method='xml'))
    
    with open('corpusLemm.xml', 'a') as f:
        f.write('</pages>')

if __name__ == '__main__':
    main()
