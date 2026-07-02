import os
import time
import random
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAOCDwJo1KglB4QLfGUN2Np15kv64VvJRQ")
client = genai.Client(api_key=GEMINI_API_KEY)

# Model fallback order: newest → older (each has its own free quota bucket)
FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
]

def generate_with_retry(contents, max_retries: int = 3) -> str:
    """
    Call Gemini with automatic model fallback and exponential backoff on
    RATE_LIMIT_EXCEEDED (429) or RESOURCE_EXHAUSTED errors.
    Returns the response text, or raises the last exception on total failure.
    """
    last_error = None
    for model in FALLBACK_MODELS:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents
                )
                return response.text
            except Exception as e:
                err_str = str(e).lower()
                is_rate_limit = (
                    "rate_limit_exceeded" in err_str
                    or "resource_exhausted" in err_str
                    or "429" in err_str
                    or "quota" in err_str
                )
                last_error = e
                if is_rate_limit:
                    # Exponential backoff: 2s, 4s, 8s + jitter
                    wait = (2 ** (attempt + 1)) + random.uniform(0, 1)
                    print(f"[Gemini] Rate limit on {model} (attempt {attempt+1}). Waiting {wait:.1f}s...")
                    time.sleep(wait)
                else:
                    # Non-rate-limit error — skip retries for this model
                    print(f"[Gemini] Non-rate-limit error on {model}: {e}")
                    break
        else:
            # All retries exhausted for this model → try next fallback model
            print(f"[Gemini] All retries exhausted for {model}, trying next model...")
            continue
        # If we broke out early (non-rate-limit), try next model
        continue

    raise last_error
