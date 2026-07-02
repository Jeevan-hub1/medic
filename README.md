# MediSahayak - An End-to-End Healthcare Solution

## 🚀 Overview

MediSahayak is a comprehensive healthcare application designed to **bridge gaps in medical accessibility, prescription adherence, multilingual communication, and counterfeit medicine detection**. By leveraging **AI, NLP, and Blockchain**, MediSahayak ensures:

- **Timely medication reminders**
- **Conversational AI for diagnosis**
- **Blockchain-backed medicine verification**

## 🔥 The Problem & Our Idea

### Problems We Address:
- **Language Barriers**: Patients struggle to communicate symptoms and understand prescriptions due to multilingual challenges.
- **Prescription Adherence**: Rural patients often forget or misinterpret medicine intake schedules.
- **Counterfeit Medicines**: Lack of transparency in the pharmaceutical supply chain leads to fake medicine circulation.
- **Latency in Symptom Analysis**: Existing AI-based diagnosis systems have high latency in voice-to-voice interactions.

### Our Solution:
✅ **Conversational AI for Diagnosis**: A voice-to-voice system for **multilingual symptom analysis**.  
✅ **Prescription Analysis & Reminders**: Converts unstructured doctor prescriptions into structured reminders.  
✅ **Blockchain for Fake Medicine Detection**: Scans medicines across the supply chain to verify authenticity.  
✅ **Menstrual Health & Nutrition Guide**: Personalized diet plans based on **menstrual phase, location, budget, and available resources**.  

## 💡 Challenges We Faced

### Voice-to-Voice Conversational AI
- Handling **latency** issues in real-time voice interactions.
- Developing a **low-latency symptom analysis** system.
- Supporting **multilingual conversations** for better accessibility.

### Prescription Analysis
- Parsing **inconsistent doctor handwriting** and unstructured prescriptions.
- Standardizing **time references** (e.g., 'after lunch' varies across regions).
- Ensuring **accessibility for patients with basic mobile phones**.

### Blockchain for Fake Medicine Detection
- **Tracking medicines** across manufacturer, producer, and distributor levels.
- Developing a **QR-based verification system** for governments and NGOs.

## 🏗️ Project Architecture

### Prescription Reminder System

#### Implementation Steps:
1. **Extract unstructured text** from prescriptions.
2. **Convert text into structured medication reminders**.
3. **Integrate AI voice assistant** for better accessibility.
4. **Deliver reminders via SMS/voice calls** for rural patients.

#### Major Challenges:
- Handling **mixed-language prescriptions** (English + local languages).
- Reliable **scheduling of medicine intake reminders**.
- **Offline support** for patients in remote areas.

## 🏥 Doctor Image & Voice Analysis

### Project Phases & Commands:
- **Phase 1:** Extract Doctor’s Diagnosis Brain 🧠  
- **Phase 2:** Patient’s Voice Input 🎙️  
- **Phase 3:** Doctor’s Voice Analysis 🩺  
- **Phase 4:** Deploy AI-driven UI 🌐  

## 🥗 Artemaya Chatbot - Nutritional Guide for Women

- AI-powered **diet recommendations** based on menstrual cycle phase.
- **Personalized meal plans** considering **location, budget, and food availability**.
- **Nutritional tracking** for better menstrual health.

## 🔗 Blockchain-Based Fake Medicine Detection

- **Supply chain tracking** from **manufacturer to distributor**.
- **QR-based scanning** to verify authenticity at all levels.
- **Integration for government & NGOs** to track medicine quality.

## 📁 Repository Structure

This repository bundles several loosely-coupled sub-projects, each of which can be run independently:

