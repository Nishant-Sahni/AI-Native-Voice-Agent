# Hotel Voice Receptionist

> A voice agent that answers hotel guests, handles common questions, and takes booking requests.

`Python` · `faster-whisper` · `Sentence-Transformers` · `Coqui TTS` · `FastAPI` · `PostgreSQL` · `Streamlit`

---

## Overview

The project is an AI-powered voice receptionist for hotels. It takes inbound calls, answers guest FAQs and collects booking requests through natural speech.

The pipeline is modular: speech-to-text, then intent classification, then response generation, then text-to-speech. A FastAPI service and a PostgreSQL database sit behind it.

---

## Features

| Feature | What it does |
|---|---|
| Voice interaction | Listens to the guest through the microphone and replies with synthesized speech |
| Multilingual intents | Understands English and Hindi/Hinglish, for example *"room book karna hai"* or *"wifi chalta hai"* |
| FAQ answers | Covers 13+ common hotel queries: menu, pricing, check-in/out times, parking, WiFi, cancellations and more |
| Booking flow | Captures the check-in date and the number of nights, and logs the booking to the database |
| Call logging | Stores every user and AI message for each call, with timestamps and outcomes |
| Dev dashboard | A Streamlit UI to test and debug agent workflows |

---

## Architecture

```
mic ──▶ STT ──▶ intent classifier ──┬──▶ FAQ intent ──▶ retriever ──▶ TTS ──▶ speaker
                                    │
                                    └──▶ BOOK_ROOM ──▶ booking flow (date, nights) ──▶ database
```

Every turn goes to the backend at `/calls/{id}/messages` with a sender (`USER` or `AI`). A call ends with one outcome: `ANSWERED`, `BOOKING_STARTED` or `ESCALATED`.

---

## Repository layout

```
src/
├── voice_app.py              →  main voice loop (entry point)
├── app.py                    →  alternative entry point
├── requirements.txt
├── agentic/                  →  core AI pipeline
│   ├── stt.py                →  speech-to-text (faster-whisper)
│   ├── tts.py                →  text-to-speech (Coqui TTS, Tacotron2)
│   ├── intent_classifier.py  →  semantic intent detection with embeddings
│   ├── embedder.py           →  sentence embedding wrapper
│   ├── retriever.py          →  knowledge base lookup
│   └── backend_client.py     →  HTTP client for the FastAPI backend
├── app/                      →  FastAPI backend
│   ├── main.py               →  routes for calls, messages and bookings
│   └── helper/
│       ├── database.py       →  SQLAlchemy engine and session
│       ├── models.py         →  ORM models
│       └── schemas.py        →  Pydantic schemas
├── dashboard/
│   └── dashboard.py          →  Streamlit dev dashboard
├── data/
│   ├── intents.json          →  intent name to example phrases
│   └── knowledge.txt         →  canned response for each intent
├── infrastructure/
│   ├── hotel.sql             →  PostgreSQL schema (hotels, rooms, calls, bookings)
│   └── insert.sql            →  seed data
├── input/
│   ├── calls.json            →  sample call configs
│   └── generic.json          →  generic config
└── docs/
    └── architecture.md
```

---

## Tech stack

