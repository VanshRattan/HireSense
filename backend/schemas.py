from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class SessionBase(BaseModel):
    user_id: int

class SessionCreate(SessionBase):
    pass

class SessionOut(SessionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReportOut(BaseModel):
    id: int
    session_id: int
    communication_score: Optional[float]
    confidence_score: Optional[float]
    filler_word_count: Optional[int]
    filler_words_used: Optional[Dict[str, int]]
    feedback_summary: Optional[str]
    transcript: Optional[str]
    wpm: Optional[float]

    class Config:
        from_attributes = True
