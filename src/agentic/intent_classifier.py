import json
import numpy as np
from .embedder import embed

with open("data/intents.json", "r", encoding="utf-8") as f:
        INTENTS = json.load(f)

        intent_names = []
        intent_vectors = []
        for intent, examples in INTENTS.items():
            vectors = embed(examples)
            mean_vector = np.mean(vectors, axis=0)
            intent_names.append(intent)
            intent_vectors.append(mean_vector)

intent_vectors = np.vstack(intent_vectors)

def detect_intent(user_text, threshold=0.35):
    user_vec = embed([user_text])[0]
    scores = intent_vectors @ user_vec

    best_idx = int(np.argmax(scores))
    best_score = float(scores[best_idx])
    best_intent = intent_names[best_idx]

    #print(f"[DEBUG] intent={best_intent}, score={best_score:.3f}")

    if best_score < threshold:
        #print("I'm here")
        return None, best_score

    return best_intent, best_score


