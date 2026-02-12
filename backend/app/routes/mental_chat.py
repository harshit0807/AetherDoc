from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
from app.core.database import db
from app.schemas.mental_chat import MentalChatRequest
from app.services.llm import call_llm

router = APIRouter(prefix="/mental-chat", tags=["Mental Health"])

@router.post("/message")
async def send_message(payload: MentalChatRequest):
    session_id = payload.session_id
    user_message = payload.user_message
    detected_emotion = payload.detected_emotion.dict() if payload.detected_emotion else {}

    # 1️⃣ Fetch session
    session = await db.mental_sessions.find_one({"session_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.get("ended_at"):
        raise HTTPException(status_code=400, detail="Session has ended")

    user_id = session["user_id"]

    # 2️⃣ Fetch user
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    patient_profile = {
        "name": user.get("name"),
        "conditions": user.get("conditions", []),
        "medications": user.get("medications", [])
    }

    # 3️⃣ Get recent messages from session (last 6)
    history = [
        {
            "role": m["role"],
            "content": m["content"]
        }
        for m in session.get("messages", [])[-6:]
    ]

    # 4️⃣ Append USER message
    user_msg = {
        "role": "user",
        "content": user_message,
        "emotion": detected_emotion,
        "created_at": datetime.utcnow()
    }

    await db.mental_sessions.update_one(
        {"session_id": session_id},
        {"$push": {"messages": user_msg}}
    )

    # 5️⃣ Call LLM
    ai_reply = call_llm(
        profile=patient_profile,
        session=session,
        history=history,
        user_message=user_message,
        emotion=detected_emotion
    )

    # 6️⃣ Append ASSISTANT message
    assistant_msg = {
        "role": "assistant",
        "content": ai_reply,
        "created_at": datetime.utcnow()
    }

    await db.mental_sessions.update_one(
        {"session_id": session_id},
        {"$push": {"messages": assistant_msg}}
    )

    return {
        "reply": ai_reply
    }
