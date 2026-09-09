
from agentic.intent_classifier import detect_intent
from agentic.retriever import get_response

print("🤖 Hotel Receptionist AI (type 'exit' to quit)\n")

while True:
    user = input("You: ")
    if user.lower() == "exit":
        break
    intent, score = detect_intent(user)

    if intent is None:
        print("Bot: Sorry, I’ll connect you to our staff.")
        continue

    response = get_response(intent)

    print(f"Bot: {response}", flush = True)