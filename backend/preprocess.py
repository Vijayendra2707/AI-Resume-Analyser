import re
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    if not text:
        return ""

    text = text.lower()

    # OPTIONAL BUT HIGHLY RECOMMENDED: Alias Standardization
    # Normalize variations of common tech stack names before regex
    text = re.sub(r'\bnode\.js\b|\bnode js\b', 'nodejs', text)
    text = re.sub(r'\breact\.js\b|\breact js\b', 'reactjs', text)
    text = re.sub(r'\bvue\.js\b|\bvue js\b', 'vuejs', text)

    # 1. Keep dots for versions/files (Node.js, .NET)
    # 2. Keep brackets temporarily or replace with something that doesn't merge words
    text = re.sub(r'[^a-z0-9+#\-\/\.\s]', ' ', text)

    words = text.split()

    # Protect single-letter technical terms
    tech_protected = {'r', 'c', 'go'}
    
    cleaned_words = []
    for w in words:
        # STRIP trailing periods that were at the end of a sentence
        # e.g., "node.js." becomes "node.js"
        w = w.rstrip('.') 
        
        # Only add the word if it's not empty after stripping, and passes stopword check
        if w and (w not in stop_words or w in tech_protected):
            cleaned_words.append(w)

    return " ".join(cleaned_words)
