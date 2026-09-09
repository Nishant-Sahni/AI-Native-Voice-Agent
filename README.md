# 🏨 Hotel Voice Receptionist AI

An AI-powered voice receptionist for hotels that handles inbound calls, answers guest FAQs, and collects booking requests — all through natural speech. Built with a modular pipeline: speech-to-text → intent classification → response generation → text-to-speech, backed by a FastAPI service and PostgreSQL.

---

## ✨ Features

- **Real-time voice interaction** — listens to guests via microphone, responds with synthesized speech
- **Multilingual intent detection** — understands both English and Hindi/Hinglish queries (e.g. *"room book karna hai"*, *"wifi chalta hai"*)
- **FAQ answering** — handles 13+ common hotel queries (menu, pricing, check-in/out times, parking, WiFi, cancellations, and more)
- **Booking flow** — captures check-in date and number of nights, logs booking to the database
- **Full call logging** — every conversation (user + AI messages) is persisted per call with timestamps and outcomes
- **Streamlit dashboard** — dev-only UI for testing and debugging agent workflows

---

## 🗂️ Project Structure

```
src/
├── agentic/                  # Core AI pipeline
│   ├── stt.py                # Speech-to-text (faster-whisper)
│   ├── tts.py                # Text-to-speech (Coqui TTS / Tacotron2)
│   ├── intent_classifier.py  # Semantic intent detection via embeddings
│   ├── embedder.py           # Sentence embedding wrapper
│   ├── retriever.py          # Knowledge base lookup
│   └── backend_client.py     # HTTP client for the FastAPI backend
├── app/                      # FastAPI backend service
│   ├── main.py               # API routes (calls, messages, bookings)
│   └── helper/
│       ├── database.py       # SQLAlchemy engine & session
│       ├── models.py         # ORM models
│       └── schemas.py        # Pydantic schemas
├── dashboard/
│   └── dashboard.py          # Streamlit dev dashboard
├── data/
│   ├── intents.json          # Intent → example utterances mapping
│   └── knowledge.txt         # Canned responses per intent
├── infrastructure/
│   ├── hotel.sql             # PostgreSQL schema (hotels, rooms, calls, bookings)
│   └── insert.sql            # Seed data
├── input/
│   ├── calls.json            # Sample call configs
│   └── generic.json          # Generic config
├── voice_app.py              # Main voice loop entry point
├── app.py                    # Alt entry point
├── requirements.txt
└── docs/
    └── architecture.md
```

---

## 🔁 How It Works

```
Caller speaks
    │
    ▼
[STT] faster-whisper transcribes audio
    │
    ▼
[Intent Classifier] embeds text → cosine similarity against intent vectors
    │
    ├── FAQ intent detected  →  [Retriever] looks up canned response  →  [TTS] speaks reply
    │
    └── BOOK_ROOM intent  →  enters booking flow  →  collects date + nights  →  logs to DB
```

