import xml.etree.ElementTree as et

tree = et.parse('frwiki10000.xml')
root = tree.getroot()

def printTitle():
    for child in root:
        for c in child:
            if c.tag.endswith('title'):
                print(c.text)

for child in root:
    for c in child:
        print(c)