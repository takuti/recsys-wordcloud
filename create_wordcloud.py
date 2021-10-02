import csv
import requests
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer


STOPWORDS_GIST = 'https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt'


def build_base_stopwords():
    stopwords_list = requests.get(STOPWORDS_GIST).content
    stopwords = set(stopwords_list.decode().splitlines())
    stopwords |= set(open('stopwords.txt', 'r').read().rstrip().split('\n'))
    return stopwords


def extend_stopwords(corpus, stopwords, max_features=1024):
    vectorizer = TfidfVectorizer(stop_words=stopwords,
                                 max_features=max_features)
    vectorizer.fit(corpus)
    return stopwords | vectorizer.stop_words_


def run():
    stopwords = build_base_stopwords()
    corpus = {}
    for y in range(2008, 2022):
        print(y)
        abstracts = []
        with open('csv/{}.csv'.format(y), 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                abstracts.append(row['abstract'])
        corpus[y] = ' '.join(abstracts)
    stopwords = extend_stopwords(list(corpus.values()), stopwords)

    for y, source in corpus.items():
        wc = WordCloud(
            width=800,
            height=400,
            stopwords=stopwords,
            background_color='white',
            colormap='Set2'
        ).generate(source)
        wc.to_file('png/{}.png'.format(y))


if __name__ == '__main__':
    run()
