from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            )

def embed(texts):
        return model.encode(texts, normalize_embeddings=True)

