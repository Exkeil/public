from sentence_transformers import SentenceTransformer

model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

def embed_texts(texts):
    return model.encode(texts, convert_to_tensor=True)