- **Speech-to-text:** [faster-whisper](https://github.com/guillaumekln/faster-whisper), `small` model, `int8`
- **Text-to-speech:** [Coqui TTS](https://github.com/coqui-ai/TTS), Tacotron2-DDC trained on LJSpeech
- **Intent classification:** [sentence-transformers](https://www.sbert.net/), FAISS and cosine similarity
- **Backend API:** FastAPI with Uvicorn
- **Database:** PostgreSQL through SQLAlchemy and psycopg2
- **Dashboard:** Streamlit
- **Audio I/O:** sounddevice and numpy

---

## Getting started

**You need:** Python 3.10+, PostgreSQL running locally, and a microphone with speakers or a headset.

Run every command below from the `src/` folder.

1. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Coqui TTS and faster-whisper download their model weights on the first run (a few hundred MB each).

2. **Create the database**

   Create a PostgreSQL database, then load the schema and the seed data:

   ```bash
   psql -U <your_user> -d <your_db> -f infrastructure/hotel.sql
   psql -U <your_user> -d <your_db> -f infrastructure/insert.sql
   ```

3. **Set the environment variables**

   Create a `.env` file in `src/`:

   ```env
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
   ```

4. **Start the backend API**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API runs at `http://127.0.0.1:8000`. The interactive docs are at `/docs`.

5. **Start the voice receptionist** in a second terminal

   ```bash
   python voice_app.py
   ```

   The agent greets the caller and starts to listen.

6. **Optional: start the dev dashboard**

   ```bash
   streamlit run dashboard/dashboard.py
   ```

---

## API reference

| Endpoint | Purpose |
|---|---|
| `POST /calls/start` | Start a new call session |
| `POST /calls/{id}/messages` | Log a message (USER or AI) |
| `POST /calls/{id}/end` | End a call with an outcome |
| `GET /calls` | List all calls |
| `GET /calls/{id}/messages` | Get the full transcript of a call |
| `POST /bookings/start` | Create an in-progress booking |
| `PATCH /bookings/{id}` | Update booking fields (date, nights, status) |
| `GET /bookings` | List all bookings |

---

## Intent system

`data/intents.json` maps each intent name to a list of example phrases in English and Hindi/Hinglish. At startup, the system embeds the phrases and averages them into one vector per intent. It embeds each incoming sentence and matches it by cosine similarity. The default threshold is `0.35` and you can change it.

| Group | Intents |
|---|---|
| Hotel questions | `ASK_MENU`, `ASK_BREAKFAST`, `ASK_ROOM_PRICE`, `ASK_ROOM_AVAILABILITY`, `ASK_CHECKIN_TIME`, `ASK_CHECKOUT_TIME`, `ASK_WIFI`, `ASK_PARKING`, `ASK_LOCATION`, `ASK_CANCELLATION_POLICY`, `ASK_LATE_CHECKOUT`, `ASK_CONTACT` |
| Booking | `BOOK_ROOM` |
| Conversation control | `TALK_TO_HUMAN`, `EXIT_CONVERSATION`, `CONFIRMATION` |

To add an intent, add an entry to `intents.json` and a matching response block to `data/knowledge.txt`.

---

## LLM experiments

During development, LLMs were tested as an alternative to rule-based cleaning and extraction of raw call and booking data. Two backends were tried. Both stay outside the main pipeline for now. Integration is planned with the RAG migration.

<details>
<summary><b>Ollama with Phi-3 (local)</b></summary>

<br>

[Phi-3](https://ollama.com/library/phi3) ran locally through [Ollama](https://ollama.com/). It is fully offline and costs nothing, so it suits light extraction tasks on a laptop.

Install Ollama (macOS/Linux) and pull the model:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull phi3
```

Example:

```python
import requests

def extract_with_ollama(raw_text: str) -> dict:
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "phi3",
        "prompt": f"Extract check-in date and number of nights from this text as JSON: '{raw_text}'",
        "stream": False
    })
    return response.json()["response"]
```

Phi-3 worked well for simple structured extraction. Latency was acceptable on CPU for short prompts.

</details>

<details>
<summary><b>Google Gemini (API)</b></summary>

<br>

[Gemini](https://ai.google.dev/) was tested as a cloud option for higher accuracy on ambiguous or noisy input.

Install the client:

```bash
pip install google-generativeai
```

Add the key to `.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

Example:

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def extract_with_gemini(raw_text: str) -> str:
    response = model.generate_content(
        f"Extract check-in date and number of nights from this text as JSON: '{raw_text}'"
    )
    return response.text
```

</details>

**Comparison**

| | Ollama (Phi-3) | Gemini API |
|---|---|---|
| Cost | Free (local) | Pay per use |
| Privacy | Fully local | Cloud |
| Speed | Moderate (CPU) | Fast |
| Accuracy | Good for simple input | Better on ambiguous text |
| Setup | Install Ollama | Get an API key |

---

## Roadmap

- [ ] Replace the static knowledge base with a RAG (Retrieval-Augmented Generation) pipeline
- [ ] Add a vector database (for example Qdrant or Pinecone) for dynamic retrieval
- [ ] Replace the Streamlit dashboard with a production frontend
- [ ] Support multi-agent orchestration
- [ ] Identify the caller by phone number and detect returning guests
- [ ] Check room availability in real time through the hotel PMS

---

## License

Internal use only.
