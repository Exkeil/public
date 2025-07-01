import re
import string

from nltk.corpus import stopwords

stop_words = set(stopwords.words("russian") + stopwords.words("english"))
custom_stop_words = stop_words - {"работа", "опыт", "проект"}

def preprocess_texts(text_list):
    processed = []
    for text in text_list:
        text = re.sub(r"<[^>]+>", "", text)  # remove HTML
        text = text.lower()
        text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
        words = text.split()
        words = [w for w in words if w not in stop_words and len(w) > 2]
        processed.append(" ".join(words))
    return processed