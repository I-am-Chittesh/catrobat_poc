import re
import logging
from pydantic import BaseModel, ValidationError
logger = logging.getLogger("Catrobat-Middleware")
BLACKLISTED_TERMS = re.compile(r"\b(diagnose|insomnia|seizure|syndrome|prescribe)\b", re.IGNORECASE)

class GeminiResponseSchema(BaseModel):
    summary: str
    confidence_score: float
    anomaly_flagged: bool

async def evaluate_and_route_telemetry(raw_llm_payload: str) -> dict:
    """
    Async middleware pipeline: Validates structured output from Gemini,
    enforces strict medical safety constraints, and routes to appropriate RBAC queues.
    """
    try:
        parsed_data = GeminiResponseSchema.model_validate_json(raw_llm_payload)

        if BLACKLISTED_TERMS.search(parsed_data.summary):
            logger.warning("CRITICAL: Medical terminology detected. Blocking AI output.")
            return {"status": "BLOCKED", "route": "admin_audit_queue", "reason": "Policy Violation"}
        if parsed_data.confidence_score < 85.0 or parsed_data.anomaly_flagged:
            logger.info(f"Routing to HITL Queue. AI Confidence: {parsed_data.confidence_score}%")
            return {"status": "PENDING_REVIEW", "route": "supervisor_approval", "data": parsed_data.dict()}
        return {"status": "APPROVED", "route": "family_dashboard", "data": parsed_data.dict()}

    except ValidationError as e:
        logger.error(f"LLM Schema Validation Failed: {e}")
        return {"status": "SYSTEM_ERROR", "route": "retry_pipeline", "reason": "Schema Mismatch"}