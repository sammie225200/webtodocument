from pydantic import BaseModel
from typing import Optional

class ConvertRequest(BaseModel):
    document_text: str
    style_preference: Optional[str] = "modern"

class ConvertResponse(BaseModel):
    success: bool
    html: Optional[str] = None
    error: Optional[str] = None
    document_length: int
    tokens_used: Optional[int] = None