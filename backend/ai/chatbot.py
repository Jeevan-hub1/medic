import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAOCDwJo1KglB4QLfGUN2Np15kv64VvJRQ")
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are "MediSahayak", a helpful, empathetic, and professional AI Medical Assistant designed for rural healthcare support in India.
Your primary goals:
1. Provide reliable, accurate, and easy-to-understand health information, advice, and guidelines.
2. Support multiple Indian languages (Hindi, Tamil, Telugu, Bengali, Marathi, etc.) based on the user's input language.
3. Suggest home remedies and lifestyle adjustments using easily available ingredients in Indian households for mild symptoms.
4. Warn the user when symptoms look critical and advise consulting a real doctor immediately.
5. Provide nutritional guidelines, diet charts, and phase-specific menstrual cycle advice for women.
6. Clearly state that you are an AI assistant and not a replacement for professional medical diagnosis.

Tone: Warm, respectful, clear, and reassuring. Keep explanations simple, avoiding overly complex medical jargon.
"""

def generate_chat_response(message: str, history: list = None) -> str:
    """
    Generate response from Gemini using context history
    """
    try:
        # Build contents list with system prompt as first turn
        contents = [
            types.Content(role="user", parts=[types.Part(text=SYSTEM_PROMPT)]),
            types.Content(role="model", parts=[types.Part(text="I understand. I am MediSahayak, and I am ready to help rural patients with medical advice, guidelines, and home remedies. How can I assist you today?")])
        ]

        # Add history if available
        if history:
            for h in history:
                role = h["role"] if h["role"] in ("user", "model") else "user"
                contents.append(types.Content(role=role, parts=[types.Part(text=h["content"])]))

        # Add the current message
        contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

        from .gemini_client import generate_with_retry
        return generate_with_retry(contents)
    except Exception as e:
        print(f"Error generating chat response: {e}")
        return "I'm sorry, I encountered an error processing your query. Please check your internet connection or try again later."
