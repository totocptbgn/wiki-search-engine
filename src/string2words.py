import unicodedata
from nltk.stem.snowball import FrenchStemmer
import re

stemmer = FrenchStemmer()

spec_regex = re.compile(r'[^a-z ]+')

with open('stopwords.txt', 'r') as f:
    sw_list = set(f.read().splitlines())

def requete2words(requete):
    requete = requete.lower()
    requete = unicodedata.normalize('NFKD', requete)
    requete = ''.join(c for c in requete if not unicodedata.combining(c))
    requete = spec_regex.sub(r'', requete)
    return [stemmer.stem(w) for w in requete.split() if w not in sw_list]
