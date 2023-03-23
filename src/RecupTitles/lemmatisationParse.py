import xml.etree.ElementTree as ET
import mwparserfromhell
import re
from tqdm import tqdm
# pip install spacy
# python -m spacy download fr_core_news_sm
import spacy
nlp = spacy.load("fr_core_news_sm")
from nltk.stem.snowball import SnowballStemmer
import sys

if (len(sys.argv) != 2):
    print("Waited: python " + sys.argv[0] + " [input file]")
    exit()

french_stopwords = open('out.txt')
sw_list = french_stopwords.read().splitlines()


# Script qui prends comme entrée un fichier Wikimédia Dump, qui extrait et traite les données nécessaire, puis les écrit dans un XML.

# Lecture du fichier
filename = sys.argv[1]

# Traitement des strings
def string_treatment(str):

    # et on lemmatise
    doc = nlp(str)
    words = [token.lemma_ for token in doc if token.text not in sw_list]

    str = ' '.join(words)

    return str

page = None
titre = None
text = None
links = None
nbPages = 0

with open('corpusLemm.xml', 'w') as f:
    f.write('<pages>')

# Pour chaque page, extraire le titre et le texte, les traiter puis les insérer dans un nouvel élément XML
for event, elem in ET.iterparse(filename, events=("start", "end")):

    if event == 'start':

        if elem.tag == 'page':
            page = ET.Element('page')
            nbPages += 1

        elif elem.tag == 'title':
            titre = ET.SubElement(page, 'title')

        elif elem.tag == 'text':
            text = ET.SubElement(page, 'text')

        elif elem.tag == 'links':
            links = ET.SubElement(page, 'links')

    if event == 'end':

        if elem.tag == 'title':
            titre.text = elem.text

            if nbPages % 1000 == 0:
                print(str(nbPages) + " :   " + titre.text)

        elif elem.tag == 'text':
            text.text = string_treatment(elem.text)

        elif elem.tag == 'links':
            links.text = elem.text

            with open('corpusLemm.xml', 'a') as f:
                f.write(ET.tostring(page, encoding='unicode', method='xml'))

with open('corpusLemm.xml', 'a') as f:
    f.write('</pages>')
