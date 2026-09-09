# 🧠 Voice Agent Platform

A modular, agent-driven voice assistant platform designed for real-time intent detection, retrieval, and response generation using speech-to-text (STT), text-to-speech (TTS), and backend orchestration.

---

## 📦 Project Structure

```
src/
├── agentic/
├── app/
│   └── helper/
├── dashboard/
├── data/
├── docs/
└── infrastructure/
```

---

## 🧩 Module Overview

### 🔹 `agentic/`

Contains the core intelligence layer of the system.

Responsible for:

* Speech-to-Text (STT)
* Text-to-Speech (TTS)
* Intent Classification
* Agent orchestration logic

This module forms the **decision-making brain** of the platform and processes user voice input into actionable backend queries.

---

### 🔹 `app/`

Acts as the primary backend service for the system.

Responsible for:

* API definitions
* Routing user input to appropriate agentic pipelines
* Handling service-level logic

#### `app/helper/`

Contains supporting modules used by the main backend application such as:

* Database connectors
* Schema definitions
* ORM models
* Utility functions

---

### 🔹 `dashboard/`

Currently uses **Streamlit** for:

* Local development
* Testing agent workflows
* Debugging voice-based interactions

> ⚠️ Note: This is a temporary interface and will be replaced with a production-grade frontend.

---

### 🔹 `data/`

Stores:

* Intent mappings
* Static response templates
* Knowledge base (`knowledge.txt`)

> 🚧 Planned Migration:
> The static knowledge system will be replaced with a **Retrieval-Augmented Generation (RAG)** based pipeline for dynamic response generation.

---

### 🔹 `docs/`

Contains documentation related to:

* System architecture
* API contracts
* Design decisions

---

### 🔹 `infrastructure/`

Contains database-related setup files such as:

* SQL schema definitions
* Data seeding scripts
* Migration support

---

---

### 🔹 `input/`

Contains the config files for the specific database
---
## 🔁 System Flow

For detailed architectural flow and interaction diagrams, refer to:

👉 https://excalidraw.com/#json=QfjuTBs084EPebmSCkvkw,0L1ImIBb8y5unltNS-10CA

---

## 🚀 Getting Started

### 1. Clone the Repository

```
git clone https://github.com/AyushTyagi2/startup101
cd startup101
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file based on the following:

```
DATABASE_URL=

```

---

### 4. Run Backend Server

From project root:

```
uvicorn app.main:app --reload
```

---

### 5. Run Dashboard (Dev Only)

```
streamlit run dashboard/dashboard.py
```

---

## 🛣️ Roadmap

* [ ] Replace static knowledge base with RAG pipeline
* [ ] Move Streamlit dashboard to production frontend
* [ ] Introduce vector database support
* [ ] Add multi-agent orchestration support

---

## 📄 License

Internal Use Only
