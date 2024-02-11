# Example File
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer


class LemmaTokenizer:
    def __init__(self):
        self.download_assets()

        self.wnl = WordNetLemmatizer()
        self.stopwords = set(stopwords.words("english"))

    @classmethod
    def download_assets(cls):
        nltk.download("stopwords", quiet=True)
        nltk.download("wordnet", quiet=True)
        nltk.download("punkt", quiet=True)
        nltk.download("omw-1.4", quiet=True)
        nltk.download("averaged_perceptron_tagger", quiet=True)

    def __call__(self, doc):
        nltk_tagged = pos_tag(word_tokenize(doc))
        wordnet_tagged = ((x[0], self.nltk_pos_tagger(x[1])) for x in nltk_tagged)

        return [
            self.wnl.lemmatize(token, tag)
            for token, tag in wordnet_tagged
            if token not in self.stopwords and any(c.isalpha() for c in token)
        ]

    def nltk_pos_tagger(self, nltk_tag):
        if nltk_tag.startswith("J"):
            return wordnet.ADJ
        elif nltk_tag.startswith("V"):
            return wordnet.VERB
        elif nltk_tag.startswith("N"):
            return wordnet.NOUN
        elif nltk_tag.startswith("R"):
            return wordnet.ADV
        else:
            return wordnet.NOUN
