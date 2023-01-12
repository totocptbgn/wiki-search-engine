import xml.etree.ElementTree as ET
import mwparserfromhell
import re
from tqdm import tqdm

# Script qui prends comme entrée un fichier Wikimédia Dump, qui extrait et traite les données nécessaire, puis les écrit dans un XML.

# Lecture du fichier
filename = 'data/frwiki10000.xml'
tree = ET.parse(filename)

# Traitement des strings
def string_treatment(str):

    # On enlève les majuscules
    str = str.lower()

    # On enlève les accents
    sans_accents = {'é':'e', 'è':'e', 'ê':'e', 'ë':'e', 'ô':'o', 'ö':'o', 'à':'a', 'â':'a', 'ä':'a', 'ù':'u', 'ü':'u', 'û':'u', 'î':'i', 'ï':'i', 'ç':'c'}
    for k in sans_accents.keys():
        str = str.replace(k, sans_accents[k])
    return str

# Traitement des textes
def text_treatment(txt):
    txt = txt.replace('&lt;', '<')
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

# Pour chaque page, extraire le titre et le texte, les traiter puis les insérer dans un nouvel élément XML
root = tree.getroot()
pages = ET.Element('pages')
for page in tqdm(root[1:]):

    # Extraction du titre
    p = ET.SubElement(pages, 'page')
    titre = ET.SubElement(p, 'titre')
    titre.text = string_treatment(page[0].text)

    # Extraction du texte
    for elem in page[3]:
        if elem.tag.endswith('text'):
            text = ET.SubElement(p, 'text')
            text.text = text_treatment(elem.text)

    # Extraction des liens
    links = ET.SubElement(p, 'links')
    links.text = '\n'.join(
        [string_treatment(str(link.title)) for link in mwparserfromhell.parse(elem.text).filter_wikilinks() if not ':' in str(link.title)]
    )


# On écrit le fichier xml
output_root = ET.ElementTree(pages)
output_root.write('out.xml')
