import sys
sys.stdout.reconfigure(line_buffering=True)

from agentic.stt import speech_to_text
from agentic.intent_classifier import detect_intent
from agentic.retriever import get_response
from agentic.tts import speak
import random
from agentic.backend_client import BackendClient

HOTEL_ID = "d5c74c93-d649-4d8c-8040-5c2e8769fa62"
conversation_mode = "FAQ"  # or "BOOKING"
booking_id = None
booking_state = None
backend = BackendClient(hotel_id = HOTEL_ID, caller_phone=None)
backend.start_call()
ACK_PHRASES = [
    "Just a moment please.",
    "Certainly, one moment.",
    "Sure, let me check that for you."
]

def acknowledge():
    phrase = random.choice(ACK_PHRASES)
    speak(phrase, speed=0.9)

def play_intro():
    intro_text = (
        "Thank you for calling Hotel Sunrise. "
        "It is a pleasure to assist you today. "
        "How may I help you?"
    )
    speak(intro_text)

print("🎧 Voice Receptionist AI (say 'exit' to quit)\n")
play_intro()
while True:

    text = speech_to_text()
    
    backend.log_user(text)
    
    acknowledge()
    
    print(f"You said: {text}")

    if "exit" in text.lower():
        backend.end_call(
            outcome="BOOKING_STARTED" if conversation_mode == "BOOKING" else "ANSWERED"
        )
        speak("Goodbye")
        break


    if conversation_mode == "BOOKING":
        if booking_state == "ASK_CHECKIN_DATE":
            backend.update_booking(
                {"checkin_date_raw": text}
            )
            booking_state = "ASK_NIGHTS"

            response = "Thank you. For how many nights will you be staying?"
            backend.log_ai(response)
            speak(response)
            continue

        if booking_state == "ASK_NIGHTS":
            backend.update_booking(
                {"nights": text}
            )

            response = (
                "Thank you. I have noted your booking request. "
                "Our reception team will confirm availability shortly."
            )
            backend.log_ai(response)
            speak(response)

            backend.end_call(outcome="BOOKING_STARTED")
            break
    intent, score = detect_intent(text)

    if conversation_mode == "FAQ" and intent == "BOOK_ROOM":
        conversation_mode = "BOOKING"
        booking_state = "ASK_CHECKIN_DATE"
        booking_id = backend.start_booking()
        
        backend.log_ai("Booking flow started")

        response = (
            "Certainly. I can help you with a room booking. "
            "May I know your check-in date?"
        )

        backend.log_ai(response)
        speak(response)
        continue


    if intent:
        response = get_response(intent)
    else:
        response = "Sorry, I will connect you to our staff."

    print(f"Bot: {response}")
    backend.log_ai(response)
    speak(response)
