from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.orchestrator.graph import run_website_builder

webchat_router = APIRouter()


@webchat_router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    result = run_website_builder(req)
    return result

