def load_knowledge():
    knowledge = {}
    current_intent = None

    with open("data/knowledge.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            #print("i'm yha")

            if line.startswith("[") and line.endswith("]"):
                current_intent = line[1:-1]
                knowledge[current_intent] = ""
            elif current_intent and line:
                knowledge[current_intent] += line + " "

    return knowledge


KNOWLEDGE = load_knowledge()


def get_response(intent):
    #print("i'm here")
    return KNOWLEDGE.get(intent)
