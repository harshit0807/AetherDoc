import time
import google.generativeai as genai
from app.core.config import settings
from google.api_core.exceptions import ResourceExhausted

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")


def call_llm(profile, session, history, user_message, emotion):
    prompt = f"""
You are a calm, empathetic mental health support assistant.
You do not diagnose or prescribe medication.
You speak like a professional therapist.

Patient background:
{profile}

Session context:
Goal: {session.get("session_goal")}
Risk level: {session.get("risk_level")}

Recent conversation:
{history}

Detected emotion:
{emotion}

User says:
"{user_message}"

Respond with empathy.
"""

    retries = 3
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()

        except ResourceExhausted:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # exponential backoff
            else:
                return (
                    "I’m here with you. "
                    "It looks like I need a moment to gather my thoughts. "
                    "Can you tell me a little more about how you’re feeling right now?"
                )


def analyze_report(text_content: str, report_type: str):
    prompt= f"""
    You are a medical AI assistant.
    Analyze this {report_type} report and:
    1. Extract important values if present.
    2. Explain in simple language.
    3. Identify abnormal findings.
    
    Report Content:
    {text_content}
    """
    ai_output = await generate_response(prompt)

    return {
        "structured_values": [],
        "ai_explanation": ai_output,
        "risk_level": "low"
    }