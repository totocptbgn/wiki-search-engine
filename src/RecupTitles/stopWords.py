from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import nltk
nltk.download('stopwords')

french_stopwords = set(stopwords.words('french'))



with open('out.txt', 'w') as f:
    for i in french_stopwords:
        f.write(i)
        f.write('\n')