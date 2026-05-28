from __future__ import annotations

from typing import Any, Dict, List

from app.orchestrator.state import BuilderState


def conversation_agent(state: BuilderState) -> BuilderState:
    """Extract requirements and produce clarification questions when needed.

    Prototype approach (deterministic):
    - Infer website_type heuristically from keywords.
    - Check for presence of core fields (payment, admin panel) with keyword matching.
    - If missing, create clarification_questions.

    This keeps the assignment reliable even without an OpenAI key.
    """

    prompt = state.user_prompt.lower()

    website_type = "ecommerce" if "ecommerce" in prompt or "cart" in prompt or "checkout" in prompt else "general"
    needs_payment = any(k in prompt for k in ["payment", "stripe", "paypal", "card"])
    wants_admin = any(k in prompt for k in ["admin", "admin panel", "dashboard"])

    questions: List[Dict[str, Any]] = []
    # Minimal clarification logic
    if website_type == "ecommerce":
        if "product" not in prompt and "listing" not in prompt and "catalog" not in prompt:
            questions.append({"id": "products_scope", "question": "Do you want product listing for clothing variations (sizes/colors) or simple products?"})
        if needs_payment and not any(k in prompt for k in ["stripe", "paypal"]):
            questions.append({"id": "payment_provider", "question": "Which payment provider should we integrate (Stripe/PayPal/Custom)?"})
        if wants_admin and "login" not in prompt and "auth" not in prompt:
            questions.append({"id": "admin_auth", "question": "Should admin authentication use email/password or social login?"})

    # Apply user clarifications into a small structured requirements object
    clar = state.user_clarifications or {}

    conversation = {
        "website_type": website_type,
        "requirements": {
            "needs_payment": needs_payment,
            "wants_admin": wants_admin,
        },
        "clarification_questions": questions,
        "user_clarifications": clar,
    }

    # Seed initial spec
    state.conversation = conversation
    state.spec = state.spec or {}
    state.spec.update({"website_type": website_type})
    return state

