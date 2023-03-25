import argparse
import re
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from lxml import etree
from nltk.stem.snowball import FrenchStemmer

word_regex = re.compile(r'\b\w+\b')
line_regex = re.compile(r'\b.+')

stemmer = FrenchStemmer()

parser = argparse.ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('output_file')
args = parser.parse_args()

with open('out.txt') as f:
    sw_list = set(f.read().splitlines())

def string_treatment(string):
    doc = [w for w in word_regex.findall(string) if w not in sw_list]
    words = pool.map(stemmer.stem, doc)
    return ' '.join(words)

def process_page(elem, nb_pages):
    title_elem = elem.find('title')
    text_elem = elem.find('text')
    links_elem = elem.find('links')
    title = etree.Element('title')
    title.text = title_elem.text
    text = etree.Element('text')
    text.text = string_treatment(text_elem.text)
    links = etree.Element('links')
    if links_elem.text is not None:
        links.text = '\n'.join(set(line_regex.findall(links_elem.text)))
    page = etree.Element('page')
    page.append(title)
    page.append(text)
    page.append(links)
    if nb_pages % 1000 == 0:
        print(f"{nb_pages} :   {title.text}")
    return page

if __name__ == '__main__':
    pool = Pool(processes=cpu_count() // 2)
    with open(args.output_file, 'wb') as f:
        f.write(b'<pages>')
        nb_pages = 0
        for event, elem in tqdm(etree.iterparse(args.input_file, events=("end",))):
            if elem.tag == 'page':
                page = process_page(elem, nb_pages)
                f.write(etree.tostring(page, encoding='utf-8', method='xml'))
                nb_pages += 1
        f.write(b'</pages>')
    pool.close()
