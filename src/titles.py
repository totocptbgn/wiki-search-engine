import xml.etree.ElementTree as ET
import numpy as np


liste_titles = dict()
count = 0

for event, elem in ET.iterparse('out.xml', events=("start", "end")):
	if event == 'end' and elem.tag == 'title':
		liste_titles[count] = elem.text

		print(f'title n. {count} : {liste_titles[count]}')

		count +=1

print(f'dictionnaire titres :')
print(liste_titles)



