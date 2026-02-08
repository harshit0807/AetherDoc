from fastapi import WebSocket, APIRouter
from app.services.stt_service import streaming_transcribe
from app.services.emergency_ai import classify_emergency, generate_guidance
from app.services.tts_service import synthesize_speech
from app.core.database import emergency_sessions
import asyncio

router = APIRouter()

@router.websocket("/ws/emergency")
async def emergency_ws(websocket: WebSocket):
    await websocket.accept()

    audio_queue = asyncio.Queue()

    async def audio_generator():
        while True:
            chunk = await audio_queue.get()
            if chunk is None:
                break
            yield chunk

    async def receive_audio():
        try:
            while True:
                data = await websocket.receive_bytes()
                await audio_queue.put(data)
        except:
            await audio_queue.put(None)

    asyncio.create_task(receive_audio())

    for transcript in streaming_transcribe(audio_generator()):
        emergency_type = classify_emergency(transcript)
        ai_response = generate_guidance(emergency_type)

        await emergency_sessions.insert_one({
            "recognized_text": transcript,
            "emergency_type": emergency_type,
            "ai_response": ai_response
        })

        audio = synthesize_speech(ai_response)

        await websocket.send_bytes(audio)
