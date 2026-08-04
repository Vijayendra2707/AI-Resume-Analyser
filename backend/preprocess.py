import re
import nltk
from nltk.corpus import stopwords

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))


def preprocess_text(text):
    if not text:
        return ""

    text = text.lower()

    text = re.sub(r'\bnode\.js\b|\bnode js\b', 'nodejs', text)
    text = re.sub(r'\breact\.js\b|\breact js\b', 'reactjs', text)
    text = re.sub(r'\bvue\.js\b|\bvue js\b', 'vuejs', text)

    text = re.sub(r'[^a-z0-9+#\-\/\.\s]', ' ', text)

    words = text.split()

    tech_protected = {"r", "c", "go"}

    cleaned_words = []

    for w in words:
        w = w.rstrip(".")

        if w and (w not in stop_words or w in tech_protected):
            cleaned_words.append(w)

    return " ".join(cleaned_words)