All turns are logged to the backend (`/calls/{id}/messages`) with sender (`USER` or `AI`). Calls are closed with an outcome: `ANSWERED`, `BOOKING_STARTED`, or `ESCALATED`.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Speech-to-Text | [faster-whisper](https://github.com/guillaumekln/faster-whisper) (`small` model, `int8`) |
| Text-to-Speech | [Coqui TTS](https://github.com/coqui-ai/TTS) — Tacotron2-DDC / LJSpeech |
| Intent Classification | [sentence-transformers](https://www.sbert.net/) + FAISS + cosine similarity |
| Backend API | FastAPI + Uvicorn |
| Database | PostgreSQL (via SQLAlchemy + psycopg2) |
| Dev Dashboard | Streamlit |
| Audio I/O | sounddevice + numpy |

---

## ⚙️ Setup

### Prerequisites

- Python 3.10+
- PostgreSQL running locally
- A microphone + speakers (or headset)

### 1. Clone the repository

```bash
git clone https://github.com/AyushTyagi2/startup101
cd startup101/src
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** Coqui TTS and faster-whisper will download model weights on first run (~few hundred MB each).

### 3. Set up the database

Create a PostgreSQL database and run the schema:

```bash
psql -U <your_user> -d <your_db> -f infrastructure/hotel.sql
psql -U <your_user> -d <your_db> -f infrastructure/insert.sql
```

### 4. Configure environment variables

Create a `.env` file in `src/`:

```env
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
```

### 5. Start the backend API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs at `/docs`.

### 6. Run the voice receptionist

In a separate terminal:

```bash
python voice_app.py
```

The agent will greet the caller and begin listening.

### 7. (Optional) Run the dev dashboard

```bash
streamlit run dashboard/dashboard.py
```

---

## 🔌 API Overview

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/calls/start` | Start a new call session |
| `POST` | `/calls/{id}/messages` | Log a message (USER or AI) |
| `POST` | `/calls/{id}/end` | End a call with an outcome |
| `GET` | `/calls` | List all calls |
| `GET` | `/calls/{id}/messages` | Get full transcript for a call |
| `POST` | `/bookings/start` | Create an in-progress booking |
| `PATCH` | `/bookings/{id}` | Update booking fields (date, nights, status) |
| `GET` | `/bookings` | List all bookings |

---

## 🧠 Intent System

Intents are defined in `data/intents.json` as a map of intent name → list of example phrases (English + Hindi/Hinglish). At startup, these are embedded and averaged into a single vector per intent. Incoming speech is embedded and matched by cosine similarity with a configurable threshold (default `0.35`).

**Supported intents:** `ASK_MENU`, `ASK_BREAKFAST`, `ASK_ROOM_PRICE`, `ASK_ROOM_AVAILABILITY`, `ASK_CHECKIN_TIME`, `ASK_CHECKOUT_TIME`, `ASK_WIFI`, `ASK_PARKING`, `ASK_LOCATION`, `ASK_CANCELLATION_POLICY`, `ASK_LATE_CHECKOUT`, `ASK_CONTACT`, `TALK_TO_HUMAN`, `EXIT_CONVERSATION`, `CONFIRMATION`, `BOOK_ROOM`

To add a new intent: add an entry to `intents.json` and a corresponding response block in `data/knowledge.txt`.

---

## 🧪 LLM Experiments — Data Cleaning & Extraction

During development, LLMs were explored as an alternative to rule-based data cleaning and structured extraction from raw call/booking data. Two backends were tested:

### Ollama — Local (Phi-3)

[Phi-3](https://ollama.com/library/phi3) was run locally via [Ollama](https://ollama.com/) for fully offline, zero-cost inference. Suitable for lightweight extraction tasks on a laptop.

**Setup:**

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the Phi-3 model
ollama pull phi3
```

**Example usage:**

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

> Phi-3 worked well for simple structured extraction. Latency was acceptable on CPU for short prompts.

---

### Google Gemini — API

[Gemini](https://ai.google.dev/) was tested as a cloud-based alternative for higher accuracy on ambiguous or noisy inputs.

**Setup:**

```bash
pip install google-generativeai
```

Add to `.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

**Example usage:**

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

---

### Comparison

| | Ollama (Phi-3) | Gemini API |
|---|---|---|
| Cost | Free (local) | Pay-per-use |
| Privacy | Fully local | Cloud |
| Speed | Moderate (CPU) | Fast |
| Accuracy | Good for simple inputs | Better on ambiguous text |
| Setup | Requires Ollama install | Requires API key |

Both approaches were used experimentally and are not wired into the main pipeline yet. Integration is planned as part of the RAG migration.

---

## 🗺️ Roadmap

- [ ] Replace static knowledge base with a RAG (Retrieval-Augmented Generation) pipeline
- [ ] Integrate vector database (e.g. Qdrant, Pinecone) for dynamic knowledge retrieval
- [ ] Replace Streamlit dashboard with a production frontend
- [ ] Multi-agent orchestration support
- [ ] Caller phone number identification & returning-guest detection
- [ ] Real-time availability check via hotel PMS integration

---

## 📄 License

Internal use only.
