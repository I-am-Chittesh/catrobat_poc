import json
import re

BLACKLISTED_TERMS = r"\b(diagnose|insomnia|seizure|syndrome|prescribe|treatment)\b"

def evaluate_ai_safety(gemini_json_response: str) -> dict:
    """
    Middleware circuit breaker: Evaluates Gemini's output for safety 
    and minimum confidence thresholds before routing to the dashboard.
    """
    try:
        payload = json.loads(gemini_json_response)
        summary = payload.get("summary", "").lower()
        confidence = payload.get("confidence_score", 0)

        if re.search(BLACKLISTED_TERMS, summary):
            return {"status": "BLOCKED", "reason": "Medical terminology detected."}
        if confidence < 85:
            return {"status": "PENDING_REVIEW", "reason": f"Low AI confidence ({confidence}%)."}
        return {"status": "APPROVED", "data": summary}

    except json.JSONDecodeError:
        return {"status": "BLOCKED", "reason": "LLM failed to return structured JSON."}