| Path | What it is | Stack |
|------|------------|-------|
| `backend/` | Main REST API for the platform (auth, chat, reports, predictions, recommendations, appointments, notifications, video, maps). Also serves the website at `/app`. | FastAPI, SQLAlchemy, SQLite, Gemini |
| `Sanjeevani Website/` | The web frontend (dashboard, doctors, chatbot, report analyzer, etc.). | HTML, CSS, vanilla JS |
| `Artemaya Chatbot/` | RAG-based nutrition/menstrual-health advisor API. | FastAPI, LangChain, Chroma, Gemini |
| `ai-doctor-2.0-voice-and-vision-main/` | Voice + vision "AI doctor" demo (speak a symptom, upload an image, get a spoken response). | Gradio, Groq (Whisper + vision LLM), ElevenLabs/gTTS |
| `Voice to Voice Conversational AI/` | Low-latency voice medical assistant plus standalone speech-to-text and text-to-speech web demos. | Streamlit, Flask, Groq/Gemini |
| `healthcare_ai_agent/` | CLI agent that scrapes trusted health sources and answers queries. | asyncio, BeautifulSoup, Gemini |
| `FakeMedicine.ipynb` | Notebook exploring counterfeit-medicine detection. | Jupyter |

## ⚙️ Getting Started

### Prerequisites
- **Python 3.11+** and **pip**
- Create and activate a virtual environment per sub-project you run:
  ```bash
  python -m venv .venv
  source .venv/bin/activate   # Windows: .venv\Scripts\activate
  ```
- API keys as needed (never commit them — use a `.env` file):
  - `GEMINI_API_KEY` — Google AI Studio (backend, Artemaya, healthcare_ai_agent)
  - `GROQ_API_KEY` — Groq (ai-doctor, Voice to Voice)
  - `ELEVENLABS_API_KEY` — ElevenLabs (ai-doctor, optional; gTTS works without it)

### 1. Backend API + Website
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env        # then fill in GEMINI_API_KEY and SECRET_KEY
uvicorn main:app --reload
```
- API: <http://localhost:8000/api> · Interactive docs: <http://localhost:8000/docs>
- Website (served by the backend): <http://localhost:8000/app>
- On first run, sample doctor accounts are seeded (password `doctor123`).

### 2. Sanjeevani Website (standalone)
The site is served automatically by the backend at `/app`. To run it on its own, serve the folder with any static server (so relative paths and the API base URL resolve correctly):
```bash
cd "Sanjeevani Website"
python -m http.server 5500
```
Then open <http://localhost:5500>. Make sure the backend is running and that the site's origin is listed in `ALLOWED_ORIGINS`.

### 3. Artemaya Chatbot (nutrition RAG API)
```bash
cd "Artemaya Chatbot"
pip install -r requirements.txt
# set GEMINI_API_KEY in a .env file
cd src
uvicorn rag_model:app --reload --port 8001
```
The Chroma vector store under `db/chroma_db` is reused if present, and rebuilt from `documents/` otherwise.

### 4. AI Doctor (voice + vision)
```bash
cd ai-doctor-2.0-voice-and-vision-main
pip install -r requirements.txt
# set GROQ_API_KEY (and optionally ELEVENLABS_API_KEY) in a .env file
python gradio_app.py
```
Gradio prints a local URL (default <http://localhost:7860>).

### 5. Voice to Voice Conversational AI
```bash
cd "Voice to Voice Conversational AI"
pip install -r requirements.txt
# set the required API keys in a .env file
streamlit run hey.py
```
The `speech to text/` and `text to speech/` folders contain standalone browser demos — open their `index.html` in a browser.

### 6. Healthcare AI Agent (CLI)
```bash
cd healthcare_ai_agent
pip install -r ../backend/requirements.txt   # reuses requests, bs4, psutil, python-dotenv
# set GEMINI_API_KEY in a .env file
python app.py
```

> **Security note:** All API keys are read from environment variables / `.env` files. Never hardcode secrets in source, and never commit `.env` files (they are covered by `.gitignore`).

## 🛠️ Tech Stack

- **AI & NLP:** OpenAI Whisper, FastAPI, Gradio, Langflow, Crew AI  
- **Database:** PostgreSQL, SQLite  
- **Blockchain:** Hyperledger Fabric, Solidity, IPFS  
- **Frontend:** Streamlit, React  
- **Backend:** FastAPI, Flask  
- **Deployment:** Docker 

