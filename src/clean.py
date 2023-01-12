import xml.etree.ElementTree as ET
import mwparserfromhell
import re

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
def text_treatment(str):

    # On enlève les balises ref et leurs contenus
    str = str.replace('&lt;', '<')
    str = str.replace('&gt;', '>')
    str = re.sub(r'<ref>([\s\S]*?)</ref>', '', str)

    # On enlève du gras et des italiques
    str = str.replace("\'\'\'", "")
    str = str.replace("\'\'", "")

    ## TODO:
    # - Retirer les structures dont on a pas besoin
    # - Extraire les liens
    # - Retirer les mots des structures (genre 'categorie', 'bibliographie', ...)
    # - Ne garder plus que les mots importants (retirer les stop words)

    return str

# Pour chaque page, extraire le titre et le texte, les traiter puis les insérer dans un nouvel élément XML
root = tree.getroot()
#pages = ET.Element('pages')
for page in root[1:]:
    #p = ET.SubElement(pages, 'page')
    #titre = ET.SubElement(p, 'titre')
    #titre.text = string_treatment(page[0].text)
    for elem in page[3]:
        if elem.tag.endswith('text'):
            
            #text = ET.SubElement(p, 'text')
            #text.text = text_treatment(string_treatment(elem.text))
            wiki_array = mwparserfromhell.parse(elem.text).filter_text()
            for word in wiki_array:
                # print(re.split(r'\W+', str(word)), str(word))
                print(str(word))
            words = []
    print(page[0].text)
    break


# On écrit le fichier xml 
# output_root = ET.ElementTree(pages)
# output_root.write('out.xml')
