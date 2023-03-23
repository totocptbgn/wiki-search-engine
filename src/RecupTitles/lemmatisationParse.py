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

# Traitement des textes

def text_treatment(txt):

    count = 0
    # On itère sur les bouts de texte
    wiki_array = mwparserfromhell.parse(txt).filter_text()
    words = []
    for word in wiki_array:
        w = str(word)
        if not (w.startswith('http') or w.startswith('Catégorie:')) and re.search('[a-zA-Z]', w):
            for splited_word in re.split(r'\W+', str(w)):
                if len(splited_word) != 0 and re.search('[a-zA-Z]', splited_word):
                    words.append(splited_word)
                    count+=1
    return string_treatment(' '.join(words)), count

page = None
titre = None
text = None
links = None

with open('corpusLemm.xml', 'w') as f:
    f.write('<pages>')

# Pour chaque page, extraire le titre et le texte, les traiter puis les insérer dans un nouvel élément XML
for event, elem in ET.iterparse(filename, events=("start", "end")):

    if event == 'start':

        if elem.tag.endswith('page'):
            page = ET.Element('page')

        elif elem.tag.endswith('title'):
            titre = ET.SubElement(page, 'title')

        elif elem.tag.endswith('text'):
            text = ET.SubElement(page, 'text')

        elif elem.tag.endswith('links'):
            links = ET.SubElement(page, 'links')

    if event == 'end':

        if elem.tag.endswith('title'):
            titre.text = elem.text

        elif elem.tag.endswith('text'):
            text.text, count = text_treatment(elem.text)

        elif elem.tag.endswith('links'):
            links.text = elem.text

            if count > 1000 :

                with open('corpusLemm.xml', 'a') as f:
                    f.write(ET.tostring(page, encoding='unicode', method='xml'))

with open('corpusLemm.xml', 'a') as f:
    f.write('</pages>')
