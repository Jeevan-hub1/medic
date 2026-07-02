import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAOCDwJo1KglB4QLfGUN2Np15kv64VvJRQ")
client = genai.Client(api_key=GEMINI_API_KEY)

ANALYSIS_PROMPT = """
You are an expert medical lab report analyzer. Analyze the attached lab report content (which may be medical measurements, vitals, blood tests, or other health markers).
Provide your analysis in a structured JSON format with the following keys:
1. "summary": A high-level, easy-to-understand explanation of the report in patient-friendly terms.
2. "status": One of "Normal", "Attention Required", or "Critical".
3. "key_metrics": A list of dicts, each containing "metric" (name of test/marker), "value" (numeric value + units), "reference_range" (normal range), and "flag" (one of "Normal", "High", "Low").
4. "warnings": A list of warnings or flags that look out of bounds.
5. "recommendations": Practical, non-prescriptive next steps (e.g., diet adjustments, consulting a cardiologist, repeating tests in 3 months).

Only return the raw JSON object. Do not include markdown code block syntax (like ```json ... ```).
"""

def analyze_health_report_text(report_text: str) -> dict:
    """
    Analyze report text content using Gemini
    """
    try:
        from .gemini_client import generate_with_retry
        text = generate_with_retry([ANALYSIS_PROMPT, report_text]).strip()
        # Strip code blocks if AI returned them anyway
        if text.startswith("```"):
            text = text.replace("```json", "", 1).replace("```", "", 1).strip()
            
        analysis = json.loads(text)
        return analysis
    except Exception as e:
        print(f"Error analyzing report: {e}")
        return {
            "summary": "We couldn't analyze the report due to a formatting or server error. Please ensure the report contains clear health metrics.",
            "status": "Attention Required",
            "key_metrics": [],
            "warnings": ["An error occurred during AI report processing."],
            "recommendations": ["Please consult your doctor directly with the report copy."]
        }
