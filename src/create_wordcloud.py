import argparse
import csv
import os
import requests
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer


dirname = os.path.dirname(__file__)
STOPWORDS_FILE = os.path.join(dirname, '../resources/stopwords.txt')
CSV_DIR = os.path.join(dirname, '../resources/csv/')
OUT_DIR = os.path.join(dirname, '../out/')

STOPWORDS_URLS = [
    'https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt',
    # https://github.com/SerhadS/TechNet
    # https://www.researchgate.net/publication/341926808_Stopwords_in_Technical_Language_Processing
    'https://raw.githubusercontent.com/SerhadS/TechNet/master/additional_stopwords/TN_additional_stopwords.txt',
    'https://raw.githubusercontent.com/SerhadS/TechNet/master/additional_stopwords/USPTO_stopwords_en.txt',
    'https://raw.githubusercontent.com/SerhadS/TechNet/master/additional_stopwords/nltk_stopwords_en.txt',
    'https://raw.githubusercontent.com/SerhadS/TechNet/master/additional_stopwords/technical_stopwords.txt'
]

YEAR_RANGE = range(2008, 2023)


def build_base_stopwords():
    stopwords = set()
    for url in STOPWORDS_URLS:
        stopwords_list = requests.get(url).content
        stopwords |= set(stopwords_list.decode().splitlines())
    stopwords |= set(open(STOPWORDS_FILE, 'r').read().rstrip().split('\n'))
    return stopwords


def extend_stopwords(corpus, stopwords):
    vectorizer = TfidfVectorizer(
        stop_words=stopwords,
        max_features=2048,
        ngram_range=(1, 2)
    )
    vectorizer.fit(corpus)
    return stopwords | vectorizer.stop_words_


def run():
    stopwords = build_base_stopwords()
    corpus = {}
    for year in YEAR_RANGE:
        print(year)
        abstracts = []
        path = os.path.join(CSV_DIR, '{}.csv'.format(year))
        with open(path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                abstracts.append(row['abstract'])
        corpus[year] = ' '.join(abstracts)
    stopwords = extend_stopwords(list(corpus.values()), stopwords)

    for year, source in corpus.items():
        wc = WordCloud(
            width=800,
            height=400,
            stopwords=stopwords,
            background_color='white',
            colormap='bone'
        ).generate(source)
        wc.to_file(os.path.join(OUT_DIR, '{}.png'.format(year)))


def run_single_year(year):
    stopwords = build_base_stopwords()

    abstracts = []
    path = os.path.join(CSV_DIR, '{}.csv'.format(year))
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            abstracts.append(row['abstract'])

    stopwords = extend_stopwords(abstracts, stopwords)

    wc = WordCloud(
        width=800,
        height=400,
        stopwords=stopwords,
        background_color='white',
        colormap='bone'
    ).generate(' '.join(abstracts))
    wc.to_file(os.path.join(OUT_DIR, '{}.png'.format(year)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--year', type=int)
    args = parser.parse_args()
    if not args.year:
        run()
    elif args.year in YEAR_RANGE:
        run_single_year(args.year)
    else:
        raise Exception(f'unsupported year "{args.year}"')
