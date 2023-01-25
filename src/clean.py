import xml.etree.ElementTree as ET
import mwparserfromhell
import re
from tqdm import tqdm
# pip install spacy
# python -m spacy download fr_core_news_sm
import spacy
nlp = spacy.load("fr_core_news_sm")
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import nltk
nltk.download('stopwords')

french_stopwords = set(stopwords.words('french'))

# Script qui prends comme entrée un fichier Wikimédia Dump, qui extrait et traite les données nécessaire, puis les écrit dans un XML.

# Lecture du fichier
filename = 'data/frwiki10000.xml'

# Traitement des strings
def string_treatment(str):

    # On enlève les majuscules et les stopwords
    # et on lemmatise
    str = str.lower()
    doc = nlp(str)
    words = [token.lemma_ for token in doc if token.text not in french_stopwords]

    str = ' '.join(words)

    # On enlève les accents
    sans_accents = {'é':'e', 'è':'e', 'ê':'e', 'ë':'e', 'ô':'o', 'ö':'o', 'à':'a', 'â':'a', 'ä':'a', 'ù':'u', 'ü':'u', 'û':'u', 'î':'i', 'ï':'i', 'ç':'c'}
    for k in sans_accents.keys():
        str = str.replace(k, sans_accents[k])
    return re.sub(r'[^a-zA-Z ]', ' ', str)

# Traitement des textes
def text_treatment(txt):
    txt = txt.replace('&lt;', '<') # si on enlève ces 2 lignes pas d'erreur mais mauvais comportement
    txt = txt.replace('&gt;', '>')

    # On itère sur les bouts de texte
    wiki_array = mwparserfromhell.parse(txt).filter_text()
    words = []
    for word in wiki_array:
        w = str(word)
        if not (w.startswith('http') or w.startswith('Catégorie:')) and re.search('[a-zA-Z]', w):
            for splited_word in re.split(r'\W+', str(w)):
                if len(splited_word) != 0 and re.search('[a-zA-Z]', splited_word):
                    words.append(splited_word)
    return string_treatment(' '.join(words))
    #return string_treatment(words)


pages = ET.Element('pages')
numPages = 0
page = None
titre = None
text = None
links = None

# Pour chaque page, extraire le titre et le texte, les traiter puis les insérer dans un nouvel élément XML
for event, elem in ET.iterparse(filename, events=("start", "end")):

    if event == 'start':

        if elem.tag.endswith('page'):
            page = ET.SubElement(pages, 'page')

        elif elem.tag.endswith('title'):
            titre = ET.SubElement(page, 'title')

        elif elem.tag.endswith('text'):
            text = ET.SubElement(page, 'text')

    if event == 'end':

        if elem.tag.endswith('title'):
            titre.text = string_treatment(elem.text)

        elif elem.tag.endswith('text'):
            text.text = text_treatment(elem.text)

            links = ET.SubElement(page, 'links')
            links.text = '\n'.join(
                [string_treatment(str(link.title)) for link in mwparserfromhell.parse(elem.text).filter_wikilinks() if not ':' in str(link.title)]
            )

        elif elem.tag == 'page':
            numPages += 1

            if numPages % 100 == 0:
                tree = ET.ElementTree(pages)
                tree.write('out.xml', xml_declaration=True, method='xml')
                pages.clear()

tree = ET.ElementTree(pages)
tree.write('out.xml', xml_declaration=True, method='xml')
