import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAOCDwJo1KglB4QLfGUN2Np15kv64VvJRQ")
client = genai.Client(api_key=GEMINI_API_KEY)

PREDICT_PROMPT = """
You are a symptom checker and health risk assessment assistant. Analyze the following user symptoms and health conditions.
Provide potential diseases, conditions, or risk levels. Keep it structured in JSON with the following keys:
1. "diseases": A list of dicts, each with "name" (predicted condition), "confidence" (0.0 to 1.0), and "explanation" (why this matches).
2. "risk_score": An integer from 0 to 100 representing general risk or severity.
3. "urgency": One of "Low" (rest/home care), "Medium" (schedule doctor visit), or "High" (seek emergency room/ambulance).
4. "home_remedies": A list of safe, natural home remedies or self-care tips.
5. "consultation_advised": A boolean indicating if they should see a doctor.

Only return the raw JSON object. Do not include markdown code block syntax (like ```json ... ```).
"""

def predict_disease_from_symptoms(symptoms: list, health_context: str = "") -> dict:
    """
    Predict possible issues from a list of symptoms using Gemini
    """
    try:
        query_content = f"Symptoms: {', '.join(symptoms)}.\nAdditional Context: {health_context}"
        from .gemini_client import generate_with_retry
        text = generate_with_retry([PREDICT_PROMPT, query_content]).strip()
        
        # Strip code blocks if AI returned them anyway
        if text.startswith("```"):
            text = text.replace("```json", "", 1).replace("```", "", 1).strip()
            
        prediction = json.loads(text)
        return prediction
    except Exception as e:
        print(f"Error predicting disease: {e}")
        return {
            "diseases": [
                {"name": "Undetermined Condition", "confidence": 0.5, "explanation": "Unable to pinpoint specific condition based on provided input."}
            ],
            "risk_score": 20,
            "urgency": "Low",
            "home_remedies": ["Drink warm water", "Get plenty of sleep"],
            "consultation_advised": True
        }
