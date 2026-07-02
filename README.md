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

## 🛠️ Tech Stack

- **AI & NLP:** OpenAI Whisper, FastAPI, Gradio, Langflow, Crew AI  
- **Database:** PostgreSQL, SQLite  
- **Blockchain:** Hyperledger Fabric, Solidity, IPFS  
- **Frontend:** Streamlit, React  
- **Backend:** FastAPI, Flask  
- **Deployment:** Docker 

