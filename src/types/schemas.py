from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    prompt: str
    temperature: float = Field(default=0.7, ge=0, le=1)
    max_tokens: int = Field(default=100, ge=1)

class ChatResponse(BaseModel):
    response: str