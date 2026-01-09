from pydantic import BaseModel

from pydantic import BaseModel
from datetime import date

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str


class ProgressCreate(BaseModel):
    date: date
    overs: int
    daily_target: int
    effort_level: str
    body_status: str
    session_type: str
    notes: str | None = None
