# models/schemas.py
from typing import Optional, List, Literal
from pydantic import BaseModel

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatRequest(BaseModel):
    user_id: str
    channel: str  # e.g. "web", "whatsapp", "app", "ivr"
    messages: List[Message]

class ToolCallResult(BaseModel):
    tool_name: str
    success: bool
    result: dict

class ChatResponse(BaseModel):
    reply: str
    tool_calls: Optional[List[ToolCallResult]] = None
    source: Optional[str] = None  # "knowledge_base" | "tool" | "llm"
