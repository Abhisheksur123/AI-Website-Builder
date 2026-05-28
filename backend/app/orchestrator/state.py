from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class BuilderState(BaseModel):
    session_id: Optional[str] = None
    user_prompt: str
    user_clarifications: Dict[str, Any] = Field(default_factory=dict)

    # Intermediate outputs
    conversation: Dict[str, Any] = Field(default_factory=dict)
    spec: Dict[str, Any] = Field(default_factory=dict)  # website spec draft

    # Validation output
    validation: Dict[str, Any] = Field(default_factory=dict)

    # Final outputs
    builder_actions: List[Dict[str, Any]] = Field(default_factory=list)
    preview: Dict[str, Any] = Field(default_factory=dict)

    def to_response_dict(self) -> Dict[str, Any]:
        # Ensure response contains the keys required by ChatResponse
        return {
            "session_id": self.session_id,
            "clarification_questions": self.conversation.get("clarification_questions", []),
            "spec": self.spec,
            "validated": self.validation,
            "builder_actions": self.builder_actions,
            "preview": self.preview,
        }


