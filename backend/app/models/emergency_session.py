from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EmergencySession(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    recognized_text: str
    emergency_type: str
    ai_response: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
