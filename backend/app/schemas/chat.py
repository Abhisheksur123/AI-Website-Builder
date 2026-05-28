from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class ChatRequest(BaseModel):
    user_prompt: str = Field(..., description="High-level website creation request")
    session_id: Optional[str] = Field(None, description="Optional session id for persistence")
    user_clarifications: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Optional answers to prior clarification questions (keyed by question id)",
    )


class ChatResponse(BaseModel):
    session_id: Optional[str] = None
    clarification_questions: List[Dict[str, Any]] = Field(default_factory=list)
    spec: Dict[str, Any] = Field(default_factory=dict)
    validated: Dict[str, Any] = Field(default_factory=dict)
    builder_actions: List[Dict[str, Any]] = Field(default_factory=list)
    preview: Dict[str, Any] = Field(default_factory=dict)


