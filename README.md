RecSys Wordcloud
===

Generate a wordcloud from RecSys paper abstracts.

## Installation

```sh
pip install -r requirements.txt
```

Additionally, make sure [ChromeDriver](https://chromedriver.chromium.org/home) is installed. On macOS, for example:

```sh
brew install chromedriver
# let macOS trust the developer
xattr -d com.apple.quarantine `which chromedriver`
```

## Usage

Examples: **[Understanding Research Trends in Recommender Systems from Word Cloud](https://takuti.me/note/recsys-wordcloud/)**

```sh
# all years
python src/retrieve_acm.py

# selected years
python src/retrieve_acm.py --years 2019 2022
```

```sh
# all years
python src/create_wordcloud.py

# single year
python src/create_wordcloud.py --year 2022
```
