import xml.etree.ElementTree as ET
import mwparserfromhell
import re
from tqdm import tqdm
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

# Script qui prends comme entrée un fichier Wikimédia Dump, qui extrait et traite les données nécessaire, puis les écrit dans un XML.

filename = 'data/frwiki10000.xml'
theme = ['sport', 'sports', 'sportif']

def retire_accents(str):
    sans_accents = {'é':'e', 'è':'e', 'ê':'e', 'ë':'e', 'ô':'o', 'ö':'o', 'à':'a', 'â':'a', 'ä':'a', 'ù':'u', 'ü':'u', 'û':'u', 'î':'i', 'ï':'i', 'ç':'c'}
    for k in sans_accents.keys():
        str = str.replace(k, sans_accents[k])
    return str

french_stopwords = set([retire_accents(w) for w in stopwords.words('french')])


# Lecture du fichier

# Traitement des strings
# On enlève les majuscules, les accents, les caracteres speciaux et les stopwords
def string_treatment(str):
    str = str.lower()
    str = retire_accents(str)
    words = [word for word in re.split('[^a-z]+', str) if word not in french_stopwords]
    return ' '.join(words)

# Traitement des textes

def text_treatment(txt, theme):
    txt = re.sub(r'(\[\[Fichier:.*\]\])|(\[\[Catégorie:.*\]\])', '', txt)
    txt = re.sub(r'(\<ref.+\<\/ref\>)|(\<ref .+\/\>)|(\<\/ref\>)', '', txt)
    txt = re.sub(r'#tag:ref|', '', txt)
    txt = re.sub(r'(class=\".+\")|(style=\".+\")', '', txt)
    txt = re.sub(r'\<(.+)\>(.+)\<\/\1\>', r'\2', txt)
    txt = re.sub(r'(\{\{formatnum:\d+\}\})|(colspan=\".+\")|(rowspan=\".+\")|(scope=\".+\")|(align=\".+\")', '', txt)

    # partie redondante avec string_treatment mais qui permet de ne pas split et relier plusieurs fois les mots
    txt = txt.lower()
    txt = retire_accents(txt)
    words = [word for word in re.split('[^a-z]+', txt) if word not in french_stopwords]

    inTheme = False
    for word in words:
        if word in theme:
            inTheme = True

    return ' '.join(words), len(words), inTheme


page = None
titre = None
text = None
links = None

with open('out.xml', 'w') as f:
    f.write('<pages>')

# Pour chaque page, extraire le titre et le texte, les traiter puis les insérer dans un nouvel élément XML
for event, elem in tqdm(ET.iterparse(filename, events=("start", "end"))):

    if event == 'start':

        if elem.tag.endswith('page'):
            page = ET.Element('page')

        elif elem.tag.endswith('title'):
            titre = ET.SubElement(page, 'title')

        elif elem.tag.endswith('text'):
            text = ET.SubElement(page, 'text')

    if event == 'end':

        if elem.tag.endswith('title'):
            titre.text = string_treatment(elem.text)

        elif elem.tag.endswith('text'):

            if (not isinstance(elem.text, str)): # article avec format 'bizarre', ex: xml dans lequel il y a des balises mal interpretees
                continue

            text.text, count, inTheme = text_treatment(elem.text, theme)

            if count > 1000 and inTheme:
                links = ET.SubElement(page, 'links')
                links.text = '\n'.join(
                    [string_treatment(str(link.title)) for link in mwparserfromhell.parse(elem.text).filter_wikilinks() if not ':' in str(link.title)]
                )

                with open('out.xml', 'a') as f:
                    f.write(ET.tostring(page, encoding='unicode', method='xml'))

with open('out.xml', 'a') as f:
    f.write('</pages>')
