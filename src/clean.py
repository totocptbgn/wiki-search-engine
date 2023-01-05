import xml.etree.ElementTree as ET
import re #regex

tree = ET.parse('data/frwiki10000.xml')
root = tree.getroot()

def TOFIL(str):
    str = str.lower()
    sans_accents = {'é':'e', 'è':'e', 'ê':'e', 'ë':'e', 'ô':'o', 'ö':'o', 'à':'a', 'â':'a', 'ä':'a', 'ù':'u', 'ü':'u', 'û':'u', 'î':'i', 'ï':'i', 'ç':'c'}
    for k in sans_accents.keys():
        str = str.replace(k, sans_accents[k])
    return str

pages = ET.Element('pages')

for page in root[1:]:
    p = ET.SubElement(pages, 'page')
    titre = ET.SubElement(p, 'titre')
    titre.text = TOFIL(page[0].text)
    for elem in page[3]:
        if elem.tag.endswith('text'):
            text = ET.SubElement(p, 'text')
            text.text = TOFIL(elem.text)

print(ET.tostring(pages, encoding='utf8', method='xml'